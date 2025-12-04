import random
import math
import string
from collections import defaultdict
import os 
import sys

script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","Test","Modules")
toolsPath = os.path.join(script_dir,"..")
sys.path.append(modulesPath)

import cipherTools

# Color constants (define these if not already defined)
GREEN = "\033[92m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# Assume raw_freq_data is loaded elsewhere in your code
# raw_freq_data = {"bigrams": {...}, "trigrams": {...}, "quadgrams": {...}}

class PlayfairCipher:
    """Playfair cipher with encryption, decryption, and solving capabilities."""
    
    def __init__(self, key=None):
        """Initialize with a 25-character key (I/J merged)."""
        if key is None:
            key = self.make_random_key()
        self.key = key.upper().replace('J', 'I')
        self.grid = self._make_grid()
        self.pos_map = self._make_position_map()
    
    def _make_grid(self):
        """Convert key string to 5x5 grid."""
        return [[self.key[i*5 + j] for j in range(5)] for i in range(5)]
    
    def _make_position_map(self):
        """Create reverse lookup: letter -> (row, col)."""
        pos_map = {}
        for i in range(5):
            for j in range(5):
                pos_map[self.grid[i][j]] = (i, j)
        return pos_map
    
    @staticmethod
    def make_random_key():
        """Generate a random 25-letter key."""
        letters = list(string.ascii_uppercase.replace('J', ''))
        random.shuffle(letters)
        return ''.join(letters)
    
    @staticmethod
    def make_key_from_phrase(phrase):
        """Generate key from a memorable phrase."""
        phrase = phrase.upper().replace('J', 'I')
        seen = set()
        key = []
        
        # Add unique letters from phrase
        for char in phrase:
            if char.isalpha() and char not in seen:
                key.append(char)
                seen.add(char)
        
        # Fill remaining with alphabet
        for char in string.ascii_uppercase.replace('J', ''):
            if char not in seen:
                key.append(char)
        
        return ''.join(key)
    
    @staticmethod
    def prepare_text(text):
        """Clean and prepare text for Playfair encryption."""
        text = text.upper().replace('J', 'I')
        text = ''.join(c for c in text if c.isalpha())
        
        # Break up double letters with X
        result = []
        i = 0
        while i < len(text):
            result.append(text[i])
            if i + 1 < len(text):
                if text[i] == text[i+1]:
                    result.append('X' if text[i] != 'X' else 'Z')
                else:
                    result.append(text[i+1])
                    i += 1
            i += 1
        
        # Pad to even length
        if len(result) % 2 == 1:
            result.append('X' if result[-1] != 'X' else 'Z')
        
        return ''.join(result)
    
    def encrypt(self, plaintext):
        """Encrypt plaintext using Playfair cipher."""
        plaintext = self.prepare_text(plaintext)
        ciphertext = []
        
        for i in range(0, len(plaintext), 2):
            a, b = plaintext[i], plaintext[i+1]
            row1, col1 = self.pos_map[a]
            row2, col2 = self.pos_map[b]
            
            if row1 == row2:  # Same row
                ciphertext.append(self.grid[row1][(col1 + 1) % 5])
                ciphertext.append(self.grid[row2][(col2 + 1) % 5])
            elif col1 == col2:  # Same column
                ciphertext.append(self.grid[(row1 + 1) % 5][col1])
                ciphertext.append(self.grid[(row2 + 1) % 5][col2])
            else:  # Rectangle
                ciphertext.append(self.grid[row1][col2])
                ciphertext.append(self.grid[row2][col1])
        
        return ''.join(ciphertext)
    
    def decrypt(self, ciphertext):
        """Decrypt ciphertext using Playfair cipher."""
        ciphertext = ''.join(c for c in ciphertext.upper() if c.isalpha())
        plaintext = []
        
        for i in range(0, len(ciphertext), 2):
            if i + 1 >= len(ciphertext):
                break
            a, b = ciphertext[i], ciphertext[i+1]
            row1, col1 = self.pos_map.get(a, (0, 0))
            row2, col2 = self.pos_map.get(b, (0, 0))
            
            if row1 == row2:  # Same row
                plaintext.append(self.grid[row1][(col1 - 1) % 5])
                plaintext.append(self.grid[row2][(col2 - 1) % 5])
            elif col1 == col2:  # Same column
                plaintext.append(self.grid[(row1 - 1) % 5][col1])
                plaintext.append(self.grid[(row2 - 1) % 5][col2])
            else:  # Rectangle
                plaintext.append(self.grid[row1][col2])
                plaintext.append(self.grid[row2][col1])
        
        return ''.join(plaintext)
    
    @staticmethod
    def alter_key_randomly(key):
        """Make a small random change to the key."""
        key_list = list(key)
        mutation_type = random.choice(['swap', 'reverse_row', 'reverse_col', 
                                      'rotate_row', 'rotate_col', 'swap_rows', 'swap_cols'])
        
        if mutation_type == 'swap':
            # Swap two random letters
            i, j = random.sample(range(25), 2)
            key_list[i], key_list[j] = key_list[j], key_list[i]
        
        elif mutation_type == 'reverse_row':
            # Reverse a random row
            row = random.randint(0, 4)
            start, end = row * 5, (row + 1) * 5
            key_list[start:end] = reversed(key_list[start:end])
        
        elif mutation_type == 'reverse_col':
            # Reverse a random column
            col = random.randint(0, 4)
            column_vals = [key_list[col + i*5] for i in range(5)]
            column_vals.reverse()
            for i in range(5):
                key_list[col + i*5] = column_vals[i]
        
        elif mutation_type == 'rotate_row':
            # Rotate a random row
            row = random.randint(0, 4)
            start, end = row * 5, (row + 1) * 5
            row_vals = key_list[start:end]
            row_vals = [row_vals[-1]] + row_vals[:-1]
            key_list[start:end] = row_vals
        
        elif mutation_type == 'rotate_col':
            # Rotate a random column
            col = random.randint(0, 4)
            column_vals = [key_list[col + i*5] for i in range(5)]
            column_vals = [column_vals[-1]] + column_vals[:-1]
            for i in range(5):
                key_list[col + i*5] = column_vals[i]
        
        elif mutation_type == 'swap_rows':
            # Swap two rows
            row1, row2 = random.sample(range(5), 2)
            for col in range(5):
                idx1, idx2 = row1 * 5 + col, row2 * 5 + col
                key_list[idx1], key_list[idx2] = key_list[idx2], key_list[idx1]
        
        else:  # swap_cols
            # Swap two columns
            col1, col2 = random.sample(range(5), 2)
            for row in range(5):
                idx1, idx2 = row * 5 + col1, row * 5 + col2
                key_list[idx1], key_list[idx2] = key_list[idx2], key_list[idx1]
        
        return ''.join(key_list)


