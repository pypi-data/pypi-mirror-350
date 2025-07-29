# math_server.py
import logging
from mcp import GetPromptResult, Resource
from mcp.types import Prompt, PromptArgument, PromptMessage, TextContent
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import Settings
import asyncio 

settings:Settings=Settings(log_level="DEBUG")
mcp = FastMCP("Demo",settings=settings)

@mcp.tool()
def Ajouter(a: float, b: float,context:dict) -> float:
    """
    Add two numbers
    """
    logging.info(f"Contexte: {context}")
    return a + b

@mcp.tool()
def Multiplier(a: float, b: float, context:dict) -> float:
    "Multiply two number"
    logging.info(f"Contexte: {context}")
    return a * b

@mcp.tool()
def diviser(a: float, b: float,context:dict) -> float:
    """
    Divide two number
    """
    logging.info(f"Contexte: {context}")
    if b!=0 :
        return a / b
    else :return None

# Analyse tools 
@mcp.tool()
def Extract_data(texte:str,context:dict)->str:
    """
    Extract data from a text
    """
    
    if texte==None or texte.strip()=="":
        return "Désolé mais je n'ai trouvé aucun texte à analyser"
    volumId:str|None=context.get("volumId",None)
    documentId:str|None=context.get("documentId",None)
    analyse=f"Le VolumId={volumId}\nLe documentId={documentId}\nTerminé les grandes chaleurs en période de canicule. Espace Aubade vous propose une gamme de climatiseurs monobloc à la pointe des systèmes de climatisation actuels.  Alliant économies d’énergie et performance frigorifique, ce type de climatiseur refroidit rapidement l’air ambiant sans augmenter votre facture d’électricité."
    return analyse


@mcp.resource("files://{file_id}/object_ref")
def get_file_profile(file_id: str) -> str:
    """Dynamic file data"""
    return f"gedaia/mcp/{file_id}/file"


@mcp._mcp_server.list_resources()
async def handle_list_resources()-> list[Resource] :
    return [
        Resource(
            uri="files://{file_id}/object_ref",
            name="Fichier dans le stockage interne",
            description="Récupérer le lien du file_id dans le stockage interne"
        )
    ]

  
PROMPT_CALCULATOR="Test-prompt"  
DESCRIPTION_DEMO_PROMPT="prompt Démo"

@mcp._mcp_server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict | None
) -> GetPromptResult:
    if name != PROMPT_CALCULATOR:
        raise ValueError(f"Unknown prompt: {name}")
    try :
        return GetPromptResult(
            description=DESCRIPTION_DEMO_PROMPT,
            messages=[
                PromptMessage(
                    role="user",
                    arguments=arguments,
                    content=TextContent(type="text", 
        text=f"""
        Tu es un agent intelligent capable de répondre la question comprise entre <<< >>> et en utilisant le context, les données de la questions et en priorité les outils mis à ta disposition.
        ####
        voici ton context pour exécuter les outils:
        context={arguments.get("current_context",{"volumId":"-1", "documentId":"-1"})} 
        ####
        <<<question: {arguments.get("question","")}>>> 
        """
                    ),
                )
            ],
        )
    except Exception as ex:
        logging.critical(f"Exception :\n{ex}",stack_info=True)
    
@mcp._mcp_server.list_prompts()
async def handle_list_prompts() ->list[Prompt] :
    return [
        Prompt(
            name=PROMPT_CALCULATOR,
            description=DESCRIPTION_DEMO_PROMPT,
            arguments=[
                PromptArgument(
                    name="question", description ="expression de la question"
                ),
                PromptArgument(
                    name="current_context",description="Contexte utile pour répondre à la question "
                )
            ]
        )
        
    ]



        



def start_demo_server(port:int=8000) :
    """
    Démarre le serveur démo 
    """
    mcp.settings.port=port
    asyncio.run(mcp.run(transport="sse"))    

if __name__ == "__main__":
    start_demo_server(port=8005)