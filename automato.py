#estrutura do afn-e
EPSILON = "eps" #constante para representar movimentos vazios 


def criar_automato(estados, alfabeto, inicial, finais, transicoes, palavras):
    return {
        "estados": estados,
        "alfabeto": alfabeto,
        "inicial": inicial,
        "finais": finais,
        "transicoes": transicoes,
        "palavras": palavras
    }
    
    
    '''automato deve sem pre ter a mesma estrutura:
    {
    "estados": ["q0", "q1", "q2"],
    "alfabeto": ["a", "b"],
    "inicial": "q0",
    "finais": ["q2"],
    "transicoes": {
        ("q0", "a"): ["q1"],
        ("q0", "eps"): ["q2"]
    },
    "palavras": ["ab", "ba", ""]
}
'''