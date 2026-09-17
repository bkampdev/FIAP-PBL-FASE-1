"""Fonte executável do relatório PDF final da atividade integradora.

O Markdown em ``relatorio/relatorio-pre-decolagem.md`` mantém uma versão
textual editável para revisão humana. Alterações de conteúdo devem ser
refletidas neste gerador, que controla a diagramação, tabelas e evidências.
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)


RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "relatorio" / "relatorio-pre-decolagem.pdf"
EVIDENCIAS = RAIZ / "evidencias"

AZUL = colors.HexColor("#10172A")
ROXO = colors.HexColor("#6D5CE7")
CIANO = colors.HexColor("#18B7A0")
TEXTO = colors.HexColor("#20283A")
SUAVE = colors.HexColor("#62708B")
LINHA = colors.HexColor("#D9E0EE")
FUNDO = colors.HexColor("#F4F7FC")
BRANCO = colors.white

PAGINA_L, PAGINA_A = A4
MARGEM_X = 18 * mm
MARGEM_TOPO = 20 * mm
MARGEM_BASE = 18 * mm


def registrar_fontes():
    regulares = [
        ("RelatorioSans", "/System/Library/Fonts/Supplemental/Arial.ttf"),
        ("RelatorioSansBold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    ]
    for nome, caminho in regulares:
        if Path(caminho).exists():
            pdfmetrics.registerFont(TTFont(nome, caminho))
    return (
        "RelatorioSans" if "RelatorioSans" in pdfmetrics.getRegisteredFontNames() else "Helvetica",
        "RelatorioSansBold" if "RelatorioSansBold" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold",
    )


FONTE, FONTE_BOLD = registrar_fontes()
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    "TituloCapa", fontName=FONTE_BOLD, fontSize=29, leading=34,
    textColor=BRANCO, alignment=TA_LEFT, spaceAfter=10,
))
styles.add(ParagraphStyle(
    "SubCapa", fontName=FONTE, fontSize=13, leading=18,
    textColor=colors.HexColor("#C8D4F1"), alignment=TA_LEFT,
))
styles.add(ParagraphStyle(
    "LinkCapa", fontName=FONTE_BOLD, fontSize=10.5, leading=14,
    textColor=colors.HexColor("#67E8D0"), alignment=TA_LEFT,
))
styles.add(ParagraphStyle(
    "Secao", fontName=FONTE_BOLD, fontSize=20, leading=24,
    textColor=AZUL, spaceBefore=5, spaceAfter=10,
))
styles.add(ParagraphStyle(
    "Subsecao", fontName=FONTE_BOLD, fontSize=12.5, leading=16,
    textColor=ROXO, spaceBefore=8, spaceAfter=5,
))
styles.add(ParagraphStyle(
    "Corpo", fontName=FONTE, fontSize=9.4, leading=13.4,
    textColor=TEXTO, spaceAfter=6,
))
styles.add(ParagraphStyle(
    "CorpoPequeno", fontName=FONTE, fontSize=8.2, leading=11.4,
    textColor=TEXTO, spaceAfter=4,
))
styles.add(ParagraphStyle(
    "Destaque", fontName=FONTE_BOLD, fontSize=11.2, leading=15,
    textColor=AZUL, backColor=colors.HexColor("#EAEFFD"),
    borderColor=colors.HexColor("#C8D2F2"), borderWidth=0.7,
    borderPadding=8, spaceBefore=4, spaceAfter=10,
))
styles.add(ParagraphStyle(
    "Legenda", fontName=FONTE, fontSize=8, leading=11,
    textColor=SUAVE, alignment=TA_CENTER, spaceBefore=4,
))
styles.add(ParagraphStyle(
    "Codigo", fontName="Courier", fontSize=7.4, leading=10,
    textColor=AZUL, backColor=colors.HexColor("#EEF2FA"),
    borderPadding=9, borderColor=LINHA, borderWidth=1,
    spaceBefore=4, spaceAfter=8,
))


def p(texto, estilo="Corpo"):
    return Paragraph(texto, styles[estilo])


def h1(texto):
    return Paragraph(texto, styles["Secao"])


def h2(texto):
    return Paragraph(texto, styles["Subsecao"])


def tabela(dados, larguras, cabecalho=True):
    convertidos = []
    for indice_linha, linha in enumerate(dados):
        linha_convertida = []
        for indice_coluna, celula in enumerate(linha):
            if hasattr(celula, "wrap"):
                linha_convertida.append(celula)
            elif cabecalho and indice_linha == 0:
                linha_convertida.append(Paragraph(
                    str(celula), ParagraphStyle(
                        f"Cabecalho{indice_linha}-{indice_coluna}",
                        parent=styles["CorpoPequeno"],
                        fontName=FONTE_BOLD,
                        textColor=BRANCO,
                    )
                ))
            else:
                linha_convertida.append(p(str(celula), "CorpoPequeno"))
        convertidos.append(linha_convertida)
    tabela_obj = Table(convertidos, colWidths=larguras, repeatRows=1 if cabecalho else 0, hAlign="LEFT")
    estilo = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, LINHA),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1 if cabecalho else 0), (-1, -1), [BRANCO, FUNDO]),
    ]
    if cabecalho:
        estilo += [
            ("BACKGROUND", (0, 0), (-1, 0), AZUL),
            ("TEXTCOLOR", (0, 0), (-1, 0), BRANCO),
            ("FONTNAME", (0, 0), (-1, 0), FONTE_BOLD),
        ]
    tabela_obj.setStyle(TableStyle(estilo))
    return tabela_obj


def rodape(canvas, doc):
    if doc.page == 1:
        return
    canvas.saveState()
    canvas.setStrokeColor(LINHA)
    canvas.line(MARGEM_X, 14 * mm, PAGINA_L - MARGEM_X, 14 * mm)
    canvas.setFont(FONTE, 7.5)
    canvas.setFillColor(SUAVE)
    canvas.drawString(MARGEM_X, 9.5 * mm, "FIAP · Relatório operacional de pré-decolagem · Grupo 16")
    canvas.drawRightString(PAGINA_L - MARGEM_X, 9.5 * mm, f"{doc.page}")
    canvas.restoreState()


def fundo_capa(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(AZUL)
    canvas.rect(0, 0, PAGINA_L, PAGINA_A, stroke=0, fill=1)
    canvas.setFillColor(ROXO)
    canvas.circle(PAGINA_L - 24 * mm, PAGINA_A - 32 * mm, 46 * mm, stroke=0, fill=1)
    canvas.setFillColor(CIANO)
    canvas.circle(PAGINA_L - 5 * mm, PAGINA_A - 4 * mm, 18 * mm, stroke=0, fill=1)
    canvas.setStrokeColor(colors.HexColor("#4C5A82"))
    canvas.setLineWidth(0.8)
    for deslocamento in range(0, 8):
        y = 20 * mm + deslocamento * 5 * mm
        canvas.line(18 * mm, y, PAGINA_L - 18 * mm, y + 25 * mm)
    canvas.restoreState()


def imagem_evidencia(nome, legenda):
    caminho = EVIDENCIAS / nome
    img = Image(str(caminho), width=174 * mm, height=97.875 * mm)
    return [img, p(legenda, "Legenda")]


def construir():
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(SAIDA), pagesize=A4,
        leftMargin=MARGEM_X, rightMargin=MARGEM_X,
        topMargin=MARGEM_TOPO, bottomMargin=MARGEM_BASE,
        title="Relatório Operacional de Pré-Decolagem",
        author="Grupo 16 — FIAP",
        subject="Atividade Integradora — Fase 1",
    )
    frame_capa = Frame(MARGEM_X, 22 * mm, PAGINA_L - 2 * MARGEM_X, PAGINA_A - 44 * mm, id="capa")
    frame_corpo = Frame(
        MARGEM_X, MARGEM_BASE,
        PAGINA_L - 2 * MARGEM_X,
        PAGINA_A - MARGEM_TOPO - MARGEM_BASE,
        id="corpo",
    )
    doc.addPageTemplates([
        PageTemplate(id="Capa", frames=[frame_capa], onPage=fundo_capa),
        PageTemplate(id="Corpo", frames=[frame_corpo], onPage=rodape),
    ])

    story = []
    story += [
        Spacer(1, 54 * mm),
        p("FIAP · FASE 1 · GRUPO 16", "SubCapa"),
        Spacer(1, 5 * mm),
        Paragraph("RELATÓRIO OPERACIONAL<br/>DE PRÉ-DECOLAGEM", styles["TituloCapa"]),
        Spacer(1, 6 * mm),
        p("Atividade Integradora · Decolagem da Missão", "SubCapa"),
        Spacer(1, 6 * mm),
        p(
            '<link href="https://github.com/bkampdev/FIAP-PBL-FASE-1" '
            'color="#67E8D0">github.com/bkampdev/FIAP-PBL-FASE-1</link>',
            "LinkCapa",
        ),
        Spacer(1, 31 * mm),
        p("Davi Coninck Cassaro · RM572772", "SubCapa"),
        p("Guilherme Cardoso Bremenkamp · RM574229", "SubCapa"),
        p("Lorenzo Mendes Rocha · RM575361", "SubCapa"),
        p("Gabriel Gonzales · RM574746", "SubCapa"),
        p("Eduardo Backes Klauck · RM575889", "SubCapa"),
        Spacer(1, 8 * mm),
        p("São Paulo · 16 de setembro de 2026", "SubCapa"),
        NextPageTemplate("Corpo"),
        PageBreak(),
    ]

    story += [
        h1("Resumo executivo"),
        p("Este trabalho implementa uma simulação educacional de pré-decolagem. O sistema lê dados sintéticos, valida o contrato de entrada, calcula o balanço energético, verifica faixas seguras e apresenta uma decisão explicável. A missão só é liberada quando todos os critérios são satisfeitos e o saldo energético é positivo."),
        p("A análise por IA apoia a interpretação, mas não substitui as regras determinísticas nem a revisão humana. Os limites são hipóteses didáticas do grupo e não parâmetros certificados de uma nave real.", "Destaque"),
        h2("Entregáveis consolidados"),
        tabela([
            ["Item do FIAP ON", "Artefato neste repositório"],
            ["1.1 Telemetria", "docs/telemetria.md, dados/*.json e notebook"],
            ["1.2 Algoritmo", "docs/algoritmo.md e pseudocódigo"],
            ["1.3 Script Python", "src/, notebook e testes"],
            ["1.4 Energia", "src/energia.py e docs/energia.md"],
            ["1.5 Análise por IA", "docs/analise-ia.md"],
            ["1.6 Reflexão crítica", "docs/reflexao_critica.md"],
            ["PDF + fonte", "relatorio/relatorio-pre-decolagem.pdf e .md"],
            ["README + prints", "README.md e evidencias/"],
        ], [53 * mm, 121 * mm]),
        Spacer(1, 7 * mm),
        h2("Links públicos"),
        p('<link href="https://github.com/bkampdev/FIAP-PBL-FASE-1" color="#6D5CE7">Repositório público no GitHub</link>'),
        p('<link href="https://github.com/bkampdev/FIAP-PBL-FASE-1/blob/main/notebooks/pre_decolagem.ipynb" color="#6D5CE7">Notebook pre_decolagem.ipynb</link>'),
        PageBreak(),
    ]

    story += [
        h1("1. Objetivo e arquitetura"),
        p("O objetivo é responder <b>PRONTO PARA DECOLAR</b> ou <b>DECOLAGEM ABORTADA</b> com base em telemetria e energia, acumulando os motivos encontrados."),
        tabela([
            ["Etapa", "Responsabilidade", "Módulo"],
            ["1", "Ler JSON e tratar arquivo ausente/malformado", "src/validacao.py"],
            ["2", "Validar presença, tipos e domínios", "src/validacao.py"],
            ["3", "Calcular energia inicial, perdas, saldo e autonomia", "src/energia.py"],
            ["4", "Avaliar limites, integridade, módulos e viabilidade", "src/verificacao.py"],
            ["5", "Integrar o fluxo e padronizar o resultado", "src/missao.py"],
            ["6", "Apresentar texto sem recalcular valores", "src/apresentacao.py"],
        ], [15 * mm, 101 * mm, 58 * mm]),
        Spacer(1, 7 * mm),
        h2("Princípios de projeto"),
        p("<b>Separação de responsabilidades.</b> Validação de formato, cálculo energético, decisão e apresentação ficam em módulos diferentes."),
        p("<b>Falha segura.</b> Dado ausente, inválido ou resultado energético incompleto nunca libera a missão."),
        p("<b>Explicabilidade.</b> O verificador percorre todas as regras aplicáveis e acumula os motivos, em vez de ocultar problemas após a primeira falha."),
        p("<b>Reprodutibilidade.</b> Os cenários são JSONs versionados e o núcleo não exige API key ou acesso à internet."),
        PageBreak(),
    ]

    story += [
        h1("2. Telemetria — requisito 1.1"),
        p("O contrato distingue domínio válido de faixa operacional segura. Uma falha operacional válida deve chegar ao verificador; um valor impossível é rejeitado antes da decisão."),
        tabela([
            ["Campo", "Unidade / tipo", "Domínio válido", "Faixa segura"],
            ["temperatura_interna_c", "°C · número", "-100 a 150", "15 a 30"],
            ["temperatura_externa_c", "°C · número", "-200 a 150", "-150 a 120"],
            ["integridade_estrutural", "inteiro 0/1", "0 ou 1", "1"],
            ["energia_pct", "% · número", "0 a 100", "50 a 100"],
            ["pressao_tanque_kpa", "kPa · número", "> 0 e ≤ 1000", "90 a 110"],
            ["modulos", "objeto", "cinco módulos", "todos em OK"],
        ], [47 * mm, 37 * mm, 43 * mm, 47 * mm]),
        Spacer(1, 6 * mm),
        h2("Módulos críticos"),
        p("Suporte de vida, energia, comunicação, propulsão e navegação. Os estados aceitos são <b>OK</b> e <b>FALHA</b>."),
        h2("Cenários versionados"),
        tabela([
            ["Arquivo", "Alteração principal", "Resultado esperado"],
            ["nominal.json", "nenhuma", "PRONTO PARA DECOLAR"],
            ["falha_temperatura.json", "temperatura interna = 31 °C", "aborto por temperatura"],
            ["falha_modulo.json", "propulsão = FALHA", "aborto por módulo"],
            ["falha_energia.json", "consumo = 80 kWh", "aborto por energia"],
            ["entrada_invalida.json", "pressão ausente", "aborto por entrada inválida"],
        ], [55 * mm, 67 * mm, 52 * mm]),
        PageBreak(),
    ]

    pseudocodigo = """INÍCIO
  carregar cenário
  validar estrutura, tipos e domínios
  SE houver erros:
      retornar DECOLAGEM ABORTADA e todos os erros
  calcular energia inicial, perdas, energia útil, saldo e autonomia
  motivos <- lista vazia
  PARA cada faixa segura:
      registrar valores abaixo ou acima dos limites
  verificar integridade estrutural
  PARA cada módulo crítico:
      registrar módulo em falha
  SE saldo energético <= 0:
      registrar energia insuficiente
  SE motivos estiver vazia:
      retornar PRONTO PARA DECOLAR
  SENÃO:
      retornar DECOLAGEM ABORTADA e todos os motivos
