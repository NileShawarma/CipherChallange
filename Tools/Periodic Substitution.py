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

        partitions = seperators(text,len(alphabets))

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

        partitions = seperators(text,len(alphabets))

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
def seperators(string: str,keyLength: int) -> list:
    newArray = ["" for i in range(keyLength)]

    for index in range(keyLength):
        newArray[index] = string[index::keyLength]
    return newArray
def sinkov(string,min_period=1, max_period=30):
    ENGLISH_IOC = 0.0667
    IoC_variances = {}
    
    best_key = 1
    best_variance = float("inf")

    for period in range(min_period,max_period+1):
        partitions = seperators(string,period)
        total_IoC = sum([cipherTools.ic(partition) for partition in partitions])
        avg_IoC = total_IoC/len(partitions)

        IoC_variance = ENGLISH_IOC-avg_IoC
        
        IoC_variances[str(period)] = abs(IoC_variance)
        
        if abs(IoC_variance)<best_variance:
            best_key = period
            best_variance = abs(IoC_variance)
    sorted_variances = (sorted(IoC_variances.items(), key=lambda thingy: thingy[1]))
    return {"key" : best_key, "full_data" : sorted_variances}


