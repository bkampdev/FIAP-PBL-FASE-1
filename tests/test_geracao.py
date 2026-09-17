import unittest
from src.geracao import CENARIOS, gerar_cenario
from src.validacao import validar_telemetria
from src.missao import executar_cenario, LIMITES_PADRAO

class GeracaoIntegradaTest(unittest.TestCase):
    def test_cenarios_chegam_ao_calculo_e_decisao(self):
        for cenario in CENARIOS:
            with self.subTest(cenario=cenario):
                dados = gerar_cenario(cenario, seed=42)
                self.assertEqual(validar_telemetria(dados), [])
                resultado = executar_cenario(dados, LIMITES_PADRAO)
                self.assertEqual(resultado['erros_entrada'], [])
                self.assertIsNotNone(resultado['energia'])
                esperado = 'PRONTO PARA DECOLAR' if cenario == 'nominal' else 'DECOLAGEM ABORTADA'
                self.assertEqual(resultado['decisao'], esperado)
    def test_seed_reproduzivel(self):
        self.assertEqual(gerar_cenario('nominal',42), gerar_cenario('nominal',42))
    def test_fallback_e_origem_explicitos(self):
        dados = gerar_cenario('nominal',42)
        self.assertIn(dados['geracao']['origem'], ('modelo','arquivo_fallback'))
        self.assertEqual(dados['geracao']['seed'],42)
        if dados['geracao']['origem'] == 'arquivo_fallback':
            self.assertTrue(dados['geracao']['motivos_fallback'])
    def test_cenario_invalido(self):
        with self.assertRaises(ValueError):
            gerar_cenario('inexistente',42)
