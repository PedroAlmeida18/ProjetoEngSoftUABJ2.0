import unittest
from App import Subject, Jogador

class TestObserverPattern(unittest.TestCase):
    def setUp(self):
        self.subject = Subject()
        self.jogador1 = Jogador("Jogador 1")
        self.jogador2 = Jogador("Jogador 2")

        self.subject.attach(self.jogador1)
        self.subject.attach(self.jogador2)

    def test_distribuir_exercitos(self):
        mensagem = "Jogador 1 distribuiu 3 exércitos no território Brasil."
        self.subject.notify(mensagem)

        self.assertIn(mensagem, self.jogador1.notifications)
        self.assertIn(mensagem, self.jogador2.notifications)

    def test_jogador_desanexado(self):
        self.subject.detach(self.jogador2)

        mensagem = "Jogador 1 distribuiu 2 exércitos no território Alemanha."
        self.subject.notify(mensagem)

        self.assertIn(mensagem, self.jogador1.notifications)
        self.assertIsNot(mensagem, self.jogador2.notifications)
    def test_escolher_cor(self):
        mensagem = "O Jogador 1 escolheu a cor Branca"
        self.subject.notify(mensagem)

        self.assertIn(mensagem, self.jogador1.notifications)
        self.assertIn(mensagem, self.jogador2.notifications)
if __name__ == '__main__':
    unittest.main()
