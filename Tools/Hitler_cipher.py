import os
import string
import sys

script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","Test","Modules")
sys.path.append(modulesPath)

import cipherTools

class GOD_cipher():
    def __init__(self):
        self.alphabets = {
            "A" : "E C D B A F J I G H L K O N M S P Q T R Z U X V W Y",
            "B" : "B A D C F G E I H J N O K M L S R P T Q W X V Y U Z",
            "C" : "C D A B G H E J F I K M P O L N T R Q S X U Z V W Y",
            "D" : "B A C H D J F E G I L O N P K M S Q R U Z T Y V W X",
            "E" : "A C D B H J F I G E M N L K O T R S P Q Y Z V U X W",
            "F" : "W Y Z V X A B C E F D H J I G K M P L N S R O Q U T",
            "G" : "V Y X U Z W C A B E D I H G F L K N M J Q O T P S R",
            "H" : "U X Z W Y V A E B C F D I H G J N K M L S P O R T Q",
            "I" : "X U V Z Y W A C B E D G I H J F K M O N L T R Q S P",
            "K" : "S Q R Y V X U Z T W B D C A E J H K I F G P M O N L",
            "L" : "R T S W V Y Z U X F A C B E D J K I G H O N M P Q L",
            "M" : "T R S Q Y W X Z V U E B A C D K F J I G H M L N P O",
            "N" : "R Q P S Z W T V U X Y D B C A G I E J H K F O N L M",
            "O" : "L O P N M Q S R T U V Z X Y W C A B H E D G J F K I",
            "P" : "M O L N P S R Q X T Y W Z U V A D C B H F I K E J G",
            "R" : "P O N M R T S Q W Y U X Z V C A B E D F J G K H I L",
            "S" : "L M O N T Q R P S Z X U Y V W B A C D E G J H F K I",
            "T" : "M O K N L Q S R P W Z T V U X Y D B A C E F J G I H",
            "U" : "H F I G N M J K O L Q P S R V T Z U W X Y B E D C A",
            "V" : "E D I G H F L M K P O N R Q J S U X T Z W V Y C A B",
            "W" : "I E H F G L O M J K N Q P T R S X V Y U Z W B A D C",
            "Z" : "I F H J G N K L M P O T S R Q V Y U X Z W D B C A E",
        }
        for i in self.alphabets:
            self.alphabets[i] = self.alphabets[i].replace(" ","")

        self.raw_string = "hello this is a dummy message, what's your thoughts on pancakes"
    def add_alphabet(self,alphabet):
        self.alphabets.append(alphabet)
    def clear(self):
        self.alphabets = []
    
    def encrypt(self, key, text = None):
        if text == None:
            text = self.raw_string
        
        text = "".join([char if char.isalpha() else "" for char in text.upper()])

        alphabets = []

        for char in key.upper():
            alphabets.append(self.alphabets[char])

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
    def decrypt(self, key, text = None):
        if text == None:
            text = self.raw_string
        
        text = "".join([char if char.isalpha() else "" for char in text.upper()])

        alphabets = []

        for char in key.upper():
            alphabets.append(self.alphabets[char])
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
    def auto_solve_crib(self, crib, period=None, text = None):
        if text == None:
            text = self.raw_string

        text = "".join([char if char.isalpha() else "" for char in text.upper()])

        if period == None:
            period = sinkov(text,1,12)
        
        possible_alphas = []
        for i in range(len(text)-len(crib)+1):
            alphabets = ["-"*26 for i in range(period)]

            substr = text[i:i+len(crib)]
            seq_invalid = False

            for letter_pos in range(len(substr)):
                substr_letter = substr[letter_pos].upper()
                crib_letter = crib[letter_pos].upper()
                current_alpha_pos = i%period
                current_alpha = alphabets[current_alpha_pos]

                crib_letter_num = ord(crib_letter)-65

                if current_alpha[crib_letter_num]!="-":
                    seq_invalid = True
                    break        
                else:
                    alphabets[current_alpha_pos] = substr_letter
            if not seq_invalid:
                possible_alphas.append(alphabets)
                
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

cipher = GOD_cipher()
print(sinkov("JROQLDBCVZTQRSGMXQHHZGESKLOSOTLOHEIFZOFOYJLENIFTHQFFBPHOHFCFDUSFDNKBGQLZBDIRHMKXTMDQSQYELDBHRYCHEFJRMTFCJCXRBUGTRCTHCVBSQJWEUIGNJWOWQCUYIHGPJPMFLYQJPNBTMHMXXTBEOSQYPMDCXFNIFUOMXSBMWGUIXMCHIGNXMCCHCVZQIVDRWUBMWKLKOIFUABDYQIVSHPVFBZAFVOQQUHPPGOBEBFFRLWCBOFUFDUSFDNKBGASPGOIVQJCLEIHVFFCLWHQJRI",1,12))
print(cipher.decrypt("martian","TNMPHRVYTPVYXRPXPANIZWMXPXJZTTSMSECQUPBBATTRRNXTHZADCYOJLIWTYRVYCXXJOJGIPCVKKIRRBYBHZGNZLSACRQLIORPNCCUASYTNBBCZQGVMHWZTQFRGWHDNSEYECQGVNYASAGSRNDVTKXLHJZGIRTXNTHESLJFHZASXZT"))

