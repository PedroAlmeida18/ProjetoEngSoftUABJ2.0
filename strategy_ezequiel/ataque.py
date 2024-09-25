from strategy_ezequiel.ataque_strategy import Atacar, AtaqueForte, AtaqueNormal
# from ataque_strategy import Atacar, AtaqueForte, AtaqueNormal --- Use esse import para rodar o teste


def atacar_territorio(territorio_atacante, territorio_defensor, tipo_ataque):
    if str(tipo_ataque) == "normal":
        estrategia = Atacar(AtaqueNormal())
    elif str(tipo_ataque) == "forte":
        estrategia = Atacar(AtaqueForte())
    else:
        return {"Erro": "Estratégia de ataque inválida"}
    
    ataque = estrategia.executar_ataque(territorio_atacante, territorio_defensor)

    return {"Mensagem": ataque}
