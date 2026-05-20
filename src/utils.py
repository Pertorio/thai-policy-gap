import hashlib


#For creating signature of the uploaded file
def file_hash (file_bytes: bytes) -> str:
    return hashlib.md5(file_bytes).hexdigest()
