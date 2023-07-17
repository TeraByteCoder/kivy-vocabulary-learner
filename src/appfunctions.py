# -*- coding: utf-8 -*-


import string
import time
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from mtranslate import translate
import os
import random
import requests
import openai

retries = 0

nltk.data.path.append(os.path.join(os.path.dirname(__file__), "nltk_data"))

def remove_punctuation(word):
    punctuation_removed = word.translate(str.maketrans('', '', string.punctuation))
    return punctuation_removed


def text_to_words(text):
    try:
        # Initialisiere den Lemmatizer
        stemmer = SnowballStemmer('norwegian')

        # Tokenisiere den Text in Wörter
        words = word_tokenize(text, language='norwegian')

        # Liste zum Speichern der bereinigten eindeutigen Wörter
        unique_words = set()

        # Entferne die Satzzeichen, bringe die Wörter in ihre Grundform und wandele sie in Kleinbuchstaben um
        for word in words:
            cleaned_word = remove_punctuation(word)
            lemma = stemmer.stem(cleaned_word.lower())
            unique_words.add(lemma)

        # Überprüfe, ob die Datei bereits existiert und lade vorhandene Wörter
        existing_words = set()
        if os.path.exists("save/words.txt"):
            with open("save/words.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        word, _ = line.split(" : ")
                        existing_words.add(word)

        # Öffne die Datei im Anhangmodus und schreibe neue eindeutige Wörter
        with open("save/words.txt", "a", encoding="utf-8") as f:
            for word in unique_words:
                if word.strip() and word not in existing_words:
                    f.write(f"{word} : {translate_word_internet(word)}\n")

        print("Die eindeutigen Wörter wurden erfolgreich in die Datei 'words.txt' geschrieben.")

    except LookupError:
        global retries
        if retries == 2:
            quit()
        nltk.download('punkt')
        retries = retries + 1
        text_to_words()


def translate_word_internet(word):
    translation = translate(word, 'de', 'no')
    return translation


def lese_zeile(dateiname, zeilennummer):
    with open(dateiname, 'r') as datei:
        zeilen = datei.readlines()

        if zeilennummer >= 1 and get_zeilenanzahl(dateiname) > zeilennummer:
            zeile = zeilen[zeilennummer - 1]
            return zeile.rstrip()
        else:
            return "Ungültige Zeilennummer"


def get_zeilenanzahl(dateiname):
    with open(dateiname, 'r') as datei:
        zeilen = datei.readlines()
        anzahl_zeilen = len(zeilen)
    return anzahl_zeilen


def pick_words_to_learn():
    lines = []
    anzahl_zeilen = get_zeilenanzahl("save/words.txt")
    amount = 0
    while amount <= 20:
        result = random.randint(1, anzahl_zeilen)
        if result not in lines and not(string_in_datei(dateiname="save/done_words.txt", suchstring=(lese_zeile(dateiname="save/words.txt", zeilennummer=result)))):
            lines.append(result)
            print(result)
        amount = (len(lines))
    with open('save/currently_learning.txt', 'w') as t_to:
        for i in lines:
            zeile=lese_zeile('save/words.txt', i)
            if zeile != "Ungültige Zeilennummer":
                t_to.write(f"{zeile} : 0 \n")


def get_word_data(line = 1, filename = "save/currently_learning.txt"):
        zeile = lese_zeile(filename, line)
        values = zeile.strip().split(':')
        norwegian = values[0].strip()
        german = values[1].strip()
        streak = values[2].strip()

        return norwegian, german, streak


def string_in_datei(dateiname, suchstring):
    try:
        with open(dateiname, 'r') as file:
            for zeile in file:
                if suchstring in zeile:
                    return True
            return False
    except FileNotFoundError:
        print(f"Die Datei '{dateiname}' wurde nicht gefunden.")
        return False


def delete_specific_line(filename="save/currently_learning.txt", line_number=None):
    lines = []
    # Read the file content
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Check if the line number is valid
    if line_number < 1 or line_number > len(lines):
        print("Invalid line number.")
        return

    # Remove the desired line
    del lines[line_number - 1]

    # Write the updated content back to the file
    with open(filename, 'w') as file:
        file.writelines(lines)



def write_to_specific_line(filename="save/currently_learning.txt", line_number=None, new_content=None):
    # Datei öffnen und den Inhalt lesen
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Überprüfen, ob die angegebene Zeilennummer gültig ist
    if line_number < 1 or line_number > len(lines):
        print("Ungültige Zeilennummer.")
        return

    # Die gewünschte Zeile mit dem neuen Inhalt überschreiben
    lines[line_number - 1] = new_content + '\n'

    # Den aktualisierten Inhalt zurück in die Datei schreiben
    with open(filename, 'w', encoding='utf-8') as file:
        file.writelines(lines)



def check_if_correct(line, eingabe, direction):
    no, de, streak = get_word_data(line)
    streak = int(streak)
    print(f"no:{no}, de: {de}, sreak: {streak}, eingabe: {eingabe}")
    if (de.lower() == str(eingabe).lower() and direction == "node") or (no.lower() == str(eingabe.lower()) and direction == "deno"):
        streak = streak + 1
        correct = True
    else:
        streak = 0
        correct = False
    if streak >= 5:
        with open("save/done_words.txt", "a") as f:
            f.write(f"{no} : {de} \n")
        delete_specific_line(filename="save/currently_learning.txt", line_number=line)  # Pass filename and line_number arguments

    else:
        new_content = f"{no} : {de} : {streak}"
        write_to_specific_line(filename="save/currently_learning.txt", line_number=line, new_content=new_content)  # Pass filename, line_number, and new_content arguments
    return correct,



def pick_next_word(direction=None, zeile=None):
    try:
        zeilen = get_zeilenanzahl("save/currently_learning.txt") - 1
        zeile = random.randint(1, zeilen)
        direction = random.randint(0, 1)
        if direction == 1:
            direction = "node"
        else:
            direction = "deno"
        return direction, zeile
    except ValueError:
        pick_words_to_learn()
        zeilen = get_zeilenanzahl("save/currently_learning.txt") - 1
        zeile = random.randint(1, zeilen)
        direction = random.randint(0, 1)
        if direction == 1:
            direction = "node"
        else:
            direction = "deno"
        return direction, zeile

def getsettings(setting=None):
    with open("save/settings.txt", "r") as f:
        for i in f:
            print(i)
            if i.startswith("applanguage:"):
                lang = i.strip("applanguage: ")
    return i
getsettings(1)
import json
with open(f'lang/{"en"}.json') as file:
    data = json.load(file)
    print(data)
print(data.get("main_window", {}).get("title", ''))