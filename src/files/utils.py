import hashlib


def calculate_hash_md5(input_file):
    md5 = hashlib.md5()

    with open(input_file, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            md5.update(chunk)

    return md5.hexdigest()
