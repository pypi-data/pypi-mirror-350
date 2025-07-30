import torch
from torch import nn
import torch.nn.functional as F
from typing import Union, List, Optional
from torch_model_hub.norm import RMSNorm
from torch_model_hub.model import TextCNN, RNNAttention, CNNRNNAttention, RNNCNNAttention, ResRNNCNNAttention, RotaryClassSelfAttention
from .embedding import EmbeddingLayer, CNNEmbedding

__all__ = [
	'EmbeddingClassifier',
	'MaskEmbeddingClassifier',
	'TextCNNClassifier',
	'RNNAttentionClassifier',
	'CNNRNNAttentionClassifier',
	'RNNCNNAttentionClassifier',
	'ResRNNCNNAttentionClassifier',
	'RotaryAttentionClassifier',
]


class EmbeddingClassifier(nn.Module):
	"""
	Examples
	--------
	>>> from nlpx.text_token import TokenEmbedding
	>>> from nlpx.model import TextCNN, RNNAttention
	>>> from nlpx.model.classifier import EmbeddingClassifier
	>>> tokenizer = TokenEmbedding(pretrained_path)
	>>> attn = RNNAttention(tokenizer.embed_dim, num_heads=2, out_features=len(classes))
	>>> classifier = EmbeddingClassifier(atten, embedding=tokenizer.embedding)
	>>> classifier = EmbeddingClassifier(atten, vocab_size=tokenizer.vocab_size, embed_dim=tokenizer.embed_dim)
	"""
	
	multi_class: bool
	
	def __init__(self, classifier, embedding: Union[nn.Embedding, torch.Tensor, List] = None, vocab_size: int = None,
	             embed_dim: int = None, padding_idx: Optional[int] = None, num_classes: int = 2):
		"""
		:param classifier: 分类器
		:param embedding: 输入的embedding，可以是nn.Embedding，torch.Tensor，list
		:param vocab_size: vocab size
		:param embed_dim: word embedding维度
		:param padding_idx
		"""
		super().__init__()
		self.classifier = classifier
		self.embedding = EmbeddingLayer(embed_dim, vocab_size, embedding, padding_idx)
		self.multi_class = num_classes > 1
	
	def forward(self, input_ids: torch.Tensor):
		embedding = self.embedding(input_ids)
		return self.classifier(embedding)
	
	def fit(self, input_ids: torch.Tensor, labels: torch.LongTensor):
		logits = self.forward(input_ids)
		if self.multi_class:
			return F.cross_entropy(logits, labels), logits
		return F.binary_cross_entropy(logits.reshape(-1), labels), logits


class MaskEmbeddingClassifier(EmbeddingClassifier):
	"""
	Examples
	--------
	>>> from nlpx.text_token import TokenEmbedding
	>>> from nlpx.model import TextCNN, RNNAttention
	>>> from nlpx.model.classifier import EmbeddingClassifier
	>>> tokenizer = TokenEmbedding(pretrained_path)
	>>> attn = RNNAttention(tokenizer.embed_dim, num_heads=2, out_features=len(classes))
	>>> classifier = MaskEmbeddingClassifier(atten, embedding=tokenizer.embedding)
	>>> classifier = MaskEmbeddingClassifier(atten, vocab_size=tokenizer.vocab_size, embed_dim=tokenizer.embed_dim)
	"""
	
	def forward(self, input_ids: torch.Tensor, mask: Optional[torch.Tensor] = None):
		embedding = self.embedding(input_ids)
		return self.classifier(embedding, mask)
	
	def fit(self, input_ids: torch.Tensor, mask: Optional[torch.Tensor] = None,
	        labels: Optional[torch.LongTensor] = None):
		assert labels is not None
		logits = self.forward(input_ids, mask)
		if self.multi_class:
			return F.cross_entropy(logits, labels), logits
		return F.binary_cross_entropy(logits.reshape(-1), labels), logits


