import unittest

from src.energia import calcular_energia
from src.verificacao import verificar_pre_decolagem


LIMITES = {
    "temperatura_interna_c": (15, 30),
    "temperatura_externa_c": (-150, 120),
    "energia_pct": (50, 100),
    "pressao_tanque_kpa": (90, 110),
}

DADOS_NOMINAIS = {
    "temperatura_interna_c": 22,
    "temperatura_externa_c": -50,
    "energia_pct": 80,
    "pressao_tanque_kpa": 100,
    "integridade_estrutural": "NOMINAL",
    "modulos": {
        "suporte_vida": "OK",
        "energia": "OK",
        "comunicacao": "OK",
        "propulsao": "OK",
        "navegacao": "OK",
    },
}


class VerificarPreDecolagemTest(unittest.TestCase):
    def test_aceita_autonomia_retornada_por_calcular_energia(self):
        energia = calcular_energia(100, 80, 20, 5, 10)

        resultado = verificar_pre_decolagem(DADOS_NOMINAIS, energia, LIMITES)

        self.assertEqual("PRONTO PARA DECOLAR", resultado["decisao"])
        self.assertEqual([], resultado["motivos"])

    def test_aceita_integridade_nominal_representada_por_um(self):
        dados = dict(DADOS_NOMINAIS, integridade_estrutural=1)

        resultado = verificar_pre_decolagem(
            dados, calcular_energia(100, 80, 20, 5, 10), LIMITES
        )

        self.assertEqual("PRONTO PARA DECOLAR", resultado["decisao"])
        self.assertEqual([], resultado["motivos"])

    def test_aborta_quando_autonomia_for_zero(self):
        resultado = verificar_pre_decolagem(
            DADOS_NOMINAIS, calcular_energia(100, 80, 80, 0, 10), LIMITES
        )

        self.assertEqual("DECOLAGEM ABORTADA", resultado["decisao"])
        self.assertIn("Energia insuficiente: saldo de 0.0 kWh", resultado["motivos"])

    def test_aborta_quando_resultado_energetico_nao_tem_campos_necessarios(self):
        resultado = verificar_pre_decolagem(DADOS_NOMINAIS, {}, LIMITES)

        self.assertEqual("DECOLAGEM ABORTADA", resultado["decisao"])
        self.assertIn("Resultado energetico invalido", resultado["motivos"])

    def test_aborta_sem_erro_quando_integridade_for_zero(self):
        dados = dict(DADOS_NOMINAIS, integridade_estrutural=0)

        resultado = verificar_pre_decolagem(
            dados, calcular_energia(100, 80, 20, 5, 10), LIMITES
        )

        self.assertEqual("DECOLAGEM ABORTADA", resultado["decisao"])
        self.assertIn(
            "Integridade estrutural 0, esperado NOMINAL ou 1",
            resultado["motivos"],
        )


if __name__ == "__main__":
    unittest.main()
