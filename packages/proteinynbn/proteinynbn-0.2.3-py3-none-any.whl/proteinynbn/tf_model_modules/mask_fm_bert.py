import tensorflow as tf
from dataclasses import dataclass


def heading(emphasize):
	split_line = '=' * 80
	print(split_line)
	print(emphasize)
	print(split_line)


@dataclass
class MaskedOutput:
	input_ids: tf.Tensor
	masked_lm_positions: tf.Tensor
	masked_lm_ids: tf.Tensor
	masked_lm_weights: tf.Tensor


def mask(config, inputs, vocab):
	if tf.executing_eagerly():
		heading('eager execution')
	else:
		heading('disable eager execution')
	#   最大掩码数量  type:int
	max_mask_number = config.max_prediction_per_seq
	#   掩码概率    type:float
	mask_prob = config.mask_prob
	#   位置掩码分布概率    type:float/int
	proposal_distribution = config.proposal_distribution
	#   输入数据的特征 type:int
	batch, length = inputs.input_ids.shape
	"""基本信息输入"""
	
	#   有效渔猎， 可掩码为True  type:list_bool, shape=[batch, length]
	candidates_mask = tf.cast(get_candidates_mask(inputs, vocab), tf.int32)
	#   最大有效掩码数量    type:int
	number_tokens = tf.cast(tf.reduce_sum(candidates_mask, -1), tf.float32)
	#   可以掩码数   type:int
	number_to_token = tf.maximum(1, tf.minimum(max_mask_number, tf.cast(tf.round(number_tokens * mask_prob), tf.int32)))
	#   设置被掩码的数量不超过序列有效长度 type:list, e.g.:[1, 1, 1, 0, 0, 0]
	masked_lm_weights = tf.cast(tf.sequence_mask(number_to_token, max_mask_number), tf.float32)
	"""这一部分获取了限制掩码数的权重矩阵"""
	
	#   候选掩码布尔矩阵转化为数值矩阵 type:list_float shape = [batch, length]
	candidates_mask_float = tf.cast(candidates_mask, tf.float32)
	#   加上掩码位置概率    type:list_float shape = [batch, length]
	sample_prob = (proposal_distribution * candidates_mask_float)
	#   概率归一    type:list_float shape = [batch, length]
	sample_prob = sample_prob / tf.reduce_sum(sample_prob, -1, keepdims=True)
	#   掩码概率不参与梯度传播
	sample_prob = tf.stop_gradient(sample_prob)
	#   对数  type:llist_float    shape = [batch, length]
	sample_logtis = tf.math.log(sample_prob)
	#   随机选择被掩码位置   type:list_int   $$\red{shape = [batch, max_mask_number]}$$  $$\red{大概率有重复项， 值为sequence的位置索引}
	mask_lm_positions = tf.random.categorical(sample_logtis, max_mask_number)
	mask_lm_positions = tf.cast(mask_lm_positions, tf.int32)
	#   #type:list_int   shape = [batch, max_mask_number]
	mask_lm_positions *= tf.cast(masked_lm_weights, tf.int32)
	"""这一部分计算了位置掩码的概率， 获得被掩码的位置"""
	
	#   获取偏移位置向量    type:list   shape = [batch, 1]
	shift = tf.expand_dims(length * tf.range(batch), -1)
	#   偏移后被掩码的位置   type:list   shape = [batch * max_mask_number, 1]
	token_positions = tf.reshape(mask_lm_positions + shift, [-1, 1])
	#   获取掩码位置对应id  type:list   shape = [batch * max_mask_number]
	masked_lm_ids = tf.gather(tf.reshape(inputs.input_ids, [-1]), token_positions)
	masked_lm_ids = tf.reshape(masked_lm_ids, [batch, -1])
	#   #type:list   #shape = [batch, None]
	masked_lm_ids = tf.cast(masked_lm_ids, tf.int32)
	"""这一部分提取到被掩码位置的数值id"""
	
	#   #type:list   #shape = [batch, max_mask_number]
	replace_with_mask_positions = mask_lm_positions * tf.cast(
		tf.less(tf.random.uniform([batch, max_mask_number]), 0.85), tf.int32)
	inputs_ids, _ = scatter_update(
		config,
		inputs.input_ids,  # #type:list   #shape = [batch, length]
		tf.fill([batch, max_mask_number], vocab["[MASK]"]),  # #type:list  #shape = [batch, max_mask_number]
		replace_with_mask_positions  # #type:list  #shape = [batch, max_mask_number]
	)
	return MaskedOutput(
		masked_lm_positions=mask_lm_positions,
		input_ids=tf.stop_gradient(inputs_ids),
		masked_lm_ids=masked_lm_ids,
		masked_lm_weights=masked_lm_weights
	)


