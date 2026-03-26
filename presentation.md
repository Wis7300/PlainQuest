## Fontionnement

### Type de jeu
Jeu de rôle (RPG) en 2D, développé en Python à l’aide de la bibliothèque Arcade. 
Le jeu repose sur des mécaniques d’exploration, et de survie par l’amélioration de l’équipement.

### Objectif
L’objectif principal est de survivre, explorer une carte générée aléatoirement, vaincre des monstres et améliorer son équipement grâce à la récolte de ressources, l’artisanat et le commerce. 
Le joueur doit évoluer dans un environnement dangereux et tirer parti des ressource disponibles pour progresser.

### Idée principale
Le cœur du jeu repose sur un cycle équilibré entre les quatre piliers majeurs :

- Combat contre différents monstres qui obligent à adapter sa stratégie.
- Récolte de ressources (bois et pierre) indispensables à la survie.
- Artisanat (craft) pour transformer les ressources en équipements plus puissants.
- Commerce avec des marchands pour acheter ou vendre des objets et compléter les ressources manquantes.


## Architecture du projet

Le projet a été structuré selon une logique modulaire et orientée objet, facilitant l’évolution et la maintenance du code.

### Organisation modulaire
Le code est séparé en plusieurs modules correspondant chacun à une fonction précise du jeu (affichage, gestion de la carte, inventaire, combats, etc.). 
Cette séparation permet d’ajouter, modifier ou corriger des éléments sans impacter le reste du code, ce qui est essentiel pour un jeu en évolution constante.

### Choix de la POO
On a choisit d'utiliser la programmation orientée objet car :

- C'est le type de structure nécessaire pour le fonctionnement d'arcade (qui fonctionne avec des classes Window, View et Sprite)
- Cela permet au code d'être plus organisé et plus clair


## Difficultés rencontrées

### Apprentissage de Python
Ce projet est notre premier vrai premier projet en python et en informatique en général. 
On a donc dû se perfectionner en python, et particulièrement sur la partie POO, zone floue pour la grande majorité du groupe.

### Apprentissage de la bibliothèque Arcade
Ce projet nous a aussi permit de découvrir la bibliothèque Arcade, qui sert à créer des jeux 2D, et qui ressemble donc à Pygame, mais en plus moderne et donc plus performant.

### Contrainte du temps
Le temps a été un motif de pression tout au long du projet, car nous n'avions que deux mois pour rendre un projet aussi bien que des projets faits sur deux ou trois fois plus de temps. 
Pendant ces deux mois, on a appris à se servir de la bibliothèque arcade, fait plusieurs mini-projets pour rentrer dans la logique de la bibliothèque avant d'enfin commencer le vrai jeu. 
C'était donc un planning serré, et compliqué à soutenir.


## Contrôles

### Déplacements
Z => Monter  
Q => Aller à gauche  
S => Descendre  
D => Aller à droite  

### Menus
A => Ouvrir l'inventaire  
- clique droit sur certains objets : utilisation de ceux-ci  
- clique gauche sur les items : on les lache  

C => Ouvrir le menu de craft  
- clique sur un bouton : ajout de l'objet créé dans l'inventaire  

E => Ouvrir le menu d'échange avec les pnj  
- clique sur un bouton : action écrite sur le bouton effectuée  

### Attaque
Clique gauche => Attaque  
- si clique à gauche du joueur => attaque à gauche du joueur  
- si clique à droite du joueur => attaque à droite du joueur  


## Mécaniques

### Création et gestion d'ennemis
Deux types de monstres peuplent le monde. 
Chacun possède des caractéristiques, vitesses et comportements distincts, ce qui oblige le joueur à adapter ses stratégies. 
Les ennemis apparaissent aléatoirement sur la carte et représentent une menace permanente pendant la récolte ou l’exploration.

### Inventaire
- L'inventaire est une liste, et non un dictionnaire (possibilité envisagée et utilisée au début du projet)
- Celui-ci choisit automatiquement la meilleure arme présente dans l'inventaire, et si il n'en existent aucunes, il choisit le poing (plus petite hitbox et très faibles dégâts)

### Craft
- Les recettes de craft sont stockées dans un fichier Json, à part, facilitant donc sa modification

### Echanges
- Le joueur peut interagir avec des marchands PNJ pour acheter ou vendre des objets.
- Ce système économique complète la récolte et permet d’obtenir des matériaux rares via des échanges plutôt que par la simple exploration.


## Possibilités d'évolution

### Cartes
Grâce à l'organisation modulaire du projet, rajouter cartes et mondes ne serait pas un défi en soit, bien que long à implémenter par la quantitée de nouvelle textures requises. 
Nous avions en effet une idée de créer une seconde carte, se situant dans une ville ayant survécu à la corruption, ville dans laquelle de nombreux survivants seraient présents, et qui auraient pu proposer des quêtes au joueur, mais aussi diversifier les échanges des pnj. 
En effet, ceux-ci pourrait avoir un métier, qui détermine une liste d'échange possibles, différente pour chaque profession.

### Objets
Le système de craft permettrait d’intégrer de nouveaux objets :

- Armes spéciales avec effets particuliers (feu, poison, gel, etc.).
- Objets consommables (potions, nourritures, kits de soin).
- Outils de récolte augmentant la vitesse ou la quantité de matériaux obtenus.

### Ennemis
De nouveaux types d’ennemis pourraient être ajoutés pour renforcer la diversité :

- Ennemis boss avec des attaques spéciales.
- Créatures rares apparaissant selon certaines conditions (zone, heure, météo…).
- Comportements plus complexes (esquives, attaques, patterns/IA)


## Inspirations

Le projet puise son inspiration dans plusieurs classiques du jeu de rôle et de survie 2D, notamment :

- Les boucles de gameplay d’exploration et de craft de Terraria.
- Le système de combat et la progression d’équipement inspirés de Zelda – A Link to the Past.
- L’idée d’un monde généré procéduralement rappelant Minecraft, favorisant la rejouabilité.


## Description plus précise des entitées

### Objets
- Ressources de base : bois et pierre.
- Objets de craft : épées, outils, et potentiellement des potions ou accessoires.
- Les objets ont une valeur économique permettant leur échange avec les PNJ.

### Ennemis
- Type 1 : créature rapide mais fragile, attaquant en nombre.
- Type 2 : monstre lent mais résistant, infligeant des dégâts plus importants.