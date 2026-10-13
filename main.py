#integrante 3
import json

from parser import carregar_automato, validar_automato
from simulador import simular, formatar_conjunto


def mostrar_resultado(resultado, finais):
    print("\n" + "=" * 50)
    print(f"PALAVRA: '{resultado['palavra']}'")
    print("=" * 50)

    print(f"Estado inicial após fecho-epsilon: "
          f"{formatar_conjunto(resultado['inicial'])}")

    for passo in resultado["passos"]:
        print(f"\nLendo símbolo: '{passo['simbolo']}'")

        if passo["fora_do_alfabeto"]:
            print("  Símbolo fora do alfabeto.")

        print(
            f"  Estados anteriores: "
            f"{formatar_conjunto(passo['estados_anteriores'])}"
        )

        print(
            f"  Destinos antes do fecho-epsilon: "
            f"{formatar_conjunto(passo['sem_fecho'])}"
        )

        print(
            f"  Estados ativos após fecho-epsilon: "
            f"{formatar_conjunto(passo['estados_ativos'])}"
        )

    print(
        f"\nEstados finais: {formatar_conjunto(set(finais))}"
    )

    print(f"Estados finais ativos: "
          f"{formatar_conjunto(resultado['finais_ativos'])}")

    print(f"Justificativa: {resultado['justificativa']}")

    if resultado["aceita"]:
        print("RESULTADO: ACEITA")
    else:
        print("RESULTADO: REJEITADA")


def carregar_e_validar(caminho):
    
    if not caminho:
        print("\nErro: nenhum caminho de arquivo foi informado.")
        return None

    # Etapa 1: leitura do arquivo
    try:
        automato = carregar_automato(caminho)

    except FileNotFoundError:
        print(f"\nErro: arquivo '{caminho}' não encontrado.")
        return None

    except IsADirectoryError:
        print(f"\nErro: '{caminho}' é uma pasta, informe um arquivo.")
        return None

    except PermissionError:
        print(f"\nErro: sem permissão para ler o arquivo '{caminho}'.")
        return None

    except json.JSONDecodeError as erro:
        print(
            f"\nErro: JSON mal formatado (linha {erro.lineno}, "
            f"coluna {erro.colno}): {erro.msg}."
        )
        return None

    except KeyError as erro:
        print(
            f"\nErro: campo obrigatório ausente no arquivo: {erro.args[0]}."
        )
        return None

    except ValueError as erro:
        print(f"\nErro: formato de arquivo inválido: {erro}")
        return None

    except (TypeError, AttributeError):
        print(
            "\nErro: a estrutura do arquivo não segue o formato esperado. "
            "Consulte o README."
        )
        return None

    except OSError as erro:
        print(f"\nErro ao abrir o arquivo '{caminho}': {erro}")
        return None

    # Etapa 2: validação da consistência do autômato
    try:
        validar_automato(automato)

    except ValueError as erro:
        print(f"\nErro: autômato inconsistente: {erro}")
        return None

    return automato


def main():
    print("=" * 50)
    print("SIMULADOR DE AFN-EPSILON")
    print("=" * 50)

    caminho = input(
        "\nDigite o caminho do arquivo do autômato "
        "(.json ou .txt): "
    ).strip()

    automato = carregar_e_validar(caminho)

    if automato is None:
        return

    print("\nAutômato carregado e validado com sucesso.")

    print(f"Estados: {formatar_conjunto(set(automato['estados']))}")
    print(f"Alfabeto: {automato['alfabeto']}")
    print(f"Estado inicial: {automato['inicial']}")
    print(
        f"Estados finais: "
        f"{formatar_conjunto(set(automato['finais']))}"
    )

    palavras = automato.get("palavras", [])

    if not palavras:
        print("\nNenhuma palavra foi encontrada no arquivo.")
        return

    print(f"\nQuantidade de palavras: {len(palavras)}")

    for palavra in palavras:
        resultado = simular(automato, palavra)
        mostrar_resultado(resultado, automato["finais"])


if __name__ == "__main__":
    main()