class TextCNNClassifier(EmbeddingClassifier):
	"""
	Examples
	--------
	>>> from nlpx.text_token import Tokenizer
	>>> from nlpx.model.classifier import TextCNNClassifier
	>>> tokenizer = Tokenizer(corpus)
	>>> classifier = TextCNNClassifier(embed_dim, len(classes), vocab_size=tokenizer.vocab_size)
	"""
	
	def __init__(self, embed_dim: int, embedding: Union[nn.Embedding, torch.Tensor, List] = None,
	             vocab_size: int = None,
	             kernel_sizes=(2, 3, 4), cnn_channels: int = 64, activation=None, num_classes: int = 2,
	             num_hidden_layer: int = 0, layer_norm=False, batch_norm=False, residual=False, dropout: float = 0.0,
	             bias=False, **kwargs):
		"""
		:param embed_dim: word embedding维度
		:param embedding: 出入的embedding
		:param vocab_size: vocab size
		:param kernel_sizes: size of each CNN kernel
		:param activation: CNN 激活函数
		:param num_classes: 类别数
		:param num_hidden_layer: 隐藏层数
		:param layer_norm：是否层正则化
		:param batch_norm: 是否层批则化
		:param residual: 是否残差
		:param dropout：
		:param bias:
		"""
		classifier = TextCNN(embed_dim, kernel_sizes, cnn_channels, num_classes, activation, num_hidden_layer,
		                     layer_norm, batch_norm, residual, dropout, bias, **kwargs)
		super().__init__(classifier, embedding, vocab_size, embed_dim, num_classes)


class RNNAttentionClassifier(MaskEmbeddingClassifier):
	"""
	如果是英文、分词, 不用residual 效果比较好
	
	Examples
	--------
	>>> from nlpx.text_token import Tokenizer
	>>> from nlpx.model.classifier import RNNAttentionClassifier
	>>> tokenizer = Tokenizer(corpus)
	>>> classifier = RNNAttentionClassifier(embed_dim, len(classes), vocab_size=tokenizer.vocab_size)
	"""
	
	def __init__(self, embed_dim: int, num_classes: int, embedding: Union[nn.Embedding, torch.Tensor, List] = None,
	             vocab_size: int = None, hidden_size: int = 64, num_layers: int = 2, num_heads: int = 1, rnn=nn.GRU,
	             bidirectional=True, layer_norm=False, residual=False, padding_idx: Optional[int] = None,
	             dropout: float = 0.0, **kwargs):
		"""
		:param embed_dim: word embedding维度
		:param num_classes: 类别数
		:param embedding: 出入的embedding
		:param vocab_size: vocab size
		:param hidden_size: RNN的hidden_size, RNN隐藏层维度
		:param num_layers: RNN的num_layers, RNN层数
		:param num_heads: 抽头数
		:param rnn: 所用的RNN模型：GRU和LSTM，默认是GRU
		:param bidirectional： 是否是双向RNN
		:param layer_norm：是否层正则化
		:param residual: 是否残差
		:param padding_idx
		:param dropout：
		"""
		classifier = RNNAttention(embed_dim, num_classes, hidden_size, num_layers, num_heads, rnn, bidirectional,
								layer_norm, residual, dropout, **kwargs)
		super().__init__(classifier, embedding, vocab_size, embed_dim, padding_idx, num_classes)


