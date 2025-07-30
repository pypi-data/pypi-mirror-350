class FullTokenizer(object):
	"""
	DESCRIPTION:
		the protien letter alphabet
	return:None
	functions:
		get_vocab: returns the vocabulary
	"""
	
	def __init__(self, vocab_file):
		self.vocab = dict()
		with open(vocab_file, 'r') as vocab_file:
			vocab_lines = vocab_file.readlines()
			index = 0
			for vocab_line in vocab_lines:
				token = vocab_line.strip()
				self.vocab[token] = index
				index += 1
	
	def get_vocab(self):
		return self.vocab
	