from strategy_ezequiel.ataque import atacar_territorio
#from ataque import atacar_territorio --- Use esse import para rodar o teste

def test_ataque_normal():
    assert atacar_territorio('Brasil', 'Argentina', 'normal') == {'Mensagem': 'Brasil realizou um ataque a Argentina com 1 exército'}

def test_ataque_forte():
    assert atacar_territorio('Brasil', 'Argentina', 'forte') == {'Mensagem': 'Brasil realizou um ataque a Argentina com 10 exércitos'}

def test_ataque_invalido():
    assert atacar_territorio('Brasil', 'Argentina', 'extremamente forte') == {"Erro": "Estratégia de ataque inválida"}