class CNNRNNAttentionClassifier(EmbeddingClassifier):
	"""
	Examples
	--------
	>>> from nlpx.text_token import Tokenizer
	>>> from nlpx.model.classifier import CNNRNNAttentionClassifier
	>>> tokenizer = Tokenizer(corpus)
	>>> classifier = CNNRNNAttentionClassifier(embed_dim, num_classes=len(classes), vocab_size=tokenizer.vocab_size)
	"""
	
	def __init__(self, embed_dim: int, seq_length: int = 16, cnn_channels: int = None, kernel_sizes=(2, 3, 4),
	             activation=None, num_classes: int = 2,
	             embedding: Union[nn.Embedding, torch.Tensor, List] = None, vocab_size: int = None,
	             hidden_size: int = 64, num_layers: int = 2, num_heads: int = 2, rnn=nn.GRU, bidirectional=True,
	             layer_norm=False, batch_norm=False, residual=False, padding_idx: Optional[int] = None,
	             dropout: float = 0.0, bias=False):
		"""
		:param embed_dim: word embedding维度
		:param seq_length: 句子序列长度
		:param cnn_channels: CNN out_channels
		:param kernel_sizes: size of each CNN kernel
		:param activation: CNN 激活函数
		:param num_classes: 类别数
		:param embedding: 出入的embedding
		:param vocab_size: vocab size
		:param hidden_size: RNN的hidden_size, RNN隐藏层维度
		:param num_layers: RNN的num_layers, RNN层数
		:param num_heads: 抽头数
		:param rnn: 所用的RNN模型：GRU和LSTM，默认是GRU
		:param bidirectional： 是否是双向RNN
		:param layer_norm：是否层正则化
		:param batch_norm: 是否层批则化
		:param residual: 是否残差
		:param padding_idx
		:param dropout：
		:param bias：
		"""
		cnn_channels = cnn_channels or embed_dim
		classifier = CNNRNNAttention(embed_dim, num_classes, seq_length, cnn_channels, kernel_sizes, activation,
		                             hidden_size,num_layers, num_heads, rnn, bidirectional, layer_norm, batch_norm,
		                             residual, dropout, bias)
		super().__init__(classifier, embedding, vocab_size, embed_dim, padding_idx, num_classes)


class RNNCNNAttentionClassifier(MaskEmbeddingClassifier):
	"""
	Examples
	--------
	>>> from nlpx.text_token import Tokenizer
	>>> from nlpx.model.classifier import CNNRNNAttentionClassifier
	>>> tokenizer = Tokenizer(corpus)
	>>> classifier = RNNCNNAttentionClassifier(embed_dim, num_classes=len(classes), vocab_size=tokenizer.vocab_size)
	"""
	
	def __init__(self, embed_dim: int, seq_length: int = 16, cnn_channels: int = None, kernel_sizes=(2, 3, 4),
	             activation=None, num_classes: int = 2,
	             embedding: Union[nn.Embedding, torch.Tensor, List] = None, vocab_size: int = None,
	             hidden_size: int = 64, num_layers: int = 2, num_heads: int = 2, rnn=nn.GRU, bidirectional=True,
	             layer_norm=False, batch_norm=False, padding_idx: Optional[int] = None, dropout: float = 0.0,
	             bias=False):
		"""
		:param embed_dim: word embedding维度
		:param seq_length: 句子序列长度
		:param cnn_channels: CNN out_channels
		:param kernel_sizes: size of each CNN kernel
		:param activation: CNN 激活函数
		:param num_classes: 类别数
		:param embedding: 出入的embedding
		:param vocab_size: vocab size
		:param hidden_size: RNN的hidden_size, RNN隐藏层维度
		:param num_layers: RNN的num_layers, RNN层数
		:param num_heads: 抽头数
		:param rnn: 所用的RNN模型：GRU和LSTM，默认是GRU
		:param bidirectional： 是否是双向RNN
		:param layer_norm：是否层正则化
		:param batch_norm: 是否层批则化
		:param padding_idx
		:param dropout：
		:param bias：
		"""
		cnn_channels = cnn_channels or embed_dim
		classifier = RNNCNNAttention(embed_dim, num_classes, seq_length, cnn_channels, kernel_sizes, activation, 
							   		hidden_size, num_layers, num_heads, rnn, bidirectional, layer_norm, batch_norm,
		                            dropout, bias)
		super().__init__(classifier, embedding, vocab_size, embed_dim, padding_idx, num_classes)


