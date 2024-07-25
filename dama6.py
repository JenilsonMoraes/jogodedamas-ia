import tkinter as tk
from tkinter import messagebox
import random

# Dimensões do tabuleiro e peças
TAMANHO_CELULA = 100
DIMENSAO_TABULEIRO = 6
Cores = ["white", "black"]

# Função para inicializar o tabuleiro
def inicializar_tabuleiro():
    tabuleiro = [
        [0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, -1, 0, -1, 0, -1],
        [-1, 0, -1, 0, -1, 0],
    ]
    return tabuleiro

# Função para atualizar o tabuleiro na interface gráfica
def atualizar_tabuleiro(tabuleiro):
    canvas.delete("all")
    desenhar_tabuleiro()
    for i in range(DIMENSAO_TABULEIRO):
        for j in range(DIMENSAO_TABULEIRO):
            if tabuleiro[i][j] != 0:
                cor = "red" if tabuleiro[i][j] > 0 else "blue"
                if abs(tabuleiro[i][j]) == 1:
                    canvas.create_oval(j*TAMANHO_CELULA + 10, i*TAMANHO_CELULA + 10,
                                       j*TAMANHO_CELULA + TAMANHO_CELULA - 10, i*TAMANHO_CELULA + TAMANHO_CELULA - 10,
                                       fill=cor)
                elif abs(tabuleiro[i][j]) == 2:
                    if cor == "red":
                        canvas.create_text(j*TAMANHO_CELULA + TAMANHO_CELULA / 2,
                            i*TAMANHO_CELULA + TAMANHO_CELULA / 2,
                            text="👑", font=("Arial", 24), fill="red")
                    else:
                        canvas.create_text(j*TAMANHO_CELULA + TAMANHO_CELULA / 2,
                            i*TAMANHO_CELULA + TAMANHO_CELULA / 2,
                            text="👑", font=("Arial", 24), fill="blue")
    root.update()

# Função para desenhar o tabuleiro
def desenhar_tabuleiro():
    for i in range(DIMENSAO_TABULEIRO):
        for j in range(DIMENSAO_TABULEIRO):
            cor = Cores[(i+j)%2]
            canvas.create_rectangle(j*TAMANHO_CELULA, i*TAMANHO_CELULA,
                                    j*TAMANHO_CELULA + TAMANHO_CELULA, i*TAMANHO_CELULA + TAMANHO_CELULA,
                                    fill=cor, outline="black")

def validar_movimento(tabuleiro, origem, destino):
    x1, y1 = origem
    x2, y2 = destino
    peca = tabuleiro[x1][y1]
    destino_valido = False

    if abs(peca) == 2:  # Dama
        return False

    if 0 <= x2 < DIMENSAO_TABULEIRO and 0 <= y2 < DIMENSAO_TABULEIRO and tabuleiro[x2][y2] == 0:
        if abs(peca) == 1:  # Peça normal
            if (peca == 1 and x2 - x1 == 1 or peca == -1 and x2 - x1 == -1) and abs(y2 - y1) == 1:
                destino_valido = True
            elif (peca == 1 and x2 - x1 == 2 or peca == -1 and x2 - x1 == -2) and abs(y2 - y1) == 2:
                meio_x, meio_y = (x1 + x2) // 2, (y1 + y2) // 2
                if tabuleiro[meio_x][meio_y] == -peca:
                    destino_valido = True

    return destino_valido

def aplicar_movimento(tabuleiro, origem, destino):
    x1, y1 = origem
    x2, y2 = destino
    peca = tabuleiro[x1][y1]
    tabuleiro[x2][y2] = peca
    tabuleiro[x1][y1] = 0

    # Remover a peça capturada
    if abs(x2 - x1) == 2 and abs(y2 - y1) == 2:
        meio_x, meio_y = (x1 + x2) // 2, (y1 + y2) // 2
        tabuleiro[meio_x][meio_y] = 0

    # Promoção de peças
    if peca == 1 and x2 == DIMENSAO_TABULEIRO - 1:
        tabuleiro[x2][y2] = 2
    elif peca == -1 and x2 == 0:
        tabuleiro[x2][y2] = -2

def verificar_fim_de_jogo(tabuleiro, minimax):
    jogador1_tem_pecas = any(tabuleiro[x][y] > 0 for x in range(DIMENSAO_TABULEIRO) for y in range(DIMENSAO_TABULEIRO))
    jogador2_tem_pecas = any(tabuleiro[x][y] < 0 for x in range(DIMENSAO_TABULEIRO) for y in range(DIMENSAO_TABULEIRO))

    jogador1_tem_movimentos = any(
        validar_movimento(tabuleiro, (x, y), (x + dx, y + dy))
        for x in range(DIMENSAO_TABULEIRO) for y in range(DIMENSAO_TABULEIRO)
        for dx in (-1, 1, -2, 2) for dy in (-1, 1, -2, 2)
        if tabuleiro[x][y] > 0
    )
    jogador2_tem_movimentos = any(
        validar_movimento(tabuleiro, (x, y), (x + dx, y + dy))
        for x in range(DIMENSAO_TABULEIRO) for y in range(DIMENSAO_TABULEIRO)
        for dx in (-1, 1, -2, 2) for dy in (-1, 1, -2, 2)
        if tabuleiro[x][y] < 0
    )

    if not jogador1_tem_pecas or not jogador1_tem_movimentos:
        if (minimax):
            root.quit()
            return True
        else:
            messagebox.showinfo("Fim de Jogo", "Jogador Azul venceu!")
            root.quit()
            return True
    if not jogador2_tem_pecas or not jogador2_tem_movimentos:
        if (minimax):
            root.quit()
            return True
        else:
            messagebox.showinfo("Fim de Jogo", "Jogador Vermelho venceu!")
            root.quit()
            return True
    return False

