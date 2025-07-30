
# Metawork

Biblioteca para manipular metadados em arquivos de código-fonte, documentos e mídias.

## Instalação

```bash
pip install metawork
```

## Exemplo de uso

```python
from metawork import code_meta

comments = code_meta.extract_comments('exemplo.py')
print(comments)
```

## Testes

```bash
pytest tests/
```
