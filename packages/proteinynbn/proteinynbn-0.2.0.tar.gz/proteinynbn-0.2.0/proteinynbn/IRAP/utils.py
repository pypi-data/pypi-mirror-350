

class IrapSeq:
	def __init__(self) -> None:
		self.irap_dict: dict = self.__readirap__()
	
	def __readirap__(self) -> dict[str, str]:
		irap: dict[str, str] = dict()
		with open('./irap.txt', 'r') as file:
			for line in file:
				line = line.strip().split(' ')
				the_type: str = line[1]
				the_size: str = line[3]
				context: str = line[-1]
				name = f'type:{the_type}+size:{the_size}'
				irap[name] = context
		return irap
		
	def irap_dict(self, type:str, size: str) -> str:
		name: str = f'type:{type}+size:{size}'
		return self.irap_dict[name]
	
	def irap_dicts(self) -> dict[str, str]:
		return self.irap_dict
		
	def irap(self, seq:str, type: str='0', size:str='20') -> str:
		name: str = f'type:{type}+size:{size}'
		assert name in self.irap_dict.keys(), f"this type and size are not in irap_dict, {self.irap_dict.keys()=}"
		irap_context: list = self.irap_dict[name].split("-")
		return self.__seqtoirap__(seq.upper(), irap_context)
		
	@staticmethod
	def __seqtoirap__(seq: str, irap_list: list) -> str:
		irap_seq: str = ''
		for res in seq:
			for irap_type in irap_list:
				if res in irap_type:
					irap_seq += irap_type[0]
		return irap_seq


if __name__ == '__main__':
    irap_str = "LVIMCAGSTPFYW-EDNQKRH"
    fasta_file: str = './cd_hit_ready.fasta'
    # main(fasta_file, irap_str)
    a = IrapSeq()
    print(a.irap(seq='eeewe', type='1', size='2'))