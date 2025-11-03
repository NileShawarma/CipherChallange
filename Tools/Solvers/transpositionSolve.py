from itertools import permutations
import os 
import sys
import random
import math

"""
If the cipher text is not perfectibly divisible by the chunk length, the remaining cipher text is ommitted
Uses simulated annealing
"""

script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","..","Test","Modules")
sys.path.append(modulesPath)

import cipherTools # type: ignore

string = """
FOUIYRREAEDNGAIHSTTIEIMHNYEDABAAGEDIKIANLDTLEIENWCWYTOBEOSHPDGITIASUTLVILREACELNYDISNAEICTIMSFAILATLIETLVEYOHNMYBUAMONEYYOPLHITHEFYAVEHKLLEIDETEMETHHNSETILEWITRLAVLHBENEEITRDSBTEIUIUNDNNRYECTDFPERTOOMLTHALSCIEOLEDAMAITISSNDEALTHALNWSEEGNCAEEINISHWOTELTHRDINAEREILMWBKNLEWTOONVRYEENANOETESDHOYOTRWATFHHYTTEIDTREDWIOOLEHLBALIEDEEWNNINOSFTENTHYOPMHITHESTOUAYILKWLETHEPSUIIQTOREFOFONWYURROAEASKWLLSESORAFIEMMNNMEYASAMIJLADEILARAMNIAADPRTMAYESLROSIPNLFOBETISRHESTMSILEHSTRITEMATSYEPTTMOXPTEANMLIRLEYONHAIWHPPTANDIEETEHNHPTHOETOTANIGLHNKITIEILEWLEHAVRPNAPEANTGIEYNHSIATDCWSAEAOERGVMNTNENTIIITVEAIORETPAEFPRRWOOALINRDHCHWINRYECTONPIILBWLSSEEOUETCRANOHTNCAOECACNRITHKTTORAWDSALIMSTLOEEAHRDHENTUNTQAMECUTNLOHOYEVGRLTIOUNSLOIKLYIEOIVTGBRTEITITHOONISONTHFONCHIGNESAGRVAPIYILCWBABLEOUTSLADSENWLLOIERESCYOWCHOFEYULBOEATHAUTDPETEDALNSTNWOOOOUHYRANAEWOYDHUHIOTKASNHOTTMSGINOAWSNIAURAETBTWLUEMYHNRENFIMRTDANUGISETEGSTATDHEOUWCDDALATOMPSOTHEFTCHEEOOGNLWDEYEEOPVLDOREFHLITEOROGPETIJCAEXWSIEDCTTHEATOSIPSIITBLEOUISPANRLATOWSULDBIEAVBHORAIUTMPLEAEFLTLERITTTRSOCGRAKUACOPIITTVEONISHWETEOIGBRNLLIAWHOYEETOPDOELMDHSPTEEDORAIEAFDMRTSANASIWNERITSEDETNHEITAKEMRIGATNGEANLDAWNSTSAIAAOFWYELISLGRONPUTSDCYNDBURTAESDNGNIOMEHWEPRMSPGAOAEWATIMRESONERITSEDETNNDIURTAESDNGNIOPOHWIICLTLDEAISPRASATHEDOGHRUPPUAOAIOLTIWANTAILSMINMLOLSFIEOOURMRALRERASAEFXPOERISETADIENHULSOHVEDAELIRAETHSDDNGEARMUESHARCEIRTLEEARHWAESGMEARDPMNTTETYNADMXSAIWHEATOENPTILFTARHIOTTOLSOOEUTBEASSDTENAWYIRTFTENSCUYVTRRIOESOSINFITAGNLWILOGNTNILIGELNEAECECIGNSNDEAOERGVMNTNETTRSOCSMAKLGRALUACOPIITTVEBYISACHMTNONIGIEBLNHVIEAUTOORNWNKOEPLTMTSSAEALGMLOPSRUNLUICIGTDNRORERSCEITLTHLSPSSEDNICYDTHAAEAENDGSTJTASABUTUEVOTRAREYSANMMFCTUARRIUETEWNHSINETLDICUGYNNDMXWAIETHHNYECEBMAWAEROFAEUWOORKHERTARAYRGDFNERYNODMXTAIRCROEIUSUTNHEOTRNTIIRSCENEEIHMWSATAAAZNMNTIIGEEHMWDVEAEYESRRUCEOREOUWCDANLWADATNFRSTITEFTHEDORETDOMOHTWWAWNTEADENEGLTHTYYROEBGTUUHRUNSOTWODOKNGRINMAOSLROLGPYNUDMCTAIAKIRCGNDNAOLOFLIGSWNMOFOEHRETEETTCNAEDRGEIWISREDOKUFOOTMSERYFHELTOENPTILOTAORSFUFWAOTEODRTTCTEENPRADVNTEEEROTRIMBRSTENUWEEDEDAAWDTCLLEADTTEIEEMHTBNKPADTAAAAEOBSBHAFEIURVOLEMATLTEPAWICSHWWOHELUSUDTMAEOCAGTHISTANIEOLVLNENIRFFTACOHITGLIIHHARGTAOFESNERITSNOETNHAOEEERDVOKEWROTHDNSORISOPATFTRNTEAEDBSRCKTANBEIGOESFRWHAOENDADOANWTOIHTHCBSEOAHTETEPATMLSODEMLINELCMMGONCAUIINPTOTERATSETNBENMWEMEREBOATSFRORERSGRITUWIOPHUTTOHTETEPATMLSTWEISMPAISIBOSEOCLTRYOARTEAURTMELIOITMNRNGOISHEATAARDTTWAAEFRTSAOIGOHFRLHOVANIELSIAYIAISREMYSDOCECNNWIRSHHETTEDOHARSEFERHAACDNATYIANMXTATDHAWHWSNWAEIITRSNDCEOUTSODOENEMORMTFOEYNHSIATDCTEYEHRMIPOEUSSDAABDTSDOAEMTHNAMTIEAAMOCLESDDLVLOEEEBYPDHDETEATMPRNOFETEENDFENDCAHPRTEJCTOEOTICNUDINEWSMTARSUOECSSCEUTHFLNEHAWDARADDOHETPASOERAMTEFIGOHQALHUTDAIYAILTFETHLDTMPEEAKABNDHENTLORAGTMBIHGNTEASOTOPELWRARDEOLAPLXMSHAETCOSTLLMAEYCEDTHHTETEPATMLSFCEOUSEORLTOAOTATFHAJUWSTHASCTRTTEEEIHRAORSWDFDLOFERIFNEBECTEEEWDSCNISINUSADCGNRYIARGUTNONTTAACANAKNSEDOUITCRSRVYECCAIEIVENNTGASIEVETEYELRDDDFUENASATOLIYNENONIDRTREFNDOIHONTERALEELTDPONMIYAWREXEXITECDYWEBAWEHTAACHDIVEHEBTADUTERSHSLTEURLLSODNTEIEDEHYADEMNMREDOCURACCANAYFRTDOAWEHTEDENEMCHDUETEBTDTARAHSYTEDCANIEERTWHPPEATOBYOIEALGDHANTIWHTSNREEILSEAITEHDHWAROFHYWTERPREEPREEATGODOTIEIRTCODOVNCNIMSEEYFHALTTESTHNICYDTHAAEACEDCSOASTAGELRAABDTSOFAEXSTEINCOIGMNIMUAIOCTSHANTTEYTHEEUWRIGTSNETROXCBEATAIOHVRLTUAMLAEPEBUTSTEMTHRITOEOGHHUAOUTBITHTTMREEONIKULLITEYEMESEORSDUFWAOTEASRWEINSERALGEOLDWRTACATPTTKARSTENAWEHTEUSRSIIOPCSYSULMLAIIAMORLTHOSCEGRROPEDAHNIBADGNTEAWNDOORFTEIEDSHPYDISNAEWCTRNOEEJSTTURCKTANTEIGRRIROTCTSAVTYIIUWEBTENCREUAGORNITIGMNGAORUPGOTATSHHYHTEDENAPTATERDNOEIDRTREBILOUAENDNYLOCCADIPEOBEAFAIOHVRLTUAMLAEPETHTSTOUACDEULBETOSDPTFSOTREUUTACATSEFKBRTHOEYAPEHEEDPNHSYTEDCANIEADTHNCHAALESILELIHEWSNTATOSOPILESBOOOTCDNARIEHETTRESIRACHERRGRPOMEWAMTOUIHLAVTENTHIGIOWERDGINIAFOTLTRIOPTARNMIANTNIEFDRCSEOUOREDUFRTFOOTRSNCINAKTEMGHONADWDOUNFDLLNAHEVTEDNCIEWNEEEDDBEETHEUTWREYEHEXTEETSPROUSNTNWEADUTHMSVTRAEGERIGDNAEAAMSLRMWHOERTHEEYAVEGUONESCOIEHEYDCMAHWETSOWANNVIIEALETBHONTEYUELQTONSIAWHWSTEREHROTONTOUIWDEFLBKDOAECIWNESFFAOCALIIYEALDIOUDWDAVLHNPREOTCTOEOBUINWWETEEALRVALEUBOHETTADTMNAWAHTTEKSHYOOETRURUSIALVVNVEIEKEWRNHNATEEFTMOEIRHGTEYLHSDTUEFKEOAYUIMSIEBCDTHEUTDDAYISRESUEHAMTSEHTHDIEADONADFUALTRASECUIOPSHTATEHUHWMCSRUATTESEHNICYDTWEAEEHERTELERAPRTXEIESSNINAPOEUTGBATIMRADINNATHHDEGEEDNODICNTHIGYATEWHDUCECRESAULYFLUWEBTAAGMNDOPETATALNIUSVRNHEITAABDTSENAEIEAGNDTWNILHAILEEEVBTIGNREEDGROGBLNFREEOOREYUDHIATIISSTEIGDSETONDNECIFEERTVCPYYOFUROOLORAGTMAIHDOENTCYPNRCUCTRAELILMNTEEOTHSFCDEEOEDERNIGIRNUUSTNBEWALLAREEEALNDTROOFSUDMTIGSYNUNETXADTTNEEMHTBNKPAILSWLFERUFHSATEEATMFATHESIANERACEINTIFNRGSNUEWHEOTIUSVRSELIRAEDESEONWCICEVNTESDHNICYDTTOAEUDAFNAKEHCCLLROCIVETINOENWYARADOANTLWMLORINATOORTWTERKHUDEENCVEROAFARSATHRSYEREWCNCEOREDENEILHWBHALEVSTRENBAIGEINSLDTAEAONOFRSFIIETRILEGNSNICALOIEIAMDRFFTACUTIBEILHWBDILETIBSRTNGUIHSFTILANIETEVDHRSTIUAMAOSYERNSESAVRHCASEWTHNIUALOTRINETTEMGHATIMRIGONSDTTOAIHEHSAALHSEDYRAAKEHCAUMDNEOFBRAKUBCCMPPONANAYAPSDPREREVADUSNETHSDMSAEAITRDSBTIIUNECOMAISHNWHAMEELSVABENOEEVILAGTRNAIFOALTEIRHTLLNEGNCIESRVEECSWIEHVEEAOEANROTOSNEIEBLEHEVTOERGVMNTNEAECSRNECONEWITDHHITTADESNEYRVRAONESOELTBEETIVEMAHYBOUYEBSTREOEOHPSOPFTIGTPNEARHMWSAEEEROFPALYBBOORNTHSITISRANUCPONEIYWLCUDHOLVREAEANEMIJSTDUHTWTAMGHEIBONTEHRUTETOUNHHNAGULTOBERGGTIRHEETEDMDANWIASCTHTHTASAWEPIKEGHENTEILSFSAFESWDOEEOPLNTNNGAOVNGIIPNDUAERGWUYUNEOTOEOTTERIH
"""
cribs = ["my","dear"]

