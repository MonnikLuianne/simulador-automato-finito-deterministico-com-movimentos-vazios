"""
simulador.py — Motor de simulação de AFN-ε (Integrante 2)

Funções exportadas:
    fecho_epsilon(estados, transicoes) -> set
    mover(estados, simbolo, transicoes) -> set
    simular(automato, palavra) -> dict

O dicionário `automato` segue o formato combinado com o parser (Integrante 1):
    {
      'estados':    ['q0', 'q1', 'q2'],
      'alfabeto':   ['a', 'b'],
      'inicial':    'q0',
      'finais':     ['q2'],
      'transicoes': { ('q0','a'): ['q1'], ('q0','eps'): ['q2'] },
      'palavras':   ['ab', 'ba', '']
    }

Nenhuma biblioteca de autômatos/grafos é usada: a busca é feita à mão.
"""

# Convenção para transição vazia. 'eps' é o padrão combinado com o parser;
# os demais nomes são aceitos para tolerar variações no arquivo de entrada.
EPSILON = 'eps'
SIMBOLOS_EPSILON = ('eps', 'epsilon', 'lambda', 'ε', 'λ', '')


def _destinos(transicoes, estado, simbolo):
    """Retorna δ(estado, simbolo) como lista (vazia se não houver transição)."""
    return transicoes.get((estado, simbolo), [])


def _destinos_epsilon(transicoes, estado):
    """Retorna todos os destinos de `estado` por transições vazias."""
    destinos = []
    for eps in SIMBOLOS_EPSILON:
        destinos.extend(_destinos(transicoes, estado, eps))
    return destinos


def fecho_epsilon(estados, transicoes):
    """
    Calcula o fecho-ε de um conjunto de estados: todos os estados alcançáveis
    a partir deles usando zero ou mais transições ε.

    Algoritmo: busca em profundidade (DFS) com pilha explícita.
      1. O resultado começa com os próprios estados (zero transições ε).
      2. Enquanto a pilha não estiver vazia, retira um estado e, para cada
         destino por ε ainda não visitado, adiciona ao resultado e empilha.
    O conjunto `fecho` também funciona como "visitados", o que garante término
    mesmo com ciclos de ε (ex.: q0 -ε-> q1 -ε-> q0).
    """
    fecho = set(estados)
    pilha = list(estados)

    while pilha:
        atual = pilha.pop()
        for destino in _destinos_epsilon(transicoes, atual):
            if destino not in fecho:
                fecho.add(destino)
                pilha.append(destino)

    return fecho


def mover(estados, simbolo, transicoes):
    """
    Um passo da computação: lê `simbolo` a partir do conjunto `estados`.

        mover(S, a) = fecho-ε( ⋃_{q ∈ S} δ(q, a) )

    Pressupõe que `estados` já está fechado por ε (o que `simular` garante).
    """
    alcancados = set()
    for estado in estados:
        alcancados.update(_destinos(transicoes, estado, simbolo))
    return fecho_epsilon(alcancados, transicoes)


def formatar_conjunto(estados):
    """Formata um conjunto de estados de forma determinística: {q0, q1}."""
    if not estados:
        return '∅'
    return '{' + ', '.join(sorted(estados)) + '}'