FIM"""
    story += [
        h1("3. Algoritmo — requisito 1.2"),
        p("As fronteiras das faixas são inclusivas. A energia só é viável com saldo estritamente positivo. Todas as falhas aplicáveis são reunidas antes da decisão."),
        Preformatted(pseudocodigo, styles["Codigo"]),
        h2("Percurso nominal"),
        p("Temperaturas, energia e pressão estão dentro das faixas; a integridade é 1; todos os módulos estão em OK; o saldo energético é 56 kWh. Como a lista de motivos permanece vazia, o resultado é <b>PRONTO PARA DECOLAR</b>."),
        h2("Percurso com falha"),
        p("Com temperatura interna de 31 °C, o verificador registra que o valor excede o máximo de 30 °C. O saldo energético positivo não elimina a falha térmica. A decisão é <b>DECOLAGEM ABORTADA</b> e o motivo permanece visível."),
        h2("Contrato de saída"),
        Preformatted(
            '{"decisao": "PRONTO PARA DECOLAR", "motivos": []}\n'
            '{"decisao": "DECOLAGEM ABORTADA", "motivos": ["..."]}',
            styles["Codigo"],
        ),
        PageBreak(),
    ]

    codigo = """from src.missao import executar_cenario, LIMITES_PADRAO
from src.apresentacao import formatar_resultado

