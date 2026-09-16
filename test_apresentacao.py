"""
Testes unitários para src/apresentacao.py

Autoria: Gabriel (@ItsTheContext)
Revisão: Davi

Cobertura:
- cenário nominal (sem motivos)
- cenário abortado (um motivo)
- múltiplos motivos
- energia ausente (não deve quebrar)
- autonomia None (não vira "0 h")
- dicionário original não é alterado
- decisão ausente sinaliza erro
"""

import unittest
from src.apresentacao import formatar_resultado


class TestFormatarResultado(unittest.TestCase):

    def test_nominal_sem_motivos(self):
        resultado = {
            "cenario": "nominal_01",
            "decisao": "PRONTO PARA DECOLAR",
            "motivos": [],
            "energia": {
                "autonomia_horas": 4.25,
                "capacidade_kwh": 120.0,
                "carga_percentual": 87.5,
            },
        }
        texto = formatar_resultado(resultado)
        self.assertIn("PRONTO PARA DECOLAR", texto)
        self.assertIn("Nenhuma falha operacional identificada", texto)
        self.assertIn("4.25 h", texto)

    def test_abortado_com_motivo(self):
        resultado = {
            "cenario": "falha_modulo",
            "decisao": "DECOLAGEM ABORTADA",
            "motivos": ["Pressão do tanque fora da faixa"],
            "energia": {
                "autonomia_horas": None,
                "capacidade_kwh": 100.0,
                "carga_percentual": 40.0,
            },
        }
        texto = formatar_resultado(resultado)
        self.assertIn("DECOLAGEM ABORTADA", texto)
        self.assertIn("Pressão do tanque fora da faixa", texto)

    def test_multiplos_motivos(self):
        resultado = {
            "cenario": "falha_dupla",
            "decisao": "DECOLAGEM ABORTADA",
            "motivos": ["Falha estrutural", "Energia insuficiente"],
            "energia": {},
        }
        texto = formatar_resultado(resultado)
        self.assertIn("Falha estrutural", texto)
        self.assertIn("Energia insuficiente", texto)
        # garante que os dois motivos aparecem, não só o último
        self.assertEqual(texto.count("- Motivo:"), 2)

    def test_energia_ausente_nao_causa_erro(self):
        resultado = {
            "cenario": "sem_energia",
            "decisao": "PRONTO PARA DECOLAR",
            "motivos": [],
        }
        # não deve lançar KeyError/TypeError
        texto = formatar_resultado(resultado)
        self.assertIsInstance(texto, str)
        self.assertIn("Autonomia temporal não calculada", texto)

    def test_autonomia_none_nao_vira_zero(self):
        resultado = {
            "cenario": "x",
            "decisao": "PRONTO PARA DECOLAR",
            "motivos": [],
            "energia": {"autonomia_horas": None},
        }
        texto = formatar_resultado(resultado)
        self.assertIn("Autonomia temporal não calculada", texto)
        self.assertNotIn("0.00 h", texto)
        self.assertNotIn("0 h", texto)

    def test_nao_altera_dicionario_original(self):
        resultado = {
            "cenario": "x",
            "decisao": "PRONTO PARA DECOLAR",
            "motivos": [],
            "energia": {"capacidade_kwh": 100.0},
        }
        copia = {
            "cenario": "x",
            "decisao": "PRONTO PARA DECOLAR",
            "motivos": [],
            "energia": {"capacidade_kwh": 100.0},
        }
        formatar_resultado(resultado)
        self.assertEqual(resultado, copia)

    def test_decisao_ausente_sinaliza_erro(self):
        resultado = {"motivos": []}
        texto = formatar_resultado(resultado)
        self.assertIn("ERRO", texto)


if __name__ == "__main__":
    unittest.main()
