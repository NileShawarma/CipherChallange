from collections import Counter
import numpy
import os 
import math
import wordsegment
import random

RED = "\033[91m"
BLUE = "\033[1;36m"
MAGENTA = "\033[1;35m"
GREEN = "\033[1;32m"
RESET = "\033[0m"

wordsegment.load()

raw_freq_data = {}

for ngram in ["monograms","bigrams","trigrams","quadgrams"]:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","Data","ngrams",f"{ngram}.txt"), "r") as file:
        raw_freq_data[ngram] = {"TOTAL_VALUE":0}
        for line in file:
            data = line.split(" ")
            raw_freq_data[ngram][data[0]] = int(data[1])
            raw_freq_data[ngram]["TOTAL_VALUE"] += int(data[1])

class bigram():
    def __init__(self):
        self.bigrams = raw_freq_data["bigrams"].copy()
            
        for key in list(self.bigrams.keys()):
            probability = self.bigrams[key]/self.bigrams["TOTAL_VALUE"]
            if key != "TOTAL_VALUE":
                self.bigrams[key] = math.log10(probability)

        self.baseScore = math.log10(0.01/self.bigrams["TOTAL_VALUE"])
        print(f"{GREEN}Loaded {len(self.bigrams)} bigrams.{RESET}")    
    def score(self, text):
        
        finalScore = 0

        for index in range(len(text)-2+1):
            bigram = text[index:index+2].upper()
            
            if bigram in self.bigrams:
                finalScore += self.bigrams[bigram]
            else:
                finalScore += self.baseScore
        
        return finalScore
class trigram():
    def __init__(self):
        self.trigrams = raw_freq_data["trigrams"].copy()

        for key in list(self.trigrams.keys()):
            probability = self.trigrams[key]/self.trigrams["TOTAL_VALUE"]
            if key != "TOTAL_VALUE":
                self.trigrams[key] = math.log10(probability)

        self.baseScore = math.log10(0.01/self.trigrams["TOTAL_VALUE"])
        print(f"{GREEN}Loaded {len(self.trigrams)} trigrams.{RESET}")    
    def score(self, text):
        
        finalScore = 0

        for index in range(len(text)-3+1):
            trigram = text[index:index+3].upper()
            
            if trigram in self.trigrams:
                finalScore += self.trigrams[trigram]
            else:
                finalScore += self.baseScore
        
        return finalScore
class quadgram():
    def __init__(self):
        self.quadgrams = raw_freq_data["quadgrams"].copy()
            
        for key in list(self.quadgrams.keys()):
            probability = self.quadgrams[key]/self.quadgrams["TOTAL_VALUE"]
            if key != "TOTAL_VALUE":
                self.quadgrams[key] = math.log10(probability)
        self.baseScore = math.log10(0.01/self.quadgrams["TOTAL_VALUE"])
        print(f"{GREEN}Loaded {len(self.quadgrams)} quadgrams.{RESET}")    
    def score(self, text):
        
        finalScore = 0

        for index in range(len(text)-4+1):
            quadgram = text[index:index+4].upper()
            
            if quadgram in self.quadgrams:
                finalScore += self.quadgrams[quadgram]
            else:
                finalScore += self.baseScore
        
        return finalScore
class ngrams():
    def __init__(self):
        self.trigrams = trigram()
        self.bigrams = bigram()
        self.quadgrams = quadgram()
        print(f"{MAGENTA}Total Freqs:\n     Bi   - {self.bigrams.bigrams["TOTAL_VALUE"]}\n     Tri  - {self.trigrams.trigrams["TOTAL_VALUE"]}\n     Quad - {self.quadgrams.quadgrams["TOTAL_VALUE"]} {RESET}")
    def score(self, text):
        finalScore = 0

        biScore = self.bigrams.score(text)
        triScore = self.trigrams.score(text)
        quadScore = self.quadgrams.score(text)

        finalScore = 0.1 * biScore + 0.3 * triScore + 0.6 * quadScore
        
        return finalScore

def frequencyAnalysis(string: str) -> dict:
    freqs = Counter(string)
    print(sorted(freqs.items(), key=lambda thingy: thingy[0]))
def recommendedShiftFrequencyAnalysis(string: str, info = False) -> int:
    frequencies = frequencyAnalysis(string)

    distance = ord("E") - ord(frequencies[-1])
    if distance < 0: distance = 26+distance

    if info:
        print(frequencies[-1])
        print(frequencies[-2])
        print(frequencies[-3])
        print(frequencies[-4])

    return distance
def Affineshift(text: str,key: list) -> str:
    result = ""
    multi = key[0]
    shift = key[1]
    for i in range(len(text)):
        char = text[i]
        if not char.isalpha():
            result += char
            continue
        # Encrypt uppercase characters
        if (char.isupper()):
            result += chr((((ord(char)-65)*multi)+(shift))%26+65)
        # Encrypt lowercase characters
        else:
            result += chr( ( ( (ord(char)-97) *multi) +shift) % 26 + 97)

    return result
