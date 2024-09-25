from abc import ABC, abstractmethod

class EstrategiaAtaque(ABC):
    @abstractmethod
    def atacar(self, atacante, defensor):
        pass


class AtaqueNormal(EstrategiaAtaque):
    def atacar(self, atacante, defensor):
        return f'{atacante} realizou um ataque a {defensor} com 1 exército'


class AtaqueForte(EstrategiaAtaque):
    def atacar(self, atacante, defensor):
        return f'{atacante} realizou um ataque a {defensor} com 10 exércitos'


class Atacar:
    def __init__(self, estrategia: EstrategiaAtaque):
        self.estrategia = estrategia

    def executar_ataque(self, atacante, defensor):
        return self.estrategia.atacar(atacante, defensor)
