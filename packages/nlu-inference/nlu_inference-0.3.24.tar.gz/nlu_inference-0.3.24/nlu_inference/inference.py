from typing import List
from onnxruntime import InferenceSession, SessionOptions
from fasttext import load_model
from pathlib import Path
from .utils import ner_post_process
import json
import numpy as np
from .tokenizer import TokenList
from pydantic import validate_arguments
from .config import registry
from .io import CLSResult, NERResult
from .log_utils_fastapi import RequestContextMiddleware,setup_logging,get_logger
logger = get_logger()

class CLSInference():
    
    @validate_arguments
    def __call__(self, tokens: TokenList) -> CLSResult:
        tokens = self._preprocess(tokens)
        results = self._predict(tokens)
        results = self._postprocess(results)
        return results
    
    def _predict(self, tokens: TokenList) -> CLSResult:
        raise NotImplementedError
    
    def _preprocess(self, tokens: TokenList) -> TokenList:
        return tokens
    
    def _postprocess(self, result: CLSResult) -> CLSResult:
        return result



@registry.inferences.register("domain.fasttext")
class FasttextInference(CLSInference):
    def __init__(self, model_path: str):
        super().__init__()
        if isinstance(model_path, str):
            self.model = load_model(model_path)
        if isinstance(model_path, Path):
            self.model = load_model(str(model_path))
    
    def _predict(self, tokens: TokenList) -> CLSResult:
        """fasttext 模型推理

        Args:
            query (str): 原始问题文本
        """
        texts = [token.text for token in tokens if not token.is_pad]  #确保不会受到pad的影响
        query = ' '.join(texts)
        result = self.model.predict(query)
        label = result[0][0]
        score = result[1][0]
        return CLSResult(label=label, score=round(score, 4))
    
    def _postprocess(self, result: CLSResult) -> CLSResult:
        result: CLSResult = CLSResult(label=result.label.replace("__label__", "").replace("#", ""), score=result.score)
        if result.label == "0":
            result.score = 0.0
        return result
    
@registry.inferences.register("intention.fasttext")
class FasttextInference(CLSInference):
    def __init__(self, model_path: str):
        super().__init__()
        if isinstance(model_path, str):
            try:
                self.model = load_model(model_path)
            except:
                logger.error("模型初始化失败 - intention模型失败")
        if isinstance(model_path, Path):
            try:
                self.model = load_model(str(model_path))
            except:
                logger.error("模型初始化失败 - intention模型失败")
    def _predict(self, tokens: TokenList) -> CLSResult:
        """fasttext 模型推理

        Args:
            query (str): 原始问题文本
        """
        try:
            texts = [token.text for token in tokens if not token.is_pad] # 确保不会受到pad的影响
            query = ' '.join(texts)
            result = self.model.predict(query)
            label = result[0][0]
            score = result[1][0]
        except:
            logger.error("模型推理失败 - intention模型失败")
        return CLSResult(label=label, score=round(score, 4))
    
    def _postprocess(self, result: CLSResult) -> CLSResult:
        result = CLSResult(label=result.label.replace("__label__", "").replace("#", ""), score=result.score)
        return result

    
class NERInference():
    
    @validate_arguments
    def __call__(self, tokens: TokenList) -> NERResult:
        return self._predict(tokens)
    
    def _predict(self, tokens: TokenList) -> NERResult:
        raise NotImplementedError
    


@registry.inferences.register("ner.onnx.local")
class NERInferenceLocal(NERInference):
    """ner模型推理, 返回格式如下 (2, 6, '明天上午', 'DateChanged')
    """
    def __init__(self, 
                 embedding_path: str,
                 model_path: str,
                 label_path: str):
        super().__init__()
        so = SessionOptions()
        so.log_severity_level = 3
        if isinstance(model_path, str):
            self.classifier_model = InferenceSession(model_path, so)
        if isinstance(embedding_path, Path):
            self.classifier_model = InferenceSession(str(model_path), so)
        
        with open(label_path, 'r') as f:
            self.id2label = json.load(f)
            
        self.embedding_model = InferenceSession(embedding_path, so)
    
    
    def _predict(self, tokens: TokenList) -> NERResult:
        """ner 模型推理

        Args:
            query (str): 原始问题文本
        """
        embeddings = self.get_embeddings(ids=tokens.ids)
        labels = self.get_labels(embeddings)
        
        # 后处理
        ents = ner_post_process(labels, tokens=tokens)
        slots = {}
        for ent in ents:
            slots[ent[3]] = ent[2]
        return slots
    
    
    def get_embeddings(self, ids: List[int]) -> np.ndarray:
        """获取embedding

        Args:
            query (str): 原始问题文本
        """
        input_ids = np.array(ids, dtype=np.int64).reshape(1, -1)
        # 获取embedding
        embeddings = self.embedding_model.run(None, {'input': input_ids})[0]
        embeddings = np.array(embeddings, dtype=np.float32)
        return embeddings
    
    
    def get_labels(self, embeddings: np.ndarray) -> List[str]:
        """获取标签

        Args:
            embeddings (np.ndarray): embedding
        """
        label_ids = self.classifier_model.run(None, {'input': embeddings})[0][0]
        # 兼容tf版本转换的onnx模型
        if len(label_ids.shape) == 2:
            label_ids = np.argmax(label_ids, axis=-1)
            
        labels = [self.id2label[str(i)] for i in label_ids]
        return labels
    
    

@registry.inferences.register("ner.onnx.cloud")
class NERInferenceCloud(NERInference):
    """ner模型推理, 返回格式如下 (2, 6, '明天上午', 'DateChanged')
    """
    def __init__(self, 
                 model_path: str,
                 label_path: str):
        super().__init__()
        
        so = SessionOptions()
        so.log_severity_level = 3
        try:
            self.model = InferenceSession(str(model_path), so)
       
            with open(label_path, 'r') as f:
                self.id2label = json.load(f)
        except:
            logger.error("模型初始化失败 - ner模型失败")
    def _predict(self, tokens: TokenList) -> NERResult:
        """ner 模型推理

        Args:
            query (str): 原始问题文本
        """
        try:
            label_ids = self.model.run(None, {'input': np.array([tokens.ids], dtype=np.int64)})[0][0]
            # 兼容tf版本转换的onnx模型
            if len(label_ids.shape) == 2:
                label_ids = np.argmax(label_ids, axis=-1)
                
            labels = [self.id2label[str(i)] for i in label_ids]
            
            # 后处理
            ents = ner_post_process(labels, tokens=tokens)
            
            slots = {}
            for ent in ents:
                slots[ent[3]] = ent[2]
        except:
            logger.error("模型推理失败 - ner模型失败")
        return slots
    
    
    