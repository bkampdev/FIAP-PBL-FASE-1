import copy
import unittest
from pathlib import Path

from src.apresentacao import formatar_resultado
from src.missao import LIMITES_PADRAO, executar_cenario


RAIZ = Path(__file__).resolve().parents[1]


class FormatarResultadoTest(unittest.TestCase):
    def executar(self, nome):
        return executar_cenario(RAIZ / "dados" / nome, LIMITES_PADRAO)

    def test_nominal_apresenta_decisao_energia_e_autonomia_reais(self):
        texto = formatar_resultado(self.executar("nominal.json"))

        self.assertIn("Cenário: nominal.json", texto)
        self.assertIn("PRONTO PARA DECOLAR", texto)
        self.assertIn("Nenhuma falha operacional identificada.", texto)
        self.assertIn("Energia inicial: 80.00 kWh", texto)
        self.assertIn("Saldo após decolagem: 56.00 kWh", texto)
        self.assertIn("Autonomia estimada: 5.60 h", texto)

    def test_abortado_mostra_motivo_sem_recalcular_energia(self):
        texto = formatar_resultado(self.executar("falha_modulo.json"))

        self.assertIn("DECOLAGEM ABORTADA", texto)
        self.assertIn("- Modulo critico em falha: propulsao", texto)
        self.assertIn("Saldo após decolagem: 56.00 kWh", texto)

    def test_multiplos_motivos_sao_listados_um_por_linha(self):
        resultado = self.executar("falha_temperatura.json")
        resultado["motivos"].append("Motivo adicional para teste")

        texto = formatar_resultado(resultado)

        self.assertIn("- temperatura_interna_c 31 acima do maximo de 30", texto)
        self.assertIn("- Motivo adicional para teste", texto)

    def test_energia_indisponivel_nao_lanca_erro(self):
        resultado = {"origem": "entrada inválida", "decisao": "DECOLAGEM ABORTADA", "motivos": ["campo inválido"], "energia": None}

        texto = formatar_resultado(resultado)

        self.assertIn("- campo inválido", texto)
        self.assertIn("Energia: indisponível.", texto)

    def test_autonomia_none_nao_vira_zero_horas(self):
        texto = formatar_resultado(self.executar("falha_energia.json"))

        self.assertIn("Autonomia temporal não calculada.", texto)
        self.assertNotIn("0.00 h", texto)

    def test_decisao_ausente_sinaliza_erro_e_preserva_motivo(self):
        texto = formatar_resultado({"origem": "sem decisão", "motivos": ["campo ausente"]})

        self.assertIn("ERRO", texto)
        self.assertIn("- campo ausente", texto)
        self.assertIn("Energia: indisponível.", texto)

    def test_nao_altera_resultado_recebido(self):
        resultado = self.executar("nominal.json")
        original = copy.deepcopy(resultado)

        formatar_resultado(resultado)

        self.assertEqual(resultado, original)
