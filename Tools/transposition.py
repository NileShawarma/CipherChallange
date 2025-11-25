from itertools import permutations
import os
import sys
script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","Test","Modules")
sys.path.append(modulesPath)
import cipherTools

string = """
YLRPC CHGHS CHLYC UNJUG UJSZB CTJZB PWKGB EENGB CURGZ TJSLZ UECLR XIZSU IGBEP GKBDJ BGBDP JLCTU MCYLZ LSCRU BJZSL JGLJC JRLTL AUMLJ UNTLT JYTAC UILZC BIJYE BLBJG KLSLX GTDCI CJIJZ BUIRZ CTLMC HZLLG ZZKUU SZJIZ BCXDY LOLJJ JZULL AGDRL JEYBG JJLTG EECUC DAIZU ISGTJ BTSKJ IBTLE EBUIL AULSZ ZCGLX LPYZZ USLIG LTLMC HZLLT TSUXY UPDIL GIHRL PKBPG ALYTU ZCITJ YLLNP GICLJ UZBIR LTCTJ JLLDI LUNRJ TNTUU TAJIC NCLXH JCDBG JLITG JLCUE EARZC JBABG ALGJE PXXYS CLCII SJILT RJCLG LIMGB LGKFL USLGG JCLLJ CGJJZ LUAZB KBUGK PXITL NBMBG LZEBL JJLTL SLXGI YCTGI CLIUI JCRLJ ACJWJ BHTPP HBAGK BKDYJ CGLZP HRYGA PPBJD XUSBI RIJLU DIJTJ LLCGU ZPYRH JILLB EEGJI JTNPL LKLGZ XHCLR BJLGL JYLZU JZLTC GKJLJ EBTLJ LOJUJ AJZBC IZUJJ LTLZT AUCUA ZBTNH KBGSK JTIKB PGCXD ZCJIW JILTU MLLTJ NCTJJ LILYI LSCYT PCCHL MLLZL ZPGAD RLJKZ UISUM CSLZL GUALD GLTCJ RZTLI LCBLG EKBAG ZLIBG BJUIK BXURP EAUEK JJXBL GHCLD WGDCT INJUU GXXLI UIJCI KXZUX NAUTT ICALY CUCCG EUTJR CUYJS KJTZG LRYLZ UJMLT CLKXB TJEUZ LIRMC LBUGK CBTYD SZUJJ CTPBK BGKBP GUGEL NRZTJ CLIZB JLSUY TLHJC LXHIS SKLCJ IYURB ECAUJ ZBUBB PEKCY GAZUT LCTJJ ZCAGL IUJTJ BLCTA XZLXS AULCG DZBRU MLLZB KELIK JUXLE BYULJ ZXSUX LLAZJ JCTYT PCLUD XZALR ULTDG SZUJA LTKLI GRXLJ LCGSY NJUCD CIDLG CZPXJ IJZLE YBGJB LTEAU ELCEB ZPNLB HWGKZ UILYI ICPHZ JZLTC BLYEX UYXCG LZCYR PMCTL LLHZL GCDJP XBBZC JGLTY IILCE LSGIY BBBLY ZUILS ZUZSJ UNTLT JISZU XLXLJ GLJGK YUIBA JZCGS JCXKJ BPLKL JGAUZ TAZCU EYGBC ZUWSU TJIZB AZJAL UJZBT ZULJA GLLLJ DRILY ILSCJ UYBXG LXEYB GGICN LGAZP LJDRU IKZIC SUXDY LLCAI IGCTJ EUATD ULTNG UTTAC BZRZT JLLIL XIKCA ICRLI NBXRZ NBUTJ ZLDDC CJCGK NBIUJ SZBLT JEJAC JJCTJ JLTLT JOCLH RLXHZ BLWAR EZUUX LMLLJ JGBGS KNIDT LXUNJ UCUES ZBTJG LSZLU LLZGB JIJLZ KJYLT LCTAZ YIUJD IBLKR LDLTJ RGALP UJDBB PZKBA GXCLX SALKG WACLT JRCUA JDGLT HCTPZ ZCRRG LAJZU CCLDI ABIJE UJUZK XARSZ UJKLT IEBLC JUZCC UXZGB EYYEB ULXXG CZIYJ CLJAC GJTRL LJCGJ JZLUI ZBLUJ JZECS XJSCB ZBYUG BJYII LCILS EYBGJ ZLTLT SUHGK BTRBB BUEEA LXLRJ BJTUR LIMBA LBPGE UTJIO LJJTJ UUUWZ JDIUL CTGDB NIGLT JOUYC ZSZUE JGKTU GLEXZ BPTBJ LUDXY BGDMB PLKLY GAZCT URYIB LSR
""".replace("\n","")

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
#print("".join([swapValues(chunk, [0,3,2,1]) for chunk in chunkBreaker(string,4,"column")]))
#print(" ".join(cipherTools.clean_plaintext("".join(["".join([swapValues(chunk, [0,3,2,1]) for chunk in chunkBreaker(string,4,"column")]]))))
while True:
    testString = "HTEUQ IKCBO RWFNO JXUPM SVOET RHLEA YZDGO X".replace(" ","") #Decryption Key is [1,0,2]
    chunkLength = 4
    cribs = ["dynamix","citadelle","pds", "syndicate","gravitational", "waves","jamelia","martin","seismological","phenomenon","neutron", "star"]

    chunkified = chunkBreaker(string,chunkLength,"row")
    print(chunkified)

    input(chunkified[-1])
    for key in all_full_permutations([i for i in range(chunkLength)]):
        
        decipheredText = ""
        for chunk in chunkified:
            decipheredText += "".join(swapValues(chunk,[0,3,2,1]))
        print("\n")
        print(decipheredText)
        print("\n")
        input()
        if "DEAR" in decipheredText[:10] and (decipheredText[0] == "D" or decipheredText[0] == "M"):
            input()
        """
        for i in cribs:
            if i.upper() in decipheredText:
                input()
        """
    chunkLength = int(input("End of decryption: "))