# mkcrack/cracker.py

import crypt

def crack_yescrypt(stored_hash, wordlist_path):
    """
    Attempts to crack the given yescrypt hash using the provided wordlist.
    
    Args:
        stored_hash (str): The yescrypt hash to crack.
        wordlist_path (str): Path to the wordlist file.
    
    Returns:
        str or None: The cracked password if found, else None.
    """
    try:
        parts = stored_hash.split('$')
        salt = '$'.join(parts[:-1])
        print(f"Using salt: {salt}")

        with open(wordlist_path, 'r', encoding='utf-8') as f:
            for line in f:
                candidate = line.strip()
                candidate_hash = crypt.crypt(candidate, salt)
                if candidate_hash == stored_hash:
                    print(f"Password found: {candidate}")
                    return candidate

        print("Password not found in wordlist.")
        return None

    except FileNotFoundError:
        print(f"File not found: {wordlist_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
