import streamlit as st
from googletrans import Translator
from textblob import TextBlob


# --- Fonctions de logique métier (inchangées ou légèrement ajustées) ---

# Adjusted chatbot_conversation to be compatible with Gradio's output
# It will return a string to be displayed, rather than using print/input directly.
def chatbot_conversation_gradio():  # Renommée pour éviter la confusion avec Streamlit
    conversation_output = "Chatbot: Bonjour\n"
    conversation_output += "Chatbot: ça va ?\n"
    conversation_output += "Chatbot: Génial!\n"  # Simulating a "bien" response for demonstration
    conversation_output += "Chatbot: Merci pour ta réponse.\n"
    conversation_output += "Chatbot: Je vais te poser quelques questions pour t’aider dans votre orientation !"
    return conversation_output


def demander_notes(branche):
    # Cette fonction n'est pas utilisée directement dans l'interface Streamlit interactive.
    # Les entrées de notes sont gérées par les widgets Streamlit.
    return 0, 0, 0, 0


def calculer_moyenne(note1, note2, note3, note4):
    return (note1 + note2 + note3 + note4) / 4


def afficher_message(moyenne, branche):
    # Cette fonction n'est pas utilisée directement dans l'interface Streamlit.
    # Le message est retourné par gradio_interface (renommée orientation_interface).
    if moyenne >= 10:
        print(f"Félicitations ! Votre moyenne de {moyenne:.2f} montre que vous avez fait un bon choix en {branche}.")
    else:
        print(
            f"Votre moyenne de {moyenne:.2f} est en dessous de 10. Peut-être devriez-vous réfléchir à votre choix de branche.")


def choice():
    # Cette fonction est pour une utilisation en console, pas pour l'interface Streamlit.
    pass


# Fonction principale pour la logique d'orientation (ex-gradio_interface)
def orientation_interface(branche, note1, note2, note3, note4):
    # Validation de la branche (même logique que votre original)
    if branche not in ["Sciences", "Lettres", "Économie et services", "Technologie de l'informatique"]:
        return "Branche invalide"

    # Validation des notes
    if all(isinstance(n, (int, float)) and 0 <= n <= 20 for n in [note1, note2, note3, note4]):
        moyenne = calculer_moyenne(note1, note2, note3, note4)

        if moyenne >= 10:
            return f"Félicitations ! Votre moyenne de {moyenne:.2f} montre que vous avez fait un bon choix en {branche}."
        else:
            return f"Votre moyenne de {moyenne:.2f} est en dessous de 10. Peut-être devriez-vous réfléchir à votre choix de {branche}."
    else:
        return "Les notes doivent être comprises entre 0 et 20."


# Fonction d'analyse de satisfaction (synchronisée pour Streamlit)
def analyze_satisfaction(satisfaction_text):
    if not satisfaction_text.strip():
        return "Veuillez écrire votre avis."

    translator = Translator()

    try:
        # Les méthodes de googletrans sont généralement synchrones
        detected_lang_obj = translator.detect(satisfaction_text)
        detected_lang = detected_lang_obj.lang
        # st.write(f"Langue détectée: {detected_lang}") # On peut afficher ceci dans le terminal ou un st.expander si nécessaire

        if detected_lang != 'en':
            translated_obj = translator.translate(satisfaction_text, dest='en')
            translated_text = translated_obj.text
            # st.write(f"Texte original: '{satisfaction_text}' -> Texte traduit (EN): '{translated_text.lower()}'")
        else:
            translated_text = satisfaction_text

        analysis = TextBlob(translated_text).lower()
        polarity = analysis.sentiment.polarity

        # --- SEUILS AJUSTÉS ---
        # Utilisation de 'in' pour une vérification de mot plus robuste
        translated_text_lower = translated_text.lower()

        if polarity > 0 or "alright" in translated_text_lower:
            return f"Avis = Positif: Merci beaucoup pour votre avis positif ! Nous sommes ravis d’avoir pu vous aider dans votre orientation scolaire."
        elif polarity < 0 or "dissatisfied" in translated_text_lower or "unattended" in translated_text_lower or "not well" in translated_text_lower or "mal" in translated_text_lower:
            return f"Avis = Négatif: Nous sommes désolés d’apprendre que votre expérience n’a pas répondu à vos attentes, nous continuerons à travailler dur pour vous offrir la meilleure expérience possible."
        else:
            return f"Avis = Neutre: Nous comprenons votre neutralité, nous continuerons à travailler dur pour vous offrir la meilleure expérience possible."

    except Exception as e:
        st.error(f"Erreur lors de l'analyse de sentiment: {e}")  # Affichage d'erreur dans Streamlit
        return "**Polarité : Neutre** (Analyse impossible ou erreur de connexion)"


