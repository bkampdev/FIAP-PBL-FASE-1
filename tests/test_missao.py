import copy
import json
import tempfile
import unittest
from pathlib import Path

from src.missao import LIMITES_PADRAO, executar_cenario


RAIZ = Path(__file__).resolve().parents[1]


class ExecutarCenarioTest(unittest.TestCase):
    def carregar_cenario(self, nome):
        with open(RAIZ / "dados" / nome, encoding="utf-8") as arquivo:
            return json.load(arquivo)

    def test_cenario_nominal_carregado_do_json(self):
        resultado = executar_cenario(RAIZ / "dados" / "nominal.json", LIMITES_PADRAO)

        self.assertEqual(resultado["origem"], str(RAIZ / "dados" / "nominal.json"))
        self.assertEqual(resultado["erros_entrada"], [])
        self.assertEqual(resultado["decisao"], "PRONTO PARA DECOLAR")
        self.assertEqual(resultado["motivos"], [])
        self.assertTrue(resultado["energia"]["viavel"])
        self.assertEqual(resultado["energia"]["saldo_kwh"], 56.0)

    def test_limites_padrao_seguem_contrato_documentado(self):
        self.assertEqual(
            LIMITES_PADRAO,
            {
                "temperatura_interna_c": (15, 30),
                "temperatura_externa_c": (-150, 120),
                "energia_pct": (50, 100),
                "pressao_tanque_kpa": (90, 110),
            },
        )

    def test_entrada_estruturalmente_invalida_aborta_sem_calcular_energia(self):
        dados = self.carregar_cenario("nominal.json")
        dados["energia_pct"] = 120
        dados["carga_pct"] = 120

        resultado = executar_cenario(dados, LIMITES_PADRAO)

        self.assertEqual(resultado["decisao"], "DECOLAGEM ABORTADA")
        self.assertIsNone(resultado["energia"])
        self.assertTrue(
            any("energia_pct deve estar entre 0 e 100" in motivo for motivo in resultado["motivos"])
        )

    def test_falha_operacional_preserva_motivo_do_modulo(self):
        resultado = executar_cenario(
            self.carregar_cenario("falha_modulo.json"), LIMITES_PADRAO
        )

        self.assertEqual(resultado["decisao"], "DECOLAGEM ABORTADA")
        self.assertTrue(resultado["energia"]["viavel"])
        self.assertIn("Modulo critico em falha: propulsao", resultado["motivos"])

    def test_falha_de_energia_usa_resultado_do_modulo_energetico(self):
        resultado = executar_cenario(
            self.carregar_cenario("falha_energia.json"), LIMITES_PADRAO
        )

        self.assertEqual(resultado["decisao"], "DECOLAGEM ABORTADA")
        self.assertFalse(resultado["energia"]["viavel"])
        self.assertIn("Energia insuficiente: saldo de -4.0 kWh", resultado["motivos"])

    def test_nao_altera_dados_fornecidos_pelo_chamador(self):
        dados = self.carregar_cenario("nominal.json")
        original = copy.deepcopy(dados)

        executar_cenario(dados, LIMITES_PADRAO)

        self.assertEqual(dados, original)

    def test_limites_invalidos_abortam_antes_da_decisao(self):
        resultado = executar_cenario(
            self.carregar_cenario("nominal.json"),
            {"temperatura_interna_c": (float("nan"), 30)},
        )

        self.assertEqual(resultado["decisao"], "DECOLAGEM ABORTADA")
        self.assertIsNone(resultado["energia"])
        self.assertEqual(resultado["motivos"], ["Entrada inválida: limite inválido para temperatura_interna_c"])

    def test_cenario_sem_campos_de_energia_aborta_sem_lancar_key_error(self):
        dados = self.carregar_cenario("nominal.json")
        for campo in (
            "capacidade_kwh",
            "carga_pct",
            "consumo_decolagem_kwh",
            "perdas_pct",
        ):
            del dados[campo]

        resultado = executar_cenario(dados, LIMITES_PADRAO)

        self.assertEqual(resultado["decisao"], "DECOLAGEM ABORTADA")
        self.assertIsNone(resultado["energia"])
        self.assertIn(
            "Entrada inválida: campo energético obrigatório ausente: capacidade_kwh",
            resultado["motivos"],
        )

    def test_arquivo_malformado_aborta_com_erro_explicito(self):
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "invalido.json"
            caminho.write_text("{", encoding="utf-8")

            resultado = executar_cenario(caminho, LIMITES_PADRAO)

        self.assertEqual(resultado["decisao"], "DECOLAGEM ABORTADA")
        self.assertIsNone(resultado["energia"])
        self.assertTrue(any("JSON malformado" in motivo for motivo in resultado["motivos"]))
