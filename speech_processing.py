import speech_recognition as sr
import spacy

def capture_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        # Convert audio to text
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError:
        print("Could not request results; check your internet connection")
        return ""
    
# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)
    entities = {
        "location": [],
        "rating": [],
        "beds": []
    }
    for ent in doc.ents:
        if ent.label_ == "GPE":  # Geopolitical entity (likely location)
            entities["location"].append(ent.text)
        elif ent.label_ == "CARDINAL":  # Cardinal number (for beds or rating)
            entities["beds"].append(ent.text)
        elif ent.label_ == "ORDINAL" or ent.label_ == "QUANTITY":  # (Rating example)
            entities["rating"].append(ent.text)
    return entities

def process_voice_input():
    text = capture_audio()
    if text:
        entities = extract_entities(text)
        print("Extracted entities:", entities)
        return entities
    return {}

if __name__ == "__main__":
    process_voice_input()


