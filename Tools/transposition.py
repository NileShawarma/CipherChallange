from itertools import permutations
import os
import sys
script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","Test","Modules")
sys.path.append(modulesPath)
import cipherTools

string = """
REDMA YMRNI OALOY NATKH OOROU YFUET ERTLR RFDAO NYCER ONUON GAUIR GNPSR OESRE FEAII EYATB MAETT LLIWE ELHBI FAIEO CRNDV OPIRE ETRFH URIET MRAAO ROLYF UUYDA ONRBL LCAOO SOTRR ATSRE OUPEH ITBTU ITHTN AKTUE RHPET OOIAN TFPIE TRHRT NEOIG OHDNR TAEUI VOOBS CRTAA TTSON IFOUV NACOH EVNNL OIAIN OTMIG NEBHE TOPTH UOGEE AURDS TTOMH FEHEL AEUVO VINFN AETEM SNTII EENDD FRYET AHENE UTIRT ERIHD ESOTE IORBH NITTA IRTAS EMINH TAELI TNITK HHLIW ELYRI GOENC ZTAHE TTHYM EEARB RHTEE OSEAO WRHAL WOLIS LBTGI ONITR ODIFT FAIOM OOOFO NYDUS ADAMN TDALI RLEOY LNHTP ATGIH NTCAC WNEON OTMAE AENAR GRMAT TEHNT ULLWS IIALL TPARN SETII CGIDL NUDDU OILWO GBYNE LTUYT HOARE TRPNA RTNOS ODHMT GIONA ATIKH ERRFR DOEMM COEOT PYETL MEPTO TAFRH GABIR SAMRI IENAR OYIUN SRLUT YROTM SKIEH
""".strip("\n")

string = "REDMA YMRNI OALOY NATKH OOROU YFUET ERTLR RFDAO NYCER ONUON GAUIR GNPSR OESRE FEAII EYATB MAETT LLIWE ELHBI FAIEO CRNDV OPIRE ETRFH URIET MRAAO ROLYF UUYDA ONRBL LCAOO SOTRR ATSRE OUPEH ITBTU ITHTN AKTUE RHPET OOIAN TFPIE TRHRT NEOIG OHDNR TAEUI VOOBS CRTAA TTSON IFOUV NACOH EVNNL OIAIN OTMIG NEBHE TOPTH UOGEE AURDS TTOMH FEHEL AEUVO VINFN AETEM SNTII EENDD FRYET AHENE UTIRT ERIHD ESOTE IORBH NITTA IRTAS EMINH TAELI TNITK HHLIW ELYRI GOENC ZTAHE TTHYM EEARB RHTEE OSEAO WRHAL WOLIS LBTGI ONITR ODIFT FAIOM OOOFO NYDUS ADAMN TDALI RLEOY LNHTP ATGIH NTCAC WNEON OTMAE AENAR GRMAT TEHNT ULLWS IIALL TPARN SETII CGIDL NUDDU OILWO GBYNE LTUYT HOARE TRPNA RTNOS ODHMT GIONA ATIKH ERRFR DOEMM COEOT PYETL MEPTO TAFRH GABIR SAMRI IENAR OYIUN SRLUT YROTM SKIEH".replace("\n","")

string = "".join(string.split(" "))[::1]

print(len(string))
input()

def chunkBreaker(string: list, length: int, readMode = "row") -> list:
    numChunks = len(string)//length
    match readMode:
        case "row":
            chunks=[]
            for index in range(0,len(string)-length+1,length):
                chunks.append([string[index:index+length]])
            return chunks
        case "column":
            chunks = [[""] for j in range(numChunks)]#None for i in range((length))] for j in range(numChunks)]

            for index in range(0,len(string)):
                listNumber = index%(numChunks) 
                chunks[listNumber][0] += string[index]            
            return chunks

def swapValues(array: list,key: list) -> list:
    newArray = [None for i in array[0]]

    for index,value in enumerate(key):
        newArray[index] = array[0][value]

    return newArray

def all_full_permutations(lst):#chatgpt'd code here ibr rest is clean
    return [list(p) for p in permutations(lst, len(lst))]
print(" ".join(cipherTools.clean_plaintext("".join(["".join(swapValues(chunk, [3,5,2,1,4,0, 6,10,12,9,8,11,7,13])) for chunk in chunkBreaker(string,14,"row")]))))
while True:
    testString = "HTEUQ IKCBO RWFNO JXUPM SVOET RHLEA YZDGO X".replace(" ","") #Decryption Key is [1,0,2]
    chunkLength = 10
    cribs = ["dynamix","citadelle","pds", "syndicate","gravitational", "waves","jamelia","martin","seismological","phenomenon","neutron", "star"]

    chunkified = chunkBreaker(string,chunkLength,"row")
    print(chunkified)

    input(chunkified[-1])
    print(all_full_permutations([i for i in range(chunkLength)]))
    for key in all_full_permutations([i for i in range(chunkLength)]):
        
        decipheredText = ""
        for chunk in chunkified:
            decipheredText += "".join(swapValues(chunk,key))
        print("\n")
        print(decipheredText)
        print("\n")
        if "DEAR" in decipheredText[:10] and (decipheredText[0] == "D" or decipheredText[0] == "M"):
            input()
        """
        for i in cribs:
            if i.upper() in decipheredText:
                input()
        """
    chunkLength = int(input("End of decryption: "))