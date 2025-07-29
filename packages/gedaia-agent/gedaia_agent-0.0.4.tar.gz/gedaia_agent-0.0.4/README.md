# Agent Interopérabilité GeDAIA (AIG)
*Interopérabilité avec la rédaction d'actes*

| Action | Date | Auteur | Version |
|--|--|--|--|
|Création | 4 avril 2025 | Jacques MASSA | V1.0 | 


## Présentation
Cet agent a pour but de travailler avec la rédaction d'actes de l'étude afin de retrouver toutes les informations des dossiers, clients, et documents. 

On veut pouvoir répondre aux questions suivantes :
- Fait moi une synthèse du dossier XXXX
- Quelle est nature du dossier
- Quels sont les actes, annexes, courriels, LRE etc ... 
- synthèse des formalités préalables
- état des formalités postérieurs 
- l'historique d'un client

## Méthode
Pour atteindre nos objectifs, l'agent AIG est construit sur la base d'un agent utilisant un modèle open source tel que Mistral AI 7B ou DeepSeek hébergé en local ou dans notre datacenter .  

La connexion avec la rédaction d'actes de l'étude, nous utilisons notre serveur MCP Interop Notariale.  