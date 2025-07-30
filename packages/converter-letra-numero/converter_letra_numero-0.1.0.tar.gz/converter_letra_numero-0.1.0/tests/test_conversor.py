from converter_letra_numero import letra_para_numero

def test_letra_A():
    assert letra_para_numero('A') == 0

def test_letra_Z():
    assert letra_para_numero('Z') == 25

def test_letra_minuscula():
    # deve aceitar letra minúscula também
    assert letra_para_numero('b') == 1

import pytest

@pytest.mark.parametrize("entrada", ["", "AB", "1", "@"])
def test_letras_invalidas(entrada):
    with pytest.raises(ValueError):
        letra_para_numero(entrada)
