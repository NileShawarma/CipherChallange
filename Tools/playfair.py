import string
from z3 import *
import random

ALPHABET = string.ascii_uppercase
cipherText = "6WINFVHJU2ONTIA2P256WLHP5845RDQD89HP5CFNRFYVCOVP6WVXONUPOF89HPPVOVVJVP3PEYAWPWY8RDNPE5CPAVFN75W6AWBYJR2U4B56VZVOYP6WINFVRZEYP00PWLHP5845RDQD89EYOAAU96UY2BHRPW0EN3RFYVCOC2ZVZHWPHYITHP6AOGQD2UOSCOAWNFAWIEBDMPKDV5F98OHPJR8448HYWVBYRHFROVE5TNAVJOYOHZNFNHVP98WVW6YBAR0EBVDR54O8CWUYQDHPOVFVTMZH89BYVJP0UV0PYBARRJN6NF2BWLHB5VAWOVTNPMC5BWVPIHFNNFAWHZAMPMYDVONFAW0PLEN3VF5CACMPN3H3GO560EBVDR56AW2EVO2B75HPFV75MPYPA6AWVAOEEYN3RZHZ5C89ONPMPWCRPMZRC24BPC56HZTNYURBZHAM5CACYPC5DR2UYXRANOVD5UEY0BC5VO2THFAMACTETNPWUAIETMW62H56IWIADRHPJRDYFNOH89EYAW2TYNARBXVP0EBVDRAUFNRAWPDEMBTMPWDRCKQDDROCHNFNE0YUO8VJ8456AWPWPMFVIE45IELCDRACHPPW8995VOCWNFVAHWYOPMWRAUN6R895WK2CRDQDRFUYPURYZHHFAMACN6RJLEVON3RJE5CTYBZHPDB2BYRH86JH8OCHFNXHWEHWBYCORFOJSA8O0EYBARYPRFHYBY6AJADRBAPWUPOANZBYRBRDHNOV58A396QIVOPWOVIEAFKVV5VDOCHNFNEYSOEYAWOVDEO82BVAVPOFBVPMTN89YOHZVOP0JRACHPOCLE8OWPVD58PZVPW6NADRIKPZVP0EBVDR56CK6AWNRPVOIVYCUPW6W62PE50PU5YPVPVIEWVFYPCKHPOVHPOUYAQOACYDHPDPDLDPCKTN56ZHYPVA6AIAHPOVHZFRNP456AC06759TMMTVF89HPAVAUUPBVRA2PXYFVHPPWUAVOCPIE2CQDENOD0PTBPUPYVPCUE246VOBWPYVPCARCU5NZAVAYNPE5ENOD0PTBPURPVF56H2U2EDRBVAN3VF5C95PCMPCTWLHPOU98VOFP6WAYACHPAMAVXYVAHZNPWHAY98V2HPPCEDPGAR5898YVYAQONPOEFVYBQDCAUY4POVDRDKAW6AP0ZRDRBXVPNEHZP3AY89DR98V2PWY8A6IVFRHZVPUPMPIQ64RBDVPUYAQO6AW6BD2PYDQDZVYPVFAUVPVO6AWNVPAN5U6ANPE5HPKCVOPWFVYBSAMTAVU5BYJRRAEDUYCAHWHPPWEYSOEYAWOVNZOVAUE2AV98VIACITIEAEAVYBARYPKUOVH4AYOVITVZTHMP45OFWERJARNOHPOVHP6A98VIPUVPRO5UKIRDUFBWVP48UAO8PZNPULAIZV84OV6AWYYPBV6ACKRFUYPUZO8OIKAI6ABWVPRN8O75BWYOPMFVH3RNBYPHNPWPC2UAONPUVP98HYWVPWPVOCOF89HPPWYH6WBYY8ANBYPHRBFAAU96UY2BHROHERYWDRCXNZBYP4AYOVCPR8AWHPOCOP84FVJORAHTOUARBWVPYOIN563VYDHPHPJR48UAVIE2FV6NONRDQDEYNOTY2BHRYPVFAUNPULOWIEC5YATMWT5895RAV2EYFEP0V5YPEYVOVA2CFVHPACE0KDPUNPUBEY0BCPIAVAITHPFRAURPVFOD2CHZVPIEHWO82PASPWY8AF6AWN56BHRBPZVPTR6WEDU5N3HZA2EYV2EDRBVANFAWAQAYMPWXOCVZHWRBQAPDMPHPJR48UAV2ZVYH5CODAPYWCAVAE5SAO8LURPVFUAYAQOYPVFOE59P22PYDQDHPAMKUE04B5898YV98WVCAOFUAYDBDMPUKHYEYOYSAMTAVU5ITHZ56BHPH67DRBKFRBYY8AFDRRFUYPURNVPVOUADEHDFVZHNP45BYZVDRIKYVPDB2BYRH898O5UFNWBBO2P0EYBU5IERA2CDEAWRFUYP0HZ8O3VDR8OCAHYPRPM48YVA6YBARHZAY56HPOVHP5CPWRAYBC5DEAN56A398NIYPUPBDBHVP0UNPHN56VOIADRDQ8ORPNDUAONAC8YQDBYHPOV56VOHPFRAUBYRBRAYVIKE5OAC5HWTNAYEY0BVF58YVDE46TY2BHRDRUPV2RFAZON96VOTNB2AU56VOCAWYDEUPBWPYVPOH5EAVYBAR89IESA2BBUHPOUYATMBWYVRDYBAFUP6WDRYP6N5648ANBYPHNPHN5648HWVPRNEY0BCTB2W6YAH2WYHWVPYOAYRD0ECK48JRARACITRCP2AVU56AWXVOAC89IEYVVFHPOVOCNFOYQFDRTNPWUAIAYDHPEYYH5E562BQDHP5CEDRBVANFAWHPOCNY8OOGQDRJUB6ACPWYA3OJUVBH6AJNE2PUC2FVC248N3RJTBPUEIARRCVD58YVIKE5OAC5HWRFOJLEAVWYQDW6QDOVUAON56BD1BYCBHR8OS59ZVDRBX89EDPUVPYHVHNPWLYBC5NZVPRDWB85FAPYVZBYZVCTHN5CZVWH5EOVRYPMBWPYVPUPLEWPYBARYPVOE5P0EYOF5UVOHNVPVOUADEAOFVNP45CAHZDRRN5CZVHNVPVOUADEADRAWBFRAYBYRPVHOYQF89WYVJEROVRN5U6ARAYBHPFNCPAVHPKCVOPWFVZB8RYPIHDRBXRBHFO8CFBUYPBYVJARBMZVY8APOV56WLHPPV56HY89CPEWHRTNOVAU56VO6NACITHPPUVTAWOV89HP59P03HHPPWINCR58YV0EBVDRFVUAONPMGOPUVPVZANRPVFVPPWVOMPFNFVHPPU8OVOHW89C5BHN6UPHYNPUBONE5RJZHN6WIAYHWPOEYBQO8GENFAWARYPHPPC0PCANZRBBVINCR58YVCKVANOYPOFEYHOAYOVJRDRWYVOBUCTYBN2VORJHZYTMP6AWU64PDMP89BV6AXYQDHPDRJQ98VOE5HIVHUAP0RFHZ6ABNVCTBACITHPFRAURPCTB2WLHP57RAT0ACCKAVPD2BQDEYV2EDRBVAF9O8LUVPPMCAOF89IQAM570EHP5CPWYUVFVU2BW6AWRT46YBPWPOEYBQYPDPDLDPCK6AB0ERPMEDPUNPXPRAT0ACCKIAFVRAHTPMARBXEYHJVHJRAVYHZVUPBWA2EYQIAVOVPWY8HDRHRPVFTNAYAVHT598O56NZFVWPAWVPVODR0EN3RFYVCOBYVF5CV38OPUNPA6ALOH84OYPWPU86GERAT0ACCKHPPWHPOV56VOPYVPOFMPN3VJPMPCNOUPWNRPNPE5YHAICAHWVP46HPUAON58RDHF5678PZVPRBAWVCPWVP0EYBUY6ANZRPVFYAQONPJNVUNPRDSAMTAVU5AR2UWVBMKC58QIAM5EOVFVWPAW2UVTHJ6AWX58QIPCA2P2AUPVENFVYBBDBCVUPHP256OAOSE2DRWY6DPDEYWLHP54RZBVP2KIR8E3PWVP0EYBDE3HHVIWCKVANOBD2T6ABWVPVOON5C6AR8HPOVIH6ABVFV89MPONRDQDDRTNYURPYV48UAOFONFVYBBDBD0PUPHWN6BYDRBXVPYPVURPOJAWDOYPHP6NHP5CDRYP2B95VOMPFNDRIKYVOSFYAVIAV26AZPEDTMYBFVOSE2YHDRBYRNNPSOYPRFVHOV48DRHNFVAMPUVP48UAO8ASAUPM5UYHYUP02T48UAVOBW5UPAP2KICOHZFRRBVAP0YXPHAR0EOYVAOFIFYVVAZR6ABWAYONHWVP0EN6ZOO8LUVPO8GERFYV8ODKRDNFYBARN6F9EYAWACYP4BOWHPFVE0OVP2OCAFEICOHRYPAV2BBQUPA6AWYPN6OA6AWN56VOHPPMYXPHRPZV57AM54OVNZRPVFIFTYYBHZ87AM54HPPME04BBY6ABWYVRDQDFNHPKCAVOVPW8OHJKCDRYPHVOA48UAOYQDHPAVKUZHWPCKDREYNI5EPM84C5HWC2ZVYBN3VZ56VO2CAWOVYPR8WEBDBHVP0EBVDRFVONFCZVYPVA46HY896AAV8O2EZVAVUPHOOYVFYDHPEYHREYNY8O76BDBHVPDEMBTMPWY8AFDRHPAU8O0BYATMBNENAV8YLEEDHTVHRAYDYBHZC2598OC5YPOJRDFP6AJNWPAWFNYW5VH0GOPUVP0EBVDRFVUAON5C8OWP0PAWHPPUC2AUB2MBE2598OR8WERJHPFN98V2PUFRUPABAYSAO82UEYN2O8MPNZBYPHNPYBV0DRIWEYCVHZ98VOE5HI56MPHYYPHPFRAURP2CBQWLWP75R8YV4BEDOCHWVP2BBQHPEYVFYDHPEYWHAUC5LCOVRFYV2CN3RJARYDBD0BCO6AJNAYB2BC6ARYADRAU5HWNZRPVF2BE5V3OWCPNFE5WTR8YVU5FNPMFVNZ8O798OP02BZH48UAHYVP0EBVDRPVFNCPAVWVPDMPYPUPBDMTHZVPEZHVVO89EYO8QI6AJRPWY8RDAFUP6WUACVHZIEHWDRV5YPCTB2WYZP8OEYOFPME5RFVAW6WOWPYBC5DYJRRTEYP0MPE5OR98HYWVOCHWNPUBVYUYP0YAQO"

