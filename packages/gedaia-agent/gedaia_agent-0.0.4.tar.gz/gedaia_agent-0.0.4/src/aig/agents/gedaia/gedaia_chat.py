from pathlib import Path
import time
from typing import Annotated
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END ,START
from langchain_tavily import TavilySearch
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.prebuilt.chat_agent_executor import AgentState
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool

import gradio as gr
import uuid , os
import sqlite3
from gradio import ChatMessage
import json
from aig.domain.mcp_client import MCPClientManager



class CustomState(AgentState):
        runtime_context:dict[str,any]
        # messages: Annotated[list[BaseMessage], add_messages]
        # is_last_step: IsLastStep
        # remaining_steps: RemainingSteps

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


tool_tavily = TavilySearch(max_results=2)


class InterfaceChat :
    """
    """
    def __init__(self, llm:BaseChatModel,mcp_tools:list[BaseTool]=[], memory_saver:AsyncSqliteSaver=None) :
        """
        """
        self.llm = llm
        self.agent=None
        self.mcp_tools=mcp_tools
        if memory_saver == None :
            raise ValueError("memory_saver ne peut pas être nulle")
        self.memory_saver:AsyncSqliteSaver = memory_saver
        
        
    async def _init_agent(self):    
        """
        """
        try:     
            self.agent= create_react_agent(
            model=self.llm,
            tools=self.mcp_tools,
            prompt=prepare_model_inputs,
            checkpointer=self.memory_saver  
            )   
        except Exception as ex:
            raise ValueError(f"Exception dans _init_agent: {ex}")              


    async def chatbot(self,message, history, session_id):
        # Reconstituer l’historique
        messages = history + [{"role": "user", "content": message}]
        messages_tuples = [(m["role"], m["content"]) for m in messages]
        used_tool_names = set()
        last_agent_message = None
        try:
            runtime_context:dict[str,str]=dict()
            runtime_context["volumId"]="1-0-3-volum-290ce03a-e400-4ad3-b4fd-07057ec0df8a"
            runtime_context["documentId"]=""
            runtime_context["limit"]=50
            runtime_context["threshold"]=0.45  
            runtime_context["user_token"]="123456"
            runtime_context["documentId"]="0101010101"   
            runtime_context["user_id"] = "1"         
            config={
                "configurable": {
                    "thread_id": session_id,
                    "user_id":runtime_context["user_id"],
                    "runtime_context":json.dumps(runtime_context)
                }
            }     
            if self.agent ==None :
                   await self._init_agent()
            async for step in self.agent.astream(
                {"messages": messages_tuples},
                config=config,
                stream_mode="updates"
            ):
                yield ChatMessage(content="Je réfléchis...", metadata={"title": "Réflexion"})
                print("step =", step)

                # Outils appelés
                if "tools" in step and "messages" in step["tools"]:
                    for tool_msg in step["tools"]["messages"]:
                        if hasattr(tool_msg, "name"):
                            used_tool_names.add(tool_msg.name)

                if "agent" in step and "messages" in step["agent"]:
                    msg = step["agent"]["messages"][-1]
                    last_agent_message = msg.content or "Réponse vide."

                    if hasattr(msg, "tool_calls"):
                        for call in msg.tool_calls:
                            used_tool_names.add(call["name"])

                if used_tool_names:
                    tools_text = "\n".join(f"- `{tool}`" for tool in sorted(used_tool_names))
                    content = f"**Outils utilisés :**\n{tools_text}\n\n **Réponse :**\n{last_agent_message}"
                else:
                    content = last_agent_message or "L'agent n’a généré aucune réponse."

                yield ChatMessage(
                    content=content,
                    metadata={"title": "Réponse avec trace"}
                )            
        except Exception as e:
            yield ChatMessage(content=f"Erreur durant l'exécution de l'agent : {str(e)}")



def generate_session_id():
    session_id="Session-"+str(uuid.uuid4())
    return session_id

def session_selector(choice, session_select_dropdown):
    if choice == "Créer une nouvelle session":
        return generate_session_id()
    return session_select_dropdown

def get_all_sessions():
    conn = sqlite3.connect(db_path)      
    try:              
            cursor = conn.cursor()                
            cursor.execute("SELECT DISTINCT thread_id FROM checkpoints")
            sessions = [row[0] for row in cursor.fetchall()]
            conn.close()
            return sessions
    except Exception as e:
        print("Erreur SQLite :", e)
        return []
    finally : 
        if conn!=None : 
            conn.close()

def refresh_session_dropdown():
    return gr.update(choices=get_all_sessions())


def delete_session(session_id):
    if not session_id:
        return "Aucune session sélectionnée."
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM checkpoints WHERE thread_id = ?", (session_id,))
        conn.commit()
        conn.close()
        return f"Session `{session_id}` supprimée."
    except Exception as e:
        return f"Erreur lors de la suppression : {e}"
    finally : 
        if conn!=None : 
            conn.close()

db_path:Path=Path("db/gedaiaChat.db")
async def launch_gedaia_ui_async() :
    """
    """
    config_path: Path = Path("config.json")
    async with AsyncSqliteSaver.from_conn_string(str(db_path)) as saver :  
        mcp_manager = MCPClientManager(config_path)
        await mcp_manager.initialize()
        mcp_tools = mcp_manager.get_all_langchain_tools()

        # LLM + Agent
        llm = ChatOllama(
            model="mistral-small:24b-instruct-2501-q8_0",    #"mistral-small3.1:24b-instruct-2503-q8_0",
            base_url="http://localhost:21434",
            temperature=0
        )        
        interface:InterfaceChat=InterfaceChat(llm=llm,mcp_tools=mcp_tools, memory_saver=saver)
        await interface._init_agent()
        
        # Interface 
        with gr.Blocks() as gedaiaChat:
            with gr.Row():
                choice = gr.Radio(
                    ["Créer une nouvelle session", "Reprendre une session existante"],
                    value="Reprendre une session existante",
                    label="Choix de session"
                )
                session_select_dropdown = gr.Dropdown(
                    choices=get_all_sessions(),
                    label="Sessions existantes",
                    visible=True
                )
                refresh_button = gr.Button("Rafraîchir la liste des sessions")
                delete_button =gr.Button("Supprimer cette session")
                delete_status=gr.Textbox(label="Statut",interactive=False)

            refresh_button.click(fn=refresh_session_dropdown,inputs=[],outputs=session_select_dropdown)
            delete_button.click(fn=delete_session, inputs=session_select_dropdown, outputs=delete_status)
            delete_button.click(fn=refresh_session_dropdown, inputs=[], outputs=session_select_dropdown)


            session_id_box = gr.Textbox(
                label="Session ID",
                value=generate_session_id(),
                visible=False
            )

            choice.change(fn=session_selector, inputs=[choice, session_select_dropdown], outputs=session_id_box)
            session_select_dropdown.change(fn=session_selector, inputs=[choice, session_select_dropdown], outputs=session_id_box)

            gr.ChatInterface(
                fn=interface.chatbot,
                title="GeDAIA Agent",
                description="Agent GeDAIA pour l'office notarial",
                type="messages",
                additional_inputs=[session_id_box],
                save_history=True
            )
        gedaiaChat.launch(share=True)

