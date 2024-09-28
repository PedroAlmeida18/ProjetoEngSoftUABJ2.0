from fastapi.testclient import TestClient
from App import app

client = TestClient(app)

def test_receber_cartas_iniciais():
    response = client.post("/receber-cartas-iniciais/jogador1")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["cartas_iniciais"]) == 3

def test_receber_cartas_fim_turno():
    territorios_conquistados = {"territorios": ["Brasil", "México", "Inglaterra"]}
    
    response = client.post("/receber-cartas-fim-turno/jogador1", json=territorios_conquistados)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["cartas_recebidas"]) == len(territorios_conquistados["territorios"])

def test_obter_cartas_jogador():
    response = client.get("/obter-cartas/jogador1")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["cartas_do_jogador"]) == 6  

def test_receber_cartas_fim_turno_sem_territorios():
    territorios_conquistados = {"territorios": []}
    
    response = client.post("/receber-cartas-fim-turno/jogador1", json=territorios_conquistados)
    
    assert response.status_code == 400  