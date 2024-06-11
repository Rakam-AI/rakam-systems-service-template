# dj_ai_api

Aperçu
------

L'API est conçue pour fournir une interface conversationnelle permettant aux utilisateurs d'interagir avec des guides et des documents. Elle utilise un LLM et un Vector Store pour comprendre les messages des utilisateurs et générer des réponses appropriées. L'API comporte des endpoints pour le frontend et le backend. Elle est développé en Django.

--- 

Endpoints
--------------------

- #### GET /health

Cet endpoint permet de tester le bon fonctionnement du serveur. Le status code devrait être 200.
```json
{
    "status": "healthy"
}
```

### Router api/auth/

### Router api/application/
---

Services externes
------------

L'API RAG nécessite une configuration avec les API externes suivantes :

* Endpoint LLM : L'API doit avoir un LLM endpoint LLM au format suivant :
```json
{
    "message" : "..."
}
```
* La sortie sera au format JSON avec le champ suivant :
```json
{
    "response" : "..."
}
```

Questions
--------

Backend
* Comment accéder aux différents types de données ? Documents, Guides, Pushes ?
* Comment connaître à quels documents le user a accès, dans son environnment actuel ? Est-ce que le UserId & ProjectId suffisent ?

Frontend
* Le frontend souhaite-t-il pouvoir charger un historique de chat ? Quelle sera la vie du chat dans l'expérience utilisateur ? 
* Comment connaître les variables nécessaires pour les « guides dynamiques » ? 

Ops
* Est-il clair que je peux déployer cette architecture sur AWS ? Quand est-ce que je peux avoir les accès au service cloud ?



Besoins
--------
Clé secrète JwT
Clé API Lemon


oauth2 (?) autre protocole que Jwt
-> Pour obtenir un Bearer
-> Pour aller chercher

## Install 

Go to folder "server"

conda create -n "llmapp" python=3.8

ou

python3 -m venv llmapp && source llmapp/bin/activate

puis 

pip3 install -r requirements.txt
pip install langchain
pip install -U langchain-community

## Générer un vector store 

1. ajouter des documents dans data/documents (mkdir data/documents)
2. executer : python data_processing/generate_vector_store.py

## Générer des quiz : 

source llmapp/bin/activate 
python3 application/tests.py 

Pour regarder comment le code fonctionnne, vous pouvez explorer la fonction executé ci-dessus.

## Docker :

### Lancer Docker & Build l'image :  

docker login
docker pull python:3.8
sudo docker build -t application .

http POST http://0.0.0.0:8000/app/generate_quiz_from_text/ text_input='La France à 67 Millions d'habitants' num_questions:=1
http POST http://0.0.0.0:8000/app/generate_quiz_from_text_to_md/ text_input='La France à 67 Millions dhabitants' num_questions:=1


### Lancer le container docker :

sudo docker run -it application:latest /bin/bash

Test :
pip install langchain
pip install -U langchain-community
python application/tests.py 

```bash
sudo docker compose -f docker-compose-dev.yml up
sudo docker compose -f docker-compose-prod.yml up
```

#### Stopper un container
```bash
sudo docker compose -f docker-compose-dev.yml down
```

#### Stopper un container et supprimer ses images
```bash
sudo docker compose -f docker--compose-dev.yml down && docker system prune -af && docker volume prune -f docker-compose-dev.yml
```


### Mettre à jour l'image Docker dans AWS

sudo aws ecr get-login-password --region eu-west-3 | sudo docker login --username AWS --password-stdin 471112908126.dkr.ecr.eu-west-3.amazonaws.com/lemon_generation_api
sudo docker build -t 471112908126.dkr.ecr.eu-west-3.amazonaws.com/lemon_generation_api .
sudo docker push 471112908126.dkr.ecr.eu-west-3.amazonaws.com/lemon_generation_api

471112908126.dkr.ecr.eu-west-3.amazonaws.com/lemon_generation_api

---

## Architecture du code 

```
|-- DJ-AI-API
    |-- api-auth
    |-- application
    |-- server
```

L'application est une application Django dont la logique est dans : server/

#### server
server/urls.py est le router des endpoints de l'API qui va appeler des « Views ». Ces views sont dans le dossier qui contient la logique de l'application django application/

Dans application/ il faut regarder le fichier views.py si vous souhaitez créer vos propres endpoints. Puis dans app/ pour trouver les fonctions de génération.

#### api-auth
api-auth should contain the authentication logic.
```
|-- api-auth
    |-- keys
    |-- management
        |-- commands
```
Commands contains two scrits for first implementations tests.

You can run `python manage.py generate_keys.py` to update mock JWKs file stored in keys repository.

Run `python manage.py test_auth.py` to test the auth system using the mock JWKs file.

#### application
application should contain the core logic.

The main logic should be placed in the engine repository.