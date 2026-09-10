# Segmentação de Imagens por Crescimento de Região (*Region Growing*)

Este projeto implementa um algoritmo de segmentação de imagens baseado na técnica de Crescimento de Região (*Region Growing*). O script identifica e agrupa pixels contíguos que compartilham características de intensidade similares, destacando a região resultante.

## Como o Algoritmo Funciona

O processo de segmentação ocorre nas seguintes etapas:

1.  **Semente Aleatória:** O algoritmo escolhe um pixel aleatório da imagem e seleciona seus 4 vizinhos diretos (cima, baixo, esquerda, direita) para formar a região inicial.
2.  **Critério de Inclusão:** Para cada pixel na borda da região atual, verifica-se se a sua intensidade ($I_p$) está dentro do intervalo de aceitação baseado na média ($\mu$) e no desvio padrão ($\sigma$) da região:
    $$\mu - (f \times \sigma) \leq I_p \leq \mu + (f \times \sigma)$$
    Onde $f$ é um hiperparâmetro de tolerância (definido como 2.5 no código).
3.  **Atualização Dinâmica:** Sempre que novos pixels são adicionados à região, a média e o desvio padrão são recalculados dinamicamente utilizando fórmulas de passo único, otimizando o desempenho do algoritmo.
4.  **Convergência:** O algoritmo continua expandindo a borda até que nenhum novo pixel satisfaça o critério de inclusão.
5.  **Visualização:** O resultado é exibido lado a lado com a imagem original, utilizando uma máscara de cor vermelha para destacar a região segmentada.

## Pré-requisitos

Para executar o script, é necessário ter o Python instalado junto com as seguintes bibliotecas de processamento e visualização:

```bash
pip install numpy matplotlib Pillow
```

## Estrutura do Projeto

*   `main.py` (ou o nome do seu script): Contém a lógica principal do algoritmo e as funções de cálculo matemático.
*   `cameraman.tiff`: Imagem de teste. O código espera encontrar este arquivo no mesmo diretório de execução por padrão.

## Como Executar

1.  Certifique-se de que possui uma imagem válida (por padrão o script procura por `cameraman.tiff`) no diretório do projeto. Caso queira testar com outra imagem, altere a variável `caminho` na função `main()`.
2.  Execute o script:

```bash
python main.py
```

O terminal exibirá as dimensões da imagem, as coordenadas da semente aleatória escolhida e o número total de pixels da região segmentada. Em seguida, uma janela do `matplotlib` será aberta exibindo a imagem original e a segmentação finalizada.
