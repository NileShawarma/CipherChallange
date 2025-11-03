from itertools import permutations

string = "EAMYD KERRO THSMI GRHOW FYATI TOING RFHEA YOROM ASUIW CECON DTRNE THHAT IRETH NDTEE OFAYS ENSIL INCES OUCEY STRLA SAMES IGGEM AVHTH DIEIN EDCAT TYTHA ADOUH NGCHA OUEDY NDRMI UTABO AROUR GERAN TTMEN OCHED NTUME PRYOU DEOVI EXDIS METRE ROLYP INMIS DMGAN RTYPA SANER EEREK SENTO REEMO YOARE KEULI OBLYT LEEAB BTTOO MOAIN AMRES SIPLE MTFIA NVOCO EOINC RSTHE NVTOI THEST TWENI DBOUL ODEGO ROTOP ETVID WIHEM VITHE CEDEN HEOFT UEVAL HEOFT URIRP SECHA EHSOM HIAVE DTNTE THHAT ARERE HEEOT YSRWA TTTHA COHEY PRULD EDOCE ITBUT KIHIN GHTMI POTBE BLSSI DCEAN AIERT WONLY BEULD TEBET RYRFO FWOUI ULECO GODNE TETIA ETSOM GFHIN RAAVO TOBLE PAALL ESRTI OUOFC DMRSE EPAYB TILOT NONGA RCTHE SEOUR MAAND KEYTA EPSOM UAERS NTSIO MMOCO OOITT ROURP ALPOS YOBUT VEUHA URASS STEDU YOHAT VEUHA EISOM UENFL ONNCE DEHIS IOCIS NDNSA REIAM NGLYI OUONY ELTOH ALPSE DETHE OUALY ITRFA LFHFU NDRIE INMOL ARO"



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

while True:
    testString = "HTEUQ IKCBO RWFNO JXUPM SVOET RHLEA YZDGO X".replace(" ","") #Decryption Key is [1,0,2]
    chunkLength = 5
    cribs = ["dynamix","citadelle","pds", "syndicate","gravitational", "waves","jamelia","martin","seismological","phenomenon","neutron", "star"]

    chunkified = chunkBreaker(string,chunkLength,"column")
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
        """
        for i in cribs:
            if i.upper() in decipheredText:
                input()
        """
    chunkLength = int(input("End of decryption: "))