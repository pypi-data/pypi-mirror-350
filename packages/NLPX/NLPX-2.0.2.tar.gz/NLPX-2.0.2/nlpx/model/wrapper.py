import numpy as np
import pandas as pd
import torch
from torch import nn
from torch import optim
from pathlib import Path
from typing import Union, List, Tuple, Collection, Callable
from sklearn.model_selection import train_test_split
from torch.optim.lr_scheduler import LRScheduler
from torch.utils.data import Sampler
from model_wrapper.utils import acc_predict, convert_to_long_tensor

from model_wrapper import (
    ModelWrapper,
    FastModelWrapper,
    SplitModelWrapper,
    ClassifyModelWrapper,
    FastClassifyModelWrapper,
    SplitClassifyModelWrapper,
    RegressModelWrapper,
    FastRegressModelWrapper,
    SplitRegressModelWrapper,
)

from nlpx.dataset import TokenDataset, PaddingTokenCollator
from nlpx.tokenize import (
    BaseTokenizer,
    PaddingTokenizer,
    SimpleTokenizer,
    Tokenizer,
    TokenEmbedding,
)

__all__ = [
    "ModelWrapper",
    "FastModelWrapper",
    "SplitModelWrapper",
    "ClassifyModelWrapper",
    "FastClassifyModelWrapper",
    "SplitClassifyModelWrapper",
    "TextModelWrapper",
    "SplitTextModelWrapper",
    "PaddingTextModelWrapper",
    "SplitPaddingTextModelWrapper",
    "RegressModelWrapper",
    "FastRegressModelWrapper",
    "SplitRegressModelWrapper",
]

