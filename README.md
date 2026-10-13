# Simulador de AFN-ε

Simulador e reconhecedor de Autômatos Finitos Não Determinísticos com movimentos vazios (AFN-ε).

O programa carrega um autômato a partir de um arquivo TXT ou JSON, valida sua definição e processa as palavras listadas no arquivo, mostrando o passo a passo da computação (conjunto inicial com fecho-ε, estados ativos após cada símbolo lido, resultado e justificativa).

Todo o cálculo do fecho-ε e o rastreamento das transições foram implementados manualmente, sem bibliotecas de Teoria da Computação, Teoria dos Grafos ou Autômatos.

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
│   └── multiplos\_destinos.json
│
└── testes/
    └── test\_parser.py
```

## Descrição dos arquivos

* **`automato.py`**: define a estrutura do AFN-ε e a convenção para o símbolo epsilon.
* **`parser.py`**: realiza a leitura dos arquivos TXT e JSON e valida a definição do autômato.
* **`simulador.py`**: realiza o cálculo do fecho-ε, a movimentação entre estados e a simulação das palavras.
* **`main.py`**: integra o parser e o simulador, trata os erros e apresenta os resultados.
* **`dados/`**: contém exemplos válidos e inválidos de entrada.
* **`testes/`**: contém os testes do parser.

## Requisitos

* Python 3.10 ou superior
* Nenhuma biblioteca externa é necessária.

## Execução

1. Abra o terminal na pasta do projeto e execute:

```bash
   python main.py
   ```

2. O programa solicitará o caminho do arquivo do autômato. Exemplos:

```text
   dados/exemplo.json
   dados/exemplo.txt
   dados/multiplos\_destinos.json
   ```

3. O programa carrega e valida o autômato e simula, uma a uma, todas as palavras listadas no arquivo.

## Formato do arquivo de entrada

### JSON

O arquivo JSON deve possuir os seguintes campos:

```json
{
    "estados": \["q0", "q1", "q2"],
    "alfabeto": \["a", "b"],
    "inicial": "q0",
    "finais": \["q2"],
    "transicoes": {
        "q0,a": \["q1"],
        "q0,eps": \["q2"],
        "q1,b": \["q2"]
    },
    "palavras": \["ab", "a", "b", ""]
}
```

Cada chave de `transicoes` tem o formato `"estado,símbolo"` e o valor é a lista de estados destino (pode haver mais de um destino).

### TXT

O arquivo TXT deve seguir a estrutura:

```text
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
```

Para vários destinos, separe-os por vírgula: `q0,a->q1,q2`.

### Transição vazia (ε)

Uma transição ε pode ser escrita como `eps`, `epsilon`, `lambda`, `ε` ou `λ`. Internamente, todas essas formas são normalizadas para `eps`. O símbolo ε não pode fazer parte do alfabeto.

### Palavra vazia

A palavra vazia só pode ser testada pelo formato JSON (`""` na lista de palavras). No formato TXT, linhas em branco são ignoradas pelo parser, portanto não é possível declará-la.

## Simulação

Para cada palavra, o programa:

* inicia no estado inicial;
* calcula o fecho-ε do estado inicial;
* lê cada símbolo da palavra;
* encontra os estados alcançados pelo símbolo;
* calcula novamente o fecho-ε do resultado;
* verifica, ao final, se algum estado ativo pertence ao conjunto de estados finais.

> A palavra é \*\*aceita\*\* quando a interseção entre os estados ativos ao final da leitura e o conjunto F é não vazia. Caso contrário, é \*\*rejeitada\*\*.

## Exemplos de execução

### Autômato válido (`dados/exemplo.json`)

```text
==================================================
SIMULADOR DE AFN-EPSILON
==================================================

Digite o caminho do arquivo do autômato (.json ou .txt): dados/exemplo.json

Autômato carregado e validado com sucesso.
Estados: {q0, q1, q2}
Alfabeto: \['a', 'b']
Estado inicial: q0
Estados finais: {q2}

Quantidade de palavras: 4

==================================================
PALAVRA: 'ab'
==================================================
Estado inicial após fecho-epsilon: {q0, q2}

Lendo símbolo: 'a'
  Estados anteriores: {q0, q2}
  Destinos antes do fecho-epsilon: {q1}
  Estados ativos após fecho-epsilon: {q1}

Lendo símbolo: 'b'
  Estados anteriores: {q1}
  Destinos antes do fecho-epsilon: {q2}
  Estados ativos após fecho-epsilon: {q2}

Estados finais: {q2}
Estados finais ativos: {q2}
Justificativa: {q2} ∩ F{q2} = {q2} ≠ ∅
RESULTADO: ACEITA
```

Resultados esperados para as quatro palavras de `exemplo.json`:

|Palavra|Resultado|
|-|-|
|`ab`|ACEITA|
|`a`|REJEITADA|
|`b`|REJEITADA|
|`""` (vazia)|ACEITA (o fecho-ε de q0 já contém o estado final q2)|

### Tratamento de erros

Quando ocorre algum erro (arquivo inexistente, formato inválido ou autômato inconsistente), o programa exibe uma mensagem clara explicando o problema e **é encerrado** em seguida, sem mostrar o erro interno do Python. Ele não pede o caminho novamente: para tentar outro arquivo, execute `python main.py` de novo.

Exemplo 1:

```text
Digite o caminho do arquivo do autômato (.json ou .txt): dados/nao\_existe.json

Erro: arquivo 'dados/nao\_existe.json' não encontrado.
```

Exemplo 2:

```text
Digite o caminho do arquivo do autômato (.json ou .txt): dados/invalido.json

Erro: autômato inconsistente: O estado final 'q2' não pertence ao conjunto de estados.
```

Mensagens possíveis:

|Situação|Mensagem|
|-|-|
|Arquivo inexistente|`arquivo '...' não encontrado`|
|Extensão diferente de `.json` e `.txt`|`formato de arquivo inválido`|
|JSON mal formatado|`JSON mal formatado (linha, coluna)`|
|Campo obrigatório ausente|`campo obrigatório ausente no arquivo`|
|Autômato inconsistente|`autômato inconsistente: ...`|

## Testes

* Os testes do parser podem ser executados com: `python -m testes.test\_parser`

Os testes verificam, entre outros casos:

* arquivo JSON válido;
* arquivo TXT válido;
* arquivos inválidos;
* transições epsilon;
* múltiplos destinos;
* estado inicial inválido;
* símbolo de transição inválido;
* estado destino inválido;
* estados repetidos;
* símbolos repetidos;
* epsilon no alfabeto;
* palavra contendo símbolo inválido.

