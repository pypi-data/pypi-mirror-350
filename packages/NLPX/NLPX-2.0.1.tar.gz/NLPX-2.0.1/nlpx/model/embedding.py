import torch
from torch import nn
from typing import Optional
from torch_model_hub.model.layer import TextCNNLayer


class EmbeddingLayer(nn.Module):
	
	def __init__(self, embed_dim: int, vocab_size: Optional[int] = None, embedding=None,
	             padding_idx: Optional[int] = None, dropout: float = 0.):
		"""
		:param embed_dim: word embedding维度
		:param vocab_size: vocab size
		:param embedding: 输入的embedding，可以是nn.Embedding，torch.Tensor，list
		:param padding_idx:
		"""
		super().__init__()
		if embedding is None:
			assert vocab_size, 'vocab_size must be ge 0'
			self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx)
		elif isinstance(embedding, nn.Embedding):
			self.embedding = embedding
		elif torch.is_tensor(embedding):
			self.embedding = nn.Embedding.from_pretrained(embedding)
		else:
			self.embedding = nn.Embedding.from_pretrained(torch.tensor(embedding, dtype=torch.float))
		
		if dropout:
			self.embedding = nn.Sequential(
				self.embedding,
				nn.Dropout(dropout)
			)
			
	def forward(self, input_ids: torch.LongTensor):
		"""
		:param input_ids: [(batch_size, sequence_length, embed_dim)]
		:return: [(batch_size, sequence_length, embed_dim)]
		"""
		
		return self.embedding(input_ids)


class CNNEmbedding(nn.Module):
	
	def __init__(self, embed_dim: int, vocab_size: int = None, embedding=None, seq_length: int = 16,
	             out_channels: int = None, kernel_sizes=(2, 3, 4), activation=None, batch_norm=False, bias=False,
	             padding_idx: Optional[int] = None, dropout: float = 0.):
		"""
		:param embed_dim: word embedding维度
		:param vocab_size: vocab size
		:param embedding: 输入的embedding，可以是nn.Embedding，torch.Tensor，list
		:param seq_length: 句子序列长度
		:param out_channels: CNN out_channels, default embed_dim
		:param kernel_sizes: size of each CNN kernel
		:param activation: CNN 激活函数
		:param batch_norm: 是否批正则化
		:param bias:
		:param padding_idx:
		:param dropout:
		"""
		super().__init__()
		out_channels = out_channels or embed_dim
		if dropout:
			self.embedding = nn.Sequential(
				EmbeddingLayer(embed_dim, vocab_size, embedding, padding_idx),
				TextCNNLayer(embed_dim, seq_length, out_channels, kernel_sizes, activation, batch_norm, bias),
				nn.Dropout(dropout)
			)
		else:
			self.embedding = nn.Sequential(
				EmbeddingLayer(embed_dim, vocab_size, embedding, padding_idx),
				TextCNNLayer(embed_dim, seq_length, out_channels, kernel_sizes, activation, batch_norm, bias)
			)
	
	def forward(self, input_ids: torch.LongTensor):
		"""
		:param input_ids: [(batch_size, sequence_length, embed_dim)]
		:return: [(batch_size, seq_length * len(kernel_sizes), out_channels)]
		"""
		return self.embedding(input_ids)
