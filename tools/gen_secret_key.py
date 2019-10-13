import os
from cryptography.fernet import Fernet
from webapp.utils.file_encryption import FernetVault
from webapp.constants import SECRET_KEYFILE, DB_CONFIG_FILE

"""
This script allows the admin to generate a new secret key, should the old one be compromised.
"""
if __name__ == '__main__':
    if not os.path.exists(SECRET_KEYFILE):
        print("Error: You must have the original key file before you can change to a new one.")
        exit(-1)

    # read URI with old key file
    old_vault = FernetVault(SECRET_KEYFILE)
    URI = old_vault.read_file(DB_CONFIG_FILE)

    # generate new key and save it
    new_key = Fernet.generate_key()
    with open(SECRET_KEYFILE, 'wb') as fp:
        fp.write(new_key)

    # encrypt DB config with new key
    new_vault = FernetVault(SECRET_KEYFILE)
    new_vault.write_file(URI, DB_CONFIG_FILE)