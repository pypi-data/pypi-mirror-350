# converter_letra_numero

**Biblioteca Python simples para converter letras (A–Z) em índices numéricos (0–25).**

---

## Pré-requisitos

- Python 3.12 instalado  
- Virtual environment (recomendado) ou pip configurado  
- Windows 11, macOS ou Linux  

## Estrutura do Projeto

```
converter_letra_numero/        # pasta raiz do projeto
│
├── .venv/                   # ambiente virtual (PyCharm)
├── converter_letra_numero/  # pacote Python
│   ├── __init__.py
│   └── conversor.py         # função letra_para_numero()
│
├── README.md                # documentação do pacote
├── setup.py                 # configurações de build/install
├── requirements.txt         # dependências (vazio)
├── LICENSE                  # texto da licença MIT
└── tests/                   # testes automatizados (pytest)
```

> Ainda pendente:
> - adicionar o arquivo `LICENSE` com texto MIT  
> - criar a pasta `tests/` com testes de `pytest`  
> - (opcional) subpacote `inverso/` para conversão número→letra  

---

## Instalando localmente

Abra o terminal (PowerShell/CMD no Windows, Terminal no macOS/Linux) **na pasta raiz do projeto** e execute:

```bash
# ativa virtualenv (opcional)
pip install -e .
```

Instala o pacote em modo editável, refletindo alterações imediatamente.

---

## Exemplo de uso

```python
from converter_letra_numero import letra_para_numero

print(letra_para_numero('C'))  # → 2
```

### Submódulo inverso (opcional)

Se tiver criado `converter_letra_numero/inverso/numero_para_letra.py`, importe:

```python
from converter_letra_numero import numero_para_letra

print(numero_para_letra(0))  # → 'A'
```

---

## Testes (pytest)

1. Instale o pytest:
   ```bash
   pip install pytest
   ```
2. Crie `tests/test_conversor.py`:
   ```python
   from converter_letra_numero import letra_para_numero

   def test_letra_A():
       assert letra_para_numero('A') == 0

   def test_letra_Z():
       assert letra_para_numero('Z') == 25
   ```
3. Execute:
   ```bash
   pytest
   ```

---

## Publicação no PyPI (opcional)

```bash
pip install build twine
python -m build
twine upload dist/*
```

---

## Licença

Licenciado sob MIT. Veja o arquivo `LICENSE` para detalhes.

---

**Compatível com:** Python 3.12
