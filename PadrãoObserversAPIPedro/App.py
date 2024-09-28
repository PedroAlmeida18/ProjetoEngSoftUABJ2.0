from fastapi import FastAPI, Query, Form
from fastapi.responses import HTMLResponse
from cor import cores, escolha_cor
from territorio import receber_carta_território
from objetivos import escolher_objetivo_aleatorio
from exercito import receber_exercito_inicial, colocar_exercito

import random

app = FastAPI()
numero_Participantes = None
territorios_recebido = []
jogadores = []
rodada_atual = 0

class Observer:
    def update(self, mensagem: str):
        raise NotImplementedError

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, mensagem: str):
        for observer in self._observers:
            observer.update(mensagem)

class Jogador(Observer):
    def __init__(self, id):
        self.notifications = [] 
        self.id = id

    def update(self, mensagem: str):
        self.notifications.append(mensagem) 
        print(f"Jogador {self.id} recebeu notificação: {mensagem}")

subject = Subject()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
        <html>
            <head></head>
            <body>
                <h1>Bem-Vindo ao jogo War</h1>
                <p>Você precisa definir o número de Participantes para iniciar o jogo, podendo jogar até 6 pessoas.</p>
                <form action="/escolhernumeroPartipantes" method="post">
                    <p>Digite abaixo o número de Participantes:</p>
                    <input type="number" id="numero_Participantes" name="numero_Participantes" min="2" max="6" required>
                    <button type="submit">Enviar</button>
                </form>
            </body>
        </html>
    """

@app.post("/escolhernumeroPartipantes", response_class=HTMLResponse)
async def escolher_numero_participantes(numero_Participantes: int = Form(...)):
    global jogadores
    for i in range(1, numero_Participantes + 1):
        jogador = Jogador(i)
        jogadores.append(jogador)
        subject.attach(jogador)  

    return f"""
        <html>
            <head></head>
            <body>
                <h1>Jogo iniciado com {numero_Participantes} participantes!</h1>
                <p>Agora os participantes irão escolher suas cores dos exércitos para continuar o jogo.</p>
                <p>1- Azul, 2 - Branco, 3- Vermelha, 4 - Preta, 5 - Amarela, 6 - Verde</p>
                <form action="/escolher-cor/" method="get">
                    <label for="numero_cor">Escolha sua cor (1-6):</label>
                    <input type="number" id="numero_cor" name="numero_cor" min="1" max="6" required>
                    <button type="submit">Confirmar cor</button>
                </form>
                <p>Para saber a ordem dos jogadores, digite novamente o número de Participantes:</p>
                <form action="/ordem-jogadores/" method="get">
                    <input type="number" id="numero_Participantes" name="numero_Participantes" min="2" max="6" required>
                    <button type="submit">Ordem das jogadas</button>
                </form>
                    <button onclick="history.back()" type="submit">Voltar página</button>
                </form>
            </body>
        </html>
    """

@app.get("/escolher-cor/", response_class=HTMLResponse)
async def escolher_cor(numero_cor: int = Query(...)):
    resultado = escolha_cor(numero_cor)
    subject.notify(f"O jogador  escolheu :{resultado['Cor']}")
    return f"""
        <html>
            <head></head>
            <body>
                <h1>{resultado['Mensagem']}</h1>
                <p>Cor escolhida: {resultado['Cor']}</p>
                <p>{resultado['Mensagem2']}</p>
                <p>Descubra 1° os seus territórios e após isso vá descobrir seus objetivos. O último a descobrir o objetivo deve preencher o campo para saber a ordem das rodadas</p>
                <form action="/meus-territorios" method="get">
                    <label for="numero_cor">Digite seu id para descobrir seus territórios:</label>
                    <input type="number" id="numero_cor" name="numero_cor" min="1" max="6" required>
                    <button type="submit">Receber Territórios</button>
                </form>
                
                <form action="/receber-objetivo/" method="get">
                    <label for="numero_cor">Digite seu id com base no número da cor (1-6):</label>
                    <input type="number" id="numero_cor" name="numero_cor" min="1" max="6" required>
                    <button type="submit">Receber objetivo</button>
                </form>
                <button onclick="history.back()">Voltar</button>     
            </body>
        </html>
    """

@app.get("/receber-objetivo/", response_class=HTMLResponse)
async def receber_objetivo(numero_cor: int = Query(...)):
     objetivo = escolher_objetivo_aleatorio()
     return f"""
         <html>
            <head></head>
            <body>
                <h1>{objetivo['Objetivo']}</h1>
                <button onclick="history.back()">Voltar</button>
            </body>
        </html>
     """

@app.get("/ordem-jogadores/", response_class=HTMLResponse)
async def definir_ordem(numero_Participantes: int = Query(...)):
    ordem_jogadores = []
    ordem2 = random.sample(range(1, numero_Participantes + 1), numero_Participantes)
    for i in range(numero_Participantes):
        ordem = ordem2[i]
        ordem_jogadores.append(f"<p>A ordem do jogador {i + 1}: {ordem}° a jogar</p>")
        jogadores[i].update(f"A sua ordem é: {ordem}° a jogar")
        subject.notify(f"A ordem do jogador {i + 1}: {ordem}° a jogar")
    return "".join(ordem_jogadores)

@app.get("/meus-territorios", response_class=HTMLResponse)
async def meus_territorios(numero_cor: int = Query(...)):
    território = receber_carta_território()
    return f"""
         <html>
            <head>Parabéns você recebeu o território:</head>
            <body>
                <h1>{território["Territorio"]}</h1>
                <form action="/recebe-exercitos" method="get">
                    <p>Digite seu id para receber seus exércitos:</p>
                    <input type="number" id="numero_cor" name="numero_cor" required>
                    <button type="submit">Receber exércitos</button>
                </form>
                <button onclick="history.back()">Voltar</button>
            </body>
        </html>
   """

@app.get("/recebe-exercitos", response_class=HTMLResponse)
async def recebe_exercitos(numero_cor: int = Query(...)):
    exercito = receber_exercito_inicial()
    return f"""
            <html>
            <head></head>
            <body>
                <h2>{exercito["mensagem"]}</h2>
                <form action="/meus-territorios1" method="get">
                    <p>Digite o nome do território que deseja colocar seu exército:</p>
                    <input type="text" id="nome_territorio" name="nome_territorio" required>
                    <p>Digite o valor do seu exército:</p>
                    <input type="number" id="valor_exercito" name="valor_exercito" min=1 required>
                    <button type="submit">Por exército</button>
                </form>
                <button onclick="history.back()">Voltar</button>
            </body>
        </html>
    """

@app.get("/meus-territorios1", response_class=HTMLResponse)
async def por_exercito(nome_territorio: str = Query(...), valor_exercito: int = Query(...)):
    resultado = colocar_exercito(nome_territorio, valor_exercito)
    return f"""
        <html>
            <head>Você colocou os exércitos no território:</head>
            <body>
                <h1>{resultado["Mensagem"]}</h1>
                <button onclick="history.back()">Voltar</button>
                <button onclick="window.location.href='/iniciar-rodada'">Iniciar Rodada</button>
            </body>
        </html>
   """

@app.get("/iniciar-rodada", response_class=HTMLResponse)
async def iniciar_rodada():
    global rodada_atual
    rodada_atual += 1  
    return f"""
        <html>
            <head></head>
            <body>
                <h1>Rodada {rodada_atual} Iniciada!</h1>
                <p>Você recebeu 3 exércitos para distribuir em seus territórios.</p>
                <form action="/distribuir-exercitos" method="get">
                    <p>Digite o nome do território:</p>
                    <input type="text" id="nome_territorio" name="nome_territorio" required>
                    <p>Digite a quantidade de exércitos:</p>
                    <input type="number" id="quantidade_exercitos" name="quantidade_exercitos" min="1" required>
                    <button type="submit">Distribuir Exércitos</button>
                </form>
            </body>
        </html>
    """

@app.get("/distribuir-exercitos", response_class=HTMLResponse)
async def distribuir_exercitos(nome_territorio: str = Query(...), quantidade_exercitos: int = Query(...)):
    resultado = colocar_exercito(nome_territorio, quantidade_exercitos)
    subject.notify(f"Jogador distribuiu {quantidade_exercitos} exércitos em {nome_territorio}.")  # Notificar todos os jogadores
    return f"""
        <html>
            <head></head>
            <body>
                <h1>{resultado["Mensagem"]}</h1>
                <p>Você distribuiu {quantidade_exercitos} exércitos em {nome_territorio}.</p>
                <button onclick="history.back()">Voltar</button>
            </body>
        </html>
    """