class Playfair():
    def __init__(self,key = "A",omission = "Q"):
        self.primary_filler_char = "X"
        self.secondary_filler_char = "Q"
        self.grid_size = 5
        self.locations = {}

        self.grid = self.GeneratePlayfairGrid(key,omission)
        
        for _,row in enumerate(self.grid):
            for __, char in enumerate(row):
                self.locations[char] = [_,__]
    def GeneratePlayfairGrid(self,key = "A",omission = "Q", fullKey = ""):
        if fullKey == "":
            key = key.upper()
            key_copy = key

            temp_key = ""
            temp_alpha = ALPHABET

            #how do you make a key :sob
            for char in key_copy:
                if not char in temp_key:
                    temp_key+=char

            lastLetter = temp_key[-1]
            lastIndex = temp_alpha.index(lastLetter)

            temp_key+=temp_alpha[lastIndex+1::]
            temp_key+=temp_alpha[lastIndex-1::-1][::-1]

            finalKey = ""
            for char in temp_key:
                if not(char in finalKey):
                    finalKey += char
            finalKey = finalKey.replace(omission,"")
        else:
            finalKey = fullKey

        grid = [finalKey[_*self.grid_size:_*self.grid_size+self.grid_size] for _ in range(self.grid_size)]
        try:
            for _,row in enumerate(grid):
                for __, char in enumerate(row):
                    self.locations[char] = [_,__]
        except:
            pass #Obj probably hasn't been initialised yet so nothing to worry abt
        return grid
    def showGrid(self):
        print("+"+"-"*len(self.grid[0]) + "-"*3*(len(self.grid[0])-1) + "+") 
        for row in self.grid:
            print("|"+" , ".join(row)+"|")
        print("+"+"-"*len(self.grid[0]) + "-"*3*(len(self.grid[0])-1) + "+") 
    def encrypt(self,text):
        fixed_text = self.fix_text(text)
        size = self.grid_size
        pairs = []

        if len(fixed_text)%2 != 0:
            if fixed_text[-1] != self.primary_filler_char:
                fixed_text += self.primary_filler_char
            else:
                fixed_text += self.secondary_filler_char

        for _ in range(0,len(fixed_text),2):
            pairs.append(fixed_text[_:_+2])
        
        #print(f"Pairs: {",".join(pairs)}")
        
        cipheredText = ""
        for pair in pairs:
            char1_pos = self.locations[pair[0]]
            char2_pos = self.locations[pair[1]]

            newChar1, newChar2 = "",""

            if char1_pos[1] == char2_pos[1]: #Same column
                row_number1,row_number2 = (char1_pos[0]-1) % size,(char2_pos[0]+1) % size
                column_number1, column_number2 = (char1_pos[1]) % size,(char2_pos[1]) % size

                newChar1 = self.grid[row_number1][column_number1]
                newChar2 = self.grid[row_number2][column_number2]

            elif char1_pos[0] == char2_pos[0]: #Same row
                row_number1,row_number2 = (char1_pos[0])%size,(char2_pos[0])%size
                column_number1, column_number2 = (char1_pos[1]+1)%size,(char2_pos[1]+1)%size
                
                newChar1 = self.grid[row_number1][column_number1]
                newChar2 = self.grid[row_number2][column_number2]
                
            else: #BOX FORMED
                newChar1 = self.grid[char1_pos[0]][char2_pos[1]]
                newChar2 = self.grid[char2_pos[0]][char1_pos[1]]
            cipheredText += newChar1 + newChar2
        
        return cipheredText
    
        #print(f"Enciphered text: {cipheredText}")
    def decrypt(self,text):
        if len(text)%2 != 0:
            raise ValueError("yeah no is this even possible to decrypt if it aint possible to put it into pairs")
        pairs = []
        size = self.grid_size
        for _ in range(0,len(text),2):
            pairs.append(text[_:_+2])
        
        decryptedText = ""
        for pair in pairs:
            char1_pos = self.locations[pair[0]]
            char2_pos = self.locations[pair[1]]

            newChar1,newChar2 = "",""
            if char1_pos[0] == char2_pos[0]: #Same row
                newChar1 = self.grid[char1_pos[0]][(char1_pos[1]-1)%size]
                newChar2 = self.grid[char2_pos[0]][(char2_pos[1]-1)%size]
            
            elif char1_pos[1] == char2_pos[1]: #Same column
                newChar1 = self.grid[(char1_pos[0]-1)%size][char1_pos[1]]
                newChar2 = self.grid[(char2_pos[0]-1)%size][char2_pos[1]]
            
            else: #B O X
                newChar1 = self.grid[char1_pos[0]][char2_pos[1]]
                newChar2 = self.grid[char2_pos[0]][char1_pos[1]]
            
            decryptedText += newChar1 + newChar2
        return decryptedText
        #print(decryptedText)
    def fix_text(self,text):
        #fix_text basically just inserts a character in between two characters if those two characters are equal, the back up filler is Q
        prev_char = ""
        text_list = list(text)
        redo = False

        primary = self.primary_filler_char
        secondary = self.secondary_filler_char

        result = ""
        offset = 0 
        for index,char in enumerate(text_list):
            if char==prev_char:
                offset += 1
                if char == primary:
                    result += secondary
                else:
                    result += primary
            result += char
            if (index+offset)%2==1: 
                prev_char=""
            else: 
                prev_char = char
        
        
        if len(result)%2 != 0:
            if result[-1] != self.primary_filler_char:
                result += self.primary_filler_char
            else:
                result += self.secondary_filler_char

        return result