def simulated_annealing_crack(ciphertext, ngram_scorer,
                              max_iterations=50000, initial_temp=20.0,
                              cooling_rate=0.995, restart_patience=3000,
                              verbose=True):
    """
    Crack Playfair cipher using simulated annealing.
    
    Args:
        ciphertext: The encrypted text
        ngram_scorer: Instance of ngrams() class for scoring
        max_iterations: Maximum iterations
        initial_temp: Starting temperature
        cooling_rate: Temperature cooling rate
        restart_patience: Restart after this many iterations without improvement
        verbose: Print progress
    
    Returns:
        best_key, best_plaintext, best_score
    """
    # Start with random key
    current_key = PlayfairCipher.make_random_key()
    cipher = PlayfairCipher(current_key)
    current_plaintext = cipher.decrypt(ciphertext)
    current_score = ngram_scorer.score(current_plaintext)
    
    best_key = current_key
    best_plaintext = current_plaintext
    best_score = current_score
    
    temperature = initial_temp
    no_improvement = 0
    accepted = 0
    
    for iteration in range(max_iterations):
        # Generate candidate key
        new_key = PlayfairCipher.alter_key_randomly(current_key)
        cipher = PlayfairCipher(new_key)
        new_plaintext = cipher.decrypt(ciphertext)
        new_score = ngram_scorer.score(new_plaintext)
        
        delta = new_score - current_score
        
        # Accept or reject
        if delta > 0 or random.random() < math.exp(delta / temperature):
            current_key = new_key
            current_plaintext = new_plaintext
            current_score = new_score
            accepted += 1
            
            if current_score > best_score:
                best_key = current_key
                best_plaintext = new_plaintext
                best_score = current_score
                no_improvement = 0
                
                if verbose:
                    print(f"✓ Iteration {iteration}: New best score {best_score:.2f}")
                    print(f"  Key: {best_key}")
                    print(f"  Sample: {best_plaintext[:80]}...\n")
        else:
            no_improvement += 1
        
        # Cool down
        temperature *= cooling_rate
        
        # Restart if stuck
        if no_improvement > restart_patience:
            if verbose:
                print(f"↻ Restarting at iteration {iteration} (stuck for {no_improvement} iterations)")
            current_key = best_key
            current_score = best_score
            temperature = initial_temp / 3
            no_improvement = 0
        
        # Progress report
        if verbose and (iteration + 1) % 10000 == 0:
            acceptance_rate = (accepted / 10000) * 100
            print(f"Iteration {iteration + 1}/{max_iterations}:")
            print(f"  Best score: {best_score:.2f}")
            print(f"  Temperature: {temperature:.6f}")
            print(f"  Acceptance: {acceptance_rate:.1f}%")
            print(f"  Sample: {best_plaintext[:80]}...\n")
            accepted = 0
    
    return best_key, best_plaintext, best_score


