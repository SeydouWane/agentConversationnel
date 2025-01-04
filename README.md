# Agent Conversationnel

Ce projet est un **chatbot éducatif** développé avec Flask et OpenAI, capable de répondre aux questions des utilisateurs sur des modules de leadership à partir de fichiers PDF.

## 🚀 Fonctionnalités
- **Interaction par Chatbot** : Répondre aux questions des utilisateurs sur des modules de cours spécifiques.
- **Extraction de texte depuis des fichiers PDF** : Utilisation de `PyPDF2` pour extraire le contenu des fichiers PDF.
- **Résumé des points clés** : Utilisation de `scikit-learn` et `KMeans` pour extraire des points clés des modules.
- **Intégration de l'API OpenAI** : Génération de réponses pédagogiques basées sur le contenu des modules.
- **Interface Web** : Interface conviviale développée avec Flask et un frontend en HTML/CSS.

---

## 📦 Installation
1. **Cloner le dépôt :**
    ```bash
    git clone https://github.com/SeydouWane/agentConversationnel.git
    cd agentConversationnel
    ```

2. **Créer un environnement virtuel et l'activer :**
    ```bash
    python -m venv .venv
    .venv\Scripts\activate  # Windows
    source .venv/bin/activate  # macOS/Linux
    ```

3. **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configurer l'API Key OpenAI :**
    - Créer un fichier `.env` à la racine avec le contenu suivant :
    ```plaintext
    OPENAI_API_KEY= mettre le clé API sur github n'est pas autorisé
    ```
    ⚠️ **Ne partagez jamais votre clé API publiquement.**

5. **Lancer l'application Flask :**
    ```bash
    python agentOp.py
    ```
    L'application sera accessible à : `http://127.0.0.1:5000`

---

## 📊 Dossiers du projet
- `Dossiers` : Contient les fichiers PDF utilisés pour chaque module.
- `static/css` : Fichiers CSS pour le style de l'interface.
- `templates` : Contient le fichier `index.html` pour l'interface utilisateur.
- `agentOp.py` : Script principal contenant la logique Flask.

---

## 🔧 Dépendances principales
- Flask
- PyPDF2
- scikit-learn
- OpenAI
- dotenv

---

## 📈 Améliorations futures
- [ ] Ajouter une gestion avancée des erreurs.
- [ ] Implémenter un historique des conversations.
- [ ] Optimisation de l'extraction des points clés.

---

## 📜 Licence
Ce projet est sous licence UNCHK_BDA.

---

## 🤝 Contribution
Les contributions sont les bienvenues ! Veuillez ouvrir une `issue` ou une `pull request`.

---

## 📧 Contact
- **Développeur** : [Seydou Wane](https://github.com/SeydouWane)
- **Email** : [seydou@example.com](mailto:papaseydou.wane@unchk.edu.sn)

---

**Merci d'utiliser le chatbot éducatif !** 🎓

