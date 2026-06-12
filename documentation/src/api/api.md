# Homepedia REST API

Nous avons choisi d'utiliser FastAPI pour la création d'une API REST pour servir les données de notre application.

## Architecture Système

L'architecture API REST + Single Page Application est la norme en développement web ces dernières années. Avec le Data Warehouse que nous allons constuire on reconnait ici
la fameuse [architecture trois tiers](https://fr.wikipedia.org/wiki/Architecture_trois_tiers) à l'échelle de notre système:
- Couche de présentation (Single Page Application)
- Couche de traitement (API REST)
- Couche d'accés aux données (Data Warehouse)

## Architecture Logicielle

À propos de l'API en elle même l'idée serait également d'adopter [une architecture en couche (layered)](https://softwarearchitecture.fr/layered_architecture/). On découpes ici notre application en couches horizontales qui rappellent celles de notre architecture système. 

> [!NOTE]
> Comme mentionné sur le site [softwarearchitecture.fr](https://softwarearchitecture.fr/layered_architecture/#ce-que-nest-pas-une-architecture-en-couche) l'architecture en couches organises nos composants en couches techniques et non par domaine métier. Cependant ce tradeoff semble acceptable dans la mesure ou ce n'est pas une application d'entreprise ou l'on cherches à modéliser plusieurs domaines métiers.

On retrouves souvent les Design Patterns (patrons de conception) *Service*, *Controller* et *Repository* pour gérer le découpage des responsabilités dans l'application. Ceci sont trés bien expliqués dans [cet article](./services_controllers_repositories.md)


