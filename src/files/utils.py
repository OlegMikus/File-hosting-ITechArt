import hashlib


def calculate_hash_md5(file):
    h = hashlib.md5()

    with open(file, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)

    return h.hexdigest()
