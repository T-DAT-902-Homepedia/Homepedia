# Services, Controllers et Repositories — Une Introduction

[*Article Medium par Gabriel Gomes, PhD*](https://gabrielgomes61320.medium.com/services-controllers-and-repositories-an-introduction-241ac52cdd93)

Dans le paysage actuel du développement logiciel, construire des APIs scalables et maintenables est essentiel, d'autant plus que nous nous orientons vers des architectures en microservices. Séparer les responsabilités des fonctions et établir des frontières claires dans notre code accélère considérablement le développement et facilite la maintenance ou l'extension de nos services. L'une des clés pour y parvenir est l'utilisation de design patterns bien établis : ces patterns nous fournissent des techniques éprouvées qui favorisent la création de logiciels scalables, adaptables et faciles à comprendre. Dans cet article, nous aborderons les services, les controllers et les repositories (avec, en bonus, une introduction au pattern Unit of Work). Nous expliquerons également comment ces patterns interagissent au sein d'un Web Service pour promouvoir un cycle d'appels de fonctions clair, isolé en termes de responsabilité, et complémentaire dans l'atteinte de l'objectif final : apporter de la valeur à un domaine donné.

---

## Controllers : La couche externe

Les controllers constituent la couche externe de votre architecture d'API. Ils servent de pont entre les APIs HTTP/REST et la couche métier (domaine). Concrètement, ils gèrent les requêtes HTTP, les en-têtes, les paramètres et le routage. Ils dirigent les requêtes entrantes vers les opérations appropriées de la couche domaine.

Les controllers doivent rester simples et se concentrer uniquement sur la gestion des requêtes et le routage. Dans des applications très simples où la couche métier se résume à des opérations CRUD basiques, il arrive que la couche service et la couche controller soient fusionnées en une seule fonction — mais cela **n'est pas une bonne pratique**, surtout si l'on sait que le service deviendra plus complexe, ou si l'on souhaite ajouter des tests unitaires (ce qu'on devrait **toujours** vouloir faire dans n'importe quelle base de code).

---

## Services : La logique métier

La couche service est l'endroit où réside la logique métier de l'application. Elle traite les fonctionnalités et les règles fondamentales du domaine. Bien que dans les applications simples certains placent la logique métier directement dans les controllers, cette pratique n'est pas recommandée. Isoler la logique métier dans des services garantit une meilleure organisation, réutilisabilité et maintenabilité du code.

Plus concrètement : les fonctions de la couche service sont appelées depuis la couche controller, et seule la réponse du service est renvoyée au controller, qui peut ensuite l'exposer (ou une version modifiée) à l'utilisateur.

*Exemple concret :* une requête HTTP POST pour créer une nouvelle commande d'achat crée une entrée dans le système. La création de cette commande est déclenchée dans le controller en appelant une fonction de la couche service. Celle-ci génère un identifiant (nombre ou UUID, généralement correspondant à l'ID de la commande en base de données). Toute l'abstraction de la création de la commande reste encapsulée dans la couche service. Le controller se contente de récupérer le résultat (l'UUID) et de le retourner à l'utilisateur en réponse au POST.

---

## Repositories : La couche de persistance

La couche de persistance agit comme un intermédiaire entre les modèles de l'application et la base de données. Elle est responsable de la création, la mise à jour et la suppression des données (ou de toute opération impliquant une communication avec la base de données). Le **pattern Repository** est un choix de conception populaire pour implémenter cette couche, car il découple la logique de persistance de la couche service, favorisant une architecture plus propre grâce à la programmation par interfaces plutôt que par implémentations bas niveau.

Les repositories favorisent également la réutilisabilité du code : une opération atomique en base de données (comme la création d'un enregistrement) peut être nécessaire dans plusieurs fonctions de service. Le pattern Repository évite la duplication en garantissant que ces opérations simples sont toujours effectuées de la même manière.

Un autre avantage majeur : en exposant une interface utilisée par la couche service pour la persistance, le repository isole *comment* on persiste les données et *quelle* solution de base de données on utilise. En d'autres termes, changer de base de données (par exemple, passer de PostgreSQL à Oracle, ou même d'un modèle SQL à NoSQL) ne nécessite pas de modifier le code de la couche service. On modifie uniquement l'implémentation interne des méthodes du repository, et la couche service continue d'utiliser la même interface avec les mêmes schémas d'entrée/sortie.

---

## Unit of Work : Garantir cohérence et atomicité

Pour maintenir la cohérence des données et garantir des transactions ACID (Atomicité, Cohérence, Isolation, Durabilité), le pattern **Unit of Work (UoW)** est souvent employé conjointement avec le pattern Repository. L'UoW gère une séquence d'opérations en base de données en s'assurant que soit toutes les opérations se terminent avec succès, soit aucune n'est appliquée. Cela évite les mises à jour partielles qui pourraient conduire à des incohérences. En Python, l'UoW est généralement implémentée via des gestionnaires de contexte (context managers), utilisant les méthodes magiques `__enter__` et `__exit__`.

---

## Combiner tous les patterns dans un Web Service

Les sections précédentes expliquent pourquoi chaque couche est nécessaire, mais pas comment elles interagissent concrètement. Voici le flux typique :

1. **Les controllers** sont le "point d'entrée" du service exposé. Ils reçoivent les requêtes des clients et utilisateurs.
2. **La couche service** est ensuite appelée depuis les fonctions du controller. Par exemple, pour créer un nouvel utilisateur, on soumet une requête POST à `/users`. À l'intérieur de cette fonction controller, on appellera une fonction `create_user` de la couche service.
3. **La couche repository** est ensuite utilisée par le service pour persister les données. Une interface `UserRepository` exposerait des méthodes comme `add`, `delete`, `get`, `list`, accessibles depuis la couche service.
4. Une fois toutes les opérations nécessaires effectuées (créer l'utilisateur, stocker une photo sur S3, etc.), on **valide la transaction** avec le pattern Unit of Work.

---

## Conclusion

Cet article a présenté les quatre couches généralement implémentées dans les Web Services pour favoriser scalabilité, cohérence, organisation du code et développement centré sur le métier. Un prochain article appliquera ces design patterns en pratique pour construire une API back-end en Python. Restez connectés !

---

*Références :*
- Microservice APIs in Python — José Haro Peralta (2023)
- https://dev.to/manukanne/a-python-implementation-of-the-unit-of-work-and-repository-design-pattern-using-sqlmodel-3mb5
- https://www.cosmicpython.com/book/chapter_06_uow.html