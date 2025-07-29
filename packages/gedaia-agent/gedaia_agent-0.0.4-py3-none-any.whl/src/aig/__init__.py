from enum import Enum 
import logging
import os
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models.chat_models import BaseChatModel

class LLM_MODEL(Enum):
    OLLAMA="ollama"
    OPENAI="openai"
    ANTRHOPIC="anthropic"
    MISTRAL="mistral"
    

def load_model(llm:str=LLM_MODEL.OLLAMA.value,
               api_key:str="",
               name="mistral-small:24b-instruct-2501-q8_0", 
               base_url="http://localhost:21434", 
               temperature:float=0.5,**kwargs) ->BaseChatModel :
    """
    Créé et retourn un modèle ChatOllaman
    """
    try :
        model:BaseChatModel = None
        if llm==LLM_MODEL.OLLAMA.value:
            model = ChatOllama( model=name,
                    base_url=base_url,
                    temperature=temperature,
                    **kwargs)
            
        elif llm==LLM_MODEL.OPENAI.value :  
            model = ChatOpenAI(model=name,
                               temperature=temperature,
                               api_key=api_key,**kwargs)       
            
        elif llm==LLM_MODEL.ANTRHOPIC.value:
            model = ChatAnthropic(model=name,
                                  temperature=temperature, 
                                  api_key=api_key,**kwargs)
        elif llm==LLM_MODEL.MISTRAL :
            pass
        return model
    except Exception as ex :
        logging.critical(f"Exception pendant le chargement du modèle {name} avec l'exeception : \n{ex}")
        return None 