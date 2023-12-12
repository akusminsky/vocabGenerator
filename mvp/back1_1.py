from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/italiano', methods=['POST'])
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

@app.route('/hebreo', methods=['POST'])
def get_hebrew():
    data = request.get_json()
    txt = data.get("text")
    if not txt:
        return jsonify({"error": "No text provided"}), 400

    word_list = txt.split()
    sorted_word_list = sorted(set(word_list))

    vocabulary = {}

    for word in sorted_word_list:
        dictItem = trad_hebrew(word)
        if dictItem:
            for key, value in dictItem.items():
                vocabulary[key] = value

    return jsonify(vocabulary)


def trad_hebrew(word):
    vocabItem = {}
    url = f"https://www.morfix.co.il/{word}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    word_elem = soup.find('span', {'class': 'Translation_spTop_heToen'})
    translation_elem = soup.find('div', {'class': 'normal_translation_div'})

    if word_elem is not None and translation_elem is not None:
        word_elem = word_elem.get_text().strip()
        translation_elem = translation_elem.get_text().strip()
        vocabItem[word_elem] = translation_elem
        
        return vocabItem
    else:
        return
    
@app.route('/ingles', methods=['POST'])
def get_en():
    data = request.get_json()
    txt = data.get("text")
    if not txt:
        return jsonify({"error": "No text provided"}), 400

    word_list = txt.split()
    sorted_word_list = sorted(set(word_list))

    vocabulary = {}

    for word in sorted_word_list:
        dictItem = trad_en(word)
        if dictItem:
            for key, value in dictItem.items():
                vocabulary[key] = value

    return jsonify(vocabulary)


def trad_en(word):
    vocabItem = {}
    url = f"https://www.wordreference.com/es/translation.asp?tranword={word}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    word_elem = soup.find('h3', {'class': 'headerWord'})
    translation_elem = soup.find_all('em', {'data-lang': 'es'})

    trans_list = list()
    if word_elem is not None and translation_elem is not None:
        for i in translation_elem[0:2]:
            i = i.parent
            i = i.get_text().strip()
            trans_list.append(i)

        word_elem = word_elem.get_text().strip()
        vocabItem[word_elem] = trans_list
        
        return vocabItem
    else:
        return
    
@app.route('/frances', methods=['POST'])

def get_fr():
    data = request.get_json()
    txt = data.get("text")
    if not txt:
        return jsonify({"error": "No text provided"}), 400

    word_list = txt.split()
    sorted_word_list = sorted(set(word_list))

    vocabulary = {}

    for word in sorted_word_list:
        dictItem = trad_fr(word)
        if dictItem:
            for key, value in dictItem.items():
                vocabulary[key] = value

    return jsonify(vocabulary)


def trad_fr(word):
    vocabItem = {}
    url = f"https://www.wordreference.com/fres/{word}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    word_elem = soup.find('h3', 'headerWord')
    translation_elem = soup.find_all('em', {'data-lang': 'es'})

    trans_list = list()
    if word_elem is not None and translation_elem is not None:
        for i in translation_elem[0:2]:
            i = i.parent
            i = i.get_text().strip()
            trans_list.append(i)

        word_elem = word_elem.get_text().strip()
        vocabItem[word_elem] = trans_list
        
        return vocabItem
    else:
        return

if __name__ == '__main__':
    app.run(debug=True)
