from typing import Dict, List, Literal, Optional, Union
from pydantic import validator, constr, BaseModel, validate_arguments
from docarray import BaseDoc, DocList
from wasabi import msg
from pathlib import Path
import json
import re
from .config import registry
from .log_utils_fastapi import get_logger

logger = get_logger()



class Token(BaseDoc):
    id: Optional[Union[int, str]] = None
    text: constr(strip_whitespace=True, min_length=1)
    space: Optional[bool] = False
    indices: Optional[List[int]] = None
    is_pad: Optional[bool] = False
    
    @validator('id')
    def validate_id(cls, v, values, **kwargs):
        return str(v)
    

class TokenList(DocList[Token]):
    
    raw_text: Optional[str] = None
    processed_text: Optional[str] = None
    
    def char_to_token(self, char_index: int):
        """字符索引转换为token索引
        """
        for idx, doc in enumerate(self):
            if doc.indices and char_index in doc.indices:
                return idx
        return None
    
    def token_to_char(self, token_index: int) -> Optional[List[int]]:
        """token索引转换为字符索引
        """
        if token_index >= len(self):
            return None
        return self[token_index].indices
    
    @property
    def pad_length(self):
        return sum([1 for token in self if token.is_pad])
    
    @property
    def pad_mask(self):
        mask = []
        for token in self:
            if token.is_pad:
                mask.append(0)
            else:
                mask.append(1)
        return mask
    
    @property
    def ids(self):
        return [int(token.id) for token in self]
    
    def check_indices_in_processed(self):
        for token in self:
            if token.indices:
                assert token.text == self.processed_text[token.indices[0]: token.indices[-1]+1], f"token {token.text} indices error"
        msg.good("token indices check pass")
        
    
    def check_indices_in_raw(self):
        for token in self:
            if token.indices:
                assert token.text == self.raw_text[token.indices[0]: token.indices[-1]+1], f"token {token.text} indices error"
        msg.good("token indices check pass")
    


