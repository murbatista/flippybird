import pygame
import random
import math

pygame.init()

# ==========================================
# CONFIGURACAO GERAL
# ==========================================
LARGURA, ALTURA = 480, 640
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Astro Flappy - Multiverso")

relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 20, bold=True)
fonte_das_regras = pygame.font.SysFont("arial", 15, bold=True)
fonte_pequena = pygame.font.SysFont("arial", 16)
titulo = pygame.font.SysFont("arial", 34, bold=True)

BRANCO = (245, 248, 255)
CIANO = (60, 220, 255)
VERMELHO = (255, 75, 90)

# Jogador
JOGADOR_X = 105
y = ALTURA / 2
velocidade_y = 0
GRAVIDADE = 0.32
IMPULSO = -6.2

# Obstaculos
RAIO_METEORO = 23
ALTURA_PASSAGEM = 230
LARGURA_OBSTACULO = 78

# Modos de jogo
modo = "classico"
estado = "menu"
pontos = 0
obstaculos = []
proximo_id = 0
proxima_geracao = 0


# ==========================================
# TEMAS E DIFICULDADE
# ==========================================
def tema_atual():
    fase = pontos % 60

    if fase < 20:
        return "espaco"
    elif fase < 40:
        return "ovni"
    return "tempestade"


def nome_tema():
    tema = tema_atual()

    if tema == "espaco":
        return "ESPACO - ASTRONAUTA"
    elif tema == "ovni":
        return "CEU FUTURISTA - OVNI"
    return "TEMPESTADE - ROADSTER"


def velocidade_atual():
    if modo == "chuva":
        return min(3.5 + pontos * 0.045, 9.0)

    return min(2.7 + pontos * 0.025, 6.5)


def intervalo_atual():
    if modo == "chuva":
        return max(48, int(110 - pontos * 0.65))

    return max(78, int(145 - pontos * 0.45))


# ==========================================
# CRIACAO DE OBSTACULOS
# ==========================================
def criar_obstaculo(x=None):
    global proximo_id

    if x is None:
        x = LARGURA + 35

    tema = tema_atual()

    if tema == "espaco":
        tipo = "meteoro"
    elif tema == "ovni":
        tipo = "laser"
    else:
        tipo = "nuvem"

    grupo = []

    if modo == "classico":
        # Uma passagem vertical entre dois objetos.
        centro = random.randint(205, ALTURA - 205)
        topo = centro - ALTURA_PASSAGEM // 2
        base = centro + ALTURA_PASSAGEM // 2

        grupo.append({
            "id": proximo_id,
            "tipo": tipo,
            "lado": "topo",
            "x": float(x),
            "y": float(topo),
            "marcou": False
        })
        proximo_id += 1

        grupo.append({
            "id": proximo_id,
            "tipo": tipo,
            "lado": "baixo",
            "x": float(x),
            "y": float(base),
            "marcou": False
        })
        proximo_id += 1

    else:
        # Chuva: grupos de objetos soltos.
        if pontos < 20:
            quantidade = random.randint(2, 3)
        elif pontos < 40:
            quantidade = random.randint(3, 4)
        else:
            quantidade = random.randint(4, 5)

        for _ in range(quantidade):
            grupo.append({
                "id": proximo_id,
                "tipo": tipo,
                "x": float(x + random.randint(0, 100)),
                "y": float(random.randint(65, ALTURA - 65)),
                "marcou": False
            })
            proximo_id += 1

    return grupo


def reiniciar():
    global y, velocidade_y, obstaculos, pontos, estado
    global proximo_id, proxima_geracao

    y = ALTURA / 2
    velocidade_y = 0
    pontos = 0
    proximo_id = 0
    proxima_geracao = 0
    obstaculos = []

    obstaculos.extend(criar_obstaculo(440))
    estado = "jogando"


# ==========================================
# FUNDO
# ==========================================
estrelas = [
    (random.randrange(LARGURA),
     random.randrange(ALTURA),
     random.choice([1, 1, 2, 3]))
    for _ in range(100)
]


