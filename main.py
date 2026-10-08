#integrante 3
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


def main():
    print("=" * 50)
    print("SIMULADOR DE AFN-EPSILON")
    print("=" * 50)

    caminho = input(
        "\nDigite o caminho do arquivo do autômato "
        "(.json ou .txt): "
    ).strip()

    try:
        automato = carregar_automato(caminho)
        validar_automato(automato)

        print("\nAutômato carregado e validado com sucesso.")

        print(f"Estados: {formatar_conjunto(set(automato['estados']))}")
        print(f"Alfabeto: {automato['alfabeto']}")
        print(f"Estado inicial: {automato['inicial']}")
        print(
            f"Estados finais: "
            f"{formatar_conjunto(set(automato['finais']))}"
        )

    except (OSError, ValueError, KeyError) as erro:
        print(f"\nErro ao carregar o autômato: {erro}")
        return

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