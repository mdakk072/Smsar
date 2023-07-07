
# Smsar

## Description du Projet

Ce projet vise à développer une application web qui fournit des statistiques et des informations sur le marché immobilier. L'application recueille des informations sur différentes annonces immobilières et les présente sous forme de statistiques. En outre, l'application offre des informations sur les quartiers des villes, y compris les établissements locaux et les articles de presse pertinents.

# Sections du Projet
![Image](https://raw.githubusercontent.com/mdakk072/Smsar/main/diagrams/projet%20shema.svg)


## Web Scrapping

Le web scrapping est une technique essentielle dans ce projet, utilisée pour extraire des informations à partir de divers sites web d'annonces immobilières. Cette méthode nous permet de recueillir une grande quantité de données pertinentes pour notre analyse, y compris le type de propriété (par exemple, maison, appartement, terrain, etc.), le prix demandé, l'emplacement de la propriété, et d'autres détails qui peuvent être importants pour les acheteurs, les vendeurs, et les investisseurs immobiliers.

Dans le cadre de notre preuve de concept, nous avons mis en œuvre le web scrapping pour la catégorie "immobilier à vendre" sur [Avito](https://www.avito.ma/), un site web populaire d'annonces immobilières. Au total, nous avons réussi à scraper 128 000 annonces, ce qui nous a fourni une base de données initiale pour commencer notre analyse.

Cependant, il est important de noter que notre module de web scrapping est conçu pour être flexible et extensible. Bien que notre preuve de concept se concentre sur Avito, le module peut être adapté pour scraper des données à partir d'une variété de sites immobiliers, tels que [Sarouty](https://www.sarouty.ma/), [Mubawab](https://www.mubawab.ma/), et [Maroc Annonces](https://www.marocannonces.com/). Cela signifie que nous pouvons élargir notre base de données pour inclure des informations provenant de plusieurs sources, ce qui nous permettra d'avoir une vue plus complète et plus précise du marché immobilier.

En outre, notre module de web scrapping est également capable de scraper les API d'information. Par exemple, nous pourrions utiliser l'API de Google Places pour obtenir des informations sur les établissements locaux dans un quartier spécifique, ou l'API de Twitter pour recueillir des tweets relatifs à l'immobilier. Ces API peuvent nous fournir des informations supplémentaires qui peuvent être pertinentes pour notre analyse, comme les tendances du marché, les nouvelles de l'industrie, et les commentaires des utilisateurs sur les propriétés spécifiques.


### **Description**

Le module de web scrapping est implémenté en utilisant les bibliothèques Selenium, BeautifulSoup et Requests. Il est capable de scraper les sites web en fonction d'une configuration fournie.

### **Dépendances**

- Selenium
- BeautifulSoup
- Requests

### **Exemple d'utilisation**

```python
scraper = Scraper('config.yaml')
scraper.scrape_site()
```

### **Méthodes**
| Méthode | Description | Paramètres | Retour |
| --- | --- | --- | --- |
| `__init__(self, config_file)` | Initialise le scraper avec le fichier de configuration. | `config_file` : Chemin vers le fichier de configuration. | Aucun |
| `init_driver(self)` | Initialise le web driver pour Selenium. | Aucun | Aucun |
| `scrap_page(self, by_method, value)` | Scraper une page web. | `by_method` : Méthode de sélection des éléments à scraper (ex: XPATH, CSS Selector, etc.), `value` : Valeur utilisée avec la méthode de sélection pour identifier les éléments à scraper. | Objet contenant les données scrapées de la page. |
| `extract_data(self, raw_data, selectors)` | Extraire des données spécifiques à partir des données brutes scrapées. | `raw_data` : Données brutes scrapées, `selectors` : Sélecteurs utilisés pour identifier les données à extraire. | Objet contenant les données extraites. |
| `extract_infos(self, extracted_data, data_to_find)` | Extraire des informations spécifiques à partir des données extraites. | `extracted_data` : Données extraites, `data_to_find` : Clés des informations à extraire. | Objet contenant les informations extraites. |
| `extract_attributes(self, element)` | Extraire les attributs d'un élément HTML. | `element` : Élément HTML dont les attributs doivent être extraits. | Objet contenant les attributs de l'élément. |
| `goto_next_page(self, base_url, next_page)` | Naviguer vers la page suivante d'un site web. | `base_url` : URL de base du site web, `next_page` : Numéro de la page suivante à visiter. | Objet contenant les données scrapées de la page suivante. |
| `goto_link(self, link)` | Naviguer vers un lien spécifique. | `link` : Lien vers lequel naviguer. | Objet contenant les données scrapées du lien. |
| `call_api(self, api_url)` | Faire une requête GET à une API spécifique. | `api_url` : URL de l'API à appeler. | Objet contenant les données renvoyées par l'API. |



### **Configuration**

La configuration du scraper est définie dans un fichier YAML. Ce fichier contient des informations sur les états et les paramètres du scraper. Voici une explication des attributs de configuration :

| Attribut | Description |
| --- | --- |
| `base_url` | L'URL de base du site à scraper. |
| `initial_state` | L'état initial du scraper. |
| `states` | Les différents états que le scraper peut avoir. Chaque état a une méthode associée et des paramètres. |
| `states.[state_name].method` | La méthode à exécuter dans cet état. |
| `states.[state_name].next_state` | L'état suivant après l'exécution de la méthode actuelle. |
| `states.[state_name].parameters` | Les paramètres nécessaires pour exécuter la méthode. |
| `states.[state_name].parameters.[parameter_name]` | Un paramètre spécifique nécessaire pour exécuter la méthode. |
| `states.[state_name].parameters.[parameter_name].attribute` | L'attribut à extraire pour le paramètre spécifique. |
| `states.[state_name].parameters.[parameter_name].extract` | Comment extraire l'attribut (par exemple, texte, attribut). |
| `states.[state_name].parameters.[parameter_name].type` | Le type d'élément à partir duquel extraire l'attribut (par exemple, xpath). |
| `states.[state_name].parameters.[parameter_name].attribute_name` | Le nom de l'attribut à extraire si `extract` est défini sur `attribute`. |
| `userAgent` | L'agent utilisateur à utiliser pour les requêtes web. |


Et voici un exemple simplifié de fichier de configuration :
![Image](https://raw.githubusercontent.com/mdakk072/Smsar/main/diagrams/FSM%20SCRAPPER%20YAML.svg)

```yaml
base_url: https://www.example.com?page={i}
initial_state: goto_next_page
states:
  goto_next_page:
    method: goto_next_page
    next_state: scrap_page
    parameters:
      base_url: https://www.example.com?page={i}
      next_page: 1
  scrap_page:
    method: scrap_page
    next_state: extract_data
    parameters:
      by_method: xpath
      value: //div[@class="content"]
  extract_data:
    method: extract_data
    next_state: send_data
    parameters:
      raw_data: '{previous_result}'
      selectors:
      - attrs:
          class: item
        name: div
  send_data:
    method: send_data
    next_state: goto_next_page
    parameters:
      address: http://localhost:5000/api/receive_data
      data: '{previous_result}'
userAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36

```

### **Changements futurs prévus**
- Amélioration de la gestion des erreurs lors du scraping.
- Ajout de la prise en charge d'autres types d'API d'information.
- Optimisation de la vitesse de scraping.

## Analyse des Données

Les données recueillies sont analysées pour produire des statistiques sur le marché immobilier. Ces statistiques peuvent inclure des informations sur les tendances des prix, les types de propriétés les plus courants, et d'autres informations utiles pour les acheteurs, les vendeurs, et les investisseurs immobiliers.

AD

## Base de Données 

La base de données est utilisée pour stocker les informations recueillies et les résultats de l'analyse des données. Le module de base de données est responsable de la gestion des opérations de base de données en fonction d'une configuration fournie. Il utilise SQLAlchemy pour interagir avec la base de données.

### **Comment ça fonctionne**

La classe `DatabaseManager` est initialisée avec un fichier de configuration. Ce fichier de configuration contient des informations sur la base de données telles que le nom, l'identifiant, le mot de passe, l'hôte et le port. Il contient également des informations sur le moteur SQLAlchemy et les configurations de mise en commun.

Une fois initialisé, le `DatabaseManager` configure le moteur SQLAlchemy et crée une base déclarative. Il crée ensuite dynamiquement une classe pour chaque table définie dans le fichier de configuration et crée toutes les tables dans le moteur.

Le `DatabaseManager` fournit des méthodes pour créer une nouvelle session, ajouter un nouvel enregistrement à une table, mettre à jour un enregistrement existant dans une table, supprimer un enregistrement d'une table, récupérer un enregistrement d'une table et rechercher des enregistrements dans une table.

### **Exemple de code**

Voici un exemple d'utilisation du `DatabaseManager` :

```python
db_manager = DatabaseManager('configDB.yaml')
session = db_manager.get_session()
```

### **Méthodes**
| Méthode | Description |
| --- | --- |
| `__init__(self, config_file)` | Initialise le scraper avec le fichier de configuration spécifié. |
| `init_driver(self)` | Initialise le pilote web pour Selenium. |
| `scrap_page(self, by_method, value)` | Récupère le contenu de la page en utilisant la méthode et la valeur spécifiées. |
| `extract_data(self, raw_data, selectors)` | Extrait les données du HTML brut en utilisant les sélecteurs fournis. |
| `extract_infos(self, extracted_data, data_to_find)` | Extrait les informations d'intérêt à partir des données extraites en utilisant les clés spécifiées dans `data_to_find`. |
| `extract_attributes(self, element)` | Extrait les attributs de l'élément HTML donné. |
| `goto_next_page(self, base_url, next_page)` | Va à la page suivante en utilisant l'URL de base et le numéro de la page suivante. |
| `goto_link(self, link)` | Va au lien spécifié. |
| `call_api(self, api_url)` | Fait une requête GET à l'URL de l'API spécifiée. |
| `send_data(self, data, address)` | Envoie des données à l'adresse spécifiée en utilisant une requête POST. |
| `scrape_site(self, config=None)` | Récupère le site web en utilisant les états et les paramètres spécifiés dans le fichier de configuration. |


### **Configuration**

Le `DatabaseManager` utilise un fichier de configuration YAML. Voici un exemple de fichier de configuration :

```yaml
database:
  name: 'mydb'
  username: 'user'
  password: 'password'
  host: 'localhost'
  port: 5432

sqlalchemy:
  echo: false
  track_modifications: false

pooling:
  max_overflow: 10
  pool_size: 5
  pool_timeout: 30
  pool_recycle: 3600

tables:
  - name: 'table1'
    columns:
      - name: 'ID'
        type: 'Integer'
        primary_key: true
      - name: 'column1'
        type: 'String'
  - name: 'table2'
    columns:
      - name: 'ID'
        type: 'Integer'
        primary_key: true
      - name: 'column1'
        type: 'String'
      - name: 'column2'
        type: 'Integer'
        foreign_key: 'table1.ID'
```
Dans cet exemple, deux tables sont définies : `table1` et `table2`. `table1` a deux colonnes : `ID` (clé primaire) et `column1`. `table2` a trois colonnes : `ID` (clé primaire), `column1` et `column2` (clé étrangère vers `table1.ID`).
| Clé | Description |
| --- | --- |
| `database:name` | Le nom de la base de données. |
| `database:username` | Le nom d'utilisateur pour se connecter à la base de données. |
| `database:password` | Le mot de passe pour se connecter à la base de données. |
| `database:host` | L'hôte où se trouve la base de données. |
| `database:port` | Le port pour se connecter à la base de données. |
| `database:sslmode` | Le mode SSL pour la connexion à la base de données. |
| `database:drivername` | Le nom du driver de la base de données à utiliser. |
| `sqlalchemy:echo` | Si `true`, SQLAlchemy affiche les requêtes SQL brutes. |
| `sqlalchemy:track_modifications` | Si `false`, SQLAlchemy ne suit pas les modifications des objets. |
| `sqlalchemy:pool_pre_ping` | Si `true`, SQLAlchemy effectuera un "ping" à la base de données avant chaque connexion pour vérifier si la connexion est toujours valide. |
| `pooling:max_overflow` | Le nombre maximum de connexions à créer au-delà de la taille du pool. |
| `pooling:pool_size` | La taille du pool de connexions à maintenir. |
| `pooling:pool_timeout` | Le nombre de secondes à attendre avant d'abandonner le retour d'une connexion au pool. |
| `pooling:pool_recycle` | Le nombre de secondes après lequel une connexion est automatiquement recyclée. |
| `pooling:pool_reset_on_return` | Détermine ce qui se passe lorsqu'une connexion est retournée au pool. Les options possibles sont `rollback`, `commit` ou `none`. |
| `tables` | Une liste de tables à créer dans la base de données. Chaque table est un dictionnaire avec les clés `name` (le nom de la table) et `columns` (une liste de colonnes). |
| `tables:name` | Le nom de la table. |
| `tables:columns` | Une liste de colonnes pour la table. Chaque colonne est un dictionnaire avec les clés `name` (le nom de la colonne), `type` (le type de la colonne), `primary_key` (si `true`, la colonne est une clé primaire), `foreign_key` (si présent, la colonne est une clé étrangère vers la colonne spécifiée), `index` (si `true`, un index est créé pour la colonne), `unique` (si `true`, la colonne est définie comme unique), `nullable` (si `true`, la colonne peut avoir des valeurs nulles), et `default` (la valeur par défaut de la colonne). |
| `tables:foreign_keys` | Une liste de clés étrangères pour la table. Chaque clé étrangère est un dictionnaire avec les clés `name` (le nom de la clé étrangère), `references` (la table et la colonne que la clé étrangère référence) et `ondelete` (l'action à effectuer lorsque la ligne référencée est supprimée). |
| `tables:indices` | Une liste d'indices à créer pour la table. Chaque indice est un dictionnaire avec les clés `name` (le nom de l'indice) et `columns` (les colonnes à inclure dans l'indice). |
| `tables:uniques` | Une liste de contraintes d'unicité à créer pour la table. Chaque contrainte est un dictionnaire avec les clés `name` (le nom de la contrainte) et `columns` (les colonnes à inclure dans la contrainte). |
| `tables:checks` | Une liste de contraintes de vérification à créer pour la table. Chaque contrainte est un dictionnaire avec les clés `name` (le nom de la contrainte) et `condition` (la condition de la contrainte). |


### **Structure de la base de données**
La base de données comprend les tables suivantes :
![Image](https://raw.githubusercontent.com/mdakk072/Smsar/main/diagrams/shema%20DB.svg)

| Nom de la Table | Attributs |
| --- | --- |
| Propriétés | ID, Type, Ville, Quartier, Prix, Date de publication, URL de l'image, Nombre d'images, Nombre de chambres, Nombre de salons, Nombre de salles de bain, Numéro d'étage, Surface habitable, Surface totale, Âge de la propriété, URL de l'annonce |
| Villes | ID, Nom |
| Quartiers | ID, Nom, ID de la ville |
| Établissements | ID, Nom, Type, Évaluation, ID du quartier |
| Avis | ID, Sentiment, Texte, ID de l'établissement |
| Articles de Presse | ID, Titre, Sentiment, Texte, Date de publication, ID du quartier |
| Posts sur les Réseaux Sociaux | ID, Sentiment, Texte, Date de publication, ID du quartier, ID de la ville, ID de l'établissement, ID de la propriété, ID de l'article de presse |
| Statistiques | ID, Date, Type de Statistique, Valeur, ID de la Ville, ID du Quartier, ID de l'Établissement, ID de la Propriété |

## API
L'API est utilisée pour fournir un accès aux informations et aux statistiques stockées dans la base de données. L'API peut être utilisée par divers clients, y compris une application web, une application mobile, ou d'autres services.
AD

## Interface Utilisateur

L'interface utilisateur permet aux utilisateurs d'interagir avec l'application. Elle peut inclure des visualisations de données, des outils de recherche, et d'autres fonctionnalités pour aider les utilisateurs à comprendre le marché immobilier.
AD
## Technologies Utilisées

Le projet utilise une variété de technologies, y compris Python pour le web scrapping et l'analyse des données, ...