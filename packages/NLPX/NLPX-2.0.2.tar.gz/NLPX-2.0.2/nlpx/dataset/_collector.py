import torch
import numpy as np
from typing import Tuple, List
from nlpx.tokenize import BaseTokenizer, TokenEmbedding
from nlpx.tokenize.utils import get_texts_max_length


class TextVecCollator:
	
	def __init__(self, tokenize_vec, max_length: int = None, **kwargs):
		"""
		初始化文本处理类。

		参数:
		tokenize_vec: TokenizeVec 或 TokenEmbedding 类型的对象，用于文本的分词或嵌入。
		max_length: 可选参数，表示处理后文本的最大长度。
		**kwargs: 其他可变关键字参数，用于灵活配置文本处理的其他选项。
		"""
		self.tokenize_vec = tokenize_vec
		self.max_length = max_length
		self.kwargs = kwargs
	
	def __call__(self, examples: List[Tuple[str, int]]):
		texts, labels = zip(*examples)
		labels = torch.from_numpy(np.array(labels, dtype=np.int64))
		
		if isinstance(self.tokenize_vec, TokenEmbedding):
			max_length = get_texts_max_length(texts, cut_type=self.tokenize_vec.cut_type,
			                                  lang=self.tokenize_vec.lang, cut_fn=self.tokenize_vec.cut_fn)
			max_length = min(max_length, self.max_length) if self.max_length and self.max_length > 0 else max_length
			return self.tokenize_vec(texts, max_length, **self.kwargs), labels
		
		max_length = get_texts_max_length(texts, cut_type='char') + 2
		max_length = min(max_length, self.max_length) if self.max_length and self.max_length > 0 else max_length
		return self.tokenize_vec.encode_plus(texts, max_length=max_length, padding='max_length',
												truncation=True, add_special_tokens=True,
												return_token_type_ids=True, return_attention_mask=True,
												return_tensors='pt', **self.kwargs), labels
		

class TokenizeCollator:
	
	def __init__(self, tokenizer, max_length: int = None, **kwargs):
		self.tokenizer = tokenizer
		self.max_length = max_length
		self.kwargs = kwargs
	
	def __call__(self, examples: List[Tuple[str, int]]):
		texts, labels = zip(*examples)
		labels = torch.from_numpy(np.array(labels, dtype=np.int64))
		
		if isinstance(self.tokenizer, BaseTokenizer):
			max_length = get_texts_max_length(texts, cut_type=self.tokenizer.cut_type, lang=self.tokenizer.lang,
			                                  cut_fn=self.tokenizer.cut_fn)
			max_length = min(max_length, self.max_length) if self.max_length else max_length
			return torch.LongTensor(self.tokenizer.batch_encode(texts, max_length, **self.kwargs)), labels
		
		max_length = get_texts_max_length(texts, cut_type='char') + 2
		max_length = min(max_length, self.max_length) if self.max_length and self.max_length > 0 else max_length
		result = self.tokenizer.batch_encode_plus(texts, max_length=max_length, padding='max_length',
		                                          return_token_type_ids=True, return_attention_mask=True,
		                                          truncation=True, add_special_tokens=True, return_tensors='pt',
		                                          **self.kwargs)
		result['labels'] = labels
		return result


class PaddingTokenCollator:
	"""与TokenDataset配合使用, 只有token, label两列数数

	Examples
	--------
	>>> tokenizer = PaddingTokenizer(texts=texts)
	>>> X_train = tokenizer.batch_encode(texts, padding=False)
	>>> train_set = TokenDataset(X_train, y_train)
	>>> model_wrapper = ClassifyModelWrapper(classes=classes)
	>>> model_wrapper.train(model, train_set, early_stopping_rounds=5, show_progress=False,
	>>>                     collate_fn=PaddingTokenCollator(tokenizer.pad, return_sequence_length=True))
	"""
	
	def __init__(self, pad_func, max_length: int = None, truncation=True, padding_side='right',
	             return_sequence_length=False, bos=False, eos=False):
		self.pad_func = pad_func
		self.max_length = max_length
		self.truncation = truncation
		self.padding_side = padding_side
		self.return_sequence_length = return_sequence_length
		self.bos, self.eos = bos, eos
	
	def __call__(self, examples: List[Tuple[List[int], int]]) -> Tuple[torch.Tensor]:
		tokens, labels = zip(*examples)
		labels = torch.from_numpy(np.array(labels, dtype=np.int64))
		
		max_length = max(map(lambda x: len(x), tokens))
		max_length = min(max_length, self.max_length) if self.max_length and self.max_length > 0 else max_length
		params = {'truncation': self.truncation, 'padding_side': self.padding_side}
		if self.bos:
			params['bos'] = self.bos
		if self.eos:
			params['eos'] = self.eos
		
		if self.return_sequence_length:
			params['return_sequence_length'] = self.return_sequence_length
			ids, sequence_lengths = self.pad_func(tokens, max_length, **params)
			return (torch.from_numpy(np.array(ids, dtype=np.int64)), 
		   			torch.from_numpy(np.array(sequence_lengths, dtype=np.int16)), 
					labels)
		
		ids = self.pad_func(tokens, max_length, **params)
		if isinstance(ids, Tuple):
			ids = ids[0]
		return torch.from_numpy(np.array(ids, dtype=np.int64)), labels


class PaddingTensorCollector:
	""" 可以有多列数据 
	配合ListDataset使用
	"""
	
	def __init__(self, pad_func):
		self.pad_func = pad_func
	
	def __call__(self, batch: List[Tuple]) -> Tuple[torch.Tensor]:
		batch = (self.pad_func(x) if isinstance(x[0], List) else x for x in zip(*batch))
		return tuple(torch.from_numpy(x.astype(np.int64) if isinstance(x, np.ndarray) else np.array(x, dtype=np.int64)) for x in batch)
	

def text_collate(examples: List[Tuple[str, int]]) -> Tuple[List[str], torch.Tensor]:
	"""传入(text, label), 返回的是(texts: List, labels: torch.Tensor), 一般配合BertTextClassifier使用"""
	texts, labels = zip(*examples)
	labels = torch.from_numpy(np.asarray(labels, dtype=np.int64))
	return texts, labels
		