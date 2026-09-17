import unittest
from unittest.mock import patch
from copy import deepcopy
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
                if cenario == 'nominal':
                    self.assertEqual(resultado['decisao'], 'PRONTO PARA DECOLAR')
                else:
                    self.assertEqual(resultado['decisao'], 'DECOLAGEM ABORTADA')
                self.assertEqual(dados['geracao']['origem'], 'modelo')
    def test_seed_reproduzivel(self):
        self.assertEqual(gerar_cenario('nominal',42), gerar_cenario('nominal',42))
    def test_sem_seed_preserva_variacao_e_amostras_inseguras(self):
        base = dict(temperatura_interna_c=22, temperatura_externa_c=-50,
                    energia_pct=80, pressao_tanque_kpa=420,
                    integridade_estrutural='NOMINAL',
                    modulos={k:'OK' for k in ['suporte_vida','energia',
                              'comunicacao','propulsao','navegacao']})
        outra = deepcopy(base)
        outra['pressao_tanque_kpa'] = 430
        with patch('src.geracao.gerar_telemetria', side_effect=[base, outra]) as gerar:
            primeiro = gerar_cenario('nominal')
            segundo = gerar_cenario('nominal')
        self.assertEqual(primeiro['pressao_tanque_kpa'], 420)
        self.assertEqual(segundo['pressao_tanque_kpa'], 430)
        self.assertTrue(all(c.kwargs['seed'] is None for c in gerar.call_args_list))
        self.assertEqual(executar_cenario(primeiro, LIMITES_PADRAO)['decisao'],
                         'DECOLAGEM ABORTADA')
    def test_cenario_invalido(self):
        with self.assertRaises(ValueError):
            gerar_cenario('inexistente',42)