def desenhar_fundo():
    tema = tema_atual()

    if tema == "espaco":
        tela.fill((5, 8, 29))

        for sx, sy, tamanho in estrelas:
            pygame.draw.circle(
                tela, BRANCO, (sx, sy), tamanho
            )

        pygame.draw.circle(
            tela, (22, 25, 65), (375, 180), 90
        )
        pygame.draw.circle(
            tela, (30, 22, 70), (375, 180), 60
        )

    elif tema == "ovni":
        tela.fill((10, 32, 78))

        for sx, sy, tamanho in estrelas:
            pygame.draw.circle(
                tela, (140, 220, 255), (sx, sy), tamanho
            )

        pygame.draw.line(
            tela, (40, 150, 220), (0, 545), (480, 545), 2
        )

        for xx in range(20, 480, 60):
            pygame.draw.line(
                tela, (25, 80, 145),
                (xx, 545), (xx - 25, 640), 1
            )

    else:
        tela.fill((43, 49, 72))

        for xx, yy, raio in [
            (80, 130, 65), (360, 240, 75), (180, 420, 60)
        ]:
            pygame.draw.circle(
                tela, (60, 67, 92), (xx, yy), raio
            )
            pygame.draw.circle(
                tela, (68, 74, 100),
                (xx + 30, yy + 10), raio // 2
            )


# ==========================================
# PERSONAGENS
# ==========================================
def desenhar_astronauta(x, y):
    pygame.draw.rect(
        tela, (145, 165, 185),
        (x - 21, y - 8, 9, 21), border_radius=4
    )

    pygame.draw.line(
        tela, BRANCO, (x - 9, y + 2), (x - 19, y + 10), 5
    )
    pygame.draw.line(
        tela, BRANCO, (x + 9, y + 2), (x + 18, y - 4), 5
    )
    pygame.draw.line(
        tela, BRANCO, (x - 6, y + 13), (x - 11, y + 20), 5
    )
    pygame.draw.line(
        tela, BRANCO, (x + 6, y + 13), (x + 11, y + 20), 5
    )

    pygame.draw.ellipse(
        tela, BRANCO, (x - 13, y - 7, 26, 29)
    )
    pygame.draw.circle(tela, BRANCO, (x, y - 9), 16)
    pygame.draw.circle(
        tela, (25, 65, 110), (x + 2, y - 9), 11
    )
    pygame.draw.ellipse(
        tela, CIANO, (x - 4, y - 15, 7, 4)
    )


def desenhar_ovni(x, y):
    pygame.draw.polygon(
        tela, (30, 80, 125),
        [(x - 10, y + 8), (x + 10, y + 8),
         (x + 20, y + 24), (x - 20, y + 24)]
    )

    pygame.draw.ellipse(
        tela, (165, 180, 200), (x - 24, y - 3, 48, 17)
    )
    pygame.draw.ellipse(
        tela, (55, 200, 220), (x - 13, y - 14, 26, 19)
    )
    pygame.draw.ellipse(
        tela, (220, 245, 255), (x - 7, y - 11, 10, 6)
    )

    for dx in [-13, 0, 13]:
        pygame.draw.circle(
            tela, (255, 225, 90), (x + dx, y + 8), 3
        )


def desenhar_carro(x, y):
    pygame.draw.circle(tela, (15, 15, 22), (x - 15, y + 10), 8)
    pygame.draw.circle(tela, (15, 15, 22), (x + 17, y + 10), 8)
    pygame.draw.circle(tela, (190, 200, 210), (x - 15, y + 10), 4)
    pygame.draw.circle(tela, (190, 200, 210), (x + 17, y + 10), 4)

    pygame.draw.polygon(
        tela, (215, 35, 45),
        [(x - 29, y + 7), (x - 24, y - 3),
         (x - 10, y - 12), (x + 12, y - 12),
         (x + 25, y - 2), (x + 31, y + 7)]
    )

    pygame.draw.polygon(
        tela, (95, 195, 230),
        [(x - 10, y - 9), (x + 10, y - 9),
         (x + 19, y - 2), (x - 18, y - 2)]
    )

    pygame.draw.circle(
        tela, (255, 220, 100), (x + 27, y + 2), 3
    )