def chiSquared(text: str, mode : str = "mono") -> int: #Mode can be 'mono','bi','tri','quad'
    #im pretty sure this is a version of standard deviation :sob, 
    #adds up the square of each letters occurance subtracted from its expected occurance and divides by expected occurance
    # sigma ((counted_freq - expected_freq)^2/expected_freq) for all patterns seen
    
    pattern_length = 1

    match mode:
        case "mono":
            data_set_frequencies = raw_freq_data["monograms"]
        case "bi":
            pattern_length = 2
            data_set_frequencies = raw_freq_data["bigrams"]
        case "tri":
            pattern_length = 3
            data_set_frequencies = raw_freq_data["trigrams"]        
        case "quad":
            pattern_length = 4
            data_set_frequencies = raw_freq_data["quadgrams"]
        case _:
            data_set_frequencies = raw_freq_data["monograms"]
        
    text = text.replace(" ","").upper()
    partitioned_text = [text[i:i+pattern_length] for i in range(len(text)-pattern_length+1)]

    freqs = Counter(partitioned_text)
    length = len(partitioned_text)

    total = 0
    for pattern, freq in freqs.items():
        try:
            estimated_prob = data_set_frequencies[pattern.upper()]/data_set_frequencies["TOTAL_VALUE"]

            total +=((freq - (estimated_prob*length) )**2) / (estimated_prob*length)
        except:
            pass
    return total
def recommendedShiftChiSquared(string: str, info = False) -> int:
    minChi = [10**10,0]
    allChis = []
    possibleMultis = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    for j in possibleMultis:
        for i in range(26):
            chi = chiSquared(Affineshift(string,[j,i]))

            if chi<minChi[0]:
                minChi = [chi,[j,i]]
            allChis.append([chi,[j,i]])
    
    if info:
        allChis=sorted(allChis, key=lambda thingy: thingy[0])
        print("Chi level, and likely keys:")
        print(allChis[0])
        print(allChis[1])
        print(allChis[2])

    return minChi[1]
def ic(text, mode : int = 1):
    pattern_length = 1

    if mode>1:
        pattern_length = mode
        
    text = text.replace(" ","").upper()
    partitioned_text = [text[i*pattern_length:i*pattern_length+pattern_length] for i in range(len(text)//pattern_length)]

    freqs = Counter(partitioned_text)
    length = len(partitioned_text)


    ioc = sum([value*(value-1) for value in freqs.values()])/(length*(length-1))
    return ioc
def inverseText(string: str) -> str:
    result = ""
    for char in string:
        keyCode = 90-(ord(char)-65)
        result += chr(keyCode)
    return result

def random_insert_from_corpus(corpus,text_length : int = 500) -> str:
    contents = corpus
    
    return contents[random.randint(0,len(contents)-text_length):]
    

def clean_plaintext(plaintext: str) -> str:
    return wordsegment.segment(plaintext)

def matrixMultiplier(MatA : list, MatB : list) -> list:
    """Eg
    1 4 7     1
    2 5 8     2
    3 6 9     3

    = 1*1 + 4*2 + 7*3
      2*1 + 5*2 + 8*3
      3*1 + 6*2 + 9*3
    
    = 30
      36
      42
    """

    num_columns_mat_a = len(MatA[0])
    num_rows_mat_a = len(MatA)

    num_rows_mat_b = len(MatB)
    num_columns_mat_b = len(MatB[0])

    if num_rows_mat_b!=num_columns_mat_a:
        raise ValueError("Matrices are not compatible!")
    
    resultMat =[[0 for __ in range(num_columns_mat_b)] for _ in range(num_rows_mat_a)]

    #print(num_columns_mat_a)
    #print(num_rows_mat_a)
    ##print(num_columns_mat_b)
    #print(num_rows_mat_b)
    for ___ in range(num_columns_mat_a):
        for __ in range(num_rows_mat_a):
            for _ in range(num_columns_mat_b):
                #print(f"{_}")
                #print(f"ResultMat[{__},{_}] += {MatA[__][___]} (MatA[{__},{___}]) *{MatB[__][_]} (MatB[{__},{_}])")
                resultMat[__][_] += MatA[__][___]*MatB[___][_]
                #print(resultMat)
    return resultMat
def baseN_Inverse(num: int, base: int = 26)-> int:
    for i in range(1,base):
        if (num*i)%base == 1:
            return i
    return None
def inverseMatrixMod26(MatA: list):
    length = len(MatA)
    determinant = int(round(numpy.linalg(MatA)))
    determinant%=26

    if baseN_Inverse(determinant,26) is None:
        return None

    
    return numpy.linalg.inv(numpy.array(MatA))

if __name__ == "__main__":
    text = """
NBDWXJBOMELDZVPGWMMELBJQRPMPTDDWRRGQIDRKJFOWWTZOLVKCOYIJQ
RMCQJZYJNVBECTBJJKJFOWWWWHFFTSNXYFBVVVTTYIETCBLKMIOXYJGVV
VSWGSELMMYEIMMGFUGMMXMBVRPBITXYNAOIOYEVWVSKDTYJZZHNNBCEMN
OZRVWMXMGMMMAYNKCYJJAWPFHSNXYFBVVVYPZWRRMGIELBCEJNBNOVDEC
MTMQIXYNAXEJJQNJZAMDRFWLZVKTNDRUYPZMEIMSSWHWDRTNLZRTJNJVG
JVOEXWIHWKMMOIOYVZIUXBJFVQWIKVWBCEEKWMWDFTGIIGTJGBX
    """.replace("\n","").replace(" ","")

    for i in range(1,6):
        print(f"IC{i}: {ic(text,i)}")
