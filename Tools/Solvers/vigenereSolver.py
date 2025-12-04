from collections import Counter
import os 
import sys
import affineSolver

script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","..","Test","Modules")
toolsPath = os.path.join(script_dir,"..")
sys.path.append(modulesPath)
sys.path.append(toolsPath)

import cipherTools
import IoC_graph

class VigenereCipher():
    def __setattr__(self, name, value):
        if name == "multiplier" and hasattr(self, 'possibleMultis'):
            final_multi = value.copy()

            for val in value: #check if its a valid key
                if val in self.possibleMultis:
                    pass
                else:
                    raise Exception("Multiplier is not invertible!")
            
            
            for i in range(len(self.additives)-len(final_multi)): #the multiplier key should be the same length as the adding key, so we just pad it with 1s (identity mutliplier)
                final_multi.append(1)
            super().__setattr__(name,final_multi)
            return
        
        super().__setattr__(name,value)
    def __init__(self, text = "", multipliers = [1], key = "A", opt_args = {
        "CaesarOrAffine" : "Caesar",  "StartKey" : 2,  "MaxKey" : 30
    }):
        self.possibleMultis = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
        
        self.raw_string = text
        self.additives = cipherTools.key_to_num(key)
        self.multiplier = multipliers

        self.AffineCipher = affineSolver.AffineCipher()
        self.IoC = cipherTools.IoC()


        for arg, value in {"CaesarOrAffine" : "Caesar",  "StartKey" : 2,  "MaxKey" : 30}.items():
            self.__setattr__(arg,value)
        for arg, value in opt_args.items():
            self.__setattr__(arg, value)
    def encrypt(self, multipliers = None , key = None, text = None):
        additives, text = self.additives if key == None else cipherTools.key_to_num(key), self.raw_string if text == None else text
        multipliers = [1] if multipliers==None else multipliers

        old_add = self.additives
        old_multi = self.multiplier
        self.additives = additives #cleaning the multi relies on an updated additive
        self.multiplier = multipliers

        multipliers = self.multiplier #cleans the multiplier for us <3
        self.multiplier = old_multi
        self.additives = old_add

        text = text.replace(" ","").upper()
        period = len(additives)
        partitioned_text = cipherTools.column_seperation(text,period)

        for i,part in enumerate(partitioned_text):
            self.AffineCipher.additive, self.AffineCipher.multiplier = additives[i],multipliers[i]
            partitioned_text[i] = self.AffineCipher.encrypt(part)
        
        plaintext = ""
        for i in range(sum([len(part) for part in partitioned_text])):
            character = partitioned_text[i%period][i//period]
            
            plaintext += character

        return plaintext  
    def decrypt(self,multipliers = None , key = None, text = None, period = None):
        additives, text = self.additives if key == None else cipherTools.key_to_num(key), self.raw_string if text == None else text
        multipliers = [1] if multipliers==None else multipliers #defaults the multiplier to 1 if there is no specified multipler (1 is the identity)


        old_add = self.additives
        old_multi = self.multiplier
        self.additives = additives #cleaning the multi relies on an updated additive
        self.multiplier = multipliers

        multipliers = self.multiplier #cleans the multiplier for us <3
        self.multiplier = old_multi
        self.additives = old_add


        text = text.replace(" ","").upper()
        period = len(additives)
        partitioned_text = cipherTools.column_seperation(text,period)

        for i,part in enumerate(partitioned_text):
            self.AffineCipher.additive, self.AffineCipher.multiplier = additives[i],multipliers[i]
            print(f"Add: {self.AffineCipher.additive}, Multi : {self.AffineCipher.multiplier}")
            partitioned_text[i] = self.AffineCipher.decrypt(part)
        
        plaintext = ""
        for i in range(sum([len(part) for part in partitioned_text])):
            character = partitioned_text[i%period][i//period]
            
            plaintext += character

        return plaintext  
     
    def auto_solve(self, text = None, period = None, verbose = True):
        text = self.raw_string if text==None else text
        period = self.IoC.sinkov_first_past_the_post(text, self.StartKey, self.MaxKey)["key"] if period == None else period #determine period

        seperatedText = cipherTools.column_seperation(text,period)

        affineCipher = self.AffineCipher #vig cipher is the biggest caesar wrapper ive ever seen
        encryptionKey = ""

        for i,block in enumerate(seperatedText):
            typeShift = self.CaesarOrAffine
            
            if typeShift == "Caesar":
                affineCipher.possibleMultis = [1]
                shiftNum = affineCipher.auto_solve(block)["key"]

            elif typeShift == "Affine":
                affineCipher.possibleMultis =  [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
                shiftNum = affineCipher.auto_solve(block)["key"]
                        
            affineCipher.multiplier, affineCipher.additive = shiftNum
            seperatedText[i] = affineCipher.decrypt(block).lower()   

            encryptionKey+=str(shiftNum[1])+"|"
            decryptionMulti = shiftNum[0]
            if verbose:  print(f"Block {i+1} shift: {str(shiftNum)}")
        

        if verbose:
            RED = "\033[91m"
            BLUE = "\033[94m"
            RESET = "\033[0m"
            
            result = ""
            for subkey in encryptionKey.split("|"):
                if subkey!="-" and subkey!="":
                    result+=chr(int(subkey)+65)
                else:
                    result+="-"
            result = result[:-1]
            result2 = ""
            for subkey in encryptionKey.split("|"):
                if subkey!="-" and subkey!="":
                    if subkey=="0": result2+="A"
                    else:result2+=chr((97+26)-int(subkey)).upper()
                else:
                    result2+="-"
            result2 = result2[:-1]

            print(f"\n\n{BLUE}Multiplier of: {decryptionMulti}")
            print(f"{RED}Encryption key: {result}\nCaesar Equiv: {encryptionKey}\nDecryption Key: {result2}{RESET}")

        return {"decrypt" : self.decrypt(key=result,text=text), "key" : result}
    def auto_solve_crib(self, crib, text=None, period=None):
        text = self.raw_string if text==None else text
        period = self.IoC.sinkov_first_past_the_post(text, self.StartKey, self.MaxKey)["key"] if period == None else period #determine period

        if (period)>len(crib):
            raise ValueError("Crib length must be longer than the period!")

        same_key = [[] for i in range(period)] #holds the indexes of positions in the crib which have the same key
        for i in range(len(crib)):
            key_number = i%period
            same_key[key_number].append(i)

        seperatedText = cipherTools.column_seperation(text,period)

        possible_keys = []

        for start_of_ciphertext in range(len(text)-len(crib)+1):

            ciphertext_substr = text[start_of_ciphertext:start_of_ciphertext+len(crib)]
            full_key = []

                #TODO ADD THE POSSIBLE KEY TRACKER AND THE BEST KEY DETERMINER

            passed = True

            for same_shift_bunch_letters_thing_ykwim in same_key:

                last_shift = None

                for index in same_shift_bunch_letters_thing_ykwim:

                    crib_letter = crib[index]
                    cipher_letter = ciphertext_substr[index]

                    shift = ( ord(cipher_letter)-ord(crib_letter) ) % 26

                    if shift == last_shift or last_shift == None:
                        last_shift = shift
                        continue
                    else:
                        passed = False
                        break
                if passed:
                    full_key.append(last_shift)
                else:
                    break

            if passed:
                possible_keys.append(full_key)
                print(cipherTools.num_to_key(full_key))
        print(possible_keys)
if __name__ == "__main__":

    string = """
    IEESC CLUCO IEZIY FEIGE CNUTC QMFIC OUKIL NFIWP PDSOM DAXSE JAKMZ WWZGS VOSFT GFDSQ QRDMQ QRKVN QMZBR XIJWE YIKVE JEGFP UIUSY VOWHS GUEWE GDJHL VEJWS QPVHS CTPCF YICZY QTKVT PKDSE QOUWC GCKKS GNZHP NLPCF VHRHT HEVZE JIJHZ DEIOE JEIOY KMGCD KTZCY KHRJP CGISP FTFQZ PVVMJ QUIQZ PCVFY UFFFE JEIWR JTJCQ VHVBP YLPTC GEUAP POWHS GSFIE JAERJ QUNWW NKECH HRFAX AWIWE KNXGL PDDML ETZJT VIVGE JAKWL OIETF NLRUC GEDSY VWZHS AOLFA NAEGT EAEBZ VRVOO KLPIY FEIGE CNUKS CTFIC OEVHT PGTOY CDUHZ VHRHM WTTVL TLVGT PSZGE UTYOE YEJVZ WLUAP GTRBO CSRBZ NDWFT GNUWQ GECWX WSKCM NIXSJ QUNWW NKECH VHRHX AFZFD VCFBN GREWY OEVHT PGNWE JTYSR QVVFY OEEHT UTFGP EUISL IRVSX GNKCY RRFHP ETZCY HOIHS GWFFV QFRFE KSKGN QMGCD GRJOY FMLGT EIRBD HOIHZ QLFBR PONOX GRZQL PPLPW KSYSC UHRJP OAUSQ TEVKT VHKVP YOIYZ HOKVP TSKCH JITVE JEPVL XEECC KGYHL PDJVZ WLUVL XEECC KGYHD KTZGT PTYSA QWVFZ HYFIC EOEUC GSJHZ RRFHP ETKVZ UENVZ UECOM QUIGL TEKCZ GAJWW ASKCW GNRBO KFVSW KTZGX ADLHJ VOGSC UURRP VHVAE QUJSE JEGCH GRJHS GYNWP NDKCA TOMWO GTYOE RRFHP ETZCY FUIWY IMPTT TSKJT UIKHZ AOLFN QUEHC AICSL TNVRE JAKAJ ROJWE KOERT FNFHQ CLCKP NLNWE JTYSA GOGZP CNUWW GFKHS QRFIR JLPRT UICZF UIFBP FWZHS NIKHW GHFDP VHRHE JIEUD OIXVE EHRBR GBLHN JAEUP KSJHT TRZBR CNUHS GRZUS VSFTE JECSD UPFKP TFLZL TEZBE JERGN GNUSY VINWW NCFBD KDVFX ASVZQ VOYOG GFRWW GDZTT FOECE CCYWP XERFP HOIAZ HCFDJ TIXVE GNWCC EEDSY VIEHS GUEWE GDJHL VEJHS KSDOJ POKVL XEKVP OOIOW HOIQP QFVAL PCZDL VIFBM WTZHT USKWW NADOE VEICQ NISSC VYRBO KMLGE UTRBO DYDMA TIEQT RLVGT HYFIH KSYAP CLJCE QPVHT VIFBE JEGFP UIUSY VOEPP JACTZ HYFIC UCYSX GTYSY KWZZW FOJCM WTFBE JELBO GRJHL PDZBR VHRHT VIJOD GCFBO CRPQZ PCVFY CNUWH KLCRZ POKVT PGKCF PDVFX KNVAJ QWEAT USZCY DASPL IERGV GDDSE QCFBG GYKVP HOCZZ YIEUT PFFFX CTZCY VOPCF JENCF NDECE GXGZL KNKVP OERBT PGJOJ KNXCY NYKVL VYFIH QUCRF PDVFD VAERL EHIWD VMRGN CRFZA CGVHH GNKMZ PE
    """.replace("\n","").replace(" ","")

    vig = VigenereCipher()

    #print(cipherTools.key_to_num("ELEMERT"))

    print(vig.auto_solve(text=string))

    print(f"\n\n{" ".join(cipherTools.clean_plaintext(vig.auto_solve(text=string)["decrypt"]))}")
    input()
    #Editable toggles and shit
    
    ReverseString = False # me when ciphertext was reversed :(
    keyLength = None
    decipherData = {
        "Ready" : True,
        "AutoSolve" : True,
        "AffineOrCaesar": "Affine" #when this is affine its basically quagmire II
    }
    decryptionReady = True
    AutoICData = {
        "DoAutoIC" : True,
        "StartKey" : 2,
        "MaxKey" : 33
    }

    string = string.replace(" ","").replace("\n","")
    res = ""
    for char in string:
        if char.isalpha():
            res+=char
    string = res
    if ReverseString:
        string = string[::-1]

    RED = "\033[91m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

    print(f"String length: {len(string)}")

    input("Press enter to continue > ")

    if AutoICData["DoAutoIC"]:
        IoC_graph.gen_ioc_graph(string,AutoICData["StartKey"],AutoICData["MaxKey"])
        keyLength = int(input("Enter a key length, 0 for automated pick: "))
        if keyLength == 0:
            keyLength = None

    if keyLength == None:
        keyLength = cipherTools.IoC().sinkov_first_past_the_post(string,2,12)["key"]

    encryptionKey = ""
    if decryptionReady:
        seperatedText = cipherTools.column_seperation(string,keyLength)
        affineCipher = affineSolver.AffineCipher()
        for i,block in enumerate(seperatedText):
            typeShift = decipherData["AffineOrCaesar"]
            args = {
                "string" : block,
                "info" : True,
                "CaesarOrAffine": typeShift
            }
            if not decipherData["AutoSolve"]:
                RecommendedShift = ",".join(affineCipher.auto_solve()["key"])
                if typeShift=="Caesar":
                    shiftNum = (input(f"Shift value for block {i} (Recommended shift: {RecommendedShift} via frequency analysis): ")) 
                else:
                    shiftNum = [int(i) for i in (input(f"Shift value for block {i} (Recommended shift: {RecommendedShift} via frequency analysis): ")).split(",")]
            else:
                if typeShift == "Caesar":
                    affineCipher.possibleMultis = [1]
                    shiftNum = affineCipher.auto_solve(block)["key"]

                elif typeShift == "Affine":
                    affineCipher.possibleMultis =  [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
                    shiftNum = affineCipher.auto_solve(block)["key"]
                        
            if shiftNum or shiftNum==0 or len(shiftNum)>1:
                affineCipher.multiplier, affineCipher.additive = shiftNum
                seperatedText[i] = affineCipher.decrypt(block).lower()   

                encryptionKey+=str(shiftNum[1])+"|"
                decryptionMulti = shiftNum[0]
                print(f"Block {i+1} shift: {str(shiftNum)}")
            else:
                encryptionKey+="-"+"|"


    newString = ""
    plaintext = ""
    if decipherData["Ready"]:
        for i in range(len(string)):
            if (i%keyLength)==0: 
                print(newString)
                newString = ""
            character = seperatedText[i%keyLength][i//keyLength]
            if character.isupper():
                newString += RED + character + RESET
            else:
                newString += BLUE + character + RESET
                plaintext += character
        print(newString)

    #Converts key into words and stuff

    result = ""
    for subkey in encryptionKey.split("|"):
        if subkey!="-" and subkey!="":
            result+=chr(int(subkey)+65)
        else:
            result+="-"
    result = result[:-1]
    result2 = ""
    for subkey in encryptionKey.split("|"):
        if subkey!="-" and subkey!="":
            if subkey=="0": result2+="A"
            else:result2+=chr((97+26)-int(subkey)).upper()
        else:
            result2+="-"
    result2 = result2[:-1]

    print(f"\n\n{BLUE}Multiplier of: {decryptionMulti}")
    print(f"{RED}Encryption key: {result}\nCaesar Equiv: {encryptionKey}\nDecryption Key: {result2}{RESET}")

    print(" ".join(cipherTools.clean_plaintext(plaintext)))