import tensorflow as tf


def get_dataset(input_path, features_description, buffer_size, batch_size, exclude_examples=None, common_examples=None):
	"""
	DESCRIPTION:
		Before the model start, loading the data, which is tensorflow datatype
	:param input_path:str # path to input file
	:param features_description:dict # dictionary of features description
	:param buffer_size: int # buffer size of dataset
	:param batch_size:int # size of batch
	:param exclude_examples:str # only allow to set one exclude feature
	:param common_examples:str # only allow to set one common feature
	:return:tensorflow.data.Dataset
	"""
	
	def _parse_example(input_example):
		examples = tf.io.parse_single_example(input_example, features=features_description)
		all_featuers = features_description.keys()
		written_example = dict()
		for key in all_featuers:
			if key == exclude_examples and key != common_examples:
				continue
			written_example[key] = examples[key]
		return written_example, examples[exclude_examples]
	
	dataset = tf.data.TFRecordDataset(input_path)
	data_set = dataset.map(_parse_example)
	dataset = data_set.shuffle(buffer_size=buffer_size, reshuffle_each_iteration=True).repeat().batch(batch_size, drop_remainder=True)
	print(dataset)
	return dataset


if __name__ == '__main__':
	pass
	"""
	input_path = './test_fragment.tfrecord'
	feature_description = {
		'protein_name': tf.io.FixedLenFeature(shape=(), dtype=tf.string),
		'input_ids': tf.io.FixedLenFeature([27], tf.int64),
		'input_mask': tf.io.FixedLenFeature([27], tf.int64),
		'labels': tf.io.FixedLenFeature([27], tf.int64),
	}
	dataset = get_dataset(input_path, feature_description, buffer_size=1, batch_size=1, common_examples='labels', exclude_examples='labels')
	"""