# Executar a partir da raiz do repositório.
resultado = executar_cenario("dados/nominal.json", LIMITES_PADRAO)
print(formatar_resultado(resultado))"""
    story += [
        h1("4. Script Python — requisito 1.3"),
        p("O notebook importa os módulos do repositório e executa cenários reais. O trecho abaixo resume a integração; cada função mantém uma responsabilidade única."),
        Preformatted(codigo, styles["Codigo"]),
        h2("Tratamento de erros"),
        p("Arquivo ausente, JSON malformado, campo obrigatório ausente, tipo incorreto, número não finito ou percentuais fora de domínio geram aborto explicado. Nenhum dado crítico é preenchido silenciosamente com um valor seguro."),
        h2("Apresentação"),
        p("A função <b>formatar_resultado</b> recebe o dicionário final e retorna uma string. Ela mostra cenário, decisão, motivos e energia, lida com valores indisponíveis e não altera o objeto recebido."),
        h2("Testes automatizados"),
        p("A suíte cobre nominal, limites, cada módulo crítico, integridade, energia positiva/nula/negativa, entradas inválidas, integração e apresentação. Na versão final, 52 testes foram aprovados.", "Destaque"),
        PageBreak(),
    ]

    story += [
        h1("5. Análise energética — requisito 1.4"),
        p("A capacidade total, a carga, as perdas e o consumo são expressos em kWh/%; a potência média é usada somente para estimar a autonomia após a decolagem."),
        tabela([
            ["Etapa", "Fórmula", "Exemplo nominal"],
            ["Energia inicial", "capacidade × carga / 100", "100 × 80% = 80 kWh"],
            ["Perdas", "energia inicial × perdas / 100", "80 × 5% = 4 kWh"],
            ["Energia útil", "energia inicial − perdas", "80 − 4 = 76 kWh"],
            ["Saldo", "energia útil − consumo", "76 − 20 = 56 kWh"],
            ["Autonomia", "saldo / potência, se saldo > 0", "56 / 10 = 5,6 h"],
        ], [40 * mm, 76 * mm, 58 * mm]),
        Spacer(1, 7 * mm),
        p("<b>Regra de viabilidade:</b> saldo maior que zero. Com saldo zero ou negativo, <i>viavel</i> é falso e a autonomia é <i>None</i>.", "Destaque"),
        h2("Cenário de falha energética"),
        p("Com a mesma energia inicial e perdas, mas consumo de decolagem de 80 kWh, o saldo é 76 − 80 = <b>-4 kWh</b>. A decisão é DECOLAGEM ABORTADA e a autonomia temporal não é calculada."),
        h2("Validações numéricas"),
        p("Capacidade precisa ser positiva; carga e perdas devem estar entre 0% e 100%; consumo não pode ser negativo; potência, quando informada, precisa ser positiva. NaN e infinito são rejeitados."),
        PageBreak(),
    ]

    story += [
        h1("6. Análise assistida por IA — requisito 1.5"),
        p("A consulta ao Codex/GPT-5 pediu classificação dos dados, anomalias e sugestões de risco para os cenários nominal, temperatura e propulsão. O prompt forneceu as faixas e fórmulas e proibiu autorização operacional real."),
        tabela([
            ["Cenário", "Classificação da IA", "Revisão humana"],
            ["Nominal", "sem anomalias; saldo 56 kWh; autonomia 5,6 h", "confere com JSON e código"],
            ["Temperatura", "31 °C excede o máximo de 30 °C", "confere; energia não elimina a falha"],
            ["Propulsão", "módulo crítico em FALHA", "confere; exige aborto"],
            ["Limitação", "não há dados para causa interna da falha", "correto; não inventar diagnóstico"],
        ], [38 * mm, 72 * mm, 64 * mm]),
        Spacer(1, 7 * mm),
        p("Em caso de divergência, prevalecem os dados versionados e os módulos determinísticos de validação, energia e verificação.", "Destaque"),
        h2("Geração sintética opcional"),
        p("O módulo src/geracao.py usa GaussianMixture como extensão para produzir dados sintéticos. Ele não participa da decisão autoritativa e não é necessário para a execução do notebook principal."),
        PageBreak(),
    ]

    story += [
        h1("7. Reflexão crítica — requisito 1.6"),
        h2("Ética e responsabilidade"),
        p("Uma decisão de segurança precisa ser explicável. O sistema acumula motivos, informa valores e limites, e aborta quando faltam dados indispensáveis. A IA serve como apoio interpretativo; não recebe autoridade para aprovar a missão."),
        h2("Impacto social"),
        p("Tecnologias espaciais podem gerar aplicações em medicina, agricultura, manufatura e observação terrestre. Ao mesmo tempo, o investimento espacial disputa recursos com outras prioridades sociais. O simulador não resolve essa decisão política, mas evita apresentar dados sintéticos como segurança real."),
        h2("Sustentabilidade tecnológica"),
        p("O balanço energético torna perdas e consumo explícitos e evita declarar autonomia quando o saldo é nulo ou negativo. O projeto não mediu emissões ou consumo computacional; portanto, não faz alegações ambientais sem dados."),
        h2("Síntese"),
        p("O principal aprendizado é que uma verificação segura não se limita a responder “sim” ou “não”: ela deve explicar, registrar incertezas e permitir auditoria.", "Destaque"),
        PageBreak(),
    ]

    story += [h1("8. Evidências — cenário nominal")]
    story += imagem_evidencia(
        "01-nominal.png",
        "Figura 1 — Telemetria nominal, saldo de 56 kWh, autonomia de 5,6 h e decisão PRONTO PARA DECOLAR.",
    )
    story += [
        Spacer(1, 5 * mm),
        p("A imagem foi diagramada a partir do output persistido na célula correspondente do notebook executado. O JSON de origem é dados/nominal.json."),
        PageBreak(),
        h1("9. Evidências — aborto por temperatura"),
    ]
    story += imagem_evidencia(
        "02-aborto.png",
        "Figura 2 — Temperatura interna de 31 °C, acima do limite de 30 °C, e decisão DECOLAGEM ABORTADA.",
    )
    story += [
        Spacer(1, 5 * mm),
        p("Os demais dados permanecem nominais, o que isola a causa do aborto. O JSON de origem é dados/falha_temperatura.json."),
        PageBreak(),
        h1("10. Evidências — aborto por energia"),
    ]
    story += imagem_evidencia(
        "03-energia.png",
        "Figura 3 — Saldo de -4 kWh, autonomia não calculada e decisão DECOLAGEM ABORTADA.",
    )
    story += [
        Spacer(1, 5 * mm),
        p("O consumo de decolagem de 80 kWh supera a energia útil de 76 kWh. O JSON de origem é dados/falha_energia.json."),
        PageBreak(),
    ]

    story += [
        h1("11. Validação, conclusão e referências"),
        h2("Verificação executada em 16/09/2026"),
        Preformatted(
            "python -m unittest discover -s tests -v\n"
            "python -m jupyter nbconvert --to notebook --execute --inplace "
            "notebooks/pre_decolagem.ipynb",
            styles["Codigo"],
        ),
        p("Resultado: <b>52 testes aprovados, 0 falhas</b>, e notebook executado integralmente.", "Destaque"),
        tabela([
            ["Cenário", "Decisão", "Saldo", "Autonomia"],
            ["nominal", "PRONTO PARA DECOLAR", "56 kWh", "5,6 h"],
            ["falha de temperatura", "DECOLAGEM ABORTADA", "56 kWh", "5,6 h"],
            ["falha de energia", "DECOLAGEM ABORTADA", "-4 kWh", "não calculada"],
            ["entrada inválida", "DECOLAGEM ABORTADA", "indisponível", "indisponível"],
        ], [47 * mm, 64 * mm, 27 * mm, 36 * mm]),
        h2("Conclusão"),
        p("O projeto atende aos seis itens técnicos solicitados e inclui notebook executável, README com instruções e prints, fonte editável e PDF. A separação entre validação, energia, decisão e apresentação permite rastrear cada resultado e mantém explícito o caráter didático dos dados."),
        h2("Referências"),
        p("FIAP ON. <i>Atividade Integradora — Relatório Operacional de Pré-Decolagem</i>. Consulta em 16 set. 2026."),
        p('NASA. <i>Technology Transfer and Spinoffs</i>. <link href="https://www.nasa.gov/space-technology-mission-directorate/technology-transfer-spinoffs/" color="#6D5CE7">nasa.gov</link>.'),
        p('Projeto público: <link href="https://github.com/bkampdev/FIAP-PBL-FASE-1" color="#6D5CE7">github.com/bkampdev/FIAP-PBL-FASE-1</link>.'),
        Spacer(1, 5 * mm),
        p("Base integrada: a487de4. O notebook e os artefatos foram consolidados em 16/09/2026. A presença do PDF no GitHub não equivale à submissão no FIAP ON.", "CorpoPequeno"),
    ]

    doc.build(story)
    print(f"Relatório gerado: {SAIDA}")


if __name__ == "__main__":
    construir()
