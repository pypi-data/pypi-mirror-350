import asyncio
import os
from threading import Thread
import time
# System call
os.system("")
# Class of different styles
class print_color():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

import json
from typing import Annotated, TypedDict
from mcp import ClientSession, GetPromptResult
from mcp.client.sse import sse_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_ollama import ChatOllama
from mcp.types import Prompt, PromptArgument, PromptMessage, TextContent

from langgraph.prebuilt import create_react_agent

from langgraph.graph.graph import CompiledGraph
from langchain.prompts import PromptTemplate
from langchain_core.tools import BaseTool
from aig import LLM_MODEL, load_model
from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph.message import add_messages
from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    BaseMessage,
    SystemMessage,
    ToolMessage,
)
from langgraph.managed import IsLastStep, RemainingSteps
from langgraph.prebuilt import InjectedStore
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import MemorySaver, InMemorySaver

class CustomState(AgentState):
        runtime_context:dict[str,any]
        # messages: Annotated[list[BaseMessage], add_messages]
        # is_last_step: IsLastStep
        # remaining_steps: RemainingSteps

def save_memory(memory: str, *, config: RunnableConfig, store: Annotated[BaseStore, InjectedStore()]) -> str:
     """Save the given memory for the current user.
        Args:
            memory: les données à sauvegarder. Type: chaine de caractères            
            config : données interne sous forme de key value pair. Argument nommé.
            store : objet permettant la gestion du stockage. Argument nommé.
        Output :
            La nouvelle valeur de la mémoire de l'utilisateur user_id. Type: Chaine de caractères            
     """
     # This is a **tool** the model can use to save memories to storage
     user_id = config.get("configurable", {}).get("user_id")
     namespace = ("memories", user_id)
     store.put(namespace, f"memory_{len(store.search(namespace))}", {"data": memory})
     return f"Saved memory: {memory}"

def prepare_model_inputs(state: CustomState, config: RunnableConfig, store: BaseStore):
     # Retrieve user memories and add them to the system message
     # This function is called **every time** the model is prompted. It converts the state to a prompt
     user_id = config.get("configurable", {}).get("user_id")
     # récupération du runtime context
     runtime_context = config.get("configurable",{}).get("runtime_context",{}) 
    #  namespace = ("memories", user_id)
    #  memories = [m.value.get("data","") for m in store.search(namespace)]
     system_msg = f"""
Tu es un assistant notaire en charge de tous les dossiers, actes, minutes, brevets et documents du répertoire officiel de l'office. Répond en Français.
Voici ton runtime_context={runtime_context}.
"""
    # User memories(it may be empty): {', '.join(memories)}. 
     return [         
         {"role": "system", "content": system_msg}
         ] + state["messages"]

def graph_gedaia(LLM:str=LLM_MODEL.OLLAMA,
                       MODEL:str="mistral-small3.1:24b-instruct-2503-q8_0",
                       LLM_API_KEY:str="",
                       URL:str="http://localhost:21434",
                       TEMP:float=0.5,
                       tools:list[BaseTool]=[],
                       runtime_context:dict[str,any]=dict()) -> tuple[int, str,CompiledGraph|None] :
    """
    Retourne le Graph pour GeDAIA
    
    """
    model= load_model(llm=LLM,name=MODEL,base_url=URL,api_key=LLM_API_KEY, temperature=TEMP)
    if model==None : 
        return -1, "Pas de LLM valide" ,None             
    try :
#         prompt = f"""
# Tu es un assistant notaire en charge de tous les dossiers, actes, minutes, brevets et documents du répertoire officiel de l'office. 
# Répond en français aux demandes.
# Voici ton runtime_context={runtime_context}\n
#     """
        memory = MemorySaver() 
        store = InMemoryStore()
        namespace = ("memories", runtime_context.get("user_id","1"))
        # initalise le store
        
        store.put(namespace, f"memory_{len(store.search(namespace))}", {"data": memory})
        # tools.append(save_memory)
        agent= create_react_agent(model, 
                                    tools=tools, 
                                    name="GeDAIA Répertoire",
                                    checkpointer=memory,
                                    state_schema=CustomState,
                                    #prompt=prompt,
                                    prompt=prepare_model_inputs,
                                    store=store,
                                    config_schema=Annotated[dict[str,any],"Context pour l'éxecution des outils"],
                                    )
        
    except Exception as ex:
        msg_error =f"Création de l'Agent GeDAIA a échouée. \n{ex}"
        return -1 , msg_error, None
    return 0,"", agent

