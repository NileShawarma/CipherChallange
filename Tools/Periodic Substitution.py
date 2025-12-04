import os
import string
import sys

script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","Test","Modules")
sys.path.append(modulesPath)

import cipherTools

class Periodic_Substitution():
    def __init__(self):
        self.alphabets = []
        self.raw_string = "hello this is a dummy message, what's your thoughts on pancakes"
        self.IoC = cipherTools.IoC()
    def add_alphabet(self,alphabet):
        self.alphabets.append(alphabet)
    def clear(self):
        self.alphabets = []
    
    def encrypt(self, text = None):
        if text == None:
            text = self.raw_string
        
        text = "".join([char if char.isalpha() else "" for char in text.upper()])

        alphabets = self.alphabets
        if len(alphabets)==0:
            alphabets = [string.ascii_uppercase]

        text = text + "-"*(len(alphabets)-len(text)%len(alphabets))

        partitions = cipherTools.column_seperation(text,len(alphabets))

        ALPHABET = string.ascii_uppercase
        plaintext_parts = []
        for index,partition in enumerate(partitions):
            plaintext = ""
            encryption_map = {p: c for p, c in zip(ALPHABET, alphabets[index])}

            for char in partition:
                if char in encryption_map:
                    plaintext+= encryption_map[char]
                else:
                    plaintext += char
            plaintext_parts.append(plaintext)
        
        plaintext = ""
        for index in range(len(text)//len(plaintext_parts)):
            for part_index in range(len(plaintext_parts)):
                plaintext+=plaintext_parts[part_index][index]
        return plaintext
    def decrypt(self, text = None):
        if text == None:
            text = self.raw_string
        
        text = "".join([char if char.isalpha() else "" for char in text.upper()])

        alphabets = self.alphabets
        if len(alphabets)==0:
            alphabets = [string.ascii_uppercase]

        text = text + "-"*(len(alphabets)-len(text)%len(alphabets))

        partitions = cipherTools.column_seperation(text,len(alphabets))

        ALPHABET = string.ascii_uppercase
        plaintext_parts = []
        for index,partition in enumerate(partitions):
            plaintext = ""
            encryption_map = {c: p for p, c in zip(ALPHABET, alphabets[index])}

            for char in partition:
                if char in encryption_map:
                    plaintext+= encryption_map[char]
                else:
                    plaintext += char
            plaintext_parts.append(plaintext)
        
        plaintext = ""
        for index in range(len(text)//len(plaintext_parts)):
            for part_index in range(len(plaintext_parts)):
                plaintext+=plaintext_parts[part_index][index]
        return plaintext



