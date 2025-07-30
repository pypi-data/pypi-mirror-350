import psutil
from typing import Callable, List, Tuple, Optional, Union
from wasabi import msg
import time
from .tokenizer import TokenList
from pathlib import Path
from typing import Literal, Optional
from .config import Config
from contextlib import contextmanager


def get_cpu_memory(tag: str):
    """获取函数运行时的cpu内存

    Args:
        tag (str): 标签
    """
    def out_wrapper(fn: Callable):
        def wrapper(*args, **kwargs):
            p = psutil.Process()
            cpu_memory = p.memory_info().rss
            outputs = fn(*args, **kwargs)
            cpu_memory = p.memory_info().rss - cpu_memory
            msg.good(f"{tag} cpu memory: {cpu_memory / 1024 / 1024}MB")
            return outputs
        return wrapper
    return out_wrapper

def get_spent_time(tag: str):
    """获取函数运行时的时间

    Args:
        tag (str): 标签
    """
    def out_wrapper(fn: Callable):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            outputs = fn(*args, **kwargs)
            end_time = time.time()
            spent_time = round(end_time - start_time, 4)
            msg.info(f"{tag} spent time: {spent_time}s")
            return outputs
        return wrapper
    return out_wrapper

@contextmanager
def print_spent_time(tag: str):
    start_time = time.time()
    yield
    end_time = time.time()
    spent_time = round(end_time - start_time, 4)
    msg.info(f"{tag} spent time: {spent_time}s")



def get_ents(tags: List[str]) -> List[Tuple[int, int, str]]:
    """从序列标签中提取实体

    Args:
        tags (List[str]): 序列标签.

    Returns:
        List[Tuple[int, int, str]]: 实体列表.例如, [(2, 6, 'PER')]
    """
    entities = []
    entity = []
    for i, tag in enumerate(tags):
        if tag.startswith('B-'):
            if entity:
                entities.append(tuple(entity))
            entity = [i, i + 1, tag.split('-')[1]]
        elif tag.startswith('I-'):
            if entity:
                if entity[2] == tag.split('-')[1]:
                    entity[1] = i + 1
        else:
            if entity:
                entities.append(tuple(entity))
            entity = []
    if len(entity) == 3:
        entities.append(tuple(entity))
    return entities
def ner_post_process(labels: List[str], tokens: Optional[TokenList] = None) -> List[Tuple[int, int, str, str]]:
    """对ner模型预测的token标签进行后处理，得到最终的实体

    Args:
        labels (List[str]): 模型预测的序列标签.
        text (str): 原始文本.

    Returns:
        List[Tuple[int, int, str, str]]: 实体列表.例如, [(2, 6, '明天上午', 'DateChanged')]
    """
    if tokens:
        assert len(labels) == len(tokens)
    ents = get_ents(labels)
    if not tokens:
        return ents
    results = []
    for ent in ents:
        start, end, label = ent
        start_char = tokens.token_to_char(start)
        if start_char:
            start_char = start_char[0]
        end_char = tokens.token_to_char(end - 1)
        if end_char:
            end_char = end_char[-1] + 1
        if start_char is not None and end_char is not None:
            results.append((start_char, end_char, tokens.processed_text[start_char:end_char], label))
    return results


def get_nlu_config(domain: str, 
                   lang: Literal["cmn", "zho", "eng"], 
                   tokenzer_type: Literal["char", "word"],
                   max_length: int,
                   pad_side: Literal["left", "right"],
                   pad_id: int = 0,
                   unk_token: str = "UNK",
                   ) -> str:
    
    config_str = """
    [nlu]
    @languages = cmn
    domain = "schedule"

    [nlu.domain_inference]
    @inferences = "domain.fasttext"
    model_path = ${path.domain}

    [nlu.intention_inference]
    @inferences = "intention.fasttext"
    model_path = ${path.intention}

    [nlu.ner_inference]
    @inferences = "ner.onnx.cloud"
    model_path = ${path.ner}
    label_path = ${path.label}

    [nlu.tokenizer]
    @tokenizers = "char"
    max_length = 32
    vocab = ${path.vocab}
    pad_side = "left"
    pad_id = 0
    unk_token = "UNK"

    [path]
    ner = "model/ner/model.onnx"
    vocab = "model/ner/word2id.json"
    label = "model/ner/id2label.json"
    domain = "model/domain/model.bin"
    intention = "model/intention/model.bin"
    """
    overrides = {"nlu.domain": domain, "nlu.@languages": lang, "nlu.tokenizer.@tokenizers": tokenzer_type, "nlu.tokenizer.max_length": max_length, "nlu.tokenizer.pad_side": pad_side, "nlu.tokenizer.pad_id": pad_id, "nlu.tokenizer.unk_token": unk_token}
    config = Config().from_str(config_str, overrides=overrides, interpolate=False)
    return config
    