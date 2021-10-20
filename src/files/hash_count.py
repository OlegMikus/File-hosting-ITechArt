import hashlib


def hash_count(file):
    h = hashlib.md5()

    with open(file, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)

    return h.hexdigest()
