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
    sorted_word_list = sorted(set(word_list))

    vocabulary = {}

    for word in sorted_word_list:
        dictItem = get_vocabItem(word)
        if dictItem:
            for key, value in dictItem.items():
                vocabulary[key] = value

    return jsonify(vocabulary)

def get_vocabItem(word):

    vocabItem = {}
    url = f"https://www.wordreference.com/ites/{word}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    word_elem = soup.find('h3', {'class': 'headerWord'})
    translation_elem = soup.find('li', {'class': 'sense'})

    if word_elem is not None and translation_elem is not None:
        word_elem = word_elem.get_text().strip()
        translation_elem = translation_elem.get_text().strip()
        translation_elem = translation_elem.split(";")[:3]
        translation_elem = ";".join(translation_elem)
        translation_elem = translation_elem.replace(",", "/")
        vocabItem[word_elem] = translation_elem
        return vocabItem
    else:
        return 
        

if __name__ == '__main__':
    app.run(debug=True)
