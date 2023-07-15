# -*- coding: utf-8 -*-

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import appfunctions
import time

kivy.require('1.9.0')
zeile = 0
direction = 0
firsttime = True


class HomeScreen(Screen):
    pass


class Lesson(Screen):

    def pick_next_word(self):
        global direction, zeile
        returned = appfunctions.pick_next_word(direction, zeile)
        direction, zeile = returned

    def submit(self):
        global direction, zeile, firsttime
        if not firsttime:
            no, de, streak = appfunctions.get_word_data(zeile)
            eingabe = self.ids.userinput.text
            ergaebnis = appfunctions.check_if_correct(zeile, eingabe, direction)
            ergaebnis=ergaebnis[0]
            print(ergaebnis)
            print(type(ergaebnis))
            if ergaebnis is True:
                self.ids.correct_word.text = "Richtig"
                print("lol")

            if ergaebnis is False:
                print("lolo")
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


class SettingScreen(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("language_learning.kv")


class Lern_App(App):
    def build(self):
        return kv


if __name__ == '__main__':
    Lern_App().run()