# Fonction pour obtenir les labels des matières dynamiquement
def get_note_labels(branche):
    if branche == "Sciences":
        return "Note en Mathématiques", "Note en Physique", "Note en Sciences de la Vie et de la Terre", "Note en Technique"
    elif branche == "Lettres":
        return "Note en Français", "Note en Arabe", "Note en Histoire", "Note en Géographie"
    elif branche == "Économie et services":
        return "Note en Mathématiques", "Note en Anglais", "Note en Histoire", "Note en Géographie"
    elif branche == "Technologie de l'informatique":
        return "Note en Mathématiques", "Note en Informatique", "Note en Physique", "Note en Technique"
    else:
        return "Note en Matière 1", "Note en Matière 2", "Note en Matière 3", "Note en Matière 4"


# --- Interface Streamlit ---

# Configuration de la page
st.set_page_config(layout="centered", page_title="OrientBot")

st.markdown("# 🤖🎓OrientBot: Ton avenir commence ici.")

# Section "Orientation Scolaire"
st.header("Orientation Scolaire")
st.markdown("Entrez vos notes pour obtenir des conseils sur votre choix de branche.")

branches = ["Sciences", "Lettres", "Économie et services", "Technologie de l'informatique"]

# Selectbox pour le choix de la branche
selected_branch = st.selectbox(
    label="Sélectionnez votre Branche",
    options=branches,
    index=0  # Défaut à "Sciences"
)

# Obtenir les labels dynamiques en fonction de la branche sélectionnée
note_labels = get_note_labels(selected_branch)

# Utilisation de colonnes pour une meilleure mise en page des notes
col1, col2 = st.columns(2)
with col1:
    note1 = st.number_input(label=note_labels[0], min_value=0.0, max_value=20.0, value=10.0, step=0.1, key="note1")
    note3 = st.number_input(label=note_labels[2], min_value=0.0, max_value=20.0, value=10.0, step=0.1, key="note3")
with col2:
    note2 = st.number_input(label=note_labels[1], min_value=0.0, max_value=20.0, value=10.0, step=0.1, key="note2")
    note4 = st.number_input(label=note_labels[3], min_value=0.0, max_value=20.0, value=10.0, step=0.1, key="note4")

# Bouton de calcul
if st.button("Calculer la moyenne"):
    resultat_orientation = orientation_interface(selected_branch, note1, note2, note3, note4)
    st.subheader("Résultat de l'Orientation :")
    st.markdown(resultat_orientation)

st.markdown("---")  # Séparateur visuel

# Section "Votre avis nous intéresse !"
st.subheader("Votre avis nous intéresse !")
satisfaction_text_input = st.text_area(
    label="Veuillez écrire votre avis sur le résultat (par exemple, 'Satisfait', 'Insatisfait', ou d'autres commentaires).",
    height=100,
    placeholder="Écrivez votre avis ici..."
)

# Bouton de soumission de l'avis
if st.button("Soumettre l'avis"):
    analyse_resultat = analyze_satisfaction(satisfaction_text_input)
    st.subheader("Analyse de l'avis :")
    st.markdown(analyse_resultat)