def simular(automato, palavra):
    """
    Simula o AFN-ε sobre `palavra` e devolve o histórico da computação.

    Retorno:
      {
        'palavra': 'ab',
        'inicial': {'q0', 'q1'},          # fecho-ε({q0})
        'passos': [
           {'simbolo': 'a',
            'estados_anteriores': {...},  # conjunto antes de ler o símbolo
            'sem_fecho': {...},           # ⋃ δ(q, a), antes do fecho-ε
            'estados_ativos': {...},      # após o fecho-ε
            'fora_do_alfabeto': False},
           ...
        ],
        'finais_ativos': {'q2'},          # estados_ativos_finais ∩ F
        'aceita': True,
        'justificativa': '{q2} ∩ F({q2}) = {q2} ≠ ∅'
      }

    Palavra vazia: não há passos; aceita se fecho-ε(inicial) ∩ F ≠ ∅.
    """
    transicoes = automato['transicoes']
    finais = set(automato['finais'])
    alfabeto = set(automato.get('alfabeto', []))

    # 1. Conjunto inicial de estados ativos.
    ativos = fecho_epsilon({automato['inicial']}, transicoes)
    inicial = set(ativos)

    # 2. Um passo para cada símbolo lido.
    passos = []
    for simbolo in palavra:
        sem_fecho = set()
        for estado in ativos:
            sem_fecho.update(_destinos(transicoes, estado, simbolo))
        novos = fecho_epsilon(sem_fecho, transicoes)

        passos.append({
            'simbolo': simbolo,
            'estados_anteriores': set(ativos),
            'sem_fecho': sem_fecho,
            'estados_ativos': novos,
            'fora_do_alfabeto': bool(alfabeto) and simbolo not in alfabeto,
        })
        ativos = novos
        # Se `ativos` ficar vazio, continua vazio até o fim (nenhuma
        # transição sai de ∅); seguimos registrando os passos mesmo assim.

    # 3. Aceitação: interseção entre estados ativos finais e F.
    finais_ativos = ativos & finais
    aceita = len(finais_ativos) > 0
    justificativa = (
        f"{formatar_conjunto(ativos)} ∩ F{formatar_conjunto(finais)} = "
        f"{formatar_conjunto(finais_ativos)} {'≠' if aceita else '='} ∅"
    )

    return {
        'palavra': palavra,
        'inicial': inicial,
        'passos': passos,
        'finais_ativos': finais_ativos,
        'aceita': aceita,
        'justificativa': justificativa,
    }


# ---------------------------------------------------------------------------
# Testes manuais: autômato montado à mão, sem depender do parser.
# Execute com:  python3 simulador.py
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    # L = a* b*   (q0 lê a's, ε para q1, q1 lê b's; q1 é final)
    ab = {
        'estados': ['q0', 'q1'],
        'alfabeto': ['a', 'b'],
        'inicial': 'q0',
        'finais': ['q1'],
        'transicoes': {
            ('q0', 'a'): ['q0'],
            ('q0', 'eps'): ['q1'],
            ('q1', 'b'): ['q1'],
        },
    }

    # Ciclo de ε (q0 -> q1 -> q2 -> q0) para garantir que o fecho termina.
    ciclo = {
        'estados': ['q0', 'q1', 'q2'],
        'alfabeto': ['a'],
        'inicial': 'q0',
        'finais': ['q2'],
        'transicoes': {
            ('q0', 'eps'): ['q1'],
            ('q1', 'eps'): ['q2'],
            ('q2', 'eps'): ['q0'],
        },
    }

    # Não determinismo: palavras sobre {a,b} terminadas em "ab".
    termina_ab = {
        'estados': ['q0', 'q1', 'q2'],
        'alfabeto': ['a', 'b'],
        'inicial': 'q0',
        'finais': ['q2'],
        'transicoes': {
            ('q0', 'a'): ['q0', 'q1'],
            ('q0', 'b'): ['q0'],
            ('q1', 'b'): ['q2'],
        },
    }

    assert fecho_epsilon({'q0'}, ab['transicoes']) == {'q0', 'q1'}
    assert fecho_epsilon({'q0'}, ciclo['transicoes']) == {'q0', 'q1', 'q2'}
    assert mover({'q0', 'q1'}, 'b', ab['transicoes']) == {'q1'}

    casos = [
        (ab, '', True), (ab, 'aabb', True), (ab, 'ba', False), (ab, 'c', False),
        (ciclo, '', True), (ciclo, 'a', False),
        (termina_ab, 'ab', True), (termina_ab, 'bab', True),
        (termina_ab, 'aba', False), (termina_ab, '', False),
    ]
    for automato, palavra, esperado in casos:
        r = simular(automato, palavra)
        assert r['aceita'] == esperado, (palavra, r)

    # Exemplo de saída (a exibição "oficial" fica a cargo do Integrante 3).
    r = simular(termina_ab, 'bab')
    print(f"Palavra '{r['palavra']}'")
    print(f"  Inicial: {formatar_conjunto(r['inicial'])}")
    for p in r['passos']:
        print(f"  Lendo '{p['simbolo']}': mover({formatar_conjunto(p['estados_anteriores'])}, "
              f"{p['simbolo']}) = {formatar_conjunto(p['sem_fecho'])} "
              f"-> fecho-ε = {formatar_conjunto(p['estados_ativos'])}")
    print(f"  {r['justificativa']} --> {'ACEITA' if r['aceita'] else 'REJEITADA'}")
    print('\nTodos os testes passaram.')