class TextModelWrapper(FastClassifyModelWrapper):
    """
    Examples
    --------
    >>> from nlpx.model.wrapper import TextModelWrapper
    >>> model_wrapper = TextModelWrapper(model, tokenize_vec, classes=classes)
    >>> model_wrapper.train(train_texts, y_train, val_data, collate_fn)
    >>> model_wrapper.predict(test_texts)
    >>> model_wrapper.evaluate(test_texts, y_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        tokenize_vec,
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        """
        :param model_or_path:
        :param tokenize_vec: BaseTokenizer, TokenizeVec, TokenEmbedding
        :param classes:
        :param device:

        """
        super().__init__(model_or_path, classes, device)
        self.tokenize_vec = tokenize_vec

    def train(
        self,
        texts: Union[Collection[str], np.ndarray, pd.Series],
        y: Union[torch.LongTensor, np.ndarray, List],
        val_data: Tuple[
            Union[Collection[str], np.ndarray, pd.Series],
            Union[torch.LongTensor, np.ndarray, List],
        ] = None,
        max_length: int = None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Union[Sampler, bool] = None,
        weight: Union[torch.Tensor, np.ndarray, List] = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        n_jobs=-1,
        show_progress=True,
        amp: bool = False,
        eps=1e-5,
        monitor: str = "accuracy"
    ) -> dict:
        """
        训练模型
        
        参数:
            texts: 输入文本数据，支持字符串集合、numpy数组或pandas Series
            y: 目标标签，支持torch张量、numpy数组或列表
            val_data: 验证数据集，包含文本和标签的元组
            max_length: 文本最大长度限制
            collate_fn: 数据整理函数
            epochs: 训练轮数
            optimizer: 优化器类或实例
            scheduler: 学习率调度器
            lr: 初始学习率
            T_max: 学习率调度周期
            batch_size: 训练批次大小
            eval_batch_size: 评估批次大小
            sampler: 采样器实例或是否启用平衡采样
            weight: 类别权重
            num_workers: 训练数据加载工作线程数
            num_eval_workers: 评估数据加载工作线程数
            pin_memory: 是否固定内存
            pin_memory_device: 固定内存设备
            persistent_workers: 是否保持工作线程
            early_stopping_rounds: 早停轮数
            print_per_rounds: 打印间隔轮数
            drop_last: 是否丢弃不完整批次
            checkpoint_per_rounds: 模型保存间隔轮数
            checkpoint_name: 模型保存名称
            n_jobs: 并行工作数
            show_progress: 是否显示进度条
            amp: 是否启用自动混合精度
            eps: 数值稳定系数
            monitor: 监控指标名称
            
        返回:
            包含训练结果的字典
        """
        if isinstance(y, List):
            y = np.array(y, dtype=np.int64)

        if sampler is not None and isinstance(sampler, bool) and sampler:
            if weight is None:
                sampler, weight = self.get_balance_sampler(y, return_weights=True)
            else:
                sampler = self.get_balance_sampler_from_weights(y, weight)

        X_train = self.get_vec(texts, max_length=max_length, n_jobs=n_jobs)
        if val_data:
            val_data = (
                self.get_vec(val_data[0], max_length=max_length, n_jobs=-1),
                val_data[1],
            )

        return super().train(X_train, y, val_data, collate_fn, epochs, optimizer, scheduler, lr, T_max,
                            batch_size, eval_batch_size, sampler, weight, num_workers, num_eval_workers, pin_memory,
                            pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds, 
                            drop_last, checkpoint_per_rounds, checkpoint_name, show_progress, amp, eps, monitor)

    def train_evaluate(
        self,
        texts: Union[Collection[str], np.ndarray, pd.Series],
        y: Union[torch.LongTensor, np.ndarray, List],
        val_data: Tuple[
            Union[Collection[str], np.ndarray, pd.Series],
            Union[torch.LongTensor, np.ndarray, List],
        ],
        max_length: int = None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Union[Sampler, bool] = None,
        weight: Union[torch.Tensor, np.ndarray, List] = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        n_jobs=-1,
        show_progress=True,
        amp: bool = False,
        eps=1e-5,
        monitor: str = "accuracy",
        verbose: bool = True,
        threshold: float = 0.5,
        target_names: List[str] = None,
        num_classes: int = None
    ) -> Tuple[dict, dict]:
        """
        训练并评估模型
        
        参数:
            texts: 训练文本数据，支持多种格式(字符串集合/numpy数组/pandas Series)
            y: 训练标签，支持多种格式(torch张量/numpy数组/列表)
            val_data: 验证数据元组(文本数据, 标签)
            max_length: 文本最大长度限制
            collate_fn: 数据批处理函数
            epochs: 训练轮数
            optimizer: 优化器类或实例
            scheduler: 学习率调度器
            lr: 初始学习率
            T_max: 学习率调度周期
            batch_size: 训练批次大小
            eval_batch_size: 评估批次大小
            sampler: 采样器或是否启用平衡采样
            weight: 类别权重
            num_workers: 训练数据加载工作线程数
            num_eval_workers: 评估数据加载工作线程数
            pin_memory: 是否固定内存
            pin_memory_device: 固定内存设备
            persistent_workers: 是否保持工作进程
            early_stopping_rounds: 早停轮数
            print_per_rounds: 打印间隔轮数
            drop_last: 是否丢弃不完整批次
            checkpoint_per_rounds: 模型保存间隔轮数
            checkpoint_name: 模型保存名称
            n_jobs: 向量化并行工作数
            show_progress: 是否显示进度条
            amp: 是否启用自动混合精度
            eps: 数值稳定系数
            monitor: 监控指标
            verbose: 是否输出详细信息
            threshold: 分类阈值
            target_names: 类别名称列表
            num_classes: 类别数量
            
        返回:
            包含训练和评估结果的元组(训练指标字典, 验证指标字典)
        """

        if isinstance(y, List):
            y = np.array(y, dtype=np.int64)

        if sampler is not None and isinstance(sampler, bool) and sampler:
            if weight is None:
                sampler, weight = self.get_balance_sampler(y, return_weights=True)
            else:
                sampler = self.get_balance_sampler_from_weights(y, weight)

        X_train = self.get_vec(texts, max_length=max_length, n_jobs=n_jobs)
        if val_data:
            val_data = (
                self.get_vec(val_data[0], max_length=max_length, n_jobs=-1),
                val_data[1],
            )

        return super().train_evaluate(X_train, y, val_data, collate_fn, epochs, optimizer, scheduler, lr, T_max,
                                batch_size, eval_batch_size, sampler, weight, num_workers, num_eval_workers, pin_memory,
                                pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds, 
                                drop_last, checkpoint_per_rounds, checkpoint_name, show_progress, amp, eps, monitor,
                                verbose, threshold, target_names, num_classes)
    
    def predict(
        self,
        texts: Collection[str],
        max_length: int = None,
        n_jobs=-1,
        threshold: float = 0.5,
    ) -> np.ndarray:
        """
        :param texts:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        logits = self.logits(texts, max_length, n_jobs=n_jobs)
        return acc_predict(logits.cpu(), threshold)

    def predict_classes(
        self,
        texts: Collection[str],
        max_length: int = None,
        n_jobs=-1,
        threshold: float = 0.5,
    ) -> list:
        """
        :param texts:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        pred = self.predict(texts, max_length, n_jobs, threshold)
        return self._predict_classes(pred.ravel())

    def predict_proba(
        self,
        texts: Collection[str],
        max_length: int = None,
        n_jobs=-1,
        threshold: float = 0.5,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        :param texts:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        logits = self.logits(texts, max_length, n_jobs=n_jobs)
        return self._proba(logits, threshold)

    def predict_classes_proba(
        self,
        texts: Collection[str],
        max_length: int = None,
        n_jobs=-1,
        threshold: float = 0.5,
    ) -> Tuple[list, np.ndarray]:
        """
        :param texts:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        indices, values = self.predict_proba(texts, max_length, n_jobs, threshold)
        return self._predict_classes(indices.ravel()), values

    def logits(
        self, texts: Collection[str], max_length: int = None, n_jobs=-1
    ) -> torch.Tensor:
        X = self.get_vec(texts, max_length, n_jobs=n_jobs)
        return super().logits(X)

    def acc(
        self,
        texts: Union[str, Collection[str], np.ndarray, pd.Series],
        y: Union[torch.LongTensor, np.ndarray, List],
        batch_size: int = 64,
        num_workers: int = 0,
        max_length: int = None,
        collate_fn: Callable = None,
        n_jobs=-1,
        threshold: float = 0.5,
    ) -> dict[str, float]:
        """return accuracy"""
        X = self.get_vec(texts, max_length, n_jobs=n_jobs)
        return super().acc(X, y, batch_size, num_workers, collate_fn, threshold)
    
    def confusion_matrix(
        self,
        texts: Union[str, Collection[str], np.ndarray, pd.Series],
        y: Union[torch.LongTensor, np.ndarray, List],
        batch_size: int = 64,
        num_workers: int = 0,
        max_length: int = None,
        collate_fn: Callable = None,
        n_jobs=-1,
        threshold: float = 0.5,
        verbose: bool = True,
    ) -> dict[str, float]:
        """return confusion matrix"""
        X = self.get_vec(texts, max_length, n_jobs=n_jobs)
        return super().confusion_matrix(X, y, batch_size, num_workers, collate_fn, threshold, verbose=verbose)

    def evaluate(
        self,
        texts: Union[str, Collection[str], np.ndarray, pd.Series],
        y: Union[torch.LongTensor, np.ndarray, List],
        batch_size: int = 64,
        num_workers: int = 0,
        max_length: int = None,
        collate_fn: Callable = None,
        n_jobs=-1,
        threshold: float = 0.5,
        verbose: bool = True,
    ) -> dict[str, float]:
        """return metrics"""
        X = self.get_vec(texts, max_length, n_jobs=n_jobs)
        return super().evaluate(X, y, batch_size, num_workers, collate_fn, threshold, verbose=verbose)
    
    def classification_report(
        self,
        texts: Union[str, Collection[str], np.ndarray, pd.Series],
        y: Union[torch.LongTensor, np.ndarray, List],
        batch_size: int = 64,
        num_workers: int = 0,
        max_length: int = None,
        collate_fn: Callable = None,
        n_jobs=-1,
        threshold: float = 0.5,
        target_names: List = None,
        verbose: bool = True,
    ) -> dict[str, float]:
        """return metrics"""
        X = self.get_vec(texts, max_length, n_jobs=n_jobs)
        return super().classification_report(X, y, batch_size, num_workers, collate_fn, threshold, target_names, verbose=verbose)

    def get_vec(
        self,
        texts: Union[str, Collection[str], np.ndarray, pd.Series],
        max_length: int,
        n_jobs: int,
    ):
        if isinstance(texts, str):
            texts = [texts]

        if isinstance(self.tokenize_vec, (PaddingTokenizer, SimpleTokenizer, Tokenizer)):
            return torch.LongTensor(self.tokenize_vec.batch_encode(texts, max_length))

        elif isinstance(self.tokenize_vec, TokenEmbedding):
            return self.tokenize_vec(texts, max_length)

        return self.tokenize_vec.parallel_encode_plus(
            texts,
            max_length=max_length,
            padding="max_length",
            truncation=True,
            add_special_tokens=True,
            return_token_type_ids=True,
            return_attention_mask=True,
            return_tensors="pt",
            n_jobs=n_jobs,
        )


