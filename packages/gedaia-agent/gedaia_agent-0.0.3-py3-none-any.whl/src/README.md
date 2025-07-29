# Comment tester 

|Auteur | Date | Action | Version |
|-- | -- | -- | -- |
| Jacques MASSA|8 avril 2025| Création|V1.0 |
| Jacques MASSA | 20 avril 2025 | intégration LangGraph |

## installation 
` 
pip install pylexfluent_Agent_Interop_GeDAIA==0.0.2
` 


## Démarrer le serveur directement
> 
>python3 
>>Python 3.12.3 (main, Feb  4 2025, 14:48:35) [GCC 13.3.0] on linux
>>Type "help", "copyright", "credits" or "license" for more information.
>>> from aig.demo.server.math_server import start_demo_server
>>>start_demo_server(port=8001)

## Utiliser l'inspecteur MCP 

### Installer l'inspecteur 
` 
pip install MCP[cli]
` 
### Démarer l'inspecteur 

>**mcp dev math_server.py** 
>Need to install the following packages:
>@modelcontextprotocol/inspector@0.8.1
>Ok to proceed? (y) y
>Starting MCP inspector...
>⚙️ Proxy server listening on port 6277
>🔍 MCP Inspector is up and running at http://127.0.0.1:6274 🚀


## Tester le serveur 
>python3 
>>Python 3.12.3 (main, Feb  4 2025, 14:48:35) [GCC 13.3.0] on linux
>>Type "help", "copyright", "credits" or "license" for more information.
>>>import asyncio
>>>from aig.demo.client.ollama_client import agent_matheux
>>>if __name__=='__main__': 
>>>    asyncio.run(agent_matheux(model_name="mistral:7b-instruct-v0.3-fp16"))

```
1: prompt= Calculator-prompt (prompt pour calculer des opération d'addition, multiplication et division entre deux termes)
Quel numéro de prompt voulez utiliser? 1
Poser votre question 

Question: 45+91
=>	Type: GeDAIA(human)
	
    Vous êtes un agent intelligent capable de répondre aux questions et d'effectuer des tâches et utilisant exlusivement les outils mis à ta disposition.
    Vous ne pouvez répondre qu'en utilisant les outils fournis.
    Calcule l'opération ci-dessous:
45+91 
    

=>	Type: GeDAIA(ai)
	

=>	Type: Ajouter(tool)
	136.0

=>	Type: GeDAIA(ai)
	136 est la réponse de l'opération 45 + 91.

Question: exit
```

