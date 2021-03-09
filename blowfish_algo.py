from os import urandom
import blowfish

cipher = blowfish.Cipher(b"AnyKeyValue.MustBeALargeKeyToMakeTheEncryptionStronger")
iv = b'\x82\xcd\xbb\xf5;\x02\xc1\xe7' # initialization vector

def encrypt(inp):
    global iv
    global cipher
    data = bytes(inp, 'utf-8')
    data_encrypted = b"".join(cipher.encrypt_cfb(data, iv))
    return data_encrypted


def decrypt(inp):
    global iv
    global cipher
    data_decrypted = b"".join(cipher.decrypt_cfb(inp, iv))
    out = data_decrypted.decode("utf-8")
    return out