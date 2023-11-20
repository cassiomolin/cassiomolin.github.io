import os
import hashlib

def extract_metadata(file_path):
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    file_size_human_friendly = file_size_for_humans(file_size)
    sha256 = sha256sum(file_path)
    
    return {
        'name': file_name,
        'size': file_size,
        'size_human_friendly': file_size_human_friendly,
        'sha256': sha256
    }

def sha256sum(file_path):
    with open(file_path, 'rb', buffering=0) as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


# See https://stackoverflow.com/a/1094933/1426227
def file_size_for_humans(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"
