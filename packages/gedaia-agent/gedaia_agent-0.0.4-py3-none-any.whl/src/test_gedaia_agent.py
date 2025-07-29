

import argparse
import asyncio
import os
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

from aig import LLM_MODEL
from aig.agents.gedaia import agent_gedaia

if __name__=='__main__': 
    print(print_color.MAGENTA  +"   =========================================================================\n")
    # print(print_color.RED    +"   *************************************************************************\n")
    # print(print_color.MAGENTA+"   *************************************************************************\n")
    # print(print_color.CYAN   +"   *************************************************************************\n")
    print(print_color.CYAN     +"   =========================================================================\n")
    print(print_color.BLUE     +"    GGGGGGGG              DDDDDDDDD      AAAAA      IIIIIIII       AAAAA    \n")
    print(print_color.BLUE     +"    GG           eeeee    DD       D   A       A       II        A       A  \n")
    print(print_color.BLUE     +"    GG          e     e   DD       D   A       A       II        A       A  \n")
    print(print_color.BLUE     +"    GG   GGG    eeeeeee   DD       D   AAAAAAAAA       II        AAAAAAAAA  \n")
    print(print_color.BLUE     +"    GG     G    e         DD       D   A       A       II        A       A  \n")
    print(print_color.BLUE     +"    GGGGGGGG     eeeeee   DDDDDDDDD    A       A    IIIIIIIII    A       A  \n")
    print(print_color.CYAN     +"   =========================================================================\n")
    # print(print_color.CYAN   +"   *************************************************************************\n")    
    # print(print_color.MAGENTA+"   *************************************************************************\n")
    # print(print_color.RED    +"   *************************************************************************\n")
    print(print_color.MAGENTA  +"   =========================================================================\n")
    # Appel en tant que module principal
    parser = argparse.ArgumentParser(description="Exemple d'usage")
    parser.add_argument("--LLM","-l",nargs=1,required=False,type=str,help="Editeur LLM exemple: --LLM OPENAI ou --LLM ANTROPIC ou --LLM OLLAMA")
    parser.add_argument("--URL","-u",nargs=1,required=False,type=str,help="Url du LLM OLLAMA, exemple: --URL https://models-ai.lexfluent.com")
    parser.add_argument("--MODEL","-m",nargs=1,required=False,type=str,help="Modèle LLM, exemple: --MODEL mistral-small:24b-instruct-2501-q8_0")
    parser.add_argument("--APIKEY","-k", nargs=1,required=False, type=str,help="API KEY pour le LLM, exemple : --APIKEY XDFSGFYRFZFERZERY")
    parser.add_argument("--MCPSSE","-s",nargs=1,required=False,type=str,help="Url du serveur MCP-SSE: --MCPSSE http://localhost:8005/sse")
    parser.add_argument("--TEMP","-t",nargs=1,required=False,type=float,help="Température du LLM, exemple: --Temp 0.8")
    args = parser.parse_args()
    llm=LLM_MODEL.OLLAMA.value
    url="http://localhost:21434"
    api_key=""
    temperature=0.8
    mcp_sse="http://localhost:8005/sse"
    model="mistral-small3.1:24b-instruct-2503-q8_0" #"mistral-small:24b-instruct-2501-q8_0"
    try :
        if args.LLM !=None:
            if args.LLM[0].lower()==LLM_MODEL.OLLAMA.value : 
                llm=LLM_MODEL.OLLAMA.value
            elif args.LLM[0].lower()==LLM_MODEL.OPENAI.value : 
                llm=LLM_MODEL.OPENAI.value
            elif args.LLM[0].lower()==LLM_MODEL.ANTRHOPIC.value : 
                llm=LLM_MODEL.ANTRHOPIC.value
            else :
                raise ValueError("LLM inconnu !")
        if args.URL!=None : 
            url=args.URL[0]  
        if args.APIKEY!=None :
            api_key=args.APIKEY[0]
        if args.MODEL !=None:
            model = args.MODEL[0]
        if args.MCPSSE !=None :
            mcp_sse = args.MCPSSE[0]
        if args.TEMP!=None : 
            temperature = args.TEMP[0]
    except Exception as ex: 
        print(print_color.RED+f"Exception:\n{ex}\n")
        parser.print_help()

    asyncio.run(agent_gedaia(LLM=llm,MODEL=model,LLM_API_KEY=api_key,URL=url,MCPSSE=mcp_sse))
    print(print_color.GREEN+f"Merci d'utiliser GeDAIA Chatbot"+print_color.BLACK)