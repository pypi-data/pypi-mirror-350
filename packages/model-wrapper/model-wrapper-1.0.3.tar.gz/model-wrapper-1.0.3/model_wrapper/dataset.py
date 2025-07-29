from typing import List, Tuple, Union
import numpy as np
import torch
from torch.utils.data import Dataset


class PairDataset(Dataset):
	"""Dataset wrapping pairs of data.
	Each sample will be retrieved by indexing the list.
	进入和返回的类型相同，需配合collate_fn使用, 如配合text_collate使用

	Exampls:
    --------
    >>> X = np.random.randn(8, 3)
	>>> y = np.random.randint(0, 2, 8)
	>>> pair_data = zip(X, y)
	>>> dataset = PairDataset(list(pair_data))
	"""
	def __init__(self, pair_data: List[Tuple]) -> None:
		"""
		Args:
			pair_data (List[Tuple]): list of tuple, each tuple contains two elements.
		"""
		self.data = pair_data
	
	def __getitem__(self, index) -> Tuple:
		return self.data[index]
	
	def __len__(self) -> int:
		return len(self.data)


class ListDataset(Dataset[Tuple[List, ...]]):
	r"""Dataset wrapping List.
    可以配合ListTensorCollector使用
	Each sample will be retrieved by indexing list.

	Args:
		*lists (List): lists that have the same length.

	Exampls:
    --------
    >>> X1 = np.random.randn(8, 3)
	>>> X2 = np.random.randn(8, 2)
	>>> y = np.random.randint(0, 2, 8)
	>>> dataset = ListDataset(X1, X2, y)
	>>> dataloader = DataLoader(dataset, batch_size=4, collate_fn=ListTensorCollator([torch.float16, torch.float64, torch.long]))
	"""
	
	def __init__(self, *lists: Union[List, np.ndarray]) -> None:
		assert all(len(lists[0]) == len(sub_list) for sub_list in lists), "Size mismatch between tensors"
		self.lists = lists
	
	def __getitem__(self, index):
		if len(self.lists) == 1:
			return self.lists[0][index]
		return tuple(sub_list[index] for sub_list in self.lists)
	
	def __len__(self):
		return len(self.lists[0])
	

class DictDataset(Dataset):
	"""传入的是Dict，返回(features, labels)"""

	def __init__(self, dataset, feature_names: Union[str, List[str]], label_name: str):
		"""
		参数:
		- dataset: 可以是HuggingFace的Dataset，也可以是普通的字典列表List[Dict]
		- feature_names: 特征名，可以是单个字符串，也可以是列表
		- label_name: 标签名
		"""
		super().__init__()
		self.dataset = dataset
		self.feature_names = feature_names
		self.label_name = label_name

	def __getitem__(self, index: int):
		data = self.dataset[index]
		if isinstance(self.feature_names, str):
			features = data[self.feature_names]
		elif len(self.feature_names) == 1:
			features = data[self.feature_names[0]]
		else:
			features = [data[k] for k in self.feature_names]
		
		return features, data[self.label_name]
		
	def __len__(self):
		return len(self.dataset)
	

if __name__ == '__main__':
	import numpy as np
	from torch.utils.data import DataLoader
	from model_wrapper.collator import ListTensorCollator

	X1 = np.random.randn(8, 3)
	X2 = np.random.randn(8, 2)
	y = np.random.randint(0, 2, 8)

	pair_data = zip(X1, y)
	dataset = PairDataset(list(pair_data))
	for data in dataset:
		print(data)
		break
	
	dataset = ListDataset(X1, X2, y)
	dataloader = DataLoader(dataset, batch_size=4, collate_fn=ListTensorCollator(torch.float16, torch.float64, torch.long))
	for d in dataloader:
		print(d[0].dtype, d[1].dtype, d[2].dtype)
		break
