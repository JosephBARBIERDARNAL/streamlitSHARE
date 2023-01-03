# streamlitSHARE

### Data app project for the [SHARE study](https://share-eric.eu).

Goal: simplify the technical problems encountered by researchers working on the SHARE data. Description of the project below.


# Application Streamlit pour l'exploration de données issues de la *[Survey of Health, Ageing and Retirement in Europe](http://www.share-project.org/home0.html)* (SHARE)

> #### ***SHARE** est la plus grande étude européenne de panel en sciences sociales. Elle fournit des microdonnées longitudinales comparables au niveau international, qui permettent de mieux comprendre les domaines de la santé publique et des conditions de vie socio-économiques des individus européens.*

Entre 2004 et 2020, répartis en 8 vagues de questionnaires, plus de 140.000 individus européens ont été intérrogées sur un vaste panorama de domaines : **santé** (maladies, capacités physiques, état mental, consommation alcool/tabac, activité physique, assurance maladie...), **socio-économique** (revenu, statut marital, famille, éducation, vie professionnelle présente et passée, vie de couple...), **style de vie** (gestion des finances, vie sociale, activités...) ainsi que d'autres **sujets divers** (test de personalité, philosophie de vie, opinions...).

### Objectif du projet

Cette base de données a donc un intérêt potentiel important pour les chercheurs en sciences sociales. Cependant, il existe un certain nombre de contraintes techniques à l'exploitation de celle-ci. Chaque vague de questionnaire contient 20 et 45 jeux de données, triés par catégorie, ce qui rend l'exploitation complexe nécessitant un **important travail de merging et de nettoyage en amont**.

Pour cela, nous souhaitons créer une application [Streamlit](https://streamlit.io) qui permettrait au chercheur de choisir une vague de questionnaire (exemple : *vague 8, publiée en 2020*) les paramètres qui l'intéressent (exemple : *maladie de parkinson, les dépenses de santé annuelle et la fréquence d'activité physique*), de choisir un modèle statistique (exemple : *régression linéaire par moindre carrés*) et qui retourne les principaux résultats associés. Dans cet exemple, l'application présenterait les p-values des coefficients associés, le $R^2$, l'erreur quadratique moyenne du modèle et certains graphiques. De cette manière, un chercheur pourrait avoir **accès facilement aux résultats qui l'intéressent**.

Le but n'est pas de fournir un résultat exhaustif sur les paramètres étudiés, mais seulement de donner un premier aperçu de la dimension explicative de certaines variables sur d'autres. Pour approfondir, le chercheur pourra **récupérer un fichier .csv (merge et nettoyage des données effectués) contenant les paramètres demandés**, afin de pouvoir soi-même effectuer une analyse statistique. 

### Travail à effectuer 
- Créer une interface utilisateur avec [Streamlit](https://streamlit.io)
- Effectuer un pré-nettoyage des données pour accélerer l'utilisation de l'app
- Créer un algorithme qui sélectionne les paramètres choisis et les transforme
- Avoir un panel de modèles utilisables, notamment via la librairie [scikit-learn](https://scikit-learn.org/stable/index.html)
- Déterminer quels outputs seront présentés en fonction du type de modèle utilisé

### Informations supplémentaires

La base de données SHARE contient des jeux de données supplémentaires à ceux décrits précédemment, ayant des caractéristiques particulières. Ils ne concernent qu'un ou peu de pays ou ne s'intéressent qu'au COVID-19. Pour ces raisons, ils ne seront pas utilisés pour le projet.
