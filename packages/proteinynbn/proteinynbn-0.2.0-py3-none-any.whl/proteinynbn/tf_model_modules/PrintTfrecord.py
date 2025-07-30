import tensorflow as tf
tf.config.run_functions_eagerly(True)


def print_tfrecord(tfrecord_path, features_description, batch_size, buffer_size=10):
	"""
	Description:
		print tfrecord file's context, in order to read easily
	:param tfrecord_path: str or list of str
	:param features_description: dict # to describe the features type
	:param batch_size: int
	:param buffer_size: int
	:return: None. Just prints out the tfrecord file's context
	"""
	def _parse_example(input_example):
		return tf.io.parse_example(input_example, features=features_description)
	
	if isinstance(tfrecord_path, list):
		files_path: list = tfrecord_path
	elif isinstance(tfrecord_path, str):
		files_path: str = [tfrecord_path]
	else:
		raise TypeError('tfrecord_path must be either a string or a list')
	
	dataset: tf.data.TFRecordDataset = tf.data.TFRecordDataset(files_path)
	data_set: tf.data.Dataset = dataset.map(_parse_example)
	dataset: tf.data.Dataset = (
		data_set.shuffle(buffer_size, reshuffle_each_iteration=True)
		.batch(batch_size)
		.prefetch(tf.data.AUTOTUNE)
	)
	print(f'dataset size: {dataset}')
	all_features: list = features_description.keys()
	for batch in data_set.take(1):
		for feature in all_features:
			tf.print(f'{feature}: {batch[feature]}')
	