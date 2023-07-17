# -*- coding: utf-8 -*-

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
import appfunctions
import time
import json

kivy.require('1.9.0')
zeile = 0
direction = 0
firsttime = True

lang="en"
class HomeScreen(Screen):
    def get_text_from_json(self, key):
        global lang
        with open(f'lang/{lang}.json', encoding="utf-8") as file:
            data = json.load(file)
        return data.get("main_window", {}).get(key, '')


class Lesson(Screen):

    def pick_next_word(self):
        global direction, zeile
        returned = appfunctions.pick_next_word(direction, zeile)
        direction, zeile = returned

    def get_text_from_json(self, key):
        global lang
        with open(f'lang/{lang}.json', encoding="utf-8") as file:
            data = json.load(file)
        return data.get("study_window", {}).get(key, '')

    def submit(self):
        global direction, zeile, firsttime
        if not firsttime:
            no, de, streak = appfunctions.get_word_data(zeile)
            eingabe = self.ids.userinput.text
            ergaebnis = appfunctions.check_if_correct(zeile, eingabe, direction)
            ergaebnis = ergaebnis[0]
            print(ergaebnis)
            print(type(ergaebnis))
            if ergaebnis is True:
                self.ids.correct_word.text = "Richtig"

            if ergaebnis is False:
                if direction == 'deno':
                    self.ids.correct_word.text = f"Falsch, die richtige Übersetzung {de} wäre {no}."
                if direction == 'node':
                    self.ids.correct_word.text = f"Falsch, die richtige Übersetzung {no} wäre {de}."

        next_word = appfunctions.pick_next_word(direction=direction,
                                                zeile=zeile)  # Pass direction=direction and zeile=zeile arguments
        direction, zeile = next_word
        no, de, streak = appfunctions.get_word_data(zeile)
        if direction == "deno":  # "deno"
            self.ids.word_to_translate.text = de
        elif direction == "node":  # "node"
            self.ids.word_to_translate.text = no
        if firsttime:
            self.ids.nextbtn.text = "Überprüfen"
        firsttime = False
        self.ids.userinput.text = ""


class Input(Screen):
    def text_materialise(self):
        entered_text = self.ids.textinput.text
        appfunctions.text_to_words(entered_text)
    def get_text_from_json(self, key):
        global lang
        with open(f'lang/{lang}.json', encoding="utf-8") as file:
            data = json.load(file)
        return data.get("expandlist_window", {}).get(key, '')


class SettingScreen(Screen):
    def get_text_from_json(self, key):
        global lang
        with open(f'lang/{lang}.json', encoding="utf-8") as file:
            data = json.load(file)
        return data.get("settingswindow", {}).get(key, '')


class DictonaryMainScreen(Screen):
    def get_text_from_json(self, key):
        global lang
        with open(f'lang/{lang}.json', encoding="utf-8") as file:
            data = json.load(file)
        return data.get("dictionary_window", {}).get(key, '')


class DictonaryAllScreen(Screen):
    file_path = "save/words.txt"  # Passe den Dateipfad entsprechend an
    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    split_strings = file_content.split("\n")

    string1 = "Norwegisch\n\n"
    string2 = "Deutsch\n\n"

    for item in split_strings:
        split_item = item.split(" : ")
        if len(split_item) == 2:
            string1 += split_item[0] + "\n"
            string2 += split_item[1] + "\n"

    lines=len(string1.split("\n"))


    def get_text_from_json(self, key):
        global lang
        with open(f'lang/{lang}.json', encoding="utf-8") as file:
            data = json.load(file)
        return data.get("dictionaryall_window", {}).get(key, '')

class DictonaryLearningScreen(Screen):
    file_path = "save/currently_learning.txt"  # Passe den Dateipfad entsprechend an
    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    split_strings = file_content.split("\n")

    string1 = "Norwegisch\n\n"
    string2 = "Deutsch\n\n"
    string3 = "Streak\n\n"

    for item in split_strings:
        split_item = item.split(" : ")
        if len(split_item) == 3:
            string1 += split_item[0] + "\n"
            string2 += split_item[1] + "\n"
            string3 += split_item[2] + "\n"

    lines=len(string1.split("\n"))

    def get_text_from_json(self, key):
        global lang
        with open(f'lang/{lang}.json', encoding="utf-8") as file:
            data = json.load(file)
        return data.get("dictionarylearning_window", {}).get(key, '')

class DictonaryDoneScreen(Screen):
    file_path = "save/done_words.txt"  # Passe den Dateipfad entsprechend an
    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    split_strings = file_content.split("\n")

    string1 = "Norwegisch\n\n"
    string2 = "Deutsch\n\n"

    for item in split_strings:
        split_item = item.split(" : ")
        if len(split_item) == 2:
            string1 += split_item[0] + "\n"
            string2 += split_item[1] + "\n"

    lines=len(string1.split("\n"))

    def get_text_from_json(self, key):
        global lang
        with open(f'lang/{lang}.json', encoding="utf-8") as file:
            data = json.load(file)
        return data.get("dictionarydone_window", {}).get(key, '')

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("language_learning.kv")


class Lern_App(App):
    def build(self):
        return kv


if __name__ == '__main__':
    Lern_App().run()