class Tokenizer(BaseModel):
    
    max_length: int
    vocab: Union[str, Dict[str, int], Path]
    pad_side: Literal['left', 'right'] = "left"
    unk_token: str = "UNK"
    pad_id: int = 0
    
    
    @validator('vocab')
    def validate_vocab(cls, v, values, **kwargs):
        try:
            if isinstance(v, str) or isinstance(v, Path):
                with open(v, 'r', encoding='utf-8') as f:
                    v = json.load(f)
            if 'unk_token' in values:
                assert values['unk_token'] in v, f"unk_token {values['unk_token']} not in vocab"
        except:
            logger.error("模型初始化失败 - ner模型失败")
        return v
    
    @validator('unk_token')
    def validate_unk_token(cls, v, values, **kwargs):
        if 'vocab' in values:
            assert v in values['vocab'], f"unk_token {v} not in vocab"
        return v
    
    @property
    def token2id(self):
        return self.vocab
    
    @property
    def id2token(self):
        return {v: k for k, v in self.vocab.items()}
    
    @property
    def pad_token(self):
        return self.id2token[self.pad_id]
    
    @property
    def unk_token_id(self):
        return self.token2id[self.unk_token]
    
    def encode(self, tokens: TokenList) -> TokenList:
        for token in tokens:
            if token.text in self.vocab:
                token.id = self.vocab[token.text]
            else:
                token.id = self.unk_token_id
        return tokens
    
    def encode_batch(self, batch_tokens: List[TokenList]) -> List[TokenList]:
        return [self.encode(tokens) for tokens in batch_tokens]
    
    
    def decode(self, ids: List[int]) -> List[str]:
        return [self.id2token[int(id)] for id in ids]
    
    
    def pad(self, tokens: TokenList):
        pad_id = self.pad_id
        if self.pad_side == "left":
            pad_tokens = TokenList([Token(text=self.pad_token, id=pad_id, is_pad=True)] * (self.max_length - len(tokens)))
            pad_tokens.extend(tokens)
            pad_tokens.raw_text = tokens.raw_text
            pad_tokens.processed_text = tokens.processed_text
            tokens = pad_tokens
        else:
            tokens.extend([Token(text=self.pad_token, id=pad_id, is_pad=True)] * (self.max_length - len(tokens)))
        return tokens
    
        
    def pad_batch(self, batch_tokens: List[TokenList]):
        batch_tokens = [self.pad(tokens) for tokens in batch_tokens]
        return batch_tokens
        
    
    def save_vocab_json(self, save_path: str):
        """保存词表json文件

        Args:
            save_path (str): 保存路径
        """
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(self.vocab, f)
            
            
    def save_vocab_txt(self, save_path: str):
        """保存词表txt文件

        Args:
            save_path (str): 保存路径
        """
        with open(save_path, 'w', encoding='utf-8') as f:
            for k, v in self.vocab.items():
                f.write(f'{k} {v}\n')
                
    def to_disk(self, save_path: Union[str, Path]):
        """保存词表json文件

        Args:
            save_path (Union[str, Path]): 保存路径
        """
        json_str = self.json()
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(json_str)
    
    
    @classmethod     
    def from_disk(cls, load_path: Union[str, Path]):
        """从磁盘加载词表

        Args:
            load_path (Union[str, Path]): 加载路径
        """
        with open(load_path, 'r', encoding='utf-8') as f:
            json_str = f.read()
        return cls(**json.loads(json_str))
    
            
    
    def preprocess(self, text: str) -> TokenList:
        raise NotImplementedError
        
    
    def tokenize(self, tokens: TokenList) -> TokenList:
        raise NotImplementedError
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        return setattr(self, key, value)
    
   
    @validate_arguments
    def __call__(self, batch_text: Union[List[str], str], padding: bool = True) -> List[TokenList]:
        """对文本进行预处理,分词,编码,填充

        Args:
            batch_text (Union[List[str], str]): 输入文本
            padding (bool, optional): 是否填充. Defaults to True.

        Returns:
            List[TokenList]: 分词后的结果
        """
        if isinstance(batch_text, str):
            batch_text = [batch_text]
        batch_tokens: List[TokenList] = [self.preprocess(text) for text in batch_text]
        batch_tokens = [self.tokenize(tokens) for tokens in batch_tokens]
        batch_tokens = self.encode_batch(batch_tokens)
        if padding:
            batch_tokens = self.pad_batch(batch_tokens)
        return batch_tokens
        

class CharTokenizer(Tokenizer):
    """非常简单的基于字符的分词器,用于中文
    """
    remove_space: bool = False
    
    def preprocess(self, text: str) -> TokenList:
        tokens = TokenList()
        tokens.raw_text = text
        processed_text = text.strip()
        if self.remove_space:
            processed_text = processed_text.replace(' ', '')
        tokens.processed_text = processed_text
        return tokens
        
    def tokenize(self, tokens: TokenList) -> TokenList:
        """对文本进行字符切分

        Args:
            text (str): 输入文本

        """
        for i, char in enumerate(tokens.processed_text):
            if len(tokens) == self.max_length:
                break
            if not char.isspace():
                tokens.append(Token(text=char, indices=[i], space=False))
            else:
                tokens[-1].space = True
        return tokens


@registry.tokenizers.register('char')
def create_char_tokenizer(vocab: Union[Dict[str, int], str, Path], 
                          max_length: int, 
                          pad_side: Literal['left', 'right'] = "left", 
                          unk_token: str = "UNK", 
                          pad_id: int = 0, 
                          remove_space: bool = True):
    
    return CharTokenizer(vocab=vocab, 
                         max_length=max_length, 
                         pad_side=pad_side, 
                         unk_token=unk_token, 
                         pad_id=pad_id, 
                         remove_space=remove_space)
    