async def graph() :
    """
    """
    LLM:str=LLM_MODEL.OLLAMA
    MODEL:str="mistral-small:24b-instruct-2501-q8_0"
    LLM_API_KEY:str=""
    URL:str="http://localhost:21434"
    TEMP:float=0.5
    runtime_context:dict[str,str]=dict()
    runtime_context["volumId"]="1-0-3-volum-290ce03a-e400-4ad3-b4fd-07057ec0df8a"
    # runtime_context["documentId"]=""
    # runtime_context["limit"]=50
    runtime_context["threshold"]=0.45   
    # error, err_msg, agent =  graph_gedaia(LLM,MODEL,LLM_API_KEY,URL,TEMP,[], runtime_context)    
    # return agent   
    # Initialize the connection
    # Get tools
    MCPSSE:str="http://localhost:8005/sse"
    #async with sse_client(url=MCPSSE) as (read, write):
    async with sse_client(url=MCPSSE) as (read, write):
        async with ClientSession(read, write) as session: 
            await session.initialize()    
            mcp_tools = await load_mcp_tools(session)    
            error, err_msg, agent =  graph_gedaia(LLM,MODEL,LLM_API_KEY,URL,TEMP,mcp_tools, runtime_context)
            return agent
  
async def agent_gedaia(LLM:str=LLM_MODEL.OLLAMA,
                       MODEL:str="mistral-small:24b-instruct-2501-q8_0", #"mistral-small3.1:24b-instruct-2503-q8_0",#,
                       LLM_API_KEY:str="",
                       URL:str="http://localhost:21434",
                       MCPSSE:str="http://localhost:8005/sse",
                       TEMP:float=0.5)->tuple[int,str] :
    """
    Agent GeDAIA 
    """     
    async with sse_client(url=MCPSSE) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            # Get tools
            mcp_tools =  await load_mcp_tools(session)
            # Get prompts 
            mcp_prompts=  await session.list_prompts()    
            runtime_context:dict[str,str]=dict()
            runtime_context["volumId"]="1-0-3-volum-290ce03a-e400-4ad3-b4fd-07057ec0df8a"
            runtime_context["documentId"]=""
            runtime_context["limit"]=50
            runtime_context["threshold"]=0.45  
            runtime_context["user_token"]="123456"
            runtime_context["documentId"]="0101010101"   
            runtime_context["user_id"] = "1"   
            try:
                config={
                    "configurable": {
                        "thread_id": "thread-1",
                        "user_id":runtime_context["user_id"],
                        "runtime_context":json.dumps(runtime_context)
                    }
                }                
                error, error_msg,agent = graph_gedaia(LLM,MODEL,LLM_API_KEY,URL,TEMP,mcp_tools, runtime_context)
                if error !=0 :
                    print(print_color+error_msg)
                    return error,error_msg
            except Exception as ex:
                print(f"Exception: \n{ex}")
                return -1, ex 
            while True:
                try:
                    question = input(print_color.MAGENTA+"\tQuestion:").encode("utf-8")
                    if question.decode('utf-8').lower()=="exit" : return 0 ,"Terminé"

                    print(print_color.CYAN+f"Analyse de la demande ...")
#                     prompt = f"""
# Tu es un assistant notaire en charge de tous les dossiers, actes, minutes, brevets et documents du répertoire officiel de l'office. 
# Répond en français aux demandes.
# Voici ton runtime_context={json.dumps(runtime_context)}\n
#     """
                    runtime_context_serialized:str = json.dumps(runtime_context)
                    inputs={"messages":[
                        ("user",question)
                        ], "runtime_context":runtime_context_serialized}
                    last_content=""
                    async for stream_mode, chunk in agent.astream(
                        input=inputs,
                        config=config,debug=False,
                        stream_mode=["messages","values"]):   
                        if stream_mode=="values" :  
                            last_message = chunk["messages"][-1]
                            name = last_message.name
                            last_message_metadata=""
                            if last_message.type=='ai' :
                                last_message_metadata = f"Model:{last_message.response_metadata['model']}\tjetons fournis:{last_message.usage_metadata['input_tokens']}\tJetons retournés:{last_message.usage_metadata['output_tokens']}\tTotal jetons: {last_message.usage_metadata['total_tokens']}"
                            if hasattr(last_message, "tool_calls"):
                                for msg_tool_call in last_message.tool_calls:
                                    tool_name: str = msg_tool_call['name']                                                                                   
                                    print(print_color.BLUE+f"{name}({last_message.type}):\t{tool_name}({msg_tool_call['args']})\n{last_message_metadata}")                
                        elif stream_mode=="messages" :
                            msg, metadata = chunk
                            content:str=""
                            if msg.content=="" :
                                content =f"\nJe réfléchis ...\nMetadata={metadata}\n"
                                last_content+="\n"
                                print(print_color.CYAN+content)
                            else :
                                if len(msg.content)>0 :
                                    content = msg.content
                                    last_content=content
                                print(print_color.MAGENTA+f"{content}",end="")
                    save_memory(last_content,config=config,store=agent.store)       
                    print(print_color.CYAN+"\n"+"§"*80+"\n")
                except Exception as ex : 
                    print(print_color.RED+f"Exception :\n{ex}")
                
