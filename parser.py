
#le o arquivo de entrada em json ou txt e tranforma
#na estrutura que o restante do programa consegue usar no simulador.py 
#e validar se o automato está consistente antes de ser utilizao pelo simulador.py
import json

from automato import EPSILON, criar_automato


def normalizar_simbolo(simbolo):
    simbolo = simbolo.strip()

    if simbolo.lower() in {"eps", "epsilon", "lambda", "λ", "ε"}:
        return EPSILON

    return simbolo


def carregar_automato(caminho_arquivo):
    if caminho_arquivo.lower().endswith(".json"):
        return carregar_json(caminho_arquivo)

    if caminho_arquivo.lower().endswith(".txt"):
        return carregar_txt(caminho_arquivo)

    raise ValueError("Formato de arquivo não suportado. Use .json ou .txt.")


def carregar_json(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    transicoes = {}

    for chave, destinos in dados["transicoes"].items():
        estado, simbolo = chave.split(",", 1)

        estado = estado.strip()
        simbolo = normalizar_simbolo(simbolo)

        transicoes[(estado, simbolo)] = destinos

    return criar_automato(
        estados=dados["estados"],
        alfabeto=dados["alfabeto"],
        inicial=dados["inicial"],
        finais=dados["finais"],
        transicoes=transicoes,
        palavras=dados["palavras"]
    )


def carregar_txt(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    dados = {
        "estados": [],
        "alfabeto": [],
        "inicial": "",
        "finais": [],
        "transicoes": {},
        "palavras": []
    }

    secao = None

    for linha in linhas:
        linha = linha.strip()

        if linha.upper() == "ESTADOS:":
            secao = "estados"
            continue

        if linha.upper() == "ALFABETO:":
            secao = "alfabeto"
            continue

        if linha.upper() == "INICIAL:":
            secao = "inicial"
            continue

        if linha.upper() == "FINAIS:":
            secao = "finais"
            continue

        if linha.upper() == "TRANSICOES:":
            secao = "transicoes"
            continue

        if linha.upper() == "PALAVRAS:":
            secao = "palavras"
            continue

        if not linha:
            continue

        if secao == "estados":
            dados["estados"] = [
                item.strip()
                for item in linha.split(",")
            ]

        elif secao == "alfabeto":
            dados["alfabeto"] = [
                item.strip()
                for item in linha.split(",")
            ]

        elif secao == "inicial":
            dados["inicial"] = linha

        elif secao == "finais":
            dados["finais"] = [
                item.strip()
                for item in linha.split(",")
            ]

        elif secao == "transicoes":
            esquerda, direita = linha.split("->", 1)
            estado, simbolo = esquerda.split(",", 1)

            estado = estado.strip()
            simbolo = normalizar_simbolo(simbolo)

            destinos = [
                destino.strip()
                for destino in direita.split(",")
                if destino.strip()
            ]

            dados["transicoes"][(estado, simbolo)] = destinos

        elif secao == "palavras":
            dados["palavras"].append(linha)

    return criar_automato(
        estados=dados["estados"],
        alfabeto=dados["alfabeto"],
        inicial=dados["inicial"],
        finais=dados["finais"],
        transicoes=dados["transicoes"],
        palavras=dados["palavras"]
    )


def validar_automato(automato):
    campos_obrigatorios = {
        "estados",
        "alfabeto",
        "inicial",
        "finais",
        "transicoes",
        "palavras"
    }

    if not isinstance(automato, dict):
        raise ValueError(
            "O autômato deve ser representado por um dicionário."
        )

    if not campos_obrigatorios.issubset(automato.keys()):
        raise ValueError(
            "O arquivo não possui todos os campos obrigatórios."
        )

    estados = automato["estados"]
    alfabeto = automato["alfabeto"]
    inicial = automato["inicial"]
    finais = automato["finais"]
    transicoes = automato["transicoes"]
    palavras = automato["palavras"]

    if not estados:
        raise ValueError(
            "O conjunto de estados não pode ser vazio."
        )

    if len(estados) != len(set(estados)):
        raise ValueError(
            "Existem estados repetidos."
        )

    if len(alfabeto) != len(set(alfabeto)):
        raise ValueError(
            "Existem símbolos repetidos no alfabeto."
        )

    if any(
        normalizar_simbolo(simbolo) == EPSILON
        for simbolo in alfabeto
    ):
        raise ValueError(
            "EPSILON não pode fazer parte do alfabeto."
        )

    if inicial not in estados:
        raise ValueError(
            "O estado inicial não pertence ao conjunto de estados."
        )

    for estado in finais:
        if estado not in estados:
            raise ValueError(
                f"O estado final '{estado}' "
                "não pertence ao conjunto de estados."
            )

    for (estado, simbolo), destinos in transicoes.items():
        if estado not in estados:
            raise ValueError(
                f"O estado '{estado}' usado em uma "
                "transição não existe."
            )

        simbolo = normalizar_simbolo(simbolo)

        if simbolo != EPSILON and simbolo not in alfabeto:
            raise ValueError(
                f"O símbolo '{simbolo}' usado em uma "
                "transição não pertence ao alfabeto."
            )

        if not isinstance(destinos, list) or not destinos:
            raise ValueError(
                f"A transição ({estado}, {simbolo}) "
                "deve possuir pelo menos um destino."
            )

        for destino in destinos:
            if destino not in estados:
                raise ValueError(
                    f"O estado destino '{destino}' "
                    "não pertence ao conjunto de estados."
                )

    for palavra in palavras:
        for simbolo in palavra:
            if simbolo not in alfabeto:
                raise ValueError(
                    f"O símbolo '{simbolo}' da palavra "
                    f"'{palavra}' não pertence ao alfabeto."
                )

    return True