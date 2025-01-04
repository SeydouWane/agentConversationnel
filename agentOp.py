from flask import Flask, request, jsonify, render_template
import openai
import PyPDF2
import os
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Vérification de la clé API
if not openai.api_key:
    raise ValueError("Aucune clé API OpenAI trouvée. Vérifiez votre fichier .env.")

# Dossiers contenant les fichiers PDF pour chaque chapitre
base_path = "Dossiers"
modules = {
    "Chap 1": os.path.join(base_path, "Chap 1"),
    "Chap 2": os.path.join(base_path, "Chap 2"),
    "Chap 3": os.path.join(base_path, "Chap 3"),
    "Chap 4": os.path.join(base_path, "Chap 4")
}

def extraire_texte_depuis_dossier(dossier):
    texte_complet = ""
    try:
        fichiers_pdf = [f for f in os.listdir(dossier) if f.endswith('.pdf')]
        for fichier in fichiers_pdf:
            chemin_fichier = os.path.join(dossier, fichier)
            with open(chemin_fichier, "rb") as pdf_file:
                lecteur_pdf = PyPDF2.PdfReader(pdf_file)
                for page in lecteur_pdf.pages:
                    texte_complet += page.extract_text() or ""
    except Exception as e:
        return f"Erreur lors de l'extraction : {str(e)}"
    return texte_complet if texte_complet else "Aucun texte extrait."




def extraire_points_importants_avec_clustering(dossier):
    """Utilisation de clustering pour regrouper et résumer les points clés."""
    texte_complet = extraire_texte_depuis_dossier(dossier)
    phrases = texte_complet.split('.')
    if len(phrases) < 5:
        return phrases  # Retour direct si peu de texte

    try:
        french_stop_words = stopwords.words('french')
        vectorizer = TfidfVectorizer(stop_words=french_stop_words)
        X = vectorizer.fit_transform(phrases)
        nltk.download('stopwords')


        # Clustering K-Means pour regrouper les idées similaires
        num_clusters = min(5, len(phrases))
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        kmeans.fit(X)

        # Sélectionner une phrase représentative par cluster
        centroids = kmeans.cluster_centers_
        labels = kmeans.labels_
        points_clés = []
        for i in range(num_clusters):
            index_cluster = [j for j in range(len(labels)) if labels[j] == i]
            points_clés.append(phrases[index_cluster[0]])

    except Exception as e:
        return [f"Erreur lors du traitement : {str(e)}"]

    return points_clés


def generer_reponse_llm(contenu, question):
    """Génère une réponse uniquement si la question est liée au module sélectionné."""
    try:
        prompt = f"Le contenu du cours est : {contenu}\n\nQuestion : {question}\nRéponds uniquement si la question est liée au contenu du module."
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant pédagogique bienveillant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Erreur API : {str(e)}"

@app.route('/')
def home():
    """Page d'accueil."""
    return render_template('index.html')

@app.route('/get_points/<module>', methods=['GET'])
def get_points(module):
    """Afficher les points clés d'un chapitre sélectionné."""
    if module not in modules:
        return jsonify({"Erreur": "Module non valide."})

    points = extraire_points_importants_avec_clustering(modules[module])
    return jsonify({"Points clés": points})


@app.route('/ask_question', methods=['POST'])
def ask_question():
    """Répond uniquement si la question est pertinente pour le module choisi."""
    data = request.json
    module = data.get("module")
    question = data.get("question")

    if module not in modules:
        return jsonify({"Erreur": "Module non valide."})

    # Extraction du texte du module sélectionné
    texte_complet = extraire_texte_depuis_dossier(modules[module])
    
    # Vérification si du texte a bien été extrait
    if not texte_complet.strip():
        return jsonify({"Erreur": "Aucun texte extrait pour ce module."})

    # Générer la réponse avec le contenu extrait
    reponse = generer_reponse_llm(texte_complet, question)
    return jsonify({"Réponse": reponse})

if __name__ == '__main__':
    app.run(debug=True)