#Editable toggles and shit
ReverseString = False # me when ciphertext was reversed :(
decipherData = {
    "chunk_length" : 5,
    "startingTemp" : 20,
    "coolingRate" : 0.996,
    "max_iterations" : 5000,
    "patience" : 2000
}
decryptionReady = True
ngrams = cipherTools.ngrams()
string = string.replace(" ","")
result = ""

for char in string:
    if char.isalpha():
        result+=char
string = result

if ReverseString:
    string = string[::-1]

RED = "\033[91m"
BLUE = "\033[1;36m"
MAGENTA = "\033[1;35m"
GREEN = "\033[1;32m"
RESET = "\033[0m"


string = "".join(string.split(" "))[::1]

print(f"\nString length: {len(string)}")
#input()

#converts cipher text into nth long chunks which we can acc manipulate, im not sure why i decided to use 2d arrays for this but im not touching this function its too delicate
def chunkBreaker(string: list, length: int, readMode = "row") -> list:
    numChunks = len(string)//length

    match readMode:
        case "row":
            chunks=[]
            for index in range(0,len(string)-length+1,length): #plus one cus arrays 0 based and range doesnt acc hit the max value
                chunks.append([string[index:index+length]])
            return chunks

        case "column":
            chunks = [[""] for j in range(numChunks)]

            for index in range(0,len(string)):
                listNumber = index%(numChunks) 
                chunks[listNumber][0] += string[index]
                        
            return chunks