def mover_peca(event):
    global selecionado, tabuleiro, turno
    x, y = event.y // TAMANHO_CELULA, event.x // TAMANHO_CELULA

    if selecionado is None:
        if tabuleiro[x][y] == turno or tabuleiro[x][y] == 2*turno:
            selecionado = (x, y)
            canvas.create_rectangle(y*TAMANHO_CELULA, x*TAMANHO_CELULA,
                                    y*TAMANHO_CELULA + TAMANHO_CELULA, x*TAMANHO_CELULA + TAMANHO_CELULA,
                                    outline="green", width=2, tags="highlight")
    else:
        destino = (x, y)
        if validar_movimento(tabuleiro, selecionado, destino):
            aplicar_movimento(tabuleiro, selecionado, destino)
            selecionado = None
            atualizar_tabuleiro(tabuleiro)
            if verificar_fim_de_jogo(tabuleiro, True):
                canvas.unbind("<Button-1>")
            else:
                turno *= -1
                if turno == -1:
                    root.after(500, movimento_computador)  # Adiciona um pequeno delay para o movimento do computador
        else:
            selecionado = None
            canvas.delete("highlight")
        atualizar_tabuleiro(tabuleiro)

def avaliacao(tabuleiro):
    score = 0
    for x in range(DIMENSAO_TABULEIRO):
        for y in range(DIMENSAO_TABULEIRO):
            piece = tabuleiro[x][y]
            if piece == 1:  # Peça normal do Jogador Vermelho
                score += 5
            elif piece == 2:  # Dama do Jogador Vermelho
                score += 10
            elif piece == -1:  # Peça normal do Jogador Azul
                score -= 5
            elif piece == -2:  # Dama do Jogador Azul
                score -= 10
    return score

def minimax(tabuleiro, profundidade, maximizando):
    if profundidade == 0 or verificar_fim_de_jogo(tabuleiro, False):
        return avaliacao(tabuleiro), None

    movimentos_possiveis = []
    capturas = []
    for x in range(DIMENSAO_TABULEIRO):
        for y in range(DIMENSAO_TABULEIRO):
            if (maximizando and tabuleiro[x][y] < 0) or (not maximizando and tabuleiro[x][y] > 0):
                for dx in (-1, 1, -2, 2):
                    for dy in (-1, 1, -2, 2):
                        destino = (x + dx, y + dy)
                        if validar_movimento(tabuleiro, (x, y), destino):
                            if abs(x - destino[0]) == 2:  # Captura
                                capturas.append(((x, y), destino))
                            else:
                                movimentos_possiveis.append(((x, y), destino))

    if capturas:
        movimentos_possiveis = capturas

    if maximizando:
        max_avaliacao = float('-inf')
        melhor_movimento = None
        for origem, destino in movimentos_possiveis:
            novo_tabuleiro = [linha[:] for linha in tabuleiro]
            aplicar_movimento(novo_tabuleiro, origem, destino)
            avaliacao_atual, _ = minimax(novo_tabuleiro, profundidade - 1, False)
            if avaliacao_atual > max_avaliacao:
                max_avaliacao = avaliacao_atual
                melhor_movimento = (origem, destino)
        return max_avaliacao, melhor_movimento
    else:
        min_avaliacao = float('inf')
        melhor_movimento = None
        for origem, destino in movimentos_possiveis:
            novo_tabuleiro = [linha[:] for linha in tabuleiro]
            aplicar_movimento(novo_tabuleiro, origem, destino)
            avaliacao_atual, _ = minimax(novo_tabuleiro, profundidade - 1, True)
            if avaliacao_atual < min_avaliacao:
                min_avaliacao = avaliacao_atual
                melhor_movimento = (origem, destino)
        return min_avaliacao, melhor_movimento

def movimento_computador():
    global turno
    if not verificar_fim_de_jogo(tabuleiro, False):  # Verifica se o jogo já terminou
        _, melhor_movimento = minimax(tabuleiro, 3, True)  # Pode ajustar a profundidade conforme necessário
        if melhor_movimento:
            origem, destino = melhor_movimento
            aplicar_movimento(tabuleiro, origem, destino)
            atualizar_tabuleiro(tabuleiro)
            if verificar_fim_de_jogo(tabuleiro, False):
                canvas.unbind("<Button-1>")
            else:
                turno *= -1

def main():
    global canvas, root, tabuleiro, selecionado, turno
    selecionado = None
    turno = 1  # Começa com o jogador 1

    root = tk.Tk()
    root.title("Jogo de Damas")

    canvas = tk.Canvas(root, width=TAMANHO_CELULA*DIMENSAO_TABULEIRO, height=TAMANHO_CELULA*DIMENSAO_TABULEIRO)
    canvas.pack()

    desenhar_tabuleiro()
    tabuleiro = inicializar_tabuleiro()
    atualizar_tabuleiro(tabuleiro)
    
    canvas.bind("<Button-1>", mover_peca)
    
    root.mainloop()

if __name__ == "__main__":
    main()
