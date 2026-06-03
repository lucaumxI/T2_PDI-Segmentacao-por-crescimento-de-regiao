import numpy as np
from PIL import Image
from pathlib import Path

def segmentacao(imagem: np.ndarray, regiaoInicial: list[tuple[int, int]], f: float) -> set[tuple[int, int]]:
    # Inicializacao
    regiao = set(regiaoInicial)
    borda = set()

    # Definicao do conjunto borda
    defBorda(regiao, borda, imagem)

    valores_regiao = [imagem[rx, ry] for rx, ry in regiao]
    mu = np.mean(valores_regiao)
    sigma = np.std(valores_regiao) if len(valores_regiao) > 1 else 0
    
    houve_crescimento = True
    while houve_crescimento:
        houve_crescimento = False
        novos_pixels_regiao = set()
        novos_pixels_borda = set()

        for bx, by in borda:
            intensidade = imagem[bx, by]
            if mu - (f * sigma) < intensidade < mu + (f * sigma):
                novos_pixels_regiao.add((bx, by))

                vizinhos = [(bx+1, by), (bx-1, by), (bx, by+1), (bx, by-1)]
                for nx, ny in vizinhos:
                    if 0 <= nx < linhas and 0 <= ny < colunas:
                        novos_pixels_borda.add((nx, ny))

        # me deu preguiça de terminar, depois eu fuço mais

        

    return regiao

# def nome_da_funcao(parametro: set[tuple[int, int]]) -> set[tuple[int, int]]:

def defBorda(regiao: set[tuple[int, int]] , borda: set[tuple[int, int]], imagem: np.ndarray) -> set[tuple[int, int]]:
    # blablabla implementa como seta a borda
    return borda
def main():
    caminho = "CAMINHO_IMAGEM"
    imagem = np.array(Image.open(caminho))

    segmentacao(imagem)
if __name__ == "__main__":
    main()