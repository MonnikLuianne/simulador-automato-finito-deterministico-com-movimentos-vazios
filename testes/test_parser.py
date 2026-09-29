
#testa se o parser.py esta funcionando
#codigo de controle do integrante 1
#testes feitos: se o parser consegue ler json ou txt, se recomhece eps, se aceita 
#multiplos destinos, se detecta estado inicial inexistente, se detecta simbolo de
# transicao inexistente, se detecta estado destino inexistente, 
# se detecta estado repetido, se detecta simbolo repetido, 
# se impede de epsilon ficar no alfabeto, se detecta palavra com simbolo invalido
from parser import carregar_automato, validar_automato

def testar_json_valido():
    automato = carregar_automato("dados/exemplo.json")

    assert validar_automato(automato) is True
    assert automato["estados"] == ["q0", "q1", "q2"]
    assert automato["alfabeto"] == ["a", "b"]
    assert automato["inicial"] == "q0"
    assert automato["finais"] == ["q2"]
    assert ("q0", "eps") in automato["transicoes"]

    print("Teste JSON válido: OK")


def testar_txt_valido():
    automato = carregar_automato("dados/exemplo.txt")

    assert validar_automato(automato) is True
    assert automato["inicial"] == "q0"
    assert automato["finais"] == ["q2"]
    assert ("q0", "eps") in automato["transicoes"]

    print("Teste TXT válido: OK")


def testar_json_invalido():
    automato = carregar_automato("dados/invalido.json")

    try:
        validar_automato(automato)
        assert False
    except ValueError:
        print("Teste JSON inválido: OK")


def testar_txt_invalido():
    automato = carregar_automato("dados/invalido.txt")

    try:
        validar_automato(automato)
        assert False
    except ValueError:
        print("Teste TXT inválido: OK")


def testar_epsilon_normalizado():
    automato = {
        "estados": ["q0", "q1"],
        "alfabeto": ["a"],
        "inicial": "q0",
        "finais": ["q1"],
        "transicoes": {
            ("q0", "epsilon"): ["q1"]
        },
        "palavras": [""]
    }

    assert validar_automato(automato) is True
    assert ("q0", "epsilon") in automato["transicoes"]

    print("Teste epsilon: OK")


def testar_multiplos_destinos():
    automato = {
        "estados": ["q0", "q1", "q2"],
        "alfabeto": ["a"],
        "inicial": "q0",
        "finais": ["q1", "q2"],
        "transicoes": {
            ("q0", "a"): ["q1", "q2"]
        },
        "palavras": ["a"]
    }

    assert validar_automato(automato) is True
    assert automato["transicoes"][("q0", "a")] == ["q1", "q2"]

    print("Teste múltiplos destinos: OK")


def testar_estado_inicial_invalido():
    automato = {
        "estados": ["q0", "q1"],
        "alfabeto": ["a"],
        "inicial": "q2",
        "finais": ["q1"],
        "transicoes": {},
        "palavras": []
    }

    try:
        validar_automato(automato)
        assert False
    except ValueError:
        print("Teste estado inicial inválido: OK")


def testar_simbolo_transicao_invalido():
    automato = {
        "estados": ["q0", "q1"],
        "alfabeto": ["a"],
        "inicial": "q0",
        "finais": ["q1"],
        "transicoes": {
            ("q0", "b"): ["q1"]
        },
        "palavras": []
    }

    try:
        validar_automato(automato)
        assert False
    except ValueError:
        print("Teste símbolo de transição inválido: OK")


def testar_estado_destino_invalido():
    automato = {
        "estados": ["q0", "q1"],
        "alfabeto": ["a"],
        "inicial": "q0",
        "finais": ["q1"],
        "transicoes": {
            ("q0", "a"): ["q2"]
        },
        "palavras": []
    }

    try:
        validar_automato(automato)
        assert False
    except ValueError:
        print("Teste estado destino inválido: OK")


def testar_estado_repetido():
    automato = {
        "estados": ["q0", "q0", "q1"],
        "alfabeto": ["a"],
        "inicial": "q0",
        "finais": ["q1"],
        "transicoes": {},
        "palavras": []
    }

    try:
        validar_automato(automato)
        assert False
    except ValueError:
        print("Teste estado repetido: OK")


def testar_simbolo_repetido():
    automato = {
        "estados": ["q0", "q1"],
        "alfabeto": ["a", "a"],
        "inicial": "q0",
        "finais": ["q1"],
        "transicoes": {},
        "palavras": []
    }

    try:
        validar_automato(automato)
        assert False
    except ValueError:
        print("Teste símbolo repetido: OK")


def testar_epsilon_no_alfabeto():
    automato = {
        "estados": ["q0", "q1"],
        "alfabeto": ["a", "eps"],
        "inicial": "q0",
        "finais": ["q1"],
        "transicoes": {},
        "palavras": []
    }

    try:
        validar_automato(automato)
        assert False
    except ValueError:
        print("Teste epsilon no alfabeto: OK")


def testar_palavra_com_simbolo_invalido():
    automato = {
        "estados": ["q0", "q1"],
        "alfabeto": ["a"],
        "inicial": "q0",
        "finais": ["q1"],
        "transicoes": {
            ("q0", "a"): ["q1"]
        },
        "palavras": ["b"]
    }

    try:
        validar_automato(automato)
        assert False
    except ValueError:
        print("Teste palavra com símbolo inválido: OK")
        
def testar_multiplos_destinos_json():
    automato = carregar_automato("dados/multiplos_destinos.json")

    assert validar_automato(automato) is True
    assert automato["transicoes"][("q0", "a")] == ["q1", "q2"]

    print("Teste múltiplos destinos JSON: OK")


if __name__ == "__main__":
    testar_json_valido()
    testar_txt_valido()
    testar_json_invalido()
    testar_txt_invalido()
    testar_epsilon_normalizado()
    testar_multiplos_destinos()
    testar_estado_inicial_invalido()
    testar_simbolo_transicao_invalido()
    testar_estado_destino_invalido()
    testar_estado_repetido()
    testar_simbolo_repetido()
    testar_epsilon_no_alfabeto()
    testar_palavra_com_simbolo_invalido()
    testar_multiplos_destinos_json()

    print("\nTodos os testes passaram!")