def hill_climbing_crack(ciphertext, ngram_scorer,
                       max_iterations=10000, num_restarts=10, verbose=True):
    """
    Crack Playfair using hill climbing (faster but less thorough).
    
    Args:
        ciphertext: Encrypted text
        ngram_scorer: Instance of ngrams() class for scoring
        max_iterations: Iterations per restart
        num_restarts: Number of random restarts
        verbose: Print progress
    
    Returns:
        best_key, best_plaintext, best_score
    """
    global_best_key = None
    global_best_plaintext = None
    global_best_score = -float('inf')
    
    for restart in range(num_restarts):
        # Start with random key
        current_key = PlayfairCipher.make_random_key()
        cipher = PlayfairCipher(current_key)
        current_plaintext = cipher.decrypt(ciphertext)
        current_score = ngram_scorer.score(current_plaintext)
        
        no_improvement = 0
        
        for iteration in range(max_iterations):
            # Try mutation
            new_key = PlayfairCipher.alter_key_randomly(current_key)
            cipher = PlayfairCipher(new_key)
            new_plaintext = cipher.decrypt(ciphertext)
            new_score = ngram_scorer.score(new_plaintext)
            
            # Only accept improvements (strict hill climbing)
            if new_score > current_score:
                current_key = new_key
                current_plaintext = new_plaintext
                current_score = new_score
                no_improvement = 0
            else:
                no_improvement += 1
            
            # Stop if stuck
            if no_improvement > 1000:
                break
        
        # Update global best
        if current_score > global_best_score:
            global_best_key = current_key
            global_best_plaintext = current_plaintext
            global_best_score = current_score
            
            if verbose:
                print(f"✓ Restart {restart + 1}: New best score {global_best_score:.2f}")
                print(f"  Sample: {global_best_plaintext[:80]}...\n")
    
    return global_best_key, global_best_plaintext, global_best_score


