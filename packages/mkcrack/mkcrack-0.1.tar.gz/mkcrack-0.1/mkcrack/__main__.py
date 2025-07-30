# mkcrack/__main__.py

from .cracker import crack_yescrypt

def main():
    stored_hash = input("Enter the yescrypt hash: ").strip()
    wordlist_file = input("Enter the path to the wordlist file: ").strip()
    crack_yescrypt(stored_hash, wordlist_file)

if __name__ == "__main__":
    main()