def get_candidates_mask(inputs, vocab):
	ignore_ids = [vocab["[SEP]"], vocab["[CLS]"], vocab["[MASK]"]]
	candidates_mask = tf.ones_like(inputs.input_ids, dtype=tf.bool)
	for ignore_id in ignore_ids:
		candidates_mask &= tf.not_equal(inputs.input_ids, ignore_id)
	candidates_mask &= tf.cast(inputs.input_mask, dtype=tf.bool)
	return candidates_mask


def scatter_update(config, sequence, updates, positions):
	#   shape = [batch, length]
	shape = sequence.shape
	if shape.ndims == 2:
		batch, length = shape
		dimension = 1
		sequence = tf.expand_dims(sequence, axis=-1)
	else:
		batch, length, dimension = shape
	max_mask_number = config.max_prediction_per_seq
	"""基本信息获取"""
	
	#   平展偏移量   type:list   shape = [batch, 1]
	shift = tf.expand_dims(length * tf.range(batch), -1)
	#   掩码的位置矩阵平展   type:list   shape = [batch, max_mask_number]
	flat_positions = tf.reshape(positions + shift, [-1, 1])
	"""将position平展"""
	
	#   将全mask矩阵平展  type:list   shape = [batch*max_mask_number, 1]
	flat_updates = tf.reshape(updates, [-1, dimension])
	#   形成类似excel表格的矩阵， 初始标记全为mask  type:list   shape = [batch*length, dimension]
	updates = tf.scatter_nd(flat_positions, flat_updates, [batch * length, dimension])
	#   #type:list   shape = [batch, length, dimension]
	updates = tf.reshape(updates, [batch, length, dimension])
	updates = tf.cast(updates, tf.float32)
	"""获得一个初始标记mask的矩阵， 匹配序列形状"""
	
	#   获得一个全1矩阵， 用于计算掩码次数  type=list   shape = [batch * max_mask_number]
	flat_updates_mask = tf.ones([batch * max_mask_number], dtype=tf.int32)
	updates_mask = tf.scatter_nd(flat_positions, flat_updates_mask, [batch * length])
	#   shape = [batch, length]
	updates_mask = tf.reshape(updates_mask, [batch, length])
	#   shape = [batch, length, 1]
	not_first_token = tf.concat([tf.zeros([batch, 1], dtype=tf.int32), tf.ones((batch, length - 1), dtype=tf.int32)], -1)
	updates_mask *= not_first_token
	updates_mask_3d = tf.expand_dims(updates_mask, -1)
	"""与上一大步类似， 不过， 这里是计算了每个位置被掩码的次数， 避免多次掩码"""
	
	#   shape = [batch, length, 1]
	sequence = tf.cast(sequence, tf.float32)
	updates_mask_3d = tf.cast(updates_mask_3d, tf.float32)
	#   shape = [batch, length, 1]
	updates /= tf.maximum(1.0, updates_mask_3d)
	"""获取掩码结果的平均值， 即某个位置如果被多次掩码， 则只保留一次"""
	
	#   #只用记录是否被掩码， 不关系重复   [batch, length]
	updates_mask = tf.minimum(updates_mask, 1)
	#   [batch, length, 1]
	updates_mask_3d = tf.minimum(updates_mask_3d, 1.0)
	#   [batch, length, 1]
	updated_sequence = (((1.0 - updates_mask_3d) * sequence) + updates_mask_3d * updates)
	if shape.ndims == 2:
		#   舍去最后一个1的维度
		updated_sequence = tf.squeeze(updated_sequence, axis=-1)
	"""将更改序列的id序列"""
	
	return updated_sequence, updates_mask
