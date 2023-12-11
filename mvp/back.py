from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    txt = data.get("text")
    if not txt:
        return jsonify({"error": "No text provided"}), 400

    word_list = txt.split()
    sorted_word_list = sorted(set(word_list))  # Remove duplicates and sort unique words

    vocabulary = {}

    for word in sorted_word_list:
        translation = get_translation(word)
        word = get_word(word)
        if translation:
            translation = translation.split(";")[:3]
            translation = ";".join(translation)
            translation = translation.replace(",", "/")
            vocabulary[word] = translation

    return jsonify(vocabulary)

def get_word(word):
    url = f"https://www.wordreference.com/ites/{word}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    word_elem = soup.find('h3', {'class': 'headerWord'})
    if word_elem:
        return word_elem.get_text().strip()
    else:
        return None

def get_translation(word):
    url = f"https://www.wordreference.com/ites/{word}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    translation_elem = soup.find('li', {'class': 'sense'})
    if translation_elem:
        return translation_elem.get_text().strip()
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