def swapValues(array: list,key: list) -> list:
    newArray = [None for i in array[0]] #Makes an empty copy of the given ciphered array

    for index,value in enumerate(key):
        newArray[index] = array[0][value] #Each value of the new array is given the nth key value of the ciphered array
    return newArray
def decrypt(array : list, key: list) -> list:
    decipheredText = ""
    for chunk in array:
        decipheredText += "".join(swapValues(chunk,key))
    
    return decipheredText
def all_full_permutations(lst):#chatgpt'd code here ibr rest is clean
    return [list(p) for p in permutations(lst, len(lst))]
def shuffleKey(key : list):
    clone = key.copy()
    i,j = [random.randint(0,len(key)-1) for i in range(2)]

    clone[i], clone[j] = clone[j], clone[i]
    
    return clone
if __name__ == "__main__":
    anneals_data = []
    for _ in range(5):
        no_improvement_count = 0

        print(f"{BLUE}")
        chunkLength = decipherData["chunk_length"]
        chunkified = chunkBreaker(string,chunkLength,"row")
        acceptedMoves = 0

        key = [int(i) for i in range(chunkLength)]
        
        current_key = [] #Randomises key
        for i in range(len(key)):
            current_key.append(random.choice(key))
            key.remove(current_key[-1])
        #print(current_key)
        #print(chunkified)
        current_score = ngrams.score(decrypt(chunkified,current_key))

        best_key,best_score = current_key, current_score

        temperature = decipherData["startingTemp"]

        for iteration in range(decipherData["max_iterations"]):
            new_key = shuffleKey(current_key)
            new_score = ngrams.score(decrypt(chunkified,new_key))

            diff = new_score - current_score
            if diff>0:
                #print(diff)
                current_score = new_score
                current_key = new_key
                acceptedMoves += 1
                no_improvement_count = 0

                if current_score > best_score:
                    best_score = current_score
                    best_key = current_key
            else:
                no_improvement_count += 1
                if temperature==0:
                    continue
                chance_of_acceptance = math.exp(diff/temperature)

                if random.random() < chance_of_acceptance:
                    current_key = new_key
                    current_score = new_score
                    acceptedMoves += 1
            if no_improvement_count > decipherData["patience"]:
                print(f"{RED}Early stopping at iteration {iteration + 1}{RESET}")
                break
            temperature *= decipherData["coolingRate"]

            if (iteration + 1) % 1000 == 0: #blank screens do be scary

                acceptance_rate = (acceptedMoves / 1000) * 100

                print(f"Iteration {iteration + 1}: Best score = {best_score:.4f}, Temp = {temperature:.4f}, Acceptance = {acceptance_rate:.1f}%, Key = {best_key}")
                decrypted_sample = decrypt(chunkified, best_key)[:120]

                print(f"Current decryption: {decrypted_sample}...\n")
                acceptedMoves = 0

            elif (iteration+1) % 250 == 0 and (iteration+1) // 250 <5:
                print(f"Iteration {iteration + 1}: Best score = {best_score:.4f}, Temp = {temperature:.4f}, Key = {best_key}")
                decrypted_sample = decrypt(chunkified, best_key)[:120]
                print(f"Current decryption: {decrypted_sample}...\n")
        print(f"\033[1m{RED}LOOP {_+1} INFO: ")
        print(f"{MAGENTA}Recommended key: {best_key}")
        print(f"Score: {best_score} {RESET}\n")
        print(f"{BLUE}Decryption: \n{GREEN}{decrypt(chunkified,best_key)}{RESET}")

        anneals_data.append([best_score,best_key])
    anneals_data = sorted(anneals_data, key=lambda thingy: thingy[0], reverse=True)
    
    print("\n"+"="*46+"\n")
    print(f"\033[1m{RED}MOST LIKELY KEY IS: {anneals_data[0][1]}")
    print(f"Most likely decryption is:\n    {GREEN}{decrypt(chunkified,anneals_data[0][1])}")
    print(f"\n\033[35mOther likely data: {anneals_data}{RESET}")

    """
    while True: 
        scores = []
        testString = "HTEUQ IKCBO RWFNO JXUPM SVOET RHLEA YZDGO X".replace(" ","") #Decryption Key is [1,0,2]
        string = testString
        chunkLength = 3

        chunkified = chunkBreaker(string,chunkLength,"row")
        print(chunkified)

        input(chunkified[-1])
        print(all_full_permutations([i for i in range(chunkLength)]))
        for key in all_full_permutations([i for i in range(chunkLength)]):
            
            decipheredText = ""
            for chunk in chunkified:
                decipheredText += "".join(swapValues(chunk,key))
            #print(decipheredText)
            if decipheredText[0:6]=="MYDEAR":
                print(decipheredText)
                print(key)
                input()
            print(ngrams.score(decipheredText))
            scores.append(ngrams.score(decipheredText)) 
            '''
            for i in cribs:
                if i.upper() in decipheredText:
                    input()
            '''
        print(f"\nMinimum fitness: {min(scores)}\n\nMaximum fitness: {sorted(scores)[-2]}")
        chunkLength = int(input("End of decryption: "))
    """