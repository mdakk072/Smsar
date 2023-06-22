
## Description du Projet

Ce projet vise à développer une application web qui fournit des statistiques et des informations sur le marché immobilier. L'application recueille des informations sur différentes annonces immobilières et les présente sous forme de statistiques. En outre, l'application offre des informations sur les quartiers des villes, y compris les établissements locaux et les articles de presse pertinents.

## Sections du Projet

### Web Scrapping

Le web scrapping est utilisé pour recueillir des informations sur les annonces immobilières à partir de divers sites web. Les informations recueillies comprennent le type de propriété, le prix, l'emplacement, et d'autres détails pertinents.

### Analyse des Données

Les données recueillies sont analysées pour produire des statistiques sur le marché immobilier. Ces statistiques peuvent inclure des informations sur les tendances des prix, les types de propriétés les plus courants, et d'autres informations utiles pour les acheteurs, les vendeurs, et les investisseurs immobiliers.

### Base de Données

La base de données est utilisée pour stocker les informations recueillies et les résultats de l'analyse des données. La base de données comprend les tables suivantes :

1. **Propriétés** : Cette table stocke des informations sur chaque annonce immobilière.
2. **Villes** : Cette table stocke des informations sur chaque ville où se trouvent les propriétés.
3. **Quartiers** : Cette table stocke des informations sur chaque quartier dans les villes.
4. **Établissements** : Cette table stocke des informations sur divers établissements dans les quartiers.
5. **Avis** : Cette table stocke des avis sur les établissements.
6. **Articles de Presse** : Cette table stocke des informations sur les articles de presse liés aux quartiers.
7. **Posts sur les Réseaux Sociaux** : Cette table stocke des informations sur les posts des réseaux sociaux liés aux quartiers, villes, établissements, propriétés, et articles de presse.

### API

L'API est utilisée pour fournir un accès aux informations et aux statistiques stockées dans la base de données. L'API peut être utilisée par divers clients, y compris une application web, une application mobile, ou d'autres services.

### Interface Utilisateur

L'interface utilisateur permet aux utilisateurs d'interagir avec l'application. Elle peut inclure des visualisations de données, des outils de recherche, et d'autres fonctionnalités pour aider les utilisateurs à comprendre le marché immobilier.

## Technologies Utilisées

Le projet utilise une variété de technologies, y compris Python pour le web scrapping et l'analyse des données, Flask pour l'API, et diverses bibliothèques JavaScript pour l'interface utilisateur. La base de données est mise en œuvre en utilisant SQLite.