def desenhar_jogador():
    if tema_atual() == "espaco":
        desenhar_astronauta(JOGADOR_X, int(y))
    elif tema_atual() == "ovni":
        desenhar_ovni(JOGADOR_X, int(y))
    else:
        desenhar_carro(JOGADOR_X, int(y))


# ==========================================
# DESENHO DOS OBSTACULOS
# ==========================================
def desenhar_meteoro(x, y):
    raio = RAIO_METEORO
    vertices = []

    for i in range(10):
        angulo = i * 2 * math.pi / 10
        r = raio * (0.82 if i % 2 == 0 else 1.0)
        vertices.append((
            int(x + math.cos(angulo) * r),
            int(y + math.sin(angulo) * r)
        ))

    pygame.draw.polygon(tela, (145, 55, 40), vertices)
    pygame.draw.polygon(tela, (235, 105, 48), vertices, 3)

    pygame.draw.circle(
        tela, (95, 40, 35), (int(x - 6), int(y - 4)), 5
    )
    pygame.draw.circle(
        tela, (255, 155, 70), (int(x + 7), int(y + 5)), 3
    )


def desenhar_laser(x, y):
    # Laser vertical: nao forma uma barra horizontal.
    pygame.draw.line(
        tela, (140, 20, 60),
        (int(x), int(y - 43)), (int(x), int(y + 43)), 12
    )
    pygame.draw.line(
        tela, (255, 45, 80),
        (int(x), int(y - 43)), (int(x), int(y + 43)), 6
    )
    pygame.draw.line(
        tela, (255, 220, 230),
        (int(x), int(y - 43)), (int(x), int(y + 43)), 2
    )

    pygame.draw.circle(
        tela, (180, 190, 215), (int(x), int(y - 43)), 7
    )
    pygame.draw.circle(
        tela, (180, 190, 215), (int(x), int(y + 43)), 7
    )


def desenhar_nuvem_raio(x, y):
    cor = (135, 145, 165)

    pygame.draw.circle(tela, cor, (int(x - 13), int(y)), 16)
    pygame.draw.circle(tela, cor, (int(x + 3), int(y - 9)), 20)
    pygame.draw.circle(tela, cor, (int(x + 19), int(y + 1)), 15)

    raio = [
        (x + 1, y + 10), (x - 6, y + 24),
        (x + 2, y + 23), (x - 3, y + 37),
        (x + 12, y + 19), (x + 4, y + 20)
    ]

    pygame.draw.polygon(
        tela, (255, 225, 55),
        [(int(px), int(py)) for px, py in raio]
    )


def desenhar_obstaculo(o):
    x = int(o["x"])
    yy = int(o["y"])

    if o["tipo"] == "meteoro":
        desenhar_meteoro(x, yy)
    elif o["tipo"] == "laser":
        desenhar_laser(x, yy)
    else:
        desenhar_nuvem_raio(x, yy)


# ==========================================
# COLISOES
# ==========================================
def circulos_colidem(x1, y1, r1, x2, y2, r2):
    dx = x1 - x2
    dy = y1 - y2
    return dx * dx + dy * dy < (r1 + r2) ** 2


def obstaculo_colide(o):
    x = o["x"]
    yy = o["y"]

    if modo == "classico":
        # Hitbox invisivel vertical.
        # Apenas a area ocupada pelo obstaculo causa colisao.
        if o["lado"] == "topo":
            limite = yy + RAIO_METEORO
            hitbox = pygame.Rect(
                int(x - 30), 0, 60, max(0, int(limite))
            )
        else:
            limite = yy - RAIO_METEORO
            hitbox = pygame.Rect(
                int(x - 30), int(limite),
                60, max(0, ALTURA - int(limite))
            )

        jogador = pygame.Rect(
            JOGADOR_X - 8, int(y) - 9, 16, 18
        )

        return jogador.colliderect(hitbox)

    # Chuva: objetos independentes.
    if o["tipo"] == "meteoro":
        return circulos_colidem(
            JOGADOR_X, y, 11, x, yy, 17
        )

    elif o["tipo"] == "laser":
        dentro_x = abs(JOGADOR_X - x) < 11
        dentro_y = abs(y - yy) < 53
        return dentro_x and dentro_y

    else:
        partes = [
            (x - 13, yy, 16),
            (x + 3, yy - 9, 20),
            (x + 19, yy + 1, 15)
        ]

        for nx, ny, raio in partes:
            if circulos_colidem(
                JOGADOR_X, y, 10,
                nx, ny, raio - 4
            ):
                return True

        return circulos_colidem(
            JOGADOR_X, y, 8, x + 2, yy + 25, 8
        )


