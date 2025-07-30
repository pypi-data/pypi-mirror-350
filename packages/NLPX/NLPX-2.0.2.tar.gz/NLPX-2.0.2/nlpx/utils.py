import torch
import numpy as np
from model_wrapper.utils import get_device


def subsequent_mask(size: int):
	mask_shape = (1, size, size)
	mask = np.triu(np.ones(mask_shape), k=1).astype(np.int8)
	return torch.from_numpy(1 - mask)


if __name__ == '__main__':
	print(subsequent_mask(5))
