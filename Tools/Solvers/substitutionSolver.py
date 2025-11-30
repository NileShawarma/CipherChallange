from collections import Counter
import string as st
import os 
import sys
import math
import random

script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","..","Test","Modules")
sys.path.append(modulesPath)

RED = "\033[91m"
BLUE = "\033[1;36m"
MAGENTA = "\033[1;35m"
GREEN = "\033[1;32m"
RESET = "\033[0m"

import cipherTools
from cipherTools import chiSquared, ngrams

def shuffleKey(currentKey: str) -> str:
    tempKey = list(currentKey)

    index1 = random.randint(0,len(currentKey)-1)
    index2 = random.randint(0,len(currentKey)-1)

    val1 = tempKey[index1]
    val2 = tempKey[index2]

    tempKey[index1],tempKey[index2] = val2, val1

    return "".join(tempKey)
def decrypt(cipherText: str, key: str) -> str:
    plaintext = ""
    ALPHABET = st.ascii_lowercase
    decryption_map = {c: p for p, c in zip(ALPHABET, key)}

    for char in cipherText:
        if char in decryption_map:
            plaintext+= decryption_map[char]
        else:
            plaintext += char
        
    return plaintext

#Editable toggles and shit
string = """
YPRLCGHCHHCSLUCYNGUJUZSJBJTCZWPBKEBGEBGNCGRUZSJTLEUZCXRLIUSZIEBGPBKGDGBJBJPDLUTCMLYCZCSLRJBUZJLSGCJLJTLRLMUALNUJTJTLYCATUZLICJIBYLBEBKGJLXLSGCDTIIJCJUBZICZRTCMLHLLZGKZZUZSUJBZICYDXLJLOJUZJLGALDJLREGBYJTLJGCEEUADCIIUZSJTGBKSTJTBILBEEUALIUZSLZLGCXYPLZSUZLLGITCMLHLLZTUSTXPUYDGLIILRHPPBKGYLATCZUIYJTLPNLGLCIJBZUITLRCJJTLIDLLRNUJTNTUATUJNCICHXLJBDCGILJTLJGCEEUACZRJBABGGLAJXPEXCSYLIICSLIJTCJRLILGMLBGGLFKUGLSGLCJLGCJJLZJUBZAKGUBKIXPTBNLMLGBZLBEJTLJLXLSGCYITCIGLIUIJLRCJJCAWHBJTHPPBKGABYDKJLGCZRHPYPAGPDJBXBSUIJIRLIDUJLJTLUGCZRYPHLIJLEEBGJIJTLPNLGLKZCHXLJBRLJLGYUZLJTLZCJKGLBEJTLJLOJUJABZJCUZIJTLJLATZUAUCZNTBHGBKSTJKIPBKGDXCZIJCWLIJTLMULNJTCJJTLYLIICSLYCPTCMLHLLZLZAGPDJLRKIUZSCMUSLZLGLAUDTLGCZRJTLILCGLBEABKGILZBJBGUBKIXPRUEEUAKXJJBHGLCWDLGTCDIUJNUXXGLIUIJKICXXUZNTUATACILUCYCEGCURJTCJYUSTJKZRLGYUZLJTLMCXKLBEJTUILZRLCMBKGUCYTBDUZSJTCJPBKBGPBKGEGULZRNTLCJIJBZLYUSTJHLCHXLIKSSLIJCYBRUEUACJUBZBEPBKGYCATUZLJTCJACZGUILJBJTLATCXXLZSLUACZDGBMURLBZLKILEKXUJLYBEUZJLXXUSLZALJTCJYCPTLXDUZRLAUDTLGUZSJTLAKGILRJLXLSGCYUJNCICDDCGLZJXPILZJEGBYJTLBEEUALBECZLNPBGWHKIUZLIIYCZHPJTLZCYLBEYUXXLGCZRYCPTCMLHLLZCGLDXPJBCZBJTLGYLIICSLEGBYIBYLBZLIUSZUZSNUJTJTLIUZSXLXLJJLGGUYKIJABZSGCJKXCJLPBKGJLATZUAUCZEBGYCWUZSJTUIABZZLAJUBZJTLUZJLGALDJLRYLIICSLJBYUXXLGEGBYGNCILZAGPDJLRKIUZSCIUYDXLACLICGITUEJAUDTLGNTUATTCRZBZLJTLXLIIACKILRCIXBNRBNZUZJTLCDDCGCJKIBNUZSJBJTLECAJJTCJJTLJLOJTCRHLLZHXBAWLRUZEUMLXLJJLGSGBKDINTUXLNCUJUZSEBGJTLLZSUZLLGIJBJKZLJTLYLATCZUIYJBIDLLRKDJTLRLAGPDJUBZPBKGABXXLCSKLAGCAWLRJTCJAUDTLGHPTCZRCZRALGJCUZCIDLAJIBEUJUZAXKRUZSJTLKILBECZUJCXUCZEBGYBEYUXXLGIZCYLCJJGCAJLRTLGCJJLZJUBZILJJUZSCEXCSJBYBZUJBGYLIICSLIEGBYJTLZLUSTHBKGTBBRBEEUALXLRJBJTLRUIABMLGPBEJTUIJLOJUJTUZWUJUIDLGTCDINBGJTLOCYUZUZSEKGJTLGUEBZXPJBTLXDUYDGBMLPBKGYLATCZUIYRBRSL
""".upper()


