# RobotFrameWords

**Languages:**  [🇬🇧 EN](#-english)/[🇫🇷 FR](#-français)
  
---

## 🇬🇧 English
  
RobotFrameWords is a graphical application dedicated to comprehensive browsing of Robot Framework documentation.
It centralizes keywords, libraries, and all relevant documentation content required for implementing and writing Robot Framework tests, within an intuitive and well-structured interface.

The goal of the project is to provide an offline, readable, ergonomic, and productivity-oriented tool, eliminating constant back-and-forth between a web browser, official documentation, and test code.

## ✨ Features

- Centralized access to Robot Framework documentation
- Advanced full-text search
- Fast navigation through keywords and sections
- Modern graphical interface based on CustomTkinter
- Readable rendering of HTML documentation converted to text
- Support for animations and visual elements (icons, animated labels)
- Fully local usage, with no dependency on external services

## 🧩 General Architecture

The application is built on:

- Python 3.10
- A Tkinter-based graphical interface enhanced with customtkinter
- An HTML documentation parsing and transformation system
- A main executable:
  KeywordsDoc.py

## 📦 Dependencies

The application must be executed inside a Python virtual environment containing the following dependencies:

```python
import os
import re
import sys
import json
import subprocess
import tkinter as tk
from tkinter import StringVar
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageDraw, ImageFont
from collections import OrderedDict
import html2text
from AnimatedLabel import AnimatedLabel
```

### Main external dependencies

- **customtkinter**
- **Pillow (PIL)**
- **html2text**

## 🐍 Virtual Environment (venv)

A minimal script is provided to create a virtual environment consistent with the project requirements.

### Script: install_kdoc_venv.sh

```bash
python3.10 -m venv kdoc_venv
source ~/rf_keywords_doc/kdoc_venv/bin/activate
```

> ⚠️ This script is intentionally minimal. Users are free to use it or not, but it provides a coherent base aligned with the project requirements.

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/<your-username>/robotFrameworkCompleteDoc.git
cd robotFrameworkCompleteDoc
```

2. Create and activate the virtual environment:
```bash
bash install_kdoc_venv.sh
```

3. Install the required dependencies (example):
```bash
pip install customtkinter pillow html2text
```

> Depending on your system, Tkinter may require a separate installation
(e.g. python3-tk on some Linux distributions).

---

## ▶️ Running the Application

Once the virtual environment is activated:
```bash
python KeywordsDoc.py
```
## 🖥️ Compatibility

Linux: ✅ tested

Windows: ⚠️ not tested

macOS: ⚠️ not tested

The interface relies on Tkinter; compatibility therefore depends on the platform’s Tk support.

## 📚 Use Cases

* Robot Framework developers and test engineers
* Fast keyword lookup without a web browser
* Offline documentation access
* Support tool for writing automated tests

## 🛠️ Project Status

* Functional project
* Possible future improvements

  
  * Dynamic library indexing
  * Additional graphical themes

---

## 📄 License

To be defined.

## 👤 Author

Project developed as an advanced tooling initiative around Robot Framework by Sébastien Dethyre.

## 🤝 Contributions

Contributions, suggestions, and feedback are welcome.  
Feel free to open an issue or submit a pull request.
  
---

<br>

---

## 🇫🇷 Français
  
**robotFrameworkCompleteDoc** est une application graphique dédiée à la consultation complète de la documentation Robot Framework. Elle centralise l’ensemble des mots-clés, librairies et contenus documentaires utiles à l’implémentation et à l’écriture de tests Robot Framework, au sein d’une interface intuitive et structurée.

L’objectif du projet est de fournir un outil **offline**, lisible, ergonomique et orienté productivité, évitant les allers-retours constants entre navigateur, documentation officielle et code.

---

## ✨ Fonctionnalités

* Consultation centralisée de la documentation Robot Framework
* Recherche plein texte avancée
* Navigation rapide par mots-clés et sections
* Interface graphique moderne basée sur **CustomTkinter**
* Rendu lisible de contenus HTML convertis en texte
* Support des animations et éléments visuels (icônes, labels animés)
* Utilisable localement, sans dépendance à un service externe

---

## 🧩 Architecture générale

L’application repose sur :

* **Python 3.10**
* Une interface graphique Tkinter enrichie via **customtkinter**
* Un système de parsing et de transformation de documentation HTML
* Un exécutable principal :

```
KeywordsDoc.py
```

---

## 📦 Dépendances

L’application doit être exécutée dans un environnement virtuel Python contenant les dépendances suivantes :

```python
import os
import re
import sys
import json
import subprocess
import tkinter as tk
from tkinter import StringVar
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageDraw, ImageFont
from collections import OrderedDict
import html2text
from AnimatedLabel import AnimatedLabel
```

### Dépendances externes principales

* **customtkinter**
* **Pillow (PIL)**
* **html2text**

---

## 🐍 Environnement virtuel (venv)

Un script minimal est fourni pour créer un environnement virtuel cohérent avec le projet.

### Script : `install_kdoc_venv.sh`

```bash
python3.10 -m venv kdoc_venv
source ~/rf_keywords_doc/kdoc_venv/bin/activate
```

> ⚠️ Ce script est volontairement minimal. L’utilisateur reste libre de l’utiliser ou non, mais il constitue une base cohérente avec les requirements du projet.

---

## 🚀 Installation

1. Cloner le dépôt :

```bash
git clone https://github.com/<votre-utilisateur>/robotFrameworkCompleteDoc.git
cd robotFrameworkCompleteDoc
```

2. Créer et activer l’environnement virtuel :

```bash
bash install_kdoc_venv.sh
```

3. Installer les dépendances nécessaires (exemple) :

```bash
pip install customtkinter pillow html2text
```

> Selon votre système, Tkinter peut nécessiter une installation séparée (ex: `python3-tk` sur certaines distributions Linux).

---

## ▶️ Lancement de l’application

Une fois l’environnement activé :

```bash
python KeywordsDoc.py
```

---

## 🖥️ Compatibilité

* Linux : ✅ testé
* Windows : ⚠️ non testé
* macOS : ⚠️ non testé

L’interface repose sur Tkinter ; la compatibilité dépend donc du support Tk de la plateforme.

---

## 📚 Cas d’usage

* Développeurs et testeurs Robot Framework
* Consultation rapide des keywords sans navigateur
* Travail hors-ligne
* Support à l’écriture de tests automatisés

---

## 🛠️ État du projet

* Projet fonctionnel
* Évolutions possibles :

  
  * Indexation dynamique des librairies
  * Thèmes graphiques supplémentaires

---

## 📄 Licence

À définir.

---

## 👤 Auteur

Projet développé dans un objectif d’outillage avancé autour de Robot Framework par Sébastien Dethyre.

---

## 🤝 Contributions

Les contributions, suggestions et retours sont les bienvenus.  
N’hésitez pas à ouvrir une issue ou une pull request.
