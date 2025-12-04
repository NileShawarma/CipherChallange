from collections import Counter
from matplotlib import pylab
import numpy
import os 
import math
import wordsegment
import random
import string

RED = "\033[91m"
BLUE = "\033[1;36m"
MAGENTA = "\033[1;35m"
GREEN = "\033[1;32m"
RESET = "\033[0m"

wordsegment.load()

raw_freq_data = {}
percentage_freq_data = {}
for ngram in ["monograms","bigrams","trigrams","quadgrams"]:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","Data","ngrams",f"{ngram}.txt"), "r") as file:
        raw_freq_data[ngram] = {"TOTAL_VALUE":0}
        percentage_freq_data[ngram] = {}
        for line in file:
            data = line.split(" ")
            raw_freq_data[ngram][data[0]] = int(data[1])
            raw_freq_data[ngram]["TOTAL_VALUE"] += int(data[1])
            percentage_freq_data[ngram][data[0]] = int(data[1])
        for key,item in percentage_freq_data[ngram].items():
            percentage_freq_data[ngram][key] = item/raw_freq_data[ngram]["TOTAL_VALUE"]

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

class what_the_fuck_was_madness_thinking():
    def __init__(self):
        #i swear to god he was on drugs when thinking this vector stuff was the best way to show beginners how english-esque text is
        pass
    def dp(self, Vect1,Vect2 = percentage_freq_data["monograms"]):

        if len(Vect1) < len(Vect2):
            Vect2,Vect1 = Vect1,Vect2
        counter = 0
        for key in Vect1.keys():
            try:
                counter += Vect1[key.upper()] * Vect2[key.upper()]
            except:
                pass
        
        return counter
    
    def cosine(self,Vect1,Vect2 = percentage_freq_data["monograms"]):
        #Takes two "vectors" (acc dictionaries in the form {letter:percent_freq}) and finds the angle between them
        #keys from each array are assumed to be in the same case and format
        #WE COULDD use numpy for the dot product bit but thats no fun

        dp_1_2 = self.dp(Vect1,Vect2)
        dp_1_1 = self.dp(Vect1,Vect1)
        dp_2_2 = self.dp(Vect2,Vect2)

        angle_cosine = dp_1_2 / math.sqrt(dp_1_1*dp_2_2)
        angle = math.acos(angle_cosine)
        
        return {"Angle" : angle, "Cosine" : angle_cosine}
class IoC():
    def __init__(self):
        pass
    def ic(self,text, mode : int = 1, overlap = False):
        pattern_length = 1

        if mode>1:
            pattern_length = mode

        if pattern_length < 1:
            return 0.0

        text = text.replace(" ","").upper()

        if overlap:
            partitioned_text = [text[i:i+pattern_length] for i in range(len(text) - pattern_length + 1)]
        else:
            partitioned_text = [text[pattern_length*i:pattern_length*(i+1)] for i in range(len(text)//pattern_length)]

        freqs = Counter(partitioned_text)
        length = len(partitioned_text)


        ioc = sum([value*(value-1) for value in freqs.values()])/(length*(length-1))
        return ioc
    def sinkov(self,string,min_period=1, max_period=30):
        ENGLISH_IOC = 0.0667
        IoC_variances = {}
        
        best_key = 1
        best_variance = float("inf")

        for period in range(min_period,max_period+1):
            partitions = column_seperation(string,period)
            total_IoC = sum([self.ic(partition) for partition in partitions])
            avg_IoC = total_IoC/len(partitions)

            IoC_variance = ENGLISH_IOC-avg_IoC
            
            IoC_variances[str(period)] = abs(IoC_variance)
            
            if abs(IoC_variance)<best_variance:
                best_key = period
                best_variance = abs(IoC_variance)
        sorted_variances = (sorted(IoC_variances.items(), key=lambda thingy: thingy[1]))
        return {"key" : best_key, "full_data" : sorted_variances}
    def sinkov_first_past_the_post(self,string,min_period=1,max_period=30):
        ENGLISH_IOC = 0.0667 *26
        IoC_variances = {}
        
        best_key = 1
        best_variance = float("inf")
        
        threshold_ioc, first_passed = 1.5, None

        for period in range(min_period,max_period+1):
            partitions = column_seperation(string,period)
            total_IoC = sum([self.ic(partition) for partition in partitions])

            avg_IoC = (total_IoC/len(partitions)) * 26 #normalised ioc gonna have to get used to this cus madness's book basically only uses normalised iocs

            IoC_variance = ENGLISH_IOC-avg_IoC
            
            IoC_variances[str(period)] = abs(IoC_variance)

            if avg_IoC >= threshold_ioc:
                first_passed = [period,total_IoC]
                best_key = first_passed[0]

                break
            
            if abs(IoC_variance)<best_variance:
                best_key = period
                best_variance = abs(IoC_variance)

        sorted_variances = (sorted(IoC_variances.items(), key=lambda thingy: thingy[1]))

        return {"key" : best_key, "full_data" : sorted_variances}

#temporary till i change all usage of seperators to column seperation
def seperators(string: str,keyLength: int) -> list:
    return column_seperation(string, keyLength)

def column_seperation(string: str,keyLength: int) -> list:
    newArray = ["" for i in range(keyLength)]

    for index in range(keyLength):
        newArray[index] = string[index::keyLength]
    return newArray
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

def inverseText(string: str) -> str:
    result = ""
    for char in string:
        keyCode = 90-(ord(char)-65)
        result += chr(keyCode)
    return result
def key_to_num(string: str):
    num_arr = []
    string = string.upper()
    for char in string:
        num_arr.append(ord(char)-65)
    return num_arr
def num_to_key(num_arr: list):
    key = ""
    for num in num_arr:
        key += chr(65+num)
    return key
def random_insert_from_corpus(corpus,text_length : int = 500) -> str:
    contents = corpus
    pos = random.randint(0,len(contents))

    return contents[pos-text_length:pos]
def random_string(length):
    alphabet = string.ascii_uppercase

    result = ""
    for _ in range(length):
        result += random.choice(alphabet)
    return result

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
    corpus = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","Data","corpus","no_newlines.txt"),"r").read()

    obj = what_the_fuck_was_madness_thinking()
    x,y = [], []
    for i in range(100,1000,100):
        x.append(i)
        freqs = Counter(random_insert_from_corpus(corpus,i))
        total = sum([ int(item) for key,item in freqs.items()])
        new = {}
        
        for key,item in freqs.items():
            new[key.upper()] = item/total
        print(obj.cosine(new))

        freqs = Counter(random_string(i))
        total = sum([ int(item) for key,item in freqs.items()])
        new = {}
        
        for key,item in freqs.items():
            new[key.upper()] = item/total
        print(obj.cosine(new), end="-Random string\n")
