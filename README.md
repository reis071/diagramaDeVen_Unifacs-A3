# Calculadora de Diagrama de Venn com Flet

Este projeto é uma **Calculadora Avançada de Diagrama de Venn** interativa, construída utilizando a biblioteca **Flet** para a interface de usuário e **Matplotlib-Venn** para a geração dos diagramas. A aplicação permite calcular a união de conjuntos e elementos fora da união, além de visualizar diagramas de Venn para 2 ou 3 conjuntos.

-----

## Funcionalidades

  * **Entrada Dinâmica de Conjuntos:** Gere campos de entrada para 2 a 6 conjuntos, permitindo que você especifique o número total de elementos em cada conjunto e suas interseções.
  * **Cálculo da União:** Calcula o total de elementos na união de todos os conjuntos inseridos, aplicando o Princípio da Inclusão-Exclusão.
  * **Cálculo de Elementos Externos:** Determina quantos elementos do universo estão fora da união dos conjuntos.
  * **Geração de Diagramas de Venn:** Para 2 ou 3 conjuntos, a aplicação gera e exibe um diagrama de Venn visual, representando graficamente as relações entre os conjuntos e suas interseções.
  * **Validação de Entrada:** Mensagens de erro claras são exibidas para entradas inválidas ou inconsistências nos dados.
  * **Interface Intuitiva:** Desenvolvida com Flet, oferece uma experiência de usuário limpa e responsiva.

-----

## Tecnologias Utilizadas

  * **Flet:** Framework para construção de interfaces de usuário reativas em Python.
  * **Itetools:** Módulo Python para criar iteradores para loops eficientes.
  * **Matplotlib:** Biblioteca de plotagem para Python, utilizada indiretamente pelo Matplotlib-Venn.
  * **Matplotlib-Venn:** Extensão do Matplotlib para desenhar diagramas de Venn de 2 e 3 conjuntos.

-----

## Como Executar

Para executar esta aplicação, siga os passos abaixo:

1.  **Clone o repositório (se aplicável) ou salve o código:**

    ```bash
    git clone https://github.com/reis071/diagramaDeVen_Unifacs-A3.git
    cd projetoMatematica
    ```

    Ou simplesmente salve o código fornecido em um arquivo `main.py`.

2.  **Instale as dependências:**
    Certifique-se de ter o Python instalado. Em seguida, instale as bibliotecas necessárias:

    ```bash
    pip install flet matplotlib matplotlib-venn
    ```

3.  **Execute a aplicação:**

    ```bash
    python main.py
    ```

    Isso abrirá a aplicação em uma nova janela do navegador ou em uma janela nativa, dependendo da configuração do Flet.

-----

## Como Usar

1.  **Defina o Número de Conjuntos:** Na caixa de texto "Quantos conjuntos? (2-6)", insira o número de conjuntos com os quais você deseja trabalhar (mínimo 2, máximo 6).
2.  **Clique em "Gerar Campos":** Isso criará dinamicamente os campos de entrada para cada conjunto e suas possíveis interseções.
3.  **Preencha os Valores:**
      * Insira o "Tamanho do Conjunto Universo (Total)".
      * Para cada conjunto (ex: "Total no Conjunto A"), insira o número total de elementos naquele conjunto.
      * Para cada interseção (ex: "Interseção (A ∩ B)"), insira o número de elementos comuns a esses conjuntos.
4.  **Clique em "Calcular e Gerar Diagrama":** A aplicação processará os dados e exibirá:
      * O total de elementos na união dos conjuntos.
      * O número de elementos que estão fora de todos os conjuntos.
      * Um diagrama de Venn (para 2 ou 3 conjuntos) visualizando as relações e os tamanhos das regiões.

-----

## Exemplo de Uso (2 Conjuntos)

Imagine que você tem:

  * Universo: 100 elementos
  * Conjunto A: 60 elementos
  * Conjunto B: 40 elementos
  * Interseção (A ∩ B): 20 elementos

A calculadora retornará:

  * União (A ∪ B): $60 + 40 - 20 = 80$
  * Elementos fora da união: $100 - 80 = 20$
  * Um diagrama de Venn mostrando as regiões exclusivas de A, exclusivas de B e a interseção.

-----

## Limitações

  * **Diagramas de Venn:** A visualização do diagrama é suportada apenas para 2 ou 3 conjuntos devido às complexidades inerentes à representação visual de múltiplos conjuntos. Os cálculos de união e elementos externos funcionam para até 6 conjuntos.
  * **Validação:** Embora haja validação básica, certifique-se de que os valores de interseção não sejam maiores que os totais dos conjuntos individuais para evitar resultados negativos em regiões exclusivas.