class WordTokenizer(Tokenizer):
    """基于空格的分词器,主要用于英文
    """
    
    do_lower: bool = True # 是否小写 My -> my
    split_number: bool = True # 是否切分数字 911 -> 9 1 1
    split_apostrophe: bool = True  # 是否切分撇号 don't -> don 't
    split_punctuation: bool = True # 是否切分标点符号 i am. -> i am .
    
    def preprocess(self, text: str) -> TokenList:
        tokens = TokenList()
        tokens.raw_text = text
        text = text.strip()
        # 将多个空格替换为一个空格
        text = re.sub(r'\s+', ' ', text)
        if self.do_lower:
            text = text.lower()
        tokens.processed_text = text
        return tokens
    
    def tokenize(self, tokens: TokenList) -> TokenList:
        spans = tokens.processed_text.split(' ')
        for i, span in enumerate(spans):
            if i == len(spans) - 1:
                space = False
            else:
                space = True
            if self.split_number:
                # 把数字单独拆分出来 911 -> 9 1 1
                # 切分数字
                _token = re.sub(r'(\d)', r' \1 ', span).split(' ')
                _token = [s for s in _token if s]
                # 如果切分后的长度大于1,说明有数字
                for s in _token[:-1]:
                    tokens.append(Token(text=s, space=False))
                    
                if _token[-1].isdigit():
                    tokens.append(Token(text=_token[-1], space=space))
                    
                else:
                    if self.split_apostrophe:
                        # 切分撇号 don't -> do n't
                        _token1 = re.sub(r"([a-zA-Z])'([a-zA-Z])", r"\1 '\2", _token[-1]).split(' ')
                        for s in _token1[:-1]:
                            if s:
                                tokens.append(Token(text=s, space=False))
                        tokens.append(Token(text=_token1[-1], space=space))
            else:
                if self.split_apostrophe:
                    _token = re.sub(r"([a-zA-Z])'([a-zA-Z])", r"\1 '\2", span).split(' ')
                    for s in _token[:-1]:
                        if s:
                            tokens.append(Token(text=s, space=False))
                    tokens.append(Token(text=_token[-1], space=space))
                else:
                    tokens.append(Token(text=span, space=space))
        if self.split_punctuation:
            # 切分标点符号
            new_tokens = TokenList()
            for token in tokens:
                _token = re.sub(r"([a-zA-Z])([,.!?])", r"\1 \2", token.text).split(' ')
                _token = [s for s in _token if s]
                for s in _token[:-1]:
                    new_tokens.append(Token(text=s, space=False))
                new_tokens.append(Token(text=_token[-1], space=token.space))
            new_tokens.raw_text = tokens.raw_text
            new_tokens.processed_text = tokens.processed_text
            tokens = new_tokens
        for i, token in enumerate(tokens):
            if i == 0:
                token.indices = list(range(len(token.text)))
            else:
                if tokens[i-1].space:
                    start = tokens[i-1].indices[-1] + 2
                    end = start + len(token.text)
                    token.indices = list(range(start, end))
                else:
                    start = tokens[i-1].indices[-1] + 1
                    end = start + len(token.text)
                    token.indices = list(range(start, end))
        final_tokens = tokens[:self.max_length]
        final_tokens.raw_text = tokens.raw_text
        final_tokens.processed_text = tokens.processed_text
        return final_tokens
    

@registry.tokenizers.register('word')
def create_word_tokenizer(vocab: Union[Dict[str, int], str, Path], 
                          max_length: int, 
                          pad_side: Literal['left', 'right'] = "left", 
                          unk_token: str = "UNK",
                          pad_id: int = 0,
                          do_lower: bool = True,
                          split_number: bool = True,
                          split_apostrophe: bool = True,
                          split_punctuation: bool = True):
    
    return WordTokenizer(vocab=vocab, 
                         max_length=max_length, 
                         pad_side=pad_side, 
                         unk_token=unk_token, 
                         pad_id=pad_id, 
                         do_lower=do_lower, 
                         split_number=split_number, 
                         split_apostrophe=split_apostrophe, 
                         split_punctuation=split_punctuation)
                          