class PlayfairSolver():
    def __init__(self):
        #We store each letter as an x and y coordinate of the playfair grid
        self.Letters = [[Int(f'x_{i}_{j}') for j in range(2)] for i in range(25)] #So we create 25 sub lists (each letter) where each sub element is an x and y coordinate of the grid hence range(2)

        position_constraints = [
            And(0 <= self.Letters[i][j], self.Letters[i][j] <= 4) #coords must be between 0-4 as those are the dims of the playfair grid
            
            for j in range(2)
            for i in range(25)
        ]

        distinct_constraints = [
            Distinct([self.Letters[i][0] * 5 + self.Letters[i][1]

            for i in range(25)])
        ]

        self.universal_constraints = position_constraints + distinct_constraints
    
    def playfair_ord(self,char):
        char = char.upper()
        if char == 'J':
            char = 'I'
        val = ord(char) - ord('A')
        if val > 8:  # 'J' is 9
            val -= 1
        return val
    
    #Main func
    def row_col_constraints(self, *indices, spacing = 0, orientation = 0):
        constraints = [
            (self.Letters[indices[i]][orientation] + spacing) % 5 == self.Letters[indices[i+1]][orientation] # <--- Corrected subscript
            for i in range(len(indices)-1)
        ]

        if len(constraints) == 0:
            return True # No constraints
        elif len(constraints) >= 2:
            return And(*constraints)
        else:
            return constraints[0]
    
    #Helper funcs
    def same_row(self, *indices):
        return self.row_col_constraints(*indices, orientation = 0, spacing = 0)
    def same_col(self, *indices):
        return self.row_col_constraints(*indices, orientation = 1, spacing = 0)    
    def next_row(self, *indices):
        return self.row_col_constraints(*indices, orientation = 0, spacing = 1)
    def next_col(self, *indices):
        return self.row_col_constraints(*indices, orientation =1, spacing = 1)   

    #Cases
    def rectangle_constraint(self, plain_digraph, cipher_digraph):
        #AB -> CD -> AB , implies A ... C
        #                         .......
        #                         D.....B

        p1, p2 = (self.playfair_ord(c) for c in plain_digraph)
        c1, c2 = (self.playfair_ord(c) for c in cipher_digraph)
        
        return And( #So basically js what letters are on the same columns and rows and what letters physically cant be on the same blah blahs
            self.same_row(p1,c1),
            self.same_row(p2,c2),
            self.same_col(p1,c2),
            self.same_col(p2,c1),

            Not(self.same_row(p1,p2)),
            Not(self.same_row(c1,c2)),
            Not(self.same_col(p1,p2)),
            Not(self.same_col(p1,c2)),
        )
    def chain_constraint(self, plain_digraph, cipher_digraph, cipher_squared_digraph):
        #AB -> CD -> BE , implies A C B D E is a row or column

        p1, p2 = (self.playfair_ord(c) for c in plain_digraph)
        c1, c2 = (self.playfair_ord(c) for c in cipher_digraph)
        n1, n2 = (self.playfair_ord(c) for c in cipher_squared_digraph) #n1=p2 so isnt used

        return Or( #Characters are either ALL on the same row or column
            And(self.same_row(p1,c1,p2,c2,n2) , self.next_col(p1,c1,p2,c2,n2)),
            And(self.same_col(p1,c1,p2,c2,n2) , self.next_row(p1,c1,p2,c2,n2))
        )
    def adjacent_constraint(self, plain_digraph, cipher_digraph):
        # AB -> BC , implies ...ABC... as a row or column

        p1, p2 = (self.playfair_ord(c) for c in plain_digraph)
        c1, c2 = (self.playfair_ord(c) for c in cipher_digraph) #c1 = p2 so isnt used
        
        return Or(
            And(self.same_row(p1,p2,c2), self.next_col(p1,p2,c2)),
            And(self.same_col(p1,p2,c2), self.next_row(p1,p2,c2)),
        )
    def basic_constraint(self, plain_digraph, cipher_digraph):
        # AB -> CD , implies uhh well nothing much except that A and C must be in the same column or row, if it is the same col then C is directly beneath A, same cant be applied for same row as rectangle rule may apply so it could be far away
        #We do this for both characters
        p1, p2 = (self.playfair_ord(c) for c in plain_digraph)
        c1, c2 = (self.playfair_ord(c) for c in cipher_digraph) #c1 = p2 so isnt used
        
        return And(
            Or(
                And(self.same_row(p1, c1), self.next_col(p1, c1)), #Row rule
                And(self.same_col(p1, c1), self.next_row(p1, c1)), #Column rule
                Not(self.same_row(p1, c1)), Not(self.same_col(p1, c1)) #Rectangle rule
            ),
            Or(
                And(self.same_row(p2, c2), self.next_col(p2, c2)), #Row rule
                And(self.same_col(p2, c2), self.next_row(p2, c2)), #Column rule
                Not(self.same_row(p2, c2)), Not(self.same_col(p2, c2)) #Rectangle rule
            )
        )

    def parse_bigraph_map(self, plaintext, ciphertext):
        plaintext_bigraphs = []
        ciphertext_bigraphs = []

        for _ in range(0,len(plaintext),2):
            plaintext_bigraphs.append(plaintext[_:_+2])        
        for _ in range(0,len(ciphertext),2):
            ciphertext_bigraphs.append(ciphertext[_:_+2])
        
        bigraph_map = {}

        for plain_bigraph, cipher_bigraph in zip(plaintext_bigraphs,ciphertext_bigraphs):
            #AB -> CD and so BA-> DC
            bigraph_map[plain_bigraph] = cipher_bigraph
            bigraph_map[plain_bigraph[::-1]] = cipher_bigraph[::-1]
        
        return bigraph_map

    def constraints_from_known_text(self, plaintext, ciphertext):
        bigraph_map = self.parse_bigraph_map(plaintext,ciphertext)

        constraints = []
        seen_already = set()

        for plain_bigraph, cipher_bigraph in bigraph_map.items():
            if plain_bigraph[::-1] in seen_already:
                continue
            else:
                seen_already.add(plain_bigraph)
            
            # AB -> BC implies ABC
            if plain_bigraph[1] == cipher_bigraph[0]:
                constraints.append(self.adjacent_constraint(plain_bigraph, cipher_bigraph))
                continue
            
            if cipher_bigraph in bigraph_map:
                next_bigraph = bigraph_map[cipher_bigraph]

                if next_bigraph == plain_bigraph: #Rectangle rule found
                    constraints.append(self.rectangle_constraint(plain_bigraph,cipher_bigraph))
                    continue

                if plain_bigraph[1] == next_bigraph[0]:
                    constraints.append(self.chain_constraint(plain_bigraph,cipher_bigraph,next_bigraph))
                    continue
            
            constraints.append(self.basic_constraint(plain_bigraph, cipher_bigraph))
        return constraints

    def solve_playfair_constraints(self,dynamic_constraints):
        solver = Solver()

        solver.add(self.universal_constraints)
        solver.add(dynamic_constraints)

        print("LF sols")
        while True:
            check = solver.check()

            if check == sat:
                print("FOUND SOL")
                model = solver.model()
                print(model)

                solver.add(Or([
                    self.Letters[i][j] != model[self.Letters[i][j]] 
                    for i in range(25) 
                    for j in range(2)
                ]))
            else:
                print("No more sols")
                break


