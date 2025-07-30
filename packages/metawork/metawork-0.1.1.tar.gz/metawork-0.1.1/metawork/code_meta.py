
import os
from datetime import datetime

def extract_comments(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    comments = [line.strip() for line in lines if line.strip().startswith(("#", "//", "/*"))]
    return comments

def insert_metadata(filepath, metadata: dict):
    meta_block = "\n".join([f"# {key}: {value}" for key, value in metadata.items()])
    with open(filepath, 'r+', encoding='utf-8') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(meta_block + '\n\n' + content)

def file_system_metadata(filepath):
    stats = os.stat(filepath)
    return {
        "size": stats.st_size,
        "created": datetime.fromtimestamp(stats.st_ctime).isoformat(),
        "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
        "permissions": oct(stats.st_mode)[-3:]
    }
