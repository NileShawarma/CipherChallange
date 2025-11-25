from collections import Counter
import os 
import sys
import math

script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","..","Test","Modules")
sys.path.append(modulesPath)

import cipherTools 

#Editable toggles and shit
string = """
LIKHKDGDQBWKLQJFRQILGHQWLDOWRVDBKHZURWHLWLQFLSKHUWKDWLVE
BVRFKDQJLQJWKHRUGHURIWKHOHWWHUVRIWKHDOSKDEHWWKDWQRWDZRUG
FRXOGEHPDGHRXWLIDQBRQHZLVKHVWRGHFLSKHUWKHVHDQGJHWDWWKHLU
PHDQLQJKHPXVWVXEVWLWXWHWKHIRXUWKOHWWHURIWKHDOSKDEHWQDPHO
BGIRUDDQGVRZLWKWKHRWKHUV
"""
ReverseString = False # me when ciphertext was reversed :(
decipherData = {
    "Ready" : True,
    "AutoSolve" : False,
    "recommendShift" : "chi",
    "mode": "cosine", #can be neek, overkill, cosine, or regular
    "cribs": ["VICTORY","DISCO","SPAIN","EUROVISION"] #only for neek mode
}
decryptionReady = True

string = string.replace(" ","").replace("\n","")
if ReverseString:
    string = string[::-1]

RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

print(f"String length: {len(string)}")


def shift(text: str,s: int) -> str:
    result = ""

    # traverse text
    for i in range(len(text)):
        char = text[i]

        # Encrypt uppercase characters
        if (char.isupper()):
            result += chr((ord(char) + s-65) % 26 + 65)

        # Encrypt lowercase characters
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)

    return result
def recommendedShift(args: dict, mode = "chi")-> int:
    match mode:
        case "frequency":
            return cipherTools.recommendedShiftFrequencyAnalysis(args["string"],args["info"])
        case "chi":
            return cipherTools.recommendedShiftChiSquared(args["string"],args["info"])

if __name__ == "__main__":
    if decryptionReady:

        if decipherData["mode"] == "overkill": # we pull up with the frequency of over 12 billion word patterns to a caesar cipher 🔥 and yes i googled the emoji and what
            ngraminator = cipherTools.ngrams()
            best_key = 0
            best_string = ""
            best_score = float("-inf")
            for i in range(25):
                attempt = shift(string,i)
                score = ngraminator.score(attempt)

                if score > best_score:
                    best_score = score
                    best_key = i
                    best_string = attempt
            string = best_string
        elif decipherData["mode"] == "neek": #mathematically deduce possible keys and thennn we use overkill mode to find the best one
            ngraminator = cipherTools.ngrams()        
            cribs = decipherData["cribs"]
            
            possible_shifts = []
            for crib in cribs:
                length = len(crib)

                for i in range(len(string)-length+1): #Sliding window through the ciphertext
                    substr = string[i:i+length]
                    shift_difference = None
                    success = True
                    for j in range(length):

                        crib_char = crib[j].upper()
                        cipher_char = substr[j].upper()

                        cipher_num, crib_num = ord(cipher_char), ord(crib_char)

                        if shift_difference == None:
                            shift_difference = cipher_num-crib_num
                            continue

                        if shift_difference != cipher_num-crib_num and shift_difference != (cipher_num-crib_num)%26:
                            success = False
                            break
                    if success:
                        possible_shifts.append(shift_difference)
            best_score = float("-inf")
            best_key = 0

            for caesar_shift in possible_shifts:
                if caesar_shift > 0:
                    caesar_shift = (26-caesar_shift)%26 #to prevent us double encrypting the text cus if its positive then we just worked out the encryption key
                else:
                    caesar_shift = -caesar_shift #if its negative then its the decrypt key but negative so we need to make it positive
                
                sample_text = shift(string,caesar_shift)
                score = ngraminator.score(sample_text)

                if score>best_score:
                    best_key, best_score = caesar_shift, score
            string = shift(string,int(best_key)).lower()
        elif decipherData["mode"] == "cosine":
            obj = cipherTools.what_the_fuck_was_madness_thinking()
            best_cosine = 0
            best_key = 0

            for key in range(26):
                VectCipher = shift(string,key)

                freqs = Counter(VectCipher)
                total = sum([ int(item) for key,item in freqs.items()])
                VectCipher = {}
                
                for keys,item in freqs.items():
                    VectCipher[keys.upper()] = item/total
                
                score = obj.cosine(VectCipher)["Cosine"]

                if score<best_cosine:
                    best_cosine = score
                    best_key = key
            
            string = shift(string,best_key).lower()
        else: #honestly useless
            args = {
                "string" : string,
                "info" : True
            }
            bestShift = 0
            best_score = float("-inf")
            for i in range(26):
                score = cipherTools.chiSquared(shift(string,i))
                if score>best_score:
                    best_score = score
                    bestShift = i

            if not decipherData["AutoSolve"]:
                RecommendedShift = bestShift
                shiftNum = (input(f"Shift value for block 1 (Recommended shift: {RecommendedShift} via frequency analysis): ")) or 0
            
            else:
                shiftNum = bestShift
            
            
            if shiftNum:
                string = shift(string,int(shiftNum)).lower()
        
        string = " ".join(cipherTools.clean_plaintext(string)) 

        if string.islower():
            print(BLUE + string + RESET)
        else:
            print(RED + string + RESET)
