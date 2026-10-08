# Simulador de AFN-ε

Simulador e reconhecedor de Autômatos Finitos Não Determinísticos com movimentos vazios (AFN-ε).

O programa permite carregar um autômato a partir de arquivos TXT ou JSON, validar sua definição e processar as palavras fornecidas no arquivo de entrada, mostrando o passo a passo da computação.

## Estrutura do projeto

```text
simulador-automato-finito-deterministico-com-movimentos-vazios/
│
├── automato.py
├── parser.py
├── simulador.py
├── main.py
├── README.md
│
├── dados/
│   ├── exemplo.json
│   ├── exemplo.txt
│   ├── invalido.json
│   ├── invalido.txt
│   └── multiplos_destinos.json
│
└── testes/
    └── test_parser.py
```
## Descrição dos arquivos
- automato.py: define a estrutura do AFN-ε e a convenção para o símbolo epsilon.
- parser.py: realiza a leitura dos arquivos TXT e JSON e valida a definição do autômato.
- simulador.py: realiza o cálculo do fecho-epsilon, movimentação entre estados e simulação das palavras.
- main.py: integra o parser e o simulador e apresenta os resultados.
- dados/: contém exemplos válidos e inválidos de entrada.
- testes/: contém os testes do parser.
## Requisitos
Python 3
Nenhuma biblioteca externa é necessária.
## Execução

1. Abra o terminal na pasta do projeto e execute: python main.py

2. O programa solicitará o caminho do arquivo do autômato.

Exemplo: dados/exemplo.json ou: dados/exemplo.txt
3. Formato JSON

O arquivo JSON deve possuir os seguintes campos:

{
    "estados": ["q0", "q1", "q2"],
    "alfabeto": ["a", "b"],
    "inicial": "q0",
    "finais": ["q2"],
    "transicoes": {
        "q0,a": ["q1"],
        "q0,eps": ["q2"],
        "q1,b": ["q2"]
    },
    "palavras": ["ab", "a", "b", ""]
}

4. Uma transição epsilon pode ser representada por:

eps, epsilon, lambda, ε, λ

Internamente, essas representações são normalizadas para eps.

5. Formato TXT

O arquivo TXT deve seguir a estrutura:

ESTADOS:
q0,q1,q2

ALFABETO:
a,b

INICIAL:
q0

FINAIS:
q2

TRANSICOES:
q0,a->q1
q0,eps->q2
q1,b->q2

PALAVRAS:
ab
a
b
## Simulação

Para cada palavra, o programa:

-inicia no estado inicial;
-calcula o fecho-epsilon;
-lê cada símbolo da palavra;
-encontra os estados alcançados pelo símbolo;
-calcula novamente o fecho-epsilon;
-verifica, ao final, se algum estado ativo pertence ao conjunto de estados finais.

> A palavra é aceita quando pelo menos um dos estados ativos ao final da leitura pertence ao conjunto de estados finais.

## Testes

- Os testes do parser podem ser executados com:

python -m testes.test_parser

Os testes verificam, entre outros casos:

arquivo JSON válido;
arquivo TXT válido;
arquivos inválidos;
transições epsilon;
múltiplos destinos;
estado inicial inválido;
símbolo de transição inválido;
estado destino inválido;
estados repetidos;
símbolos repetidos;
epsilon no alfabeto;
palavra contendo símbolo inválido.