grid = Playfair(omission="J")
grid.grid_size = 5

alphabet = list(string.ascii_uppercase) #generate random key
current_key = ""
for j in range(26):
    current_key+=str(random.choice(alphabet))
    alphabet.remove(current_key[-1])
print(f"Encryption Key is: {current_key}")

grid.grid = grid.GeneratePlayfairGrid(fullKey="GROCEISABDFHKLMNPQTUVWXYZ")
grid.showGrid()

plaintext = """
MDSOASOGTGKCDRBZEQVSKYMHFVIBDSKYMHCOROCEGODGABUICQMRORAOEAI
HPEVFHPDMQCXCNDPUMRKBBPASZKGQPLABKENPNBVIQCASYQWBGZGUAEKYKB
SHIQBUFSCPVLEQOEGUPBBNEQRFQYQCKSZGDCGUQSSIDCKGOGKRXZEQDKFVS
AUCOCLNMRRCHWCMOBVFPDNBLVXCPEDRMHFVPDFVOVRCEAHRFSRLXCZMGQUQ
BXKGGSOBPUNPMDSHQBUIFNSGDUDUDCOWGSRFYTCYMRDSLTRDBXARZRQGKDQ
ITVPLFVOIASDPQWQRDRXCPEGECRVFEDPLCDSDMCBAIQDQPLCOBNVBOZURBY
XCNURQBXNQWSEKQUTCIQAELTFICZEQSHOGHWGENLTMTCPLEKBAUNAEOW""".upper()
plaintext = plaintext.replace(" ","").replace("\n","")

sanitised_plaintext = ""
for char in plaintext:
    if char in string.ascii_uppercase:
        sanitised_plaintext+=char

ciphertext = grid.encrypt(sanitised_plaintext)
print(f"Ciphered text is: {ciphertext}")
print(f"Text length: {len(ciphertext)}")
print(grid.decrypt(sanitised_plaintext))
playfair = PlayfairSolver()
playfair.solve_playfair_constraints(playfair.constraints_from_known_text(sanitised_plaintext[:600],ciphertext[:600]))