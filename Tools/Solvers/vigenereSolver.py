from collections import Counter
import os 
import sys

script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","..","Test","Modules")
sys.path.append(modulesPath)

import cipherTools
from cipherTools import Affineshift,recommendedShiftChiSquared,ic,chiSquared,recommendedShiftFrequencyAnalysis # type: ignore

#Editable toggles and shit
string = """
ZCZCO IBLSQ YFVMY IWPZP YSXDC JZOJX DYHZK AHIWQ FVYIW EIVCN VASBU OEZWJ IZXTA DYHZD VWPFO KIBYW PSFPS INGBX KAHEY ANBVX ELUKY NWOSF VIBYP FOKDU EPGGW KEJNM AKRRG WQSVF RREDW KGRVA WCLGV PHIBF GGLWR CKRRV HCGJC PVQNI CYHWX SGZXR WOKSE KEISG ZCSAK PMSOZ YSERW EQNRU YBUKY PELJV XGMKL GNSGL JMDRI ZIJRT FBGLA MFZQV RWRCI KAHSC FVWNM JWCLB FYNCG KQHEN YBKOR SBBIV BRGKK DVXFI NCBVQ BXEYH ZXTSQ PRVKY AEJZF XYCOJ CNYHV LPCXB RWOYB USSSP FSICT IPUWE NBJPF WJYCT KPHLX VXUWC LBVWG JCJSA KATSI IGLEL UPYHL WTSEO TSPGO KOQAE RVLCV XEQCW DUIDG UYOFX EKDFB GEJAS KRNXS CQFXP PQBSK RVWOR OXOBJ KSFTY YPWZC IKGMK LOJAH MYIZP KFTKQ GZLYI UMIYK IIPMZ UEFXD YHUSF THYBE SAKPM AVOGA ERVKR RTNCG ZNRRP QCFXN RZMBT OUIDY GRCFY NYBTO GLWRH YOTSR CFEWR RPQIG ZBVPQ VZCCP WLHYS AKOUW CVZSR CJVBL UQGQB VLMYY BEYGT NMAZC RXKFC CNZCE LJVCG SNQHF QRXDC FZPGL AWHYS AOPFS ZBVRP CFVCG WWPSS OGXAP GVBII ZCZJO JLAPS JYJMJ LWEQG LAGFW SEQYM ADSGQ ALHEY JMOGB RVYSQ PWEDR VAQHJ SGMOA FLMVE HRVRD LSQYB USPSJ TWEMR XDCAF PGLAT OCERS BRVZC CVKNS IDLEJ BMFEN VAZSJ DCPWA SUDBE YOIZB RXDCS MSQIJ ASWYE YOGII QRCKS HFLRK XMFIY JSNQH VKYEY MBTVH WETSU OZSJQ HIKGM KLCWD UIRYZ LOBJP FSGBB HQAHF BGSLP CMSQI WDICV RVZCG TBVTP GCEYS XDCDC YGMJM FUOEX DYHZM NRBGB RVYCL CFJEN HAKMW BVIJB GKYPS IKWKD BFWAY ZXTYO WCLBF EJVWF EFPUK CCSAE NM
""".upper()
ReverseString = False # me when ciphertext was reversed :(
keyLength = 7
decipherData = {
    "Ready" : True,
    "AutoSolve" : True,
    "recommendShift" : "chi",
    "AffineOrCaesar": "Caesar" #when this is affine its basically quagmire II
}
decryptionReady = True
AutoICData = {
    "DoAutoIC" : False,
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

def seperators(string: str,keyLength: int) -> list:
    newArray = ["" for i in range(keyLength)]

    for index in range(keyLength):
        newArray[index] = string[index::keyLength]

    return newArray
def shift(text: str,s: int) -> str:
    return Affineshift(text,[1,s])
def recommendedShift(args: dict, mode = "chi")-> int:
    match mode:
        case "frequency":
            return recommendedShiftFrequencyAnalysis(args["string"],args["info"])
        case "chi":
            return recommendedShiftChiSquared(args["string"],args["info"])
print(seperators("hello",2))
input()
seperatedText = seperators(string,keyLength)

if AutoICData["DoAutoIC"]:
    for i in range(AutoICData["StartKey"],AutoICData["MaxKey"]):
        seperatedText = seperators(string,i)
        print(f"Key: {i}")
        seperatedText[0] = shift(seperatedText[0],0).lower()
        seperatedText[1] = shift(seperatedText[1],0).lower()
        seperatedText.append("hi")
        chiSquared(seperatedText[0])
        print(f"IC No1: {round(ic(seperatedText[0]),8)}, IC No2 : {round(ic(seperatedText[1]),8)}, IC No3 : {round(ic(seperatedText[2]),8)}")

decryptionKey = ""
if decryptionReady:
    seperatedText = seperators(string,keyLength)
    for i,block in enumerate(seperatedText):
        typeShift = decipherData["AffineOrCaesar"]
        args = {
            "string" : block,
            "info" : True,
            "CaesarOrAffine": typeShift
        }
        if not decipherData["AutoSolve"]:
            RecommendedShift = recommendedShift(args, decipherData["recommendShift"])
            if typeShift=="Caesar":
                shiftNum = (input(f"Shift value for block {i} (Recommended shift: {RecommendedShift} via frequency analysis): ")) 
            else:
                shiftNum = [int(i) for i in (input(f"Shift value for block {i} (Recommended shift: {RecommendedShift} via frequency analysis): ")).split(",")]
        else:
            shiftNum = recommendedShift(args, decipherData["recommendShift"])
        if shiftNum or shiftNum==0 or len(shiftNum)>1:
            if typeShift=="Caesar":
                seperatedText[i] = shift(block,int(shiftNum[1])).lower()
            else:
                seperatedText[i] = Affineshift(block,shiftNum).lower()   
            decryptionKey+=str(shiftNum[1])+"|"
        else:
            decryptionKey+="-"+"|"


#Converts key into words and stuff if its caesar cus i hab no idea how to do it for affine
if typeShift == "Caesar":
    print("beep")
    result = ""
    for subkey in decryptionKey.split("|"):
        if subkey!="-" and subkey!="":
            result+=chr(int(subkey)+97)
        else:
            result+="-"
    result2 = ""
    for subkey in decryptionKey.split("|"):
        if subkey!="-" and subkey!="":
            if subkey=="0": result2+="A"
            else:result2+=chr((97+26)-int(subkey)).upper()
        else:
            result2+="-"

    print(f"\n\n{RED}Decryption key: {result}\nCaesar Equiv: {decryptionKey}\nEncryption Key: {result2}{RESET}")

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
    
print(" ".join(cipherTools.clean_plaintext(plaintext)))