class SplitTextModelWrapper(TextModelWrapper):
    """
    Examples
    --------
    >>> from nlpx.model.wrapper import SplitTextModelWrapper
    >>> model_wrapper = SplitTextModelWrapper(model, tokenize_vec, classes=classes)
    >>> model_wrapper.train(texts, y, collate_fn)
    >>> model_wrapper.predict(test_texts)
    >>> model_wrapper.evaluate(test_texts, y_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        tokenize_vec,
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        """
        :param model_or_path: nn.Module or str or Path
        :param tokenize_vec: TokenizeVec or TokenEmbedding or Tokenizer or PaddingTokenizer or SimpleTokenizer
        """
        super().__init__(model_or_path, tokenize_vec, classes, device)

    def train(
        self,
        texts: Union[Collection[str], np.ndarray, pd.Series],
        y: Union[torch.LongTensor, np.ndarray, List],
        max_length: int = None,
        val_size=0.2,
        random_state=None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Union[Sampler, bool] = None,
        weight: Union[torch.Tensor, np.ndarray, List] = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        n_jobs=-1,
        show_progress=True,
        amp: bool = False,
        eps=1e-5,
        monitor: str = "accuracy"
    ) -> dict:
        """训练文本分类模型
        
        参数：
            texts: 输入文本数据，支持字符串集合、numpy数组或pandas Series
            y: 目标标签，支持torch张量、numpy数组或列表
            max_length: 文本最大截断长度
            val_size: 验证集比例，0-1之间
            random_state: 随机种子
            collate_fn: 自定义数据批处理函数
            epochs: 训练轮数
            optimizer: 优化器类型或实例
            scheduler: 学习率调度器
            lr: 初始学习率
            T_max: 学习率周期最大值
            batch_size: 训练批次大小
            eval_batch_size: 评估批次大小
            sampler: 采样器或是否启用采样
            weight: 类别权重
            num_workers: 训练数据加载线程数
            num_eval_workers: 评估数据加载线程数
            pin_memory: 是否锁页内存
            pin_memory_device: 锁页内存设备
            persistent_workers: 是否保持工作进程
            early_stopping_rounds: 早停轮数
            print_per_rounds: 打印间隔轮数
            drop_last: 是否丢弃不完整批次
            checkpoint_per_rounds: 模型保存间隔轮数
            checkpoint_name: 模型保存名称
            n_jobs: 特征提取并行数
            show_progress: 是否显示进度条
            amp: 是否启用混合精度
            eps: 数值稳定系数
            monitor: 监控指标名称
        
        返回：
            dict: 包含训练过程记录的字典
        """
        
        # 文本向量化处理
        X = self.get_vec(texts, max_length=max_length, n_jobs=n_jobs)
        
        # 划分训练集和验证集
        if 0.0 < val_size < 1.0:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=val_size, random_state=random_state
            )
            val_data = (X_test, y_test)
        else:
            X_train, y_train = X, y
            val_data = None
            
        # 调用的是TextModelWrapper 父类FastClassifyModelWrapper 的train方法
        return super(TextModelWrapper, self).train(
            X_train, y_train, val_data, collate_fn, epochs, optimizer, scheduler, lr, T_max,
            batch_size, eval_batch_size, sampler, weight, num_workers, num_eval_workers, pin_memory,
            pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds, 
            drop_last, checkpoint_per_rounds, checkpoint_name, show_progress, amp, eps, monitor
        )

    def train_evaluate(
        self,
        texts: Union[Collection[str], np.ndarray, pd.Series],
        y: Union[torch.LongTensor, np.ndarray, List],
        max_length: int = None,
        val_size=0.2,
        random_state=None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Sampler = None,
        weight: Union[torch.Tensor, np.ndarray, List] = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        n_jobs=-1,
        show_progress=True,
        amp: bool = False,
        eps=1e-5,
        monitor: str = "accuracy",
        verbose: bool = True,
        threshold: float = 0.5,
        target_names: List[str] = None,
        num_classes: int = None
    ) -> Tuple[dict, dict]:
        """
        训练并评估文本分类模型
        
        参数:
            texts: 输入文本数据，支持多种格式(字符串集合/numpy数组/pandas Series)
            y: 目标标签，支持多种格式(torch张量/numpy数组/列表)
            max_length: 文本最大长度(截断/填充)
            val_size: 验证集比例(默认0.2)
            random_state: 随机种子
            collate_fn: 自定义数据批处理函数
            epochs: 训练轮数(默认100)
            optimizer: 优化器类型或实例
            scheduler: 学习率调度器
            lr: 初始学习率(默认0.001)
            T_max: 学习率调度周期
            batch_size: 训练批次大小(默认64)
            eval_batch_size: 评估批次大小(默认128)
            sampler: 数据采样器
            weight: 类别权重
            num_workers: 训练数据加载线程数
            num_eval_workers: 评估数据加载线程数
            pin_memory: 是否固定内存
            pin_memory_device: 固定内存设备
            persistent_workers: 是否保持工作进程
            early_stopping_rounds: 早停轮数
            print_per_rounds: 打印间隔轮数
            drop_last: 是否丢弃不完整批次
            checkpoint_per_rounds: 模型保存间隔轮数
            checkpoint_name: 模型保存名称
            n_jobs: 特征提取并行数
            show_progress: 是否显示进度条
            amp: 是否启用自动混合精度
            eps: 数值稳定系数
            monitor: 早停监控指标(默认"accuracy")
            verbose: 是否输出详细信息
            threshold: 分类阈值(默认0.5)
            target_names: 类别名称列表
            num_classes: 类别数量
            
        返回:
            Tuple[dict, dict]: 训练结果字典和评估结果字典
        """

        assert 0.0 < val_size < 1.0
        X = self.get_vec(texts, max_length=max_length, n_jobs=n_jobs)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=val_size, random_state=random_state
        )
        val_data = (X_test, y_test)

        # 调用的是TextModelWrapper 父类FastClassifyModelWrapper的train_evaluate方法    
        return super(TextModelWrapper, self).train_evaluate(
            X_train, y_train, val_data, collate_fn, epochs, optimizer, scheduler, lr, T_max,
            batch_size, eval_batch_size, sampler, weight, num_workers, num_eval_workers, pin_memory,
            pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds, 
            drop_last, checkpoint_per_rounds, checkpoint_name, show_progress, amp, eps, monitor,
            verbose, threshold, target_names, num_classes
        )


class PaddingTextModelWrapper(ClassifyModelWrapper):
    """
    Examples
    --------
    >>> from nlpx.model.wrapper import PaddingTextModelWrapper
    >>> model_wrapper = PaddingTextModelWrapper(model, tokenizer, classes=classes)
    >>> model_wrapper.train(train_texts, y_train val_data)
    >>> model_wrapper.predict(test_texts)
    >>> model_wrapper.evaluate(test_texts, y_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        tokenizer: Union[PaddingTokenizer, SimpleTokenizer, Tokenizer],
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, classes, device)
        self.tokenizer = tokenizer

    def train(
        self,
        texts: Union[Collection[str], np.ndarray, pd.Series],
        y: Union[torch.LongTensor, np.ndarray, List],
        val_data: Tuple[
            Union[Collection[str], np.ndarray, pd.Series],
            Union[torch.LongTensor, np.ndarray, List],
        ] = None,
        max_length: int = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Union[Sampler, bool] = None,
        weight: Union[torch.Tensor, np.ndarray, List] = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        amp: bool = False,
        eps=1e-5,
        monitor: str = "accuracy"
    ) -> dict:
        """
        训练模型
        
        参数:
            texts: 训练文本数据，支持字符串集合、numpy数组或pandas Series
            y: 训练标签，支持torch张量、numpy数组或列表
            val_data: 验证数据，包含文本和标签的元组，可选
            max_length: 文本最大长度，可选
            epochs: 训练轮数，默认100
            optimizer: 优化器类或实例，可选
            scheduler: 学习率调度器，可选
            lr: 学习率，默认0.001
            T_max: 学习率调度器参数，默认0
            batch_size: 训练批次大小，默认64
            eval_batch_size: 评估批次大小，默认128
            sampler: 采样器实例或布尔值，为True时自动创建平衡采样器
            weight: 类别权重，可选
            num_workers: 训练数据加载工作线程数，默认0
            num_eval_workers: 评估数据加载工作线程数，默认0
            pin_memory: 是否固定内存，默认False
            pin_memory_device: 固定内存设备，默认空字符串
            persistent_workers: 是否保持工作线程，默认False
            early_stopping_rounds: 早停轮数，可选
            print_per_rounds: 打印间隔轮数，默认1
            drop_last: 是否丢弃不完整批次，默认False
            checkpoint_per_rounds: 检查点保存间隔轮数，默认0(不保存)
            checkpoint_name: 检查点文件名，默认"model.pt"
            show_progress: 是否显示进度条，默认True
            amp: 是否使用自动混合精度，默认False
            eps: 数值稳定系数，默认1e-5
            monitor: 监控指标，默认"accuracy"
            
        返回:
            包含训练结果的字典
        """
        if isinstance(y, List):
            y = np.array(y, dtype=np.int64)

        if sampler is not None and isinstance(sampler, bool) and sampler:
            if weight is None:
                sampler, weight = self.get_balance_sampler(y, return_weights=True)
            else:
                sampler = self.get_balance_sampler_from_weights(y, weight)

        X = self.tokenizer.batch_encode(texts, padding=False)
        train_set = TokenDataset(X, y)
        val_set = None
        if val_data:
            X_val = self.tokenizer.batch_encode(val_data[0], padding=False)
            val_set = TokenDataset(X_val, val_data[1])

        return super().train(
            train_set,
            val_set,
            collate_fn=PaddingTokenCollator(self.tokenizer.pad, max_length),
            epochs=epochs,
            optimizer=optimizer,
            scheduler=scheduler,
            lr=lr,
            T_max=T_max,
            batch_size=batch_size,
            eval_batch_size=eval_batch_size,
            sampler=sampler,
            num_workers=num_workers,
            num_eval_workers=num_eval_workers,
            pin_memory=pin_memory,
            pin_memory_device=pin_memory_device,
            persistent_workers=persistent_workers,
            early_stopping_rounds=early_stopping_rounds,
            print_per_rounds=print_per_rounds,
            drop_last=drop_last,
            checkpoint_per_rounds=checkpoint_per_rounds,
            checkpoint_name=checkpoint_name,
            show_progress=show_progress,
            amp=amp,
            eps=eps,
            monitor=monitor
        )
    
    def train_evaluate(
        self,
        texts: Union[Collection[str], np.ndarray, pd.Series],
        y: Union[torch.LongTensor, np.ndarray, List],
        val_data: Tuple[
            Union[Collection[str], np.ndarray, pd.Series],
            Union[torch.LongTensor, np.ndarray, List],
        ],
        max_length: int = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Union[Sampler, bool] = None,
        weight: Union[torch.Tensor, np.ndarray, List] = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        amp: bool = False,
        eps=1e-5,
        monitor: str = "accuracy",
        verbose: bool = True,
        threshold: float = 0.5,
        target_names: List[str] = None,
        num_classes: int = None
    ) -> Tuple[dict, dict]:
        """训练并评估模型
        
        参数说明:
        - texts: 训练文本数据，支持字符串集合、numpy数组或pandas Series
        - y: 训练标签，支持torch.LongTensor、numpy数组或列表
        - val_data: 验证数据元组(验证文本, 验证标签)
        - max_length: 最大序列长度(默认None表示不限制)
        - epochs: 训练轮数(默认100)
        - optimizer: 优化器类或实例(默认None)
        - scheduler: 学习率调度器(默认None)
        - lr: 学习率(默认0.001)
        - T_max: 学习率调度器周期(默认0)
        - batch_size: 训练批次大小(默认64)
        - eval_batch_size: 评估批次大小(默认128)
        - sampler: 采样器或布尔值(默认None)
        - weight: 类别权重(默认None)
        - num_workers: 训练数据加载线程数(默认0)
        - num_eval_workers: 评估数据加载线程数(默认0)
        - pin_memory: 是否固定内存(默认False)
        - pin_memory_device: 固定内存设备(默认"")
        - persistent_workers: 是否保持工作进程(默认False)
        - early_stopping_rounds: 早停轮数(默认None)
        - print_per_rounds: 打印间隔轮数(默认1)
        - drop_last: 是否丢弃不完整批次(默认False)
        - checkpoint_per_rounds: 模型保存间隔轮数(默认0)
        - checkpoint_name: 模型保存名称(默认"model.pt")
        - show_progress: 是否显示进度条(默认True)
        - amp: 是否使用自动混合精度(默认False)
        - eps: 数值稳定系数(默认1e-5)
        - monitor: 监控指标(默认"accuracy")
        - verbose: 是否显示详细信息(默认True)
        - threshold: 分类阈值(默认0.5)
        - target_names: 类别名称列表(默认None)
        - num_classes: 类别数量(默认None)
        
        返回值:
        - 训练结果字典和评估结果字典组成的元组
        """
        if isinstance(y, List):
            y = np.array(y, dtype=np.int64)

        if sampler is not None and isinstance(sampler, bool) and sampler:
            if weight is None:
                sampler, weight = self.get_balance_sampler(y, return_weights=True)
            else:
                sampler = self.get_balance_sampler_from_weights(y, weight)

        X = self.tokenizer.batch_encode(texts, padding=False)
        X_val = self.tokenizer.batch_encode(val_data[0], padding=False)
        train_set = TokenDataset(X, y)
        val_set = TokenDataset(X_val, val_data[1])
        return super().train_evaluate(
            train_set,
            val_set,
            collate_fn=PaddingTokenCollator(self.tokenizer.pad, max_length),
            epochs=epochs,
            optimizer=optimizer,
            scheduler=scheduler,
            lr=lr,
            T_max=T_max,
            batch_size=batch_size,
            eval_batch_size=eval_batch_size,
            sampler=sampler,
            num_workers=num_workers,
            num_eval_workers=num_eval_workers,
            pin_memory=pin_memory,
            pin_memory_device=pin_memory_device,
            persistent_workers=persistent_workers,
            early_stopping_rounds=early_stopping_rounds,
            print_per_rounds=print_per_rounds,
            drop_last=drop_last,
            checkpoint_per_rounds=checkpoint_per_rounds,
            checkpoint_name=checkpoint_name,
            show_progress=show_progress,
            amp=amp,
            eps=eps,
            monitor=monitor,
            verbose=verbose,
            threshold=threshold,
            target_names=target_names,
            num_classes=num_classes,
        )

    def predict(
        self, texts: Collection[str], max_length: int = None, threshold: float = 0.5
    ) -> np.ndarray:
        """
        :param texts:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        logits = self.logits(texts, max_length)
        return acc_predict(logits.cpu(), threshold)

    def predict_classes(
        self, texts: Collection[str], max_length: int = None, threshold: float = 0.5
    ) -> list:
        """
        :param texts:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        pred = self.predict(texts, max_length, threshold)
        return self._predict_classes(pred.ravel())

    def predict_proba(
        self, texts: Collection[str], max_length: int = None, threshold: float = 0.5
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        :param texts:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        logits = self.logits(texts, max_length)
        return self._proba(logits)

    def predict_classes_proba(
        self, texts: Collection[str], max_length: int = None, threshold: float = 0.5
    ) -> Tuple[list, np.ndarray]:
        """
        :param texts:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        indices, values = self.predict_proba(texts, max_length, threshold)
        return self._predict_classes(indices.ravel()), values

    def logits(self, texts: Collection[str], max_length: int = None) -> torch.Tensor:
        X = self.tokenizer.batch_encode(texts, max_length)
        X = torch.from_numpy(np.array(X, np.int64))
        return super().logits(X)

    def acc(
        self,
        texts: Union[str, Collection[str], np.ndarray, pd.Series],
        y: Union[torch.LongTensor, np.ndarray, List],
        batch_size: int = 64,
        num_workers: int = 0,
        max_length: int = None,
        threshold: float = 0.5,
    ) -> float:
        """return accuracy"""
        X = self.tokenizer.batch_encode(texts, padding=False)
        y = convert_to_long_tensor(y)
        val_set = TokenDataset(X, y)
        return super().acc(
            val_set,
            batch_size=batch_size,
            num_workers=num_workers,
            collate_fn=PaddingTokenCollator(self.tokenizer.pad, max_length),
            threshold=threshold,
        )
    
    def confusion_matrix(
            self,
            texts: Union[str, Collection[str], np.ndarray, pd.Series],
            y: Union[torch.LongTensor, np.ndarray, List],
            batch_size: int = 64,
            num_workers: int = 0,
            max_length: int = None,
            threshold: float = 0.5,
            verbose: bool = True,
        ) -> dict[str, float]:
            """return confusion matrix"""
            X = self.tokenizer.batch_encode(texts, padding=False)
            y = convert_to_long_tensor(y)
            val_set = TokenDataset(X, y)
            return super().confusion_matrix(
                val_set,
                batch_size=batch_size,
                num_workers=num_workers,
                collate_fn=PaddingTokenCollator(self.tokenizer.pad, max_length),
                threshold=threshold,
                verbose=verbose,
            )

    def evaluate(
            self,
            texts: Union[str, Collection[str], np.ndarray, pd.Series],
            y: Union[torch.LongTensor, np.ndarray, List],
            batch_size: int = 64,
            num_workers: int = 0,
            max_length: int = None,
            threshold: float = 0.5,
            verbose: bool = True,
        ) -> dict[str, float]:
            """return metrics"""
            X = self.tokenizer.batch_encode(texts, padding=False)
            y = convert_to_long_tensor(y)
            val_set = TokenDataset(X, y)
            return super().evaluate(
                val_set,
                batch_size=batch_size,
                num_workers=num_workers,
                collate_fn=PaddingTokenCollator(self.tokenizer.pad, max_length),
                threshold=threshold,
                verbose=verbose,
            )
    
    def classification_report(
            self,
            texts: Union[str, Collection[str], np.ndarray, pd.Series],
            y: Union[torch.LongTensor, np.ndarray, List],
            batch_size: int = 64,
            num_workers: int = 0,
            max_length: int = None,
            threshold: float = 0.5,
            target_names: List[str] = None,
            verbose: bool = True,
        ) -> dict[str, float]:
            """return metrics"""
            X = self.tokenizer.batch_encode(texts, padding=False)
            y = convert_to_long_tensor(y)
            val_set = TokenDataset(X, y)
            return super().classification_report(
                val_set,
                batch_size=batch_size,
                num_workers=num_workers,
                collate_fn=PaddingTokenCollator(self.tokenizer.pad, max_length),
                threshold=threshold,
                target_names=target_names,
                verbose=verbose,
            )


class SplitPaddingTextModelWrapper(PaddingTextModelWrapper):
    """
    Examples
    --------
    >>> from nlpx.model.wrapper import SplitPaddingTextModelWrapper
    >>> model_wrapper = SplitPaddingTextModelWrapper(tokenizer, classes=classes)
    >>> model_wrapper.train(model, texts, y)
    >>> model_wrapper.predict(test_texts)
    >>> model_wrapper.evaluate(test_texts, y_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        tokenizer: Union[PaddingTokenizer, SimpleTokenizer, Tokenizer],
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, tokenizer, classes, device)

    def train(
        self,
        texts: Union[Collection[str], np.ndarray, pd.Series],
        y: Union[torch.LongTensor, np.ndarray, List],
        max_length: int = None,
        val_size=0.2,
        random_state=None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Union[Sampler, bool] = None,
        weight: Union[torch.Tensor, np.ndarray, List] = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        amp: bool = False,
        eps=1e-5,
        monitor: str = "accuracy"
    ) -> dict:
        """训练模型
        
        参数:
            texts: 输入文本数据，支持字符串集合、numpy数组或pandas Series
            y: 目标标签，支持torch张量、numpy数组或列表
            max_length: 文本最大长度，None表示不限制
            val_size: 验证集比例，0.0-1.0之间或整数
            random_state: 随机种子，保证可复现性
            epochs: 训练轮数
            optimizer: 优化器类或实例
            scheduler: 学习率调度器
            lr: 初始学习率
            T_max: 学习率调度周期
            batch_size: 训练批次大小
            eval_batch_size: 评估批次大小
            sampler: 采样器或是否启用采样
            weight: 类别权重
            num_workers: 训练数据加载线程数
            num_eval_workers: 评估数据加载线程数
            pin_memory: 是否固定内存
            pin_memory_device: 固定内存的设备
            persistent_workers: 是否保持工作进程
            early_stopping_rounds: 早停轮数
            print_per_rounds: 打印间隔轮数
            drop_last: 是否丢弃不完整批次
            checkpoint_per_rounds: 检查点保存间隔
            checkpoint_name: 检查点文件名
            show_progress: 是否显示进度条
            amp: 是否启用自动混合精度
            eps: 数值稳定系数
            monitor: 监控指标名称
            
        返回:
            dict: 包含训练结果的字典
        """

        if 0.0 < val_size < 1.0:
            X_train, X_test, y_train, y_test = train_test_split(
                texts, y, test_size=val_size, random_state=random_state
            )
            val_data = (X_test, y_test)
        else:
            X_train, y_train = texts, y
            val_data = None
            
        return super().train(
            X_train, y_train, val_data, max_length, epochs, optimizer, scheduler, lr, T_max,
            batch_size, eval_batch_size, sampler, weight, num_workers, num_eval_workers, pin_memory,
            pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds, 
            drop_last, checkpoint_per_rounds, checkpoint_name, show_progress, amp, eps, monitor
        )

    def train_evaluate(
        self,
        texts: Union[Collection[str], np.ndarray, pd.Series],
        y: Union[torch.LongTensor, np.ndarray, List],
        max_length: int = None,
        val_size=0.2,
        random_state=None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        sampler: Union[Sampler, bool] = None,
        weight: Union[torch.Tensor, np.ndarray, List] = None,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        amp: bool = False,
        eps=1e-5,
        monitor: str = "accuracy",
        verbose: bool = True,
        threshold: float = 0.5,
        target_names: List[str] = None,
        num_classes: int = None
    ) -> Tuple[dict, dict]:
        """
        训练并评估模型的函数。

        参数:
        - texts: 输入文本数据，可以是集合、numpy数组或pandas Series。
        - y: 标签数据，可以是torch.LongTensor、numpy数组或列表。
        - max_length: 文本的最大长度，默认为None。
        - val_size: 验证集占总数据的比例，范围为0到1，默认为0.2。
        - random_state: 随机种子，用于划分训练集和验证集，默认为None。
        - epochs: 训练轮数，默认为100。
        - optimizer: 优化器类型或实例，默认为None。
        - scheduler: 学习率调度器，默认为None。
        - lr: 学习率，默认为0.001。
        - T_max: 学习率调度器的周期参数，默认为0。
        - batch_size: 训练时的批量大小，默认为64。
        - eval_batch_size: 验证时的批量大小，默认为128。
        - sampler: 数据采样器，可以是Sampler对象或布尔值，默认为None。
        - weight: 损失函数的权重，可以是torch.Tensor、numpy数组或列表，默认为None。
        - num_workers: 数据加载时的线程数，默认为0。
        - num_eval_workers: 验证数据加载时的线程数，默认为0。
        - pin_memory: 是否使用锁页内存，默认为False。
        - pin_memory_device: 锁页内存的设备，默认为空字符串。
        - persistent_workers: 是否保持数据加载线程，默认为False。
        - early_stopping_rounds: 提前停止的轮数，默认为None。
        - print_per_rounds: 打印日志的间隔轮数，默认为1。
        - drop_last: 是否丢弃最后一个不完整的批次，默认为False。
        - checkpoint_per_rounds: 保存检查点的间隔轮数，默认为0。
        - checkpoint_name: 检查点文件名，默认为"model.pt"。
        - show_progress: 是否显示进度条，默认为True。
        - amp: 是否启用自动混合精度训练，默认为False。
        - eps: 数值稳定性的极小值，默认为1e-5。
        - monitor: 监控指标，如"accuracy"，默认为"accuracy"。
        - verbose: 是否输出详细信息，默认为True。
        - threshold: 分类阈值，默认为0.5。
        - target_names: 目标类别名称列表，默认为None。
        - num_classes: 类别数量，默认为None。

        返回值:
        - Tuple[dict, dict]: 包含训练和验证结果的两个字典。
        """
        assert 0.0 < val_size < 1.0
        X_train, X_test, y_train, y_test = train_test_split(
            texts, y, test_size=val_size, random_state=random_state
        )
        return super().train_evaluate(
            X_train, y_train, (X_test, y_test), max_length, epochs, optimizer, scheduler, lr, T_max,
            batch_size, eval_batch_size, sampler, weight, num_workers, num_eval_workers, pin_memory,
            pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds, 
            drop_last, checkpoint_per_rounds, checkpoint_name, show_progress, amp, eps, monitor,
            verbose, threshold, target_names, num_classes
        )
