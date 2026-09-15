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

    def test_potencia_ausente_ou_zero(self):
        res_none = calcular_energia(100, 80, 20, 10, None)
        self.assertIsNone(res_none["autonomia_h"])
        
        res_zero = calcular_energia(100, 80, 20, 10, 0)
        self.assertIsNone(res_zero["autonomia_h"])

    def test_carga_ou_entrada_invalida(self):
        res = calcular_energia(100, 150, 20, 10, 10) # Carga > 100%
        self.assertFalse(res["viavel"])
        self.assertIsNone(res["autonomia_h"])

if __name__ == '__main__':
    unittest.main()