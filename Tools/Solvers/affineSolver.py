from collections import Counter
import os 
import sys

script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","..","Test","Modules")
sys.path.append(modulesPath)

import cipherTools
from cipherTools import Affineshift,recommendedShiftChiSquared # type: ignore

#Editable toggles and shit
string = """
WINOK BVYBN NOBLI SWECD KNWSD DYCYW OMYXP ECSYX KPDOB BOKNS XQIYE BVODD OBKCS MKXXY DMVOK BVICO ORYGS WSQRD LOYPK XIKCC SCDKX MODYI YEZOB RKZCD RKDCR YGCKG KXDYP SWKQS XKDSY XYXWI ZKBDL EDSDB EVIPK SVDYC OORYG KXIDR SXQSM YEVNN YGYEV NRKFO DROVO KCDSX PVEOX MOEZY XDROQ BOKDK PPKSB CXYGC DSBBS XQKMB YCCDR OYMOK XIYEK BOAES DOBSQ RDDRK DGOCR KBOKN OOZNS CVSUO YPDRK DNBOK NPEVS XCDSD EDSYX CVKFO BIKXN SBOTY SMONK CIYEN SNKDD ROFSM DYBSO CYPWB VSXMY VXKXN DROXO GRYZO DROIL BSXQD YCYWK XIVYX QCEPP OBSXQ ZOYZV OIODS MKXXY DLOVS OFODR KDKXI DRSXQ SWSQR DGBSD OYBCK IMYEV NWYFO DROMY XQBOC CYBDR OZBOC SNOXD DYGKB NCKTE CDMYE BCOSP IYEBY GXOPP YBDCR KFOXY DKVBO KNIZO BCEKN ONDRO WXYXO DROVO CCWBL KLLKQ OSCWY CDSXC SCDOX DDRKD SCRYE VNROK BIYEB CMROW OKXNS GSVVL OSXVY XNYXX OHDGO OUPYB KWOOD SXQYP DROQR YCDMV ELSPI YEKBO GSVVS XQGOW SQRDW OODDR OBOYB SPIYE ZBOPO BKAES ODOBC ODDSX QKDDR OKDRO XOEWS BOWKS XWINO KBVYB NNOBL IFOBI DBEVI IYEBC MRKBV OCNSM UOXC

"""

ReverseString = False # me when ciphertext was reversed :(
decipherData = {
    "Ready" : True,
    "AutoSolve" : True,
    "recommendShift" : "chi",
    "clean_plaintext" : True
}
decryptionReady = True

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

def recommendedShift(args: dict, mode = "chi")-> list:
    match mode:
        case "frequency":
            return recommendedShiftFrequencyAnalysis(args["string"],args["info"])
        case "chi":
            return recommendedShiftChiSquared(args["string"],args["info"])
def recommendedShiftFrequencyAnalysis(string: str, info = False) -> int:
    frequencies = Counter(string.lower())
    frequenciesVer2 = sorted(list(frequencies.items()), key= lambda thingy: thingy[1], reverse= True)

    maxDetails = ["",0]
    potentialKeys = []
    for letter, freq in frequencies.items():
        if freq>maxDetails[1]:
            maxDetails = [letter.upper(),freq]
            potentialKeys.append([letter.upper(),freq])
    
    distance = ord("E") - ord(maxDetails[0])
    if distance < 0: distance = 26+distance

    if info:
        print(frequenciesVer2[0])
        print(frequenciesVer2[1])
        print(frequenciesVer2[2])
        print(frequenciesVer2[3])

    return distance

if decryptionReady:
    args = {
        "string" : string,
        "info" : True
    }
    if not decipherData["AutoSolve"]:
        RecommendedShift = recommendedShift(args, decipherData["recommendShift"])
        shiftNum = [int(i) for i in (input(f"Shift value for block 1 (Recommended shift: {RecommendedShift} via frequency analysis): ")).split(",")] or [1,0]
    else:
        shiftNum = recommendedShift(args, decipherData["recommendShift"])
        print(shiftNum)

    if shiftNum:
        string = Affineshift(string,shiftNum).lower()
    
    if decipherData["clean_plaintext"]:    string = " ".join(cipherTools.clean_plaintext(string))
    
    if string.islower():
        print(BLUE + string + RESET)
    else:
        print(RED + string + RESET)
