from collections import Counter
import os 
import sys

script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","..","Test","Modules")
sys.path.append(modulesPath)

import cipherTools 

#Editable toggles and shit
string = """
KLYJKPMCLDUFXAESCZFRSSZZADLEESPKZZ
"""
ReverseString = False # me when ciphertext was reversed :(
decipherData = {
    "Ready" : True,
    "AutoSolve" : False,
    "recommendShift" : "chi",
    "mode": "overkill", #can be neek, overkill, or regular
    "crib": "peter" #only for neek mode
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
    elif decipherData["mode"] == "neek": #TODO WRITE THE WHOLE NEEK MODE
        length = len(decipherData["cribs"])
        result = chr((ord(char) + s-65) % 26 + 65)
        pass
    else:
        args = {
            "string" : string,
            "info" : True
        }

        if not decipherData["AutoSolve"]:
            RecommendedShift = recommendedShift(args, decipherData["recommendShift"])
            shiftNum = (input(f"Shift value for block 1 (Recommended shift: {RecommendedShift} via frequency analysis): ")) or 0
        
        else:
            shiftNum = recommendedShift(args, decipherData["recommendShift"])
        
        
        if shiftNum:
            string = shift(string,int(shiftNum)).lower()
    string = " ".join(cipherTools.clean_plaintext(string))
    if string.islower():
        print(BLUE + string + RESET)
    else:
        print(RED + string + RESET)
