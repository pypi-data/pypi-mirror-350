from confection import Config
import confection
import catalogue


class registry(confection.registry):
    
    tokenizers = catalogue.create("nlu", "tokenizers", entry_points=True)
    inferences = catalogue.create("nlu", "inferences", entry_points=True)
    languages = catalogue.create("nlu", "languages", entry_points=True)
    
    

__all__ = ["registry", "Config"]