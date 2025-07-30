import torch
import numpy as np
import pandas as pd
from typing import Union, List, Tuple, Mapping
from torch.utils.data import Dataset


class TokenDataset(Dataset):
	""" Token的长度不一样
	返回的是(token, label) 不是Tensor, 必须经过PaddingTokenCollator
	"""
	
	def __init__(self, tokens: Union[List[int], np.ndarray],
	             labels: Union[List, np.ndarray, pd.Series]):
		super().__init__()
		self.tokens = tokens
		self.labels = labels.to_numpy() if isinstance(labels, pd.Series) else labels
	
	def __getitem__(self, index: int):
		return self.tokens[index], self.labels[index]
	
	def __len__(self):
		return len(self.labels)


class SameLengthTokenDataset(Dataset):
	""" Token已经truncate和padding, 长度一样
	返回的是Tensor, 不需要经过collate_fn
	"""
	
	def __init__(self, tokens: Union[List[int], np.ndarray, torch.LongTensor],
	             labels: Union[List, np.ndarray, pd.Series, torch.LongTensor]):
		super().__init__()
		self.tokens = tokens if torch.is_tensor(tokens) else torch.LongTensor(tokens)
		labels = labels.values if isinstance(labels, pd.Series) else labels
		self.labels = labels if torch.is_tensor(labels) else torch.LongTensor(labels)
	
	def __getitem__(self, index: int):
		return self.tokens[index], self.labels[index]
	
	def __len__(self):
		return len(self.labels)


class TextDataset(Dataset):
	""" 返回的是(text, label) 都不是Tensor, 必须经过TextVecCollator """
	
	def __init__(self, texts: Union[List[str], np.ndarray, pd.Series], labels: Union[List, np.ndarray, pd.Series]):
		super().__init__()
		self.texts = texts.values if isinstance(texts, pd.Series) else texts
		self.labels = labels.values if isinstance(labels, pd.Series) else labels
	
	def __getitem__(self, index: int):
		return self.texts[index], self.labels[index]
	
	def __len__(self):
		return len(self.labels)


class TextDFDataset(Dataset):
	""" 返回的是(text, label) 不是Tensor, 必须经过TextVecCollator """
	
	def __init__(self, data_df: pd.DataFrame):
		"""
		:param data_df: 只有两列 ['text', 'label'], 注意顺序，第一列是text, 第二列是label
		"""
		super().__init__()
		self.data = data_df.values
	
	def __getitem__(self, index: int):
		return self.data[index]
	
	def __len__(self):
		return len(self.data)
	