ReverseString = False # me when ciphertext was reversed :(
decipherData = {
    "RemoveSpaces": False, #sm more readable when u do
    "Ready" : True,
    "AutoSolve" : True,
    "superfun" : True,
    "ngramToUse" : 0,
    "clean_plaintext" : True
}
statement = ""
match decipherData["ngramToUse"]:
    case 2:
        statement = "Utilising bi-grams."
        ngram_inator = ngrams().bigrams
    case 3:
        statement = "Utilising tri-grams."
        ngram_inator = ngrams().trigrams
    case 4:
        statement = "Utilising quad-grams."
        ngram_inator = ngrams().quadgrams
    case _:
        statement = "Utilising all data."
        ngram_inator = ngrams()

decryptionReady = True

result = ""
punctuation = [",","."]
if decipherData["RemoveSpaces"]: string=string.replace(" ","")
for char in string:
    if char.isalpha() or char == " " or char in punctuation:
        result+=char
string = result

if ReverseString:
    string = string[::-1]

print(f"{GREEN}String length: {len(string)}{RESET}")


if __name__ == "__main__":
    print(f"\n\033[1m{RED}{statement}{RESET}")
    bestKeys = []
    for i in range(5):
        print(f"{BLUE}")
        initial_temp = 50
        max_iterations = 10000 #normally it solves it in under 5000 but better safe than sorry
        cooling_rate = 0.9996

        alphabet = list(st.ascii_uppercase) #generate random key
        current_key = ""
        for j in range(26):
            current_key+=str(random.choice(alphabet))
            alphabet.remove(current_key[-1])

        current_score = ngram_inator.score(decrypt(string, current_key))

        best_key = current_key
        best_score = current_score

        temperature = initial_temp

        accepted_moves = 0

        for iteration in range(max_iterations):
            new_key = shuffleKey(current_key)
            new_score = ngram_inator.score(decrypt(string, new_key))
            
            #calc score diff
            diff = new_score - current_score
            
            if diff > 0:
                current_key = new_key
                current_score = new_score
                accepted_moves += 1
                
                if current_score > best_score:
                    best_key = current_key
                    best_score = current_score
            else:
                #accept worse solutions with probability based on temperature
                if temperature == 0:
                    continue
                acceptance_probability = math.exp(diff / temperature) #chatgptd math icl
                if random.random() < acceptance_probability:
                    current_key = new_key
                    current_score = new_score
                    accepted_moves += 1
            
            temperature *= cooling_rate
            
            if (iteration + 1) % 1000 == 0: #blank screens do be scary

                acceptance_rate = (accepted_moves / 1000) * 100

                print(f"Iteration {iteration + 1}: Best score = {best_score:.4f}, Temp = {temperature:.4f}, Acceptance = {acceptance_rate:.1f}%, Key = {best_key}")
                decrypted_sample = decrypt(string, best_key)[:120]

                print(f"Current decryption: {decrypted_sample}...\n")
                accepted_moves = 0

            elif (iteration+1) % 250 == 0 and (iteration+1) // 250 <5:
                print(f"Iteration {iteration + 1}: Best score = {best_score:.4f}, Temp = {temperature:.4f}, Key = {best_key}")
                decrypted_sample = decrypt(string, best_key)[:120]
                print(f"Current decryption: {decrypted_sample}...\n")
        
        if decipherData["clean_plaintext"]: output_string = " ".join(cipherTools.clean_plaintext(decrypt(string,best_key)))
        else: output_string = decrypt(string,best_key)
        
        print(f"\033[1m{RED}LOOP {i+1} INFO: ")  
        print(f"{MAGENTA}Recommended key: {best_key}")
        print(f"Score: {best_score} {RESET}\n")
        print(f"Decryption: \n{GREEN}{output_string}{RESET}")

        bestKeys.append(best_key)
    lowestChis = []
    for key in bestKeys:
        lowestChis.append([chiSquared(decrypt(string,key)),key])
    lowestChis = sorted(lowestChis, key=lambda data: data[0])

    print("\n"+"="*46+"\n")
    print(f"\033[1m{RED}MOST LIKELY KEY IS: {lowestChis[0][1]}")
    print(f"Most likely decryption is:\n {GREEN}{decrypt(string,lowestChis[0][1])}")
    print(f"\n\033[35mOther likely data: {lowestChis}{RESET}")