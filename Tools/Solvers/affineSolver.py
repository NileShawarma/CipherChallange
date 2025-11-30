from collections import Counter
import os 
import sys

script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","..","Test","Modules")
sys.path.append(modulesPath)

import cipherTools

class AffineCipher():
    def __setattr__(self, name, value):
        if name == "multiplier":
            if value in self.possibleMultis:
                super().__setattr__(name,value)
                return
            raise Exception("Multiplier is not invertible!")
        
        super().__setattr__(name,value)
    def __init__(self, shift = None, multiplier = 1, additive = 0,rawString = None):
        self.cosine_calc = cipherTools.what_the_fuck_was_madness_thinking()

        self.possibleMultis = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

        if shift != None:
            self.multiplier = shift[0]
            self.additive = shift[1]
        else:
            self.multiplier = multiplier
            self.additive = additive
        
        self.raw_string = rawString
        result = ""

        if not self.multiplier in self.possibleMultis:
            raise Exception("Multiplier is not invertible!")
    def decrypt(self, text = None):
        if text!=None:
            pass
        else:
            text = self.raw_string

        multi = self.multiplier
        shift = self.additive
        result = ""
        for i in range(len(text)):
            
            char = text[i]

            if not char.isalpha():
                result += char
                continue
            # Encrypt uppercase characters
            if (char.isupper()):
                result += chr(   (  ( (ord(char)-65)-shift)*cipherTools.baseN_Inverse(multi)  )%26+65   )
            # Encrypt lowercase characters
            else:
                result += chr(   (  ( (ord(char)-97)-shift)*cipherTools.baseN_Inverse(multi)  )%26+97   )

        return result
    def encrypt(self, text = None):
        if text==None:
            text = self.raw_string

        multi = self.multiplier
        shift = self.additive
        result = ""
        for i in range(len(text)):
            
            char = text[i]

            if not char.isalpha():
                result += char
                continue
            # Encrypt uppercase characters
            if (char.isupper()):
                result += chr(   (  ( (ord(char)-65)*multi)+shift  )%26+65   )
            # Encrypt lowercase characters
            else:
                result += chr(   (  ( (ord(char)-97)*multi)+shift  )%26+97   )

        return result        
    def auto_solve(self, text = None):
        if text == None:
            text = self.raw_string
        
        best_cosine,best_key = -1,[1,0]
        for multi in self.possibleMultis:
            for shift in range(26):
                self.multiplier,self.additive = multi, shift

                decrypt = self.decrypt(text)
                decrypt = "".join([char if char.isalpha() else "" for char in decrypt])

                VectDecrypt = Counter(decrypt)

                total = sum([ int(item) for key,item in VectDecrypt.items()])
                
                for key,item in VectDecrypt.items():
                    VectDecrypt[key.upper()] = item/total

                score = self.cosine_calc.cosine(VectDecrypt)["Cosine"]

                if score > best_cosine:
                    best_cosine = score
                    best_key = [multi,shift]
        
        return {"decrypt" : self.decrypt(text), "key" : best_key}
    def auto_solve_crib(self, crib, text=None):
        if text is None:
            text = self.raw_string
        
        if type(crib) != list:
            raise Exception("Crib must be a list of [plain, cipher].")

        plain_crib = crib[0].upper()
        enciphered_crib = crib[1].upper()

        equations = [
            [ord(plain_crib[i]) - 65, ord(enciphered_crib[i]) - 65]
            for i in range(len(plain_crib))
        ]

        for i in range(len(equations)):
            for j in range(i+1, len(equations)):
                x1, y1 = equations[i]
                x2, y2 = equations[j]

                an = (x1 - x2) % 26
                c  = (y1 - y2) % 26

                # test if invertible
                if an in self.possibleMultis:
                    inv = cipherTools.baseN_Inverse(an)
                    a = (c * inv) % 26
                    b = (y1 - a * x1) % 26

                    # decrypt with found key
                    oldA, oldB = self.multiplier, self.additive
                    self.multiplier, self.additive = a, b
                    decrypt_full = self.decrypt(text)

                    if self.encrypt(plain_crib) == enciphered_crib:
                        return {"key": [a, b], "decrypt": decrypt_full}

                    self.multiplier, self.additive = oldA, oldB
        raise Exception("Unsolvable via cribs!")

if __name__ == "__main__":
    string = """
    TSLCZFRCEFRPECCETNUMDTQCLKCVFRMWTQGFMGLNFBLBDCELBDCTHDMQFQN
    LQNLCEDCQFFQLRQWLYNCDQWNTQNCLDWELYLTNDIFXLVEZWTWCELHETHXLQH
    YFNNCELBFLSTRNNCYTUCFPLCCFCELNDBLNTWL
    """

    ReverseString = False # me when ciphertext was reversed :(
    decipherData = {
        "Ready" : False,
        "AutoSolve" : True,
        "clean_plaintext" : True
    }


    result = ""

    for char in string:
        if char.isalpha() or char == " ":
            result+=char
    string = result

    if ReverseString:
        string = string[::-1]

    RED = "\033[91m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

    print(f"String length: {len(string)}")

    if decipherData["Ready"]:
        args = {
            "string" : string,
            "info" : True
        }
        
        affine = AffineCipher()
        affine.raw_string = args["string"]

        if not decipherData["AutoSolve"]:

            RecommendedKey = ",".join(affine.auto_solve()["key"])

            shiftNum = [int(i) for i in (input(f"Shift value for text (Recommended shift: {RecommendedKey}): ")).split(",")] or [1,0]

            affine.multiplier, affine.additive = shiftNum[0], shiftNum[1]

        else:
            affine.multiplier,affine.additive = affine.auto_solve()["key"]

        
        string = affine.decrypt().lower()

        if decipherData["clean_plaintext"]:    
            string = " ".join(cipherTools.clean_plaintext(string))
        
        print(f"KEY : {affine.multiplier},{affine.additive}")
        if string.islower():
            print(BLUE + string + RESET)
        else:
            print(RED + string + RESET)
    else:
        print(f"{RED}Entering testing mode.\n\n{RESET}")
        affine = AffineCipher()
        affine.raw_string = """OYFSTGLYYRSBXPTCLLIRSBSLZANYSGYNXXPFYXTONWRTVYRAYLDJRYLQOWL
BLSOCLSLTTFSQIYLVRTRNSNGFSLUICNTRELNYQSFSVLQRTINTFCOLVWSRVR
FSRGRGFRCLQWLZNJCQZFHLJIZNJCQSOBNYRBWOAFVHONTCLLIFSQNGOLSIY
NOLTOLQCNJQCP""".replace("\n","")
        affine.multiplier = 17
        affine.additive = 2
        success = False
        for i in range(len(affine.raw_string)-len("CRIB")+1):
            try:
                deets = (affine.auto_solve_crib(["CRIB",affine.raw_string[i:i+len("CRIB")]]))
                print(deets)
            except:
                pass
        if success:
            print(deets)
        print(affine.decrypt())