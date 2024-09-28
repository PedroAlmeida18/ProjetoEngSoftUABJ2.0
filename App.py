#Objetivos  - Jogar War no navegador
#Url Base - LocalHost
#End Points - Preparação, distribuir exercitos, rodada
#localHost/preparação/cor(Get)
#localHost/preparação/objetivo(Get)
#localHost/preparação/corEnv(Post)

#localHost/Distribuir/OrdemJogadores(Get)
#localHost/Distribuir/Territórios(Get)
#localHost/Distribuir/Exercitos(Get)
#localHost/Distribuir/Exercitos/Distribuir(Post)
#Quais recursos : Jogo War

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cor import cores, escolha_cor
from objetivos import escolher_objetivo_aleatorio
from exercito import receber_exercito_inicial, colocar_exercito
from strategy_ezequiel.ataque import atacar_territorio
from singleton_matheus.receber_carta import GerenciadorCartas
from typing import List
import random

app = FastAPI()

gerenciador_cartas = GerenciadorCartas()

class TerritoriosConquistados(BaseModel):
    territorios: List[str]


@app.get("/")
async def root():
    return {"Mensagem": "Bem-vindo ao jogo war, Você precisa escolher a cor do Exercito",
            "Cor do Exército" : "1-Azul, 2-Branca, 3-Vermelha, 4-Preta, 5-Amarela, 6-Verde",
            "Mensagem ": "Para seguir o jogo altere a rota para /escolher-cor/numero da sua cor"}


@app.get("/escolher-cor/{cor}")
async def escolher_cor(cor: int):
    return escolha_cor(cor)

    
@app.get("/receber-objetivo/")
async def Receber_objetivo():
    return escolher_objetivo_aleatorio()


@app.get("/ordem-jogadores/")
async def definir_ordem():
    ordem = random.randint(1, 6)
    return {
        "Titulo": f"Você será o {ordem}° jogador a jogar",
        "Ordem": ordem,
        "Mensagem": "Para saber seu território inicial acesse a rota meus-territorios",
    }

@app.get("/receber-cartas-iniciais/{jogador_id}")
def receber_cartas_iniciais(jogador_id: str):
    cartas_iniciais = gerenciador_cartas.entregar_cartas_iniciais(jogador_id)
    return {"cartas_iniciais": [carta['Território'] for carta in cartas_iniciais]}



@app.get("/receber-cartas-fim-turno/{jogador_id}")
def receber_cartas_fim_turno(jogador_id: str, territorios_conquistados: list[str]):
    cartas_recebidas = []
    
    for _ in territorios_conquistados:
        carta = gerenciador_cartas.entregar_carta_aleatoria(jogador_id)
        if carta:
            cartas_recebidas.append(carta['Território'])
        else:
            return {"mensagem": "Não há mais cartas disponíveis."}
    
    return {"cartas_recebidas": cartas_recebidas}

@app.get("/obter-cartas/{jogador_id}")
def obter_cartas(jogador_id: str):
    cartas = gerenciador_cartas.obter_cartas_jogador(jogador_id)
    return {"cartas_do_jogador": [carta['Território'] for carta in cartas]}

@app.get("/recebe-exercitos")
async def recebe_exercitos():
    return receber_exercito_inicial()

@app.get("/meus-territorios/{território}/{valor}")
async def por_exercito(territorios: str, valor: int):
    return colocar_exercito(territorios, valor)

@app.get("/realizar-ataque/{territorio_atacante}/{territorio_defensor}/{tipo_ataque}")
async def realizar_ataque(territorio_atacante, territorio_defensor, tipo_ataque):
    return atacar_territorio(territorio_atacante, territorio_defensor, tipo_ataque)
