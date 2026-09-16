import math
import unittest
from copy import deepcopy

from src.energia import calcular_energia
from src.validacao import validar_telemetria
from src.verificacao import verificar_pre_decolagem


LIMITES = {
    "temperatura_interna_c": (15, 30),
    "temperatura_externa_c": (-150, 120),
    "energia_pct": (50, 100),
    "pressao_tanque_kpa": (90, 110),
}

MODULOS = ["suporte_vida", "energia", "comunicacao", "propulsao", "navegacao"]


def dados_nominais():
    """Cria uma entrada nova para cada teste."""
    return {
        "temperatura_interna_c": 22,
        "temperatura_externa_c": -50,
        "integridade_estrutural": 1,
        "energia_pct": 80,
        "pressao_tanque_kpa": 100,
        "modulos": {
            "suporte_vida": "OK",
            "energia": "OK",
            "comunicacao": "OK",
            "propulsao": "OK",
            "navegacao": "OK",
        },
    }


class TestPreDecolagem(unittest.TestCase):
    def verificar(self, dados=None, energia=5.6):
        if dados is None:
            dados = dados_nominais()
        return verificar_pre_decolagem(dados, energia, LIMITES)

    def test_nominal_pronto_e_sem_motivos(self):
        resultado = self.verificar()
        self.assertEqual("PRONTO PARA DECOLAR", resultado["decisao"])
        self.assertEqual([], resultado["motivos"])

    def test_fronteiras_numericas(self):
        casos = {
            "temperatura_interna_c": (14.9, 15, 30, 30.1),
            "temperatura_externa_c": (-150.1, -150, 120, 120.1),
            "energia_pct": (49.9, 50, 100, 100.1),
            "pressao_tanque_kpa": (89.9, 90, 110, 110.1),
        }

        for campo, (abaixo, minimo, maximo, acima) in casos.items():
            with self.subTest(campo=campo, posicao="abaixo"):
                dados = dados_nominais()
                dados[campo] = abaixo
                resultado = self.verificar(dados)
                self.assertEqual("DECOLAGEM ABORTADA", resultado["decisao"])
                self.assertTrue(any(campo in motivo and "abaixo do minimo" in motivo
                                    for motivo in resultado["motivos"]))

            with self.subTest(campo=campo, posicao="minimo"):
                dados = dados_nominais()
                dados[campo] = minimo
                resultado = self.verificar(dados)
                self.assertEqual("PRONTO PARA DECOLAR", resultado["decisao"])
                self.assertEqual([], resultado["motivos"])

            with self.subTest(campo=campo, posicao="maximo"):
                dados = dados_nominais()
                dados[campo] = maximo
                resultado = self.verificar(dados)
                self.assertEqual("PRONTO PARA DECOLAR", resultado["decisao"])
                self.assertEqual([], resultado["motivos"])

            with self.subTest(campo=campo, posicao="acima"):
                dados = dados_nominais()
                dados[campo] = acima
                resultado = self.verificar(dados)
                self.assertEqual("DECOLAGEM ABORTADA", resultado["decisao"])
                self.assertTrue(any(campo in motivo and "acima do maximo" in motivo
                                    for motivo in resultado["motivos"]))

    def test_integridade_um_aprova(self):
        dados = dados_nominais()
        dados["integridade_estrutural"] = 1
        resultado = self.verificar(dados)
        self.assertEqual("PRONTO PARA DECOLAR", resultado["decisao"])

    def test_integridade_zero_aborta_com_motivo(self):
        dados = dados_nominais()
        dados["integridade_estrutural"] = 0
        resultado = self.verificar(dados)
        self.assertEqual("DECOLAGEM ABORTADA", resultado["decisao"])
        self.assertTrue(any("Integridade estrutural 0" in m for m in resultado["motivos"]))

    def test_cada_modulo_critico_em_falha(self):
        for modulo in MODULOS:
            with self.subTest(modulo=modulo):
                dados = dados_nominais()
                dados["modulos"][modulo] = "FALHA"
                resultado = self.verificar(dados)
                self.assertEqual("DECOLAGEM ABORTADA", resultado["decisao"])
                self.assertIn("Modulo critico em falha: " + modulo, resultado["motivos"])

    def test_multiplas_falhas_acumulam_motivos(self):
        dados = dados_nominais()
        dados["temperatura_interna_c"] = 31
        dados["modulos"]["propulsao"] = "FALHA"
        resultado = self.verificar(dados, energia=0)

        self.assertEqual("DECOLAGEM ABORTADA", resultado["decisao"])
        self.assertTrue(any("temperatura_interna_c 31 acima do maximo de 30" in m
                            for m in resultado["motivos"]))
        self.assertIn("Modulo critico em falha: propulsao", resultado["motivos"])
        self.assertTrue(any("Energia insuficiente: autonomia de 0" in m for m in resultado["motivos"]))

    def test_validador_rejeita_campo_ausente(self):
        dados = dados_nominais()
        del dados["energia_pct"]
        erros = validar_telemetria(dados)
        self.assertTrue(any("energia_pct" in erro and "ausente" in erro for erro in erros))

    def test_validador_rejeita_null_em_numero(self):
        dados = dados_nominais()
        dados["energia_pct"] = None
        erros = validar_telemetria(dados)
        self.assertTrue(any("energia_pct" in erro and "número finito" in erro for erro in erros))

    def test_validador_rejeita_texto_no_lugar_de_numero(self):
        dados = dados_nominais()
        dados["temperatura_interna_c"] = "22"
        erros = validar_telemetria(dados)
        self.assertTrue(any("temperatura_interna_c" in erro and "número finito" in erro
                            for erro in erros))

    def test_validador_rejeita_energia_fora_do_dominio(self):
        for valor in (-1, 101):
            with self.subTest(valor=valor):
                dados = dados_nominais()
                dados["energia_pct"] = valor
                erros = validar_telemetria(dados)
                self.assertTrue(any("energia_pct" in erro for erro in erros))

    def test_validador_rejeita_estado_desconhecido_de_modulo(self):
        dados = dados_nominais()
        dados["modulos"]["propulsao"] = "DESCONHECIDO"
        erros = validar_telemetria(dados)
        self.assertTrue(any("propulsao" in erro for erro in erros))

    def test_validador_rejeita_modulos_incompletos(self):
        dados = dados_nominais()
        del dados["modulos"]["navegacao"]
        erros = validar_telemetria(dados)
        self.assertTrue(any("navegacao" in erro and "ausente" in erro for erro in erros))

    def test_validador_rejeita_numeros_nao_finitos(self):
        for valor in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(valor=valor):
                dados = dados_nominais()
                dados["temperatura_interna_c"] = valor
                erros = validar_telemetria(dados)
                self.assertTrue(any("temperatura_interna_c" in erro and "finito" in erro
                                    for erro in erros))

    def test_falha_operacional_continua_sendo_dado_valido(self):
        dados = dados_nominais()
        dados["integridade_estrutural"] = 0
        dados["modulos"]["propulsao"] = "FALHA"
        self.assertEqual([], validar_telemetria(dados))

    def test_energia_exemplo_manual_100_kwh(self):
        # 100 * 0,80 = 80; perdas = 5% de 80 = 4;
        # energia útil = 76; saldo = 76 - 20 = 56; 56 / 10 = 5,6 h.
        autonomia = calcular_energia(100, 80, 20, 5, 10)
        self.assertAlmostEqual(5.6, autonomia, places=7)

    def test_energia_saldo_positivo(self):
        autonomia = calcular_energia(100, 100, 20, 0, 10)
        self.assertAlmostEqual(8.0, autonomia, places=7)

    def test_energia_saldo_zero(self):
        autonomia = calcular_energia(100, 100, 100, 0, 10)
        self.assertEqual(0, autonomia)
        resultado = self.verificar(energia=autonomia)
        self.assertEqual("DECOLAGEM ABORTADA", resultado["decisao"])
        self.assertTrue(any("Energia insuficiente: autonomia de 0" in m for m in resultado["motivos"]))

    def test_energia_saldo_negativo(self):
        autonomia = calcular_energia(100, 100, 101, 0, 10)
        self.assertEqual(0, autonomia)
        resultado = self.verificar(energia=autonomia)
        self.assertEqual("DECOLAGEM ABORTADA", resultado["decisao"])

    def test_potencia_zero_nao_divide_por_zero(self):
        autonomia = calcular_energia(100, 80, 20, 5, 0)
        self.assertEqual(0, autonomia)

    def test_potencia_negativa_nao_libera_missao(self):
        autonomia = calcular_energia(100, 80, 20, 5, -10)
        self.assertLessEqual(autonomia, 0)
        resultado = self.verificar(energia=autonomia)
        self.assertEqual("DECOLAGEM ABORTADA", resultado["decisao"])


if __name__ == "__main__":
    unittest.main()
