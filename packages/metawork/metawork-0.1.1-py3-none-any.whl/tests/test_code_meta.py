
import os
from metawork import code_meta

def test_extract_comments(tmp_path):
    test_file = tmp_path / "test.py"
    test_file.write_text("# Comentário\nprint('Hello')\n// Comentário JS")

    comments = code_meta.extract_comments(str(test_file))
    assert "# Comentário" in comments
    assert "// Comentário JS" in comments

def test_insert_metadata(tmp_path):
    test_file = tmp_path / "test.py"
    test_file.write_text("print('Hello')")

    metadata = {"author": "Tester", "date": "2025-05-27"}
    code_meta.insert_metadata(str(test_file), metadata)

    content = test_file.read_text()
    assert "# author: Tester" in content
    assert "# date: 2025-05-27" in content
