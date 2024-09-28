import random

territorios = [
                {'id': 1, 'Região': 'América do Sul', 'Território': 'Brasil'},
                {'id': 2, 'Região': 'América do Sul', 'Território': 'Argentina/Uruguai'},
                {'id': 3, 'Região': 'América do Sul', 'Território': 'Colômbia/Venezuela'},
                {'id': 4, 'Região': 'América do Sul', 'Território': 'Peru/Bolívia/Chile'},
                {'id': 5, 'Região': 'América do Norte', 'Território': 'México'},
                {'id': 6, 'Região': 'América do Norte', 'Território': 'Califórnia'},
                {'id': 7, 'Região': 'América do Norte', 'Território': 'Nova Iorque'},
                {'id': 8, 'Região': 'América do Norte', 'Território': 'Labrador'},
                {'id': 9, 'Região': 'América do Norte', 'Território': 'Ottawa'},
                {'id': 10, 'Região': 'América do Norte', 'Território': 'Vancouver'},
                {'id': 11, 'Região': 'América do Norte', 'Território': 'Mackenzie'},
                {'id': 12, 'Região': 'América do Norte', 'Território': 'Alasca'},
                {'id': 13, 'Região': 'América do Norte', 'Território': 'Groenlândia'},
                {'id': 14, 'Região': 'Europa', 'Território': 'Islândia'},
                {'id': 15, 'Região': 'Europa', 'Território': 'Inglaterra'},
                {'id': 16, 'Região': 'Europa', 'Território': 'Suécia'},
                {'id': 17, 'Região': 'Europa', 'Território': 'Alemanha'},
                {'id': 18, 'Região': 'Europa', 'Território': 'Espanha/Portugal/França/Itália'},
                {'id': 19, 'Região': 'Europa', 'Território': 'Polônia/Iugoslávia'},
                {'id': 20, 'Região': 'Europa', 'Território': 'Moscou'},
                {'id': 21, 'Região': 'África', 'Território': 'Argélia/Nigéria'},
                {'id': 22, 'Região': 'África', 'Território': 'Egito'},
                {'id': 23, 'Região': 'África', 'Território': 'Congo'},
                {'id': 24, 'Região': 'África', 'Território': 'Sudão'},
                {'id': 25, 'Região': 'África', 'Território': 'Madagascar'},
                {'id': 26, 'Região': 'África', 'Território': 'África do Sul'},
                {'id': 27, 'Região': 'Ásia', 'Território': 'Oriente Médio'},
                {'id': 28, 'Região': 'Ásia', 'Território': 'Aral'},
                {'id': 29, 'Região': 'Ásia', 'Território': 'Omsk'},
                {'id': 30, 'Região': 'Ásia', 'Território': 'Dudinka'},
                {'id': 31, 'Região': 'Ásia', 'Território': 'Sibéria'},
                {'id': 32, 'Região': 'Ásia', 'Território': 'Tchita'},
                {'id': 33, 'Região': 'Ásia', 'Território': 'Bajdar'},
                {'id': 34, 'Região': 'Oceania', 'Território': 'Austrália'},
                {'id': 35, 'Região': 'Oceania', 'Território': 'Nova Zelândia'},
                {'id': 36, 'Região': 'Oceania', 'Território': 'Papua-Nova Guiné'},
            ]

class GerenciadorCartas:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(GerenciadorCartas, cls).__new__(cls)
            cls._instancia.cartas_disponiveis = territorios.copy()
            cls._instancia.jogadores_cartas = {}  
        return cls._instancia

    def entregar_cartas_iniciais(self, jogador_id):
        if jogador_id not in self.jogadores_cartas:
            self.jogadores_cartas[jogador_id] = []
        if len(self.cartas_disponiveis) >= 3:
            cartas_iniciais = random.sample(self.cartas_disponiveis, 3)
            self.jogadores_cartas[jogador_id].extend(cartas_iniciais)
            for carta in cartas_iniciais:
                self.cartas_disponiveis.remove(carta)
            return cartas_iniciais
        else:
            return self.cartas_disponiveis.copy()  

    def entregar_carta_aleatoria(self, jogador_id):
        if jogador_id not in self.jogadores_cartas:
            self.jogadores_cartas[jogador_id] = []
        if self.cartas_disponiveis:
            carta = random.choice(self.cartas_disponiveis)
            self.jogadores_cartas[jogador_id].append(carta) 
            self.cartas_disponiveis.remove(carta)
            return carta
        else:
            return None

    def obter_cartas_jogador(self, jogador_id):
        return self.jogadores_cartas.get(jogador_id, [])