class ResRNNCNNAttentionClassifier(MaskEmbeddingClassifier):
	"""
	Examples
	--------
	>>> from nlpx.text_token import Tokenizer
	>>> from nlpx.model.classifier import CNNRNNAttentionClassifier
	>>> tokenizer = Tokenizer(texts=corpus)
	>>> classifier = ResRNNCNNAttentionClassifier(embed_dim, num_classes=len(classes), vocab_size=tokenizer.vocab_size)
	"""
	
	def __init__(self, embed_dim: int, seq_length: int = 16, cnn_channels: int = None, kernel_sizes=(2, 3, 4),
	             activation=None, num_classes: int = 2,
	             embedding: Union[nn.Embedding, torch.Tensor, List] = None, vocab_size: int = None,
	             hidden_size: int = 64, num_layers: int = 2, num_heads: int = 2, rnn=nn.GRU, bidirectional=True,
	             layer_norm=False, batch_norm=False, padding_idx: Optional[int] = None, dropout: float = 0.0,
	             bias=False):
		"""
		:param embed_dim: word embedding维度
		:param seq_length: 句子序列长度
		:param cnn_channels: CNN out_channels
		:param kernel_sizes: size of each CNN kernel
		:param activation: CNN 激活函数
		:param num_classes: 类别数
		:param embedding: 出入的embedding
		:param vocab_size: vocab size
		:param hidden_size: RNN的hidden_size, RNN隐藏层维度
		:param num_layers: RNN的num_layers, RNN层数
		:param num_heads: 抽头数
		:param rnn: 所用的RNN模型：GRU和LSTM，默认是GRU
		:param bidirectional： 是否是双向RNN
		:param layer_norm：是否层正则化
		:param batch_norm: 是否层批则化
		:param padding_idx
		:param dropout：
		:param bias：
		"""
		cnn_channels = cnn_channels or embed_dim
		classifier = ResRNNCNNAttention(embed_dim, num_classes, seq_length, cnn_channels, kernel_sizes, activation, 
								  		hidden_size, num_layers, num_heads, rnn, bidirectional, layer_norm, batch_norm,
		                                dropout, bias)
		super().__init__(classifier, embedding, vocab_size, embed_dim, padding_idx, num_classes)


class RotaryAttentionClassifier(nn.Module):
	
	def __init__(self, embed_dim: int, max_length: int, vocab_size: Optional[int] = None, embedding=None,
	             padding_idx: Optional[int] = None, num_classes: int = 2, theta: float = 10000.0, add_cnn=False,
	             dropout: float = 0.):
		"""
		:param embed_dim: word embedding维度
		:param vocab_size: vocab size
		:param embedding: 输入的embedding，可以是nn.Embedding，torch.Tensor，list
		:param padding_idx:
		:param num_classes:
		:param theta:
		:param add_cnn: 是否加入CNN
		:param dropout:
		"""
		super().__init__()
		if add_cnn:
			self.embedding = CNNEmbedding(embed_dim, vocab_size=vocab_size, embedding=embedding,
			                              seq_length=max_length // 3, padding_idx=padding_idx, dropout=dropout)
		else:
			self.embedding = EmbeddingLayer(embed_dim, vocab_size=vocab_size, embedding=embedding,
			                                padding_idx=padding_idx, dropout=dropout)
		self.attention = RotaryClassSelfAttention(embed_dim, max_length, theta)
		self.norm = RMSNorm(embed_dim)
		self.fc = nn.Linear(in_features=embed_dim, out_features=num_classes)
		self.multi_class = num_classes > 1
	
	def forward(self, input_ids: torch.Tensor, start_pos: int = 0):
		embedding = self.embedding(input_ids)
		output = self.attention(embedding, start_pos)
		output = self.norm(output)
		return self.fc(output)
	
	def fit(self, input_ids: torch.Tensor, labels: torch.LongTensor):
		logits = self.forward(input_ids)
		if self.multi_class:
			return F.cross_entropy(logits, labels), logits
		return F.binary_cross_entropy(logits.reshape(-1), labels), logits
