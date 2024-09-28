import random

exercito = [
    {'id': 1, 'exercito': "Pequeno", 'valor': 1},
    {'id': 2, 'exercito': "Grande", 'valor': 10},
]

territorios_exercito = {}

def receber_exercito_inicial():
    exercitoInical=  random.choices(exercito, weights=[50, 50], k=1)[0]
    return {
            "mensagem": f"Parabéns você recebeu 3 exercitos " + exercitoInical['exercito'] + " no valor de : " 
            + str(exercitoInical['valor'])
    }

def colocar_exercito(territorios: str, valor: int):
    
    if territorios in territorios_exercito:
        territorios_exercito[territorios] += valor
    else:
        territorios_exercito[territorios] = valor
    return {
        "Mensagem": f"Colocados {valor} exércitos no território {territorios}.",
        "Territórios": territorios_exercito
    }    