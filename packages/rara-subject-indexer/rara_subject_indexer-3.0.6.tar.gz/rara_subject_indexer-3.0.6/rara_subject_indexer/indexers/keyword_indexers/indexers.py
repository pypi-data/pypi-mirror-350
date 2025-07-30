from rara_subject_indexer.indexers.model_indexers.omikuji_indexer import OmikujiIndexer
from rara_subject_indexer.indexers.keyword_indexers.base_keyword_indexer import BaseKeywordIndexer
from rara_subject_indexer.config import (
    TOPIC_KEYWORD_CONFIG, GENRE_KEYWORD_CONFIG, TIME_KEYWORD_CONFIG,
    CATEGORY_CONFIG,UDC_CONFIG, UDC2_CONFIG, NER_CONFIG, ALLOWED_METHODS_MAP,
    ModelArch, Language, EntityType, KeywordType, DEFAULT_RAW_KEYWORDS
)
from rara_subject_indexer.exceptions import InvalidMethodException
from typing import NoReturn
import langdetect
import os


class TopicIndexer(BaseKeywordIndexer):
    def __init__(self, 
        model_arch: str = ModelArch.OMIKUJI, 
        config: dict = TOPIC_KEYWORD_CONFIG,
        top_k: int = DEFAULT_RAW_KEYWORDS
    ) -> NoReturn:
        super().__init__(model_arch=model_arch, config=config, top_k=top_k)
        
    @property
    def keyword_type(self) -> str:
        KeywordType.TOPIC.value

        
        
class GenreIndexer(BaseKeywordIndexer):
    def __init__(self, 
        model_arch: str = ModelArch.OMIKUJI, 
        config: dict = GENRE_KEYWORD_CONFIG,
        top_k: int = DEFAULT_RAW_KEYWORDS
    ) -> NoReturn:
        super().__init__(model_arch=model_arch, config=config, top_k=top_k)
        
    @property
    def keyword_type(self) -> str:
        KeywordType.GENRE.value
    
    
class TimeIndexer(BaseKeywordIndexer):
    def __init__(self, 
        model_arch: str = ModelArch.OMIKUJI, 
        config: dict = TIME_KEYWORD_CONFIG,
        top_k: int = DEFAULT_RAW_KEYWORDS
    ) -> NoReturn:
        super().__init__(model_arch=model_arch, config=config, top_k=top_k)
        
    @property
    def keyword_type(self) -> str:
        KeywordType.TIME.value
        
class UDCIndexer(BaseKeywordIndexer):
    def __init__(self, 
        model_arch: str = ModelArch.OMIKUJI, 
        config: dict = UDC_CONFIG,
        top_k: int = DEFAULT_RAW_KEYWORDS
    ) -> NoReturn:
        super().__init__(model_arch=model_arch, config=config, top_k=top_k)

    @property
    def keyword_type(self) -> str:
        KeywordType.UDK.value
        
class UDC2Indexer(BaseKeywordIndexer):
    def __init__(self, 
        model_arch: str = ModelArch.OMIKUJI, 
        config: dict = UDC2_CONFIG,
        top_k: int = DEFAULT_RAW_KEYWORDS
    ) -> NoReturn:
        super().__init__(model_arch=model_arch, config=config, top_k=top_k)
        
    @property
    def keyword_type(self) -> str:
        KeywordType.UDK2.value
        
class CategoryIndexer(BaseKeywordIndexer):
    def __init__(self, 
        model_arch: str = ModelArch.OMIKUJI, 
        config: dict = CATEGORY_CONFIG,
        top_k: int = DEFAULT_RAW_KEYWORDS
    ) -> NoReturn:
        super().__init__(model_arch=model_arch, config=config, top_k=top_k)
              
    @property
    def keyword_type(self) -> str:
        KeywordType.CATEGORY.value
        
class NERKeywordIndexer(BaseKeywordIndexer):
    def __init__(self, 
        model_arch: str = ModelArch.NER, 
        config: dict = NER_CONFIG,
        top_k: int = DEFAULT_RAW_KEYWORDS
    ) -> NoReturn:
        super().__init__(model_arch=model_arch, config=config, top_k=top_k)
        
    @property
    def keyword_type(self) -> str:
        KeywordType.NER.value
        