# ==========================================
# TEXTOS
# ==========================================
def escrever(texto, tipo, cor, pos_y):
    imagem = tipo.render(texto, True, cor)
    tela.blit(
        imagem,
        imagem.get_rect(center=(LARGURA // 2, pos_y))
    )


# ==========================================
# LOOP PRINCIPAL
# ==========================================
executando = True

while executando:
    relogio.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                executando = False

            elif estado == "menu":
                if evento.key == pygame.K_1:
                    modo = "classico"
                    reiniciar()
                elif evento.key == pygame.K_2:
                    modo = "chuva"
                    reiniciar()

            elif evento.key == pygame.K_p:
                if estado == "jogando":
                    estado = "pausado"
                elif estado == "pausado":
                    estado = "jogando"

            elif evento.key in (pygame.K_SPACE, pygame.K_UP):
                if estado == "fim":
                    reiniciar()
                elif estado == "jogando":
                    velocidade_y = IMPULSO

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if estado == "menu":
                modo = "classico" if evento.pos[1] < ALTURA // 2 else "chuva"
                reiniciar()
            elif estado == "fim":
                estado = "menu"
            elif estado == "jogando":
                velocidade_y = IMPULSO
            elif estado == "pausado":
                estado = "jogando"

    if estado == "jogando":
        velocidade_y += GRAVIDADE
        y += velocidade_y

        for o in obstaculos:
            o["x"] -= velocidade_atual()

            if not o["marcou"] and o["x"] < JOGADOR_X:
                o["marcou"] = True
                pontos += 1

        # Geracao progressiva de obstaculos.
        if not obstaculos or max(o["x"] for o in obstaculos) < LARGURA - intervalo_atual():
            obstaculos.extend(criar_obstaculo(LARGURA + 25))

        obstaculos = [
            o for o in obstaculos if o["x"] > -70
        ]

        if y < 10 or y > ALTURA - 10:
            estado = "fim"

        for o in obstaculos:
            if obstaculo_colide(o):
                estado = "fim"
                break

    # Desenho da cena
    desenhar_fundo()

    for o in obstaculos:
        desenhar_obstaculo(o)

    if estado != "menu":
        desenhar_jogador()

    escrever(f"Pontos: {pontos}", fonte, BRANCO, 15)
    escrever(nome_tema(), fonte_pequena, CIANO, 50)

    if estado == "menu":
        escrever("ASTRO FLAPPY", titulo, CIANO, 200)
        escrever("ESCOLHA O MODO", fonte, BRANCO, 265)
        escrever("1 - CLASSICO", fonte, BRANCO, 325)
        escrever("2 - CHUVA DE OBSTACULOS", fonte, BRANCO, 370)
        escrever("REGRAS DO JOGO", fonte, VERMELHO, 420)
        escrever("No modo classico, você deve passar entre os obstaculos.\nNo modo chuva, você enfrenta uma torrente de obstaculos e deve desviar deles.", fonte_das_regras,  BRANCO, 460)
        escrever("Clique na metade superior ou inferior", fonte_pequena, CIANO, 550)
        escrever("ESPACO/clique voa | P pausa", fonte_pequena, BRANCO, 600)

    elif estado == "pausado":
        escrever("PAUSADO", titulo, CIANO, 285)
        escrever("Aperte P para continuar", fonte, BRANCO, 335)

    elif estado == "fim":
        camada = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        camada.fill((0, 0, 0, 155))
        tela.blit(camada, (0, 0))

        escrever("GAME OVER", titulo, VERMELHO, 260)
        escrever(f"Pontuacao: {pontos}", fonte, BRANCO, 315)
        escrever("ESPACO para tentar novamente", fonte, CIANO, 365)
        escrever("Clique para voltar ao menu", fonte_pequena, BRANCO, 405)

    pygame.display.flip()

pygame.quit()