# Main execution
if __name__ == "__main__":
    print("=" * 80)
    print("PLAYFAIR CIPHER SOLVER")
    print("=" * 80)
    
    # Initialize n-gram scorer
    print("\nInitializing n-gram scorer...")
    ngram_scorer = cipherTools.ngrams()
    
    # Example: Create and solve a Playfair cipher
    print("\n" + "=" * 80)
    print("EXAMPLE: Creating and solving a Playfair cipher")
    print("=" * 80)
    
    # Create cipher from memorable phrase
    original_key = PlayfairCipher.make_key_from_phrase("PLAYFAIR EXAMPLE")
    cipher = PlayfairCipher(original_key)
    
    plaintext = """
    THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG AND THEN GOES TO SLEEP
    UNDER THE MOONLIGHT WHILE DREAMING OF ADVENTURES IN FAR AWAY LANDS
    """
    
    print(f"\nOriginal key: {original_key}")
    print(f"Key grid:")
    for i in range(5):
        print("  " + " ".join(cipher.grid[i]))
    print(f"\nPlaintext: {plaintext.strip()[:80]}...")
    
    # Encrypt
    ciphertext = cipher.encrypt(plaintext)
    print(f"\nCiphertext: {ciphertext[:80]}...")
    
    # Verify decryption works
    decrypted = cipher.decrypt(ciphertext)
    print(f"Decrypted: {decrypted[:80]}...")
    
    # Try to crack it
    print("\n" + "=" * 80)
    print("METHOD 1: Simulated Annealing (Recommended)")
    print("=" * 80 + "\n")
    
    ciphertext = """UDSDAEEPVFHPKNNMPILPBMNGDOOGHPGDVFHIVQRSURBETIREAFHPAVKFREH
RRMFANFPUDMRAAUPIAGPEXFTGRUODWRBNFNDOTGPWQGDMNLQVWEUWHGLDFS
AUNOQPUALZSDZDGUFABEZDRBDFDVVQRSGMBEIZTDFNOPPLPUUVRBAUGTVEH
RARFKDRBEODUDVEUCAWRBPRDSNEBXRSLTPWQGRAFAKGLPUWHGLZBFREIERE
ZLRETZWGYNLPDUFPECPZZDMUGUUTICGUIARAODOQGDUGIZGHUALZMUBVZDD
MZDRBGUFAEFBRDMARDFOPBRPRNLOMSDSRXNOREBRADMGKANMHKIDZUMOAPL
OAAFUNRZARSIGHUSMGZDRDEPUWBEIFREOPLSFNBWAUMPTLMGNLRZARSIPIA
UXGZDPR
"""

    recovered_key, recovered_text, score = simulated_annealing_crack(
        ciphertext,
        ngram_scorer,
        max_iterations=30000,
        initial_temp=20.0,
        cooling_rate=0.997,
        restart_patience=2000,
        verbose=True
    )
    
    print("\n" + "=" * 80)
    print("RESULTS - SIMULATED ANNEALING")
    print("=" * 80)
    print(f"Original key:  {original_key}")
    print(f"Recovered key: {recovered_key}")
    print(f"Score: {score:.2f}")
    print(f"\nRecovered text:\n{recovered_text}")
    
    # Alternative: Hill climbing (faster but less reliable)
    print("\n" + "=" * 80)
    print("METHOD 2: Hill Climbing (Faster)")
    print("=" * 80 + "\n")
    
    hc_key, hc_text, hc_score = hill_climbing_crack(
        ciphertext,
        ngram_scorer,
        max_iterations=5000,
        num_restarts=5,
        verbose=True
    )
    
    print("\n" + "=" * 80)
    print("RESULTS - HILL CLIMBING")
    print("=" * 80)
    print(f"Original key:  {original_key}")
    print(f"Recovered key: {hc_key}")
    print(f"Score: {hc_score:.2f}")
    print(f"\nRecovered text:\n{hc_text}")