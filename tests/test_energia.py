import math
import unittest

from src.energia import calcular_energia

class TestEnergia(unittest.TestCase):

    def test_caso_nominal(self):
        res = calcular_energia(100, 80, 20, 10, 10)
        self.assertEqual(res["energia_inicial_kwh"], 80)
        self.assertEqual(res["perdas_kwh"], 8)
        self.assertEqual(res["energia_util_kwh"], 72)
        self.assertEqual(res["saldo_kwh"], 52)
        self.assertTrue(res["viavel"])
        self.assertAlmostEqual(res["autonomia_h"], 5.2)

    def test_saldo_insuficiente(self):
        res = calcular_energia(100, 80, 75, 10, 10)
        self.assertEqual(res["saldo_kwh"], -3)
        self.assertFalse(res["viavel"])
        self.assertIsNone(res["autonomia_h"])

    def test_potencia_ausente(self):
        res_none = calcular_energia(100, 80, 20, 10, None)
        self.assertTrue(res_none["viavel"])
        self.assertIsNone(res_none["autonomia_h"])

    def test_rejeita_entradas_fora_do_dominio(self):
        casos = [
            (100, 150, 20, 10, 10),
            (0, 80, 20, 10, 10),
            (100, 80, -1, 10, 10),
            (100, 80, 20, 10, 0),
            (100, 80, 20, 10, -1),
        ]
        for argumentos in casos:
            with self.subTest(argumentos=argumentos):
                with self.assertRaises(ValueError):
                    calcular_energia(*argumentos)

    def test_rejeita_numeros_nao_finitos(self):
        casos = [
            (math.nan, 80, 20, 10, 10),
            (100, 80, math.nan, 10, 10),
            (100, 80, 20, 10, math.nan),
        ]
        for argumentos in casos:
            with self.subTest(argumentos=argumentos):
                with self.assertRaises(ValueError):
                    calcular_energia(*argumentos)

if __name__ == '__main__':
    unittest.main()
