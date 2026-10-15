"""Gera BOM/BOM.xlsx do projeto PIBIT com design estético, profissional e executivo.

Cenários:
  U1 = Placa universal, 1 dedo (início / bancada de testes)
  U3 = Placa universal, 3 dedos (objetivo final montagem manual)
  P1 = PCB customizada, 1 dedo (bancada com placa SMD KiCad)
  P3 = PCB customizada, 3 dedos (objetivo final integrado)
"""
import math
import sys
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = sys.argv[1] if len(sys.argv) > 1 else "BOM.xlsx"
TAXA_USD = 5.60

# Constantes de Estado
COMPRAR = "Comprar"
LVIS = "L-VIS (grátis)"
LVIS_CONF = "L-VIS (confirmar)"
ALT = "Alternativa (fora do total)"
COTADO = "Cotado"
ESTIMADO = "Estimado"

# Tipografia e Paleta de Cores Executiva (Slate / Navy / Emerald)
FONT_FAMILY = "Segoe UI"

# Fills
FILL_NAVY_DARK = PatternFill("solid", fgColor="0F172A")    # Slate 900
FILL_HEADER_PRI = PatternFill("solid", fgColor="1E3A5F")   # Deep Corporate Navy
FILL_HEADER_SEC = PatternFill("solid", fgColor="2B4C7E")   # Medium Navy
FILL_CAT_BANNER = PatternFill("solid", fgColor="E2E8F0")   # Slate 200
FILL_ZEBRA = PatternFill("solid", fgColor="F8FAFC")        # Slate 50
FILL_CARD_BG = PatternFill("solid", fgColor="F1F5F9")      # Slate 100
FILL_TOTAL_ROW = PatternFill("solid", fgColor="E0E7FF")    # Indigo 100
FILL_INPUT_BOX = PatternFill("solid", fgColor="FEF3C7")    # Amber 100 (editável)

# Status Badge Fills
FILL_BADGE_COMPRAR = PatternFill("solid", fgColor="DCFCE7")  # Emerald 100
FILL_BADGE_LVIS = PatternFill("solid", fgColor="DBEAFE")     # Blue 100
FILL_BADGE_CONFIRMAR = PatternFill("solid", fgColor="FEF3C7")# Amber 100
FILL_BADGE_ALT = PatternFill("solid", fgColor="F1F5F9")      # Slate 100
FILL_BADGE_ESTIMADO = PatternFill("solid", fgColor="FEF9C3") # Yellow 100

# KPI Cards Fills
FILL_KPI_U1 = PatternFill("solid", fgColor="EFF6FF")  # Blue 50
FILL_KPI_U3 = PatternFill("solid", fgColor="ECFDF5")  # Emerald 50
FILL_KPI_P1 = PatternFill("solid", fgColor="FAF5FF")  # Purple 50
FILL_KPI_P3 = PatternFill("solid", fgColor="FFFBEB")  # Amber 50

# Fontes
F_TITLE = Font(name=FONT_FAMILY, size=16, bold=True, color="0F172A")
F_SUBTITLE = Font(name=FONT_FAMILY, size=10, italic=True, color="475569")
F_SECTION = Font(name=FONT_FAMILY, size=12, bold=True, color="0F172A")
F_HEADER = Font(name=FONT_FAMILY, size=9, bold=True, color="FFFFFF")
F_CAT = Font(name=FONT_FAMILY, size=10, bold=True, color="1E293B")
F_REGULAR = Font(name=FONT_FAMILY, size=9, color="1E293B")
F_BOLD = Font(name=FONT_FAMILY, size=9, bold=True, color="1E293B")
F_LINK = Font(name=FONT_FAMILY, size=9, color="2563EB", underline="single")
F_TOTAL = Font(name=FONT_FAMILY, size=10, bold=True, color="0F172A")

# Fontes KPI
F_KPI_LABEL = Font(name=FONT_FAMILY, size=8, bold=True, color="475569")
F_KPI_CODE = Font(name=FONT_FAMILY, size=10, bold=True, color="0F172A")
F_KPI_VAL = Font(name=FONT_FAMILY, size=15, bold=True, color="0F172A")
F_KPI_DESC = Font(name=FONT_FAMILY, size=8, italic=True, color="64748B")

# Bordas
THIN_GRAY = Side(style="thin", color="CBD5E1")
THICK_NAVY = Side(style="medium", color="1E3A5F")
DOUBLE_BOTTOM = Side(style="double", color="1E3A5F")
DOTTED_GRAY = Side(style="dotted", color="CBD5E1")

BORDER_CELL = Border(left=THIN_GRAY, right=THIN_GRAY, top=THIN_GRAY, bottom=THIN_GRAY)
BORDER_HEADER = Border(left=THIN_GRAY, right=THIN_GRAY, top=THIN_GRAY, bottom=THIN_GRAY)
BORDER_TOTAL = Border(top=THIN_GRAY, bottom=DOUBLE_BOTTOM, left=THIN_GRAY, right=THIN_GRAY)
BORDER_CARD = Border(left=THIN_GRAY, right=THIN_GRAY, top=THIN_GRAY, bottom=THIN_GRAY)

# Formatos Numéricos
FMT_CURRENCY = '"R$" #,##0.00'
FMT_USD = '"US$" #,##0.00'
FMT_DECIMAL = '#,##0.00'
FMT_INT = '#,##0'

# Alinhamentos
ALIGN_LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_RIGHT = Alignment(horizontal="right", vertical="center")
ALIGN_HEADER = Alignment(horizontal="center", vertical="center", wrap_text=True)

# Itens da BOM
ITENS = [
    # 1. Sensoriamento
    ("1. Sensoriamento eFlesh", "Módulo breakout magnetômetro 3D TLV493D (Qwiic/STEMMA QT)",
     "TLV493D breakout", "AliExpress", 36.99, "BRL", 1, COMPRAR, 1, 3, 0, 0, COTADO,
     "Versão manual. Comprar as 3 unidades de uma vez dilui o frete.",
     "https://pt.aliexpress.com/item/1005008497289675.html"),
    ("1. Sensoriamento eFlesh", "CI magnetômetro 3D TLV493D-A1B6 (TSOP-6, SMD)",
     "TLV493DA1B6HTSA1", "DigiKey / Mouser", 1.80, "USD", 1, COMPRAR, 0, 0, 2, 4, COTADO,
     "Versão PCB. Inclui 1 unidade de reserva para retrabalho de solda.",
     "https://www.digikey.com.br/pt/products/detail/infineon-technologies/TLV493DA1B6HTSA1/5802095"),
    ("1. Sensoriamento eFlesh", "Ímã de neodímio N52, disco 5×3 mm (kit 20 un.)",
     "N52 5×3 mm", "Mercado Livre", 19.80, "BRL", 20, COMPRAR, 4, 12, 4, 12, COTADO,
     "Qtd. estimada em 4 ímãs por dedo; ajustar após o CAD da cut-cell. Um kit atende todos os cenários.",
     "https://www.mercadolivre.com.br/ima-de-neodimio-disco-5mm-x-3mm-20-pecas-5x3-mm-5-x-3-mm/p/MLB2080152340"),
    ("1. Sensoriamento eFlesh", "Ímã de neodímio N52, disco 4,76×1,58 mm (3/16\"×1/16\")",
     "K&J D31-N52", "K&J Magnetics (EUA)", 0.24, "USD", 1, ALT, 4, 12, 4, 12, COTADO,
     "Modelo do artigo original. Fora do total: importação dos EUA encarece muito o frete.",
     "https://www.kjmagnetics.com/d31-n52-neodymium-disc-magnet"),
    ("1. Sensoriamento eFlesh", "Módulo multiplexador I2C TCA9548A (8 canais)",
     "TCA9548A", "Mercado Livre / AliExpress", 20.00, "BRL", 1, COMPRAR, 0, 1, 0, 1, ESTIMADO,
     "Obrigatório só com 3 sensores: o TLV493D tem apenas 2 endereços I2C.",
     ""),

    # 2. Atuação háptica
    ("2. Atuação háptica", "Motor de vibração ERM tipo moeda 8×4 mm, 3 V, com fio",
     "ERM 8×4 mm", "HU Infinito", 4.90, "BRL", 1, COMPRAR, 2, 4, 2, 4, COTADO,
     "1 por dedo + 1 de reserva. Montar no dorso do dedo ou palma (15–30 mm do sensor).",
     "https://www.huinfinito.com.br/motores/1391-motor-de-vibracao-chato-com-fio-8x4mm.html"),
    ("2. Atuação háptica", "MOSFET canal N 2N7000 (TO-92, kit 50 un.)",
     "2N7000", "Mercado Livre", 35.00, "BRL", 50, COMPRAR, 1, 3, 0, 0, COTADO,
     "Versão manual. Vgs(th) pode chegar a 3 V: validar com gate em 3,3 V. Comprar avulso em loja local sai mais barato.",
     "https://www.mercadolivre.com.br/50x-transistor-2n7000-to92-kit-com-50-pecas/up/MLBU2257180645"),
    ("2. Atuação háptica", "MOSFET canal N AO3400A (SOT-23, nível lógico)",
     "AO3400A", "Mercado Livre / AliExpress", 19.00, "BRL", 50, COMPRAR, 0, 0, 1, 3, ESTIMADO,
     "Versão PCB. Transistor SMD com acionamento pleno em 2,5V/3,3V.",
     "https://lista.mercadolivre.com.br/ao3400a-sot-23"),
    ("2. Atuação háptica", "Diodo de sinal 1N4148 (THT, kit 200 un.) — flyback",
     "1N4148", "Mercado Livre", 22.00, "BRL", 200, COMPRAR, 1, 3, 0, 0, COTADO,
     "Versão manual. Proteção indutiva em antiparalelo com cada motor.",
     "https://www.mercadolivre.com.br/diodo-de-sinal-1n4148-kit-200-pecas/p/MLB2072206267"),
    ("2. Atuação háptica", "Diodo de sinal 1N4148W (SOD-123, SMD) — flyback",
     "1N4148W", "Mercado Livre / AliExpress", 15.00, "BRL", 100, COMPRAR, 0, 0, 1, 3, ESTIMADO,
     "Versão PCB. Diodo ultra-rápido SMD.",
     ""),
    ("2. Atuação háptica", "Resistores THT 100 Ω (gate) e 10 kΩ (pull-down)",
     "Resistor 1/4 W", "L-VIS", 0.00, "BRL", 1, LVIS, 2, 6, 0, 0, COTADO,
     "Versão manual. 2 por dedo.",
     ""),
    ("2. Atuação háptica", "Kit resistores SMD 0805 (100 Ω, 10 kΩ, 4,7 kΩ)",
     "Kit 0805", "Mercado Livre / AliExpress", 25.00, "BRL", 1, COMPRAR, 0, 0, 1, 1, ESTIMADO,
     "Versão PCB. Gate, pull-down e pull-up I2C.",
     ""),

    # 3. Processamento e alimentação
    ("3. Processamento e alimentação", "Placa ESP32 DevKit V1 (Wi-Fi + Bluetooth)",
     "ESP32 DevKit V1", "RoboCore", 42.90, "BRL", 1, COMPRAR, 1, 0, 1, 0, COTADO,
     "Fase 1 (bancada, 1 dedo). Alimentada pelo cabo micro-USB.",
     "https://www.robocore.net/wifi/esp32-wifi-bluetooth"),
    ("3. Processamento e alimentação", "Placa ESP32-S3 Nano (compacta, dual-core LX7)",
     "ESP32-S3 Nano", "A definir", 90.00, "BRL", 1, COMPRAR, 0, 1, 0, 1, ESTIMADO,
     "Fase 2 (luva vestível, 3 dedos). Formato miniatura, leveza e alto poder de processamento.",
     ""),
    ("3. Processamento e alimentação", "Bateria Li-Ion 18650, 3,7 V, recarregável",
     "BATVTRLIPO3V7", "HU Infinito", 13.40, "BRL", 1, COMPRAR, 0, 1, 0, 1, COTADO,
     "Só na luva (3 dedos); a bancada usa alimentação USB.",
     "https://www.huinfinito.com.br/module/iqitsearch/searchiqit?s=BATERIA+L%C3%8DTIO+3%2C7V+%2818650+-+RECARREG%C3%81VEL%29"),
    ("3. Processamento e alimentação", "Suporte para 1 bateria 18650 (canoa)",
     "BATPLIPO3V701", "HU Infinito", 3.90, "BRL", 1, COMPRAR, 0, 1, 0, 1, COTADO,
     "Suporte mecânico para fixação segura no dorso/pulso.",
     "https://www.huinfinito.com.br/baterias-acessorios/1356-suporte-01-bateria-litio-37v-18650-canoa-preto.html"),
    ("3. Processamento e alimentação", "Módulo carregador TP4056 com proteção (USB-C)",
     "TP4056", "Mercado Livre / AliExpress", 8.00, "BRL", 1, COMPRAR, 0, 1, 0, 1, ESTIMADO,
     "Gerenciamento de carga Li-Ion e proteção contra subtensão/sobrecorrente.",
     ""),
    ("3. Processamento e alimentação", "Módulo regulador de tensão boost 5 V (MT3608)",
     "MT3608", "Mercado Livre / AliExpress", 8.00, "BRL", 1, COMPRAR, 0, 1, 0, 1, ESTIMADO,
     "Eleva e estabiliza a tensão da bateria (3,0–4,2 V) em 5,0 V para o ESP32.",
     ""),

    # 4. Montagem e interconexão
    ("4. Montagem e interconexão", "Placa de circuito universal perfurada (Ilhada, ~5×7 cm)",
     "Perfboard 5x7", "Mercado Livre / loja local", 10.00, "BRL", 1, COMPRAR, 1, 2, 0, 0, ESTIMADO,
     "Versão manual. Montagem central do circuito do pulso.",
     ""),
    ("4. Montagem e interconexão", "Fabricação de PCB (lote 5 un., 2 camadas c/ frete e taxas)",
     "PCB 2 camadas", "JLCPCB / PCBWay", 120.00, "BRL", 1, COMPRAR, 0, 0, 1, 1, ESTIMADO,
     "Versão PCB. 1 lote atende todos os dedos. Projeto customizado no KiCad.",
     ""),
    ("4. Montagem e interconexão", "Capacitor cerâmico SMD 0805 100 nF (kit 100 un.)",
     "0805 100 nF", "Mercado Livre", 19.00, "BRL", 100, COMPRAR, 0, 0, 1, 1, COTADO,
     "Versão PCB. Filtros de desacoplamento em cada magnetômetro.",
     "https://www.mercadolivre.com.br/100x-capacitor-multicamada-smd-100nf-50v-10-x7r-0805/p/MLB47645304"),
    ("4. Montagem e interconexão", "Capacitor cerâmico THT 100 nF",
     "100 nF THT", "L-VIS", 0.00, "BRL", 1, LVIS_CONF, 2, 4, 0, 0, ESTIMADO,
     "Versão manual. Desacoplamento local dos módulos.",
     ""),
    ("4. Montagem e interconexão", "Barra de pinos macho 1×40 vias, 2,54 mm",
     "Barra 1×40", "HU Infinito", 3.58, "BRL", 1, COMPRAR, 1, 2, 1, 2, COTADO,
     "Interconexões modulares de bancada.",
     "https://www.huinfinito.com.br/conectores/734-conector-barra-de-pinos-macho-1x40x20-180-graus.html"),
    ("4. Montagem e interconexão", "Conector JST macho/fêmea 2.0mm (kit 10 pares)",
     "JST PH 2.0", "Mercado Livre", 28.90, "BRL", 10, COMPRAR, 0, 4, 2, 4, COTADO,
     "Chicote destacável entre o circuito do pulso e cada dedo.",
     "https://www.mercadolivre.com.br/plug-conector-jst-da-bateria-lipo-10-pares-macho-e-femea/p/MLB2081705943"),
    ("4. Montagem e interconexão", "Fio flexível extrafino (cabinho siliconado 28–30 AWG)",
     "Cabinho 28 AWG", "Mercado Livre / loja local", 15.00, "BRL", 1, COMPRAR, 1, 1, 1, 1, ESTIMADO,
     "Fiação de articulação; essencial ser maleável para não fadigar com flexão dos dedos.",
     ""),
    ("4. Montagem e interconexão", "Protoboard, jumpers flexíveis e cabo USB de testes",
     "—", "L-VIS", 0.00, "BRL", 1, LVIS, 1, 1, 1, 1, COTADO,
     "Disponíveis para uso irrestrito no laboratório.",
     ""),

    # 5. Fabricação mecânica
    ("5. Fabricação mecânica", "Filamento TPU 95A flexível 1,75 mm, carretel 1 kg",
     "TPU 95A", "L-VIS", 149.00, "BRL", 1, LVIS, 1, 1, 1, 1, COTADO,
     "Disponível no L-VIS (valor meramente referencial). Impressão 3D das polpas eFlesh.",
     "https://www.mercadolivre.com.br/filamento-tpu-flexivel-175mm-1kg-para-impressora-3d-cor-natural-transparente/p/MLB64157424"),
    ("5. Fabricação mecânica", "Luva têxtil base e case rígido em PLA para o pulso",
     "—", "L-VIS", 0.00, "BRL", 1, LVIS_CONF, 1, 1, 1, 1, ESTIMADO,
     "Reaproveita luva do projeto anterior do L-VIS; case impresso no laboratório.",
     ""),
]

CENARIOS = [
    ("U1", "Placa Universal • 1 Dedo", "Bancada Inicial (ESP32 DevKit, USB, Breakout Qwiic)", FILL_KPI_U1),
    ("U3", "Placa Universal • 3 Dedos", "Objetivo Final Manual (ESP32-S3 Nano, Bateria, TCA9548A)", FILL_KPI_U3),
    ("P1", "PCB Customizada • 1 Dedo", "Bancada com Placa Própria (TLV493D SMD TSOP-6)", FILL_KPI_P1),
    ("P3", "PCB Customizada • 3 Dedos", "Objetivo Final Integrado (3 Dedos SMD + Luva Vestível)", FILL_KPI_P3),
]

wb = Workbook()

# ==============================================================================
# ABA 1: RESUMO (DASHBOARD EXECUTIVO)
# ==============================================================================
rs = wb.active
rs.title = "Resumo"
rs.views.sheetView[0].showGridLines = True

# Banner de Título
rs.row_dimensions[1].height = 10
rs.row_dimensions[2].height = 24
rs.row_dimensions[3].height = 18
rs.row_dimensions[4].height = 14

rs["A2"] = "PIBIT / L-VIS (UnB)  •  LUVA TÁTIL eFLESH"
rs["A2"].font = Font(name=FONT_FAMILY, size=15, bold=True, color="0F172A")

rs["A3"] = "Painel Executivo de Custos, Comparativo de Cenários e Engenharia de Materiais"
rs["A3"].font = Font(name=FONT_FAMILY, size=9.5, italic=True, color="475569")

rs["A4"] = "Autor: Artur Ferreira Gonçalves | Laboratório: L-VIS (UnB) | Data: Outubro/2026 | Versão: 2.2 Final"
rs["A4"].font = Font(name=FONT_FAMILY, size=8.5, color="64748B")

# Caixa de Parâmetros Globais (Linha 6)
rs.row_dimensions[6].height = 24
rs["A6"] = "PARÂMETRO GLOBAL:"
rs["A6"].font = Font(name=FONT_FAMILY, size=8.5, bold=True, color="1E3A5F")
rs["A6"].alignment = Alignment(horizontal="right", vertical="center")

rs["B6"] = "Câmbio USD / BRL (R$)"
rs["B6"].font = Font(name=FONT_FAMILY, size=9, bold=True, color="1E293B")
rs["B6"].alignment = Alignment(horizontal="center", vertical="center")
rs["B6"].fill = FILL_CARD_BG
rs["B6"].border = BORDER_CARD

rs["C6"] = TAXA_USD
rs["C6"].font = Font(name=FONT_FAMILY, size=10, bold=True, color="0F172A")
rs["C6"].alignment = Alignment(horizontal="center", vertical="center")
rs["C6"].fill = FILL_INPUT_BOX
rs["C6"].border = Border(top=THICK_NAVY, bottom=THICK_NAVY, left=THIN_GRAY, right=THIN_GRAY)
rs["C6"].number_format = FMT_DECIMAL

rs["D6"] = "(Célula editável — atualiza custos em US$ automaticamente)"
rs["D6"].font = Font(name=FONT_FAMILY, size=8, italic=True, color="64748B")
rs["D6"].alignment = Alignment(horizontal="left", vertical="center")

# KPI Cards (Linhas 8 a 12)
rs.row_dimensions[8].height = 16
rs.row_dimensions[9].height = 20
rs.row_dimensions[10].height = 28
rs.row_dimensions[11].height = 16
rs.row_dimensions[12].height = 10

kpi_cols = [("A", "B"), ("C", "D"), ("E", "F"), ("G", "H")]
primeira_row_comp = 6
ultima_row_comp = primeira_row_comp + len(ITENS) - 1

for idx, (cod, nome_card, desc_card, fill_kpi) in enumerate(CENARIOS):
    c1, c2 = kpi_cols[idx]
    col_letra_custo = get_column_letter(15 + idx)
    
    # Linha 8: Rótulo Cenário
    cell_top = rs[f"{c1}8"]
    rs.merge_cells(f"{c1}8:{c2}8")
    cell_top.value = f"CENÁRIO {cod}"
    cell_top.font = F_KPI_LABEL
    cell_top.alignment = Alignment(horizontal="center", vertical="center")
    
    # Linha 9: Nome Curto
    cell_nome = rs[f"{c1}9"]
    rs.merge_cells(f"{c1}9:{c2}9")
    cell_nome.value = nome_card
    cell_nome.font = F_KPI_CODE
    cell_nome.alignment = Alignment(horizontal="center", vertical="center")
    
    # Linha 10: Valor Total Grande
    cell_val = rs[f"{c1}10"]
    rs.merge_cells(f"{c1}10:{c2}10")
    cell_val.value = f"=SUM(Componentes!${col_letra_custo}${primeira_row_comp}:${col_letra_custo}${ultima_row_comp})"
    cell_val.font = F_KPI_VAL
    cell_val.alignment = Alignment(horizontal="center", vertical="center")
    cell_val.number_format = FMT_CURRENCY
    
    # Linha 11: Descrição
    cell_desc = rs[f"{c1}11"]
    rs.merge_cells(f"{c1}11:{c2}11")
    cell_desc.value = desc_card.split("(")[0].strip()
    cell_desc.font = F_KPI_DESC
    cell_desc.alignment = Alignment(horizontal="center", vertical="center")
    
    # Aplicar cores e bordas ao redor do card
    for row in range(8, 12):
        for col_name in (c1, c2):
            cell = rs[f"{col_name}{row}"]
            cell.fill = fill_kpi
            top_b = THICK_NAVY if row == 8 else THIN_GRAY
            bot_b = THICK_NAVY if row == 11 else THIN_GRAY
            left_b = THICK_NAVY if col_name == c1 else Side(style=None)
            right_b = THICK_NAVY if col_name == c2 else Side(style=None)
            cell.border = Border(top=top_b, bottom=bot_b, left=left_b, right=right_b)

# Tabela 1: Resumo Comparativo Executivo
rs.row_dimensions[14].height = 22
rs["A14"] = "1. COMPARATIVO DETALHADO DOS CENÁRIOS"
rs["A14"].font = F_SECTION

cab_resumo = ["Código", "Cenário de Prototipagem", "Objetivo / Hardware Principal", "Total Estimado", "Itens Cotados", "Itens a Cotar", "Grau de Complexidade"]
rs.row_dimensions[15].height = 22
for col_idx, text in enumerate(cab_resumo, start=1):
    cell = rs.cell(15, col_idx, text)
    cell.fill = FILL_HEADER_PRI
    cell.font = F_HEADER
    cell.alignment = ALIGN_HEADER
    cell.border = BORDER_HEADER

rng = lambda col: f"Componentes!${col}${primeira_row_comp}:${col}${ultima_row_comp}"

complexidades = [
    "Baixa (Foco em Validação Rápida)",
    "Média (Integração com 3 Dedos)",
    "Média-Alta (Soldagem SMD Inicial)",
    "Alta (Integração Total na Luva)"
]

for idx, (cod, nome_card, desc_card, fill_kpi) in enumerate(CENARIOS):
    r = 16 + idx
    rs.row_dimensions[r].height = 20
    col_letra_custo = get_column_letter(15 + idx)
    
    c_cod = rs.cell(r, 1, cod)
    c_cod.alignment = ALIGN_CENTER
    c_cod.font = F_BOLD
    c_cod.fill = fill_kpi
    
    c_nome = rs.cell(r, 2, nome_card)
    c_nome.alignment = ALIGN_LEFT
    c_nome.font = F_REGULAR
    
    c_desc = rs.cell(r, 3, desc_card)
    c_desc.alignment = ALIGN_LEFT
    c_desc.font = F_REGULAR
    
    c_tot = rs.cell(r, 4, f"=SUM({rng(col_letra_custo)})")
    c_tot.alignment = ALIGN_RIGHT
    c_tot.font = F_BOLD
    c_tot.number_format = FMT_CURRENCY
    c_tot.fill = FILL_CARD_BG
    
    c_cot = rs.cell(r, 5, f"=D{r}-F{r}")
    c_cot.alignment = ALIGN_RIGHT
    c_cot.font = F_REGULAR
    c_cot.number_format = FMT_CURRENCY
    
    c_est = rs.cell(r, 6, f'=SUMIF({rng("S")},"{ESTIMADO}",{rng(col_letra_custo)})')
    c_est.alignment = ALIGN_RIGHT
    c_est.font = F_REGULAR
    c_est.number_format = FMT_CURRENCY
    
    c_cpx = rs.cell(r, 7, complexidades[idx])
    c_cpx.alignment = ALIGN_CENTER
    c_cpx.font = F_REGULAR
    
    for c in range(1, 8):
        rs.cell(r, c).border = BORDER_CELL

# Tabela 2: Custos por Categoria de Engenharia
r_cat_title = 22
rs.row_dimensions[r_cat_title].height = 22
rs[f"A{r_cat_title}"] = "2. DISTRIBUIÇÃO DE CUSTOS POR SUBSISTEMA"
rs[f"A{r_cat_title}"].font = F_SECTION

cab_cats = ["Subsistema de Engenharia", "U1: Univ. 1 Dedo", "U3: Univ. 3 Dedos", "P1: PCB 1 Dedo", "P3: PCB 3 Dedos"]
rs.row_dimensions[r_cat_title + 1].height = 20
for c_idx, t in enumerate(cab_cats, start=1):
    cell = rs.cell(r_cat_title + 1, c_idx, t)
    cell.fill = FILL_HEADER_SEC
    cell.font = F_HEADER
    cell.alignment = ALIGN_HEADER
    cell.border = BORDER_HEADER

categorias_unicas = []
for it in ITENS:
    if it[0] not in categorias_unicas:
        categorias_unicas.append(it[0])

for c_idx, cat in enumerate(categorias_unicas):
    r = r_cat_title + 2 + c_idx
    rs.row_dimensions[r].height = 19
    c_nome = rs.cell(r, 1, cat)
    c_nome.font = F_REGULAR
    c_nome.alignment = ALIGN_LEFT
    c_nome.border = BORDER_CELL
    
    for j in range(4):
        col_letra = get_column_letter(15 + j)
        c_val = rs.cell(r, 2 + j, f'=SUMIF({rng("B")},$A{r},{rng(col_letra)})')
        c_val.font = F_REGULAR
        c_val.alignment = ALIGN_RIGHT
        c_val.number_format = FMT_CURRENCY
        c_val.border = BORDER_CELL
        if c_idx % 2 == 1:
            c_val.fill = FILL_ZEBRA

# Linha Total Categorias
r_tot_cat = r_cat_title + 2 + len(categorias_unicas)
rs.row_dimensions[r_tot_cat].height = 22
c_t_label = rs.cell(r_tot_cat, 1, "TOTAL GERAL ACUMULADO (R$)")
c_t_label.font = F_TOTAL
c_t_label.alignment = ALIGN_LEFT
c_t_label.fill = FILL_TOTAL_ROW
c_t_label.border = BORDER_TOTAL

for j in range(4):
    c_l = get_column_letter(2 + j)
    c_t_val = rs.cell(r_tot_cat, 2 + j, f"=SUM({c_l}{r_cat_title+2}:{c_l}{r_tot_cat-1})")
    c_t_val.font = F_TOTAL
    c_t_val.alignment = ALIGN_RIGHT
    c_t_val.number_format = FMT_CURRENCY
    c_t_val.fill = FILL_TOTAL_ROW
    c_t_val.border = BORDER_TOTAL

# Seção 3: Guia de Tomada de Decisão
r_guia = r_tot_cat + 2
rs.row_dimensions[r_guia].height = 20
rs[f"A{r_guia}"] = "3. DIRETRIZES DE AQUISIÇÃO E RECOMENDAÇÃO TÉCNICA"
rs[f"A{r_guia}"].font = F_SECTION

diretrizes = [
    ("Fase 1 (Validação Rápida - Início)", "Recomenda-se executar o Cenário U1 (R$ 195,07). Utiliza breakouts prontos e montagem em protoboard/placa universal, permitindo testar a aquisição I2C, compensação de ruído e resposta mecânica do TPU sem atrasos de fabricação de PCB."),
    ("Fase 2 (Escalonamento para 3 Dedos)", "A transição de U1 para U3 (R$ 421,73) não duplica os custos: os pacotes de ímãs N52, resistores e transistores já comprados são totalmente reaproveitados. O custo incremental real é de apenas ~R$ 170."),
    ("Migração para PCB Customizada (KiCad)", "Os Cenários P1 e P3 são a versão refinada de engenharia. O custo de fabricação do lote na JLCPCB (~R$ 120) é rateado entre as placas dos 3 dedos, tornando a placa final muito leve e compacta na ponta dos dedos.")
]

for idx, (titulo_d, desc_d) in enumerate(diretrizes):
    r_d = r_guia + 1 + idx
    rs.row_dimensions[r_d].height = 24
    c_t = rs.cell(r_d, 1, f"• {titulo_d}:")
    c_t.font = F_BOLD
    c_t.alignment = Alignment(horizontal="left", vertical="center")
    
    rs.merge_cells(start_row=r_d, start_column=2, end_row=r_d, end_column=7)
    c_d = rs.cell(r_d, 2, desc_d)
    c_d.font = F_REGULAR
    c_d.alignment = ALIGN_LEFT

larguras_resumo = [24, 28, 48, 16, 16, 16, 30]
for idx, w in enumerate(larguras_resumo, start=1):
    rs.column_dimensions[get_column_letter(idx)].width = w


# ==============================================================================
# ABA 2: COMPONENTES (BOM DETALHADA E MULTI-CENÁRIOS)
# ==============================================================================
ws = wb.create_sheet("Componentes")
ws.views.sheetView[0].showGridLines = True

# Título da Aba
ws.row_dimensions[1].height = 20
ws["A1"] = "BOM — ESPECIFICAÇÃO COMPLETA DE MATERIAIS E COMPONENTES"
ws["A1"].font = F_TITLE

ws.row_dimensions[2].height = 16
ws["A2"] = "Projeto PIBIT / L-VIS (UnB) | Detalhamento técnico por subsistema, precificação e regras de cálculo por lote"
ws["A2"].font = F_SUBTITLE

# Linha 4: Super-Cabeçalho (Agrupador Visual)
ws.row_dimensions[4].height = 18

super_headers = [
    ("A4:E4", "ESPECIFICAÇÃO DO COMPONENTE", FILL_HEADER_PRI),
    ("F4:I4", "PREÇO DO LOTE / PACOTE", FILL_HEADER_SEC),
    ("J4:J4", "ORIGEM", FILL_HEADER_PRI),
    ("K4:N4", "QUANTIDADES DEMANDADAS", FILL_HEADER_SEC),
    ("O4:R4", "CUSTOS POR CENÁRIO (R$)", FILL_HEADER_PRI),
    ("S4:U4", "STATUS, NOTAS & LINKS", FILL_HEADER_SEC),
]

for range_str, text, fill_sh in super_headers:
    ws.merge_cells(range_str)
    start_cell = ws[range_str.split(":")[0]]
    start_cell.value = text
    start_cell.font = Font(name=FONT_FAMILY, size=8.5, bold=True, color="FFFFFF")
    start_cell.alignment = ALIGN_CENTER
    start_cell.fill = fill_sh

# Linha 5: Cabeçalho Principal das Colunas
cab = [
    "ID", "Subsistema", "Componente / Descrição Técnica", "Modelo / Part Number", "Fornecedor",
    "Preço Orig.", "Moeda", "Qtd/Pct", "Preço Pct (R$)",
    "Origem", "U1", "U3", "P1", "P3",
    "Custo U1 (R$)", "Custo U3 (R$)", "Custo P1 (R$)", "Custo P3 (R$)",
    "Status Preço", "Notas de Engenharia", "Link do Produto"
]

ws.row_dimensions[5].height = 24
HDR = 5
for col_idx, col_name in enumerate(cab, start=1):
    cell = ws.cell(HDR, col_idx, col_name)
    cell.fill = FILL_HEADER_PRI
    cell.font = F_HEADER
    cell.alignment = ALIGN_HEADER
    cell.border = BORDER_HEADER

# Preenchimento dos Itens de Dados
primeira = HDR + 1
row_atual = primeira
ultima_cat = None

for i, it in enumerate(ITENS):
    (cat, comp, mod, forn, preco, moeda, unid, origem, u1, u3, p1, p3, conf, notas, link) = it
    r = row_atual
    ws.row_dimensions[r].height = 20
    
    ws.cell(r, 1, i + 1)
    ws.cell(r, 2, cat)
    ws.cell(r, 3, comp)
    ws.cell(r, 4, mod)
    ws.cell(r, 5, forn)
    ws.cell(r, 6, preco)
    ws.cell(r, 7, moeda)
    ws.cell(r, 8, unid)
    ws.cell(r, 9, f'=IF(G{r}="USD",F{r}*Resumo!$C$6,F{r})')
    ws.cell(r, 10, origem)
    
    for j, q in enumerate((u1, u3, p1, p3)):
        ws.cell(r, 11 + j, q)
        qcol = get_column_letter(11 + j)
        # Fórmula com arredondamento para cima em pacotes
        ws.cell(r, 15 + j, f'=IF(AND($J{r}="{COMPRAR}",{qcol}{r}>0),ROUNDUP({qcol}{r}/$H{r},0)*$I{r},0)')
        
    ws.cell(r, 19, conf)
    ws.cell(r, 20, notas)
    ws.cell(r, 21, "Acessar Link" if link else "")
    if link:
        ws.cell(r, 21).hyperlink = link
        ws.cell(r, 21).font = F_LINK
        
    # Estilização das Células
    zebra = (i % 2 == 1)
    for c in range(1, len(cab) + 1):
        cell = ws.cell(r, c)
        cell.border = BORDER_CELL
        cell.font = F_REGULAR
        
        # Alinhamentos específicos
        if c in (1, 7, 8, 10, 11, 12, 13, 14, 19, 21):
            cell.alignment = ALIGN_CENTER
        elif c in (6, 9, 15, 16, 17, 18):
            cell.alignment = ALIGN_RIGHT
        else:
            cell.alignment = ALIGN_LEFT
            
        # Formatação Numérica
        if c == 6:
            cell.number_format = FMT_USD if moeda == "USD" else FMT_CURRENCY
        elif c in (9, 15, 16, 17, 18):
            cell.number_format = FMT_CURRENCY
        elif c in (1, 8, 11, 12, 13, 14):
            cell.number_format = FMT_INT
            
        # Fundo Zebra Suave
        if zebra:
            cell.fill = FILL_ZEBRA
            
        # Destaque de Origem (Badges)
        if c == 10:
            if origem == COMPRAR:
                cell.fill = FILL_BADGE_COMPRAR
                cell.font = Font(name=FONT_FAMILY, size=8.5, bold=True, color="166534")
            elif origem == LVIS:
                cell.fill = FILL_BADGE_LVIS
                cell.font = Font(name=FONT_FAMILY, size=8.5, bold=True, color="1E40AF")
            elif origem == LVIS_CONF:
                cell.fill = FILL_BADGE_CONFIRMAR
                cell.font = Font(name=FONT_FAMILY, size=8.5, bold=True, color="92400E")
            else:
                cell.fill = FILL_BADGE_ALT
                cell.font = Font(name=FONT_FAMILY, size=8.5, italic=True, color="475569")
                
        # Destaque de Preço Estimado
        if c == 19 and conf == ESTIMADO:
            cell.fill = FILL_BADGE_ESTIMADO
            cell.font = Font(name=FONT_FAMILY, size=8.5, bold=True, color="854D0E")
        elif c == 19 and conf == COTADO:
            cell.font = Font(name=FONT_FAMILY, size=8.5, color="047857")

    row_atual += 1

ultima = row_atual - 1

# Linha de Totais da BOM
rt = row_atual
ws.row_dimensions[rt].height = 24
ws.cell(rt, 3, "TOTAL ACUMULADO (SEM FRETE)").font = F_TOTAL
ws.cell(rt, 3).alignment = Alignment(horizontal="right", vertical="center")

for j in range(4):
    col = get_column_letter(15 + j)
    c = ws.cell(rt, 15 + j, f"=SUM({col}{primeira}:{col}{ultima})")
    c.number_format = FMT_CURRENCY
    c.font = F_TOTAL
    c.alignment = ALIGN_RIGHT

for c in range(1, len(cab) + 1):
    cell = ws.cell(rt, c)
    cell.fill = FILL_TOTAL_ROW
    cell.border = BORDER_TOTAL

# Validação de Dados nas Colunas
dv_origem = DataValidation(type="list", formula1=f'"{COMPRAR},{LVIS},{LVIS_CONF},{ALT}"', allow_blank=False)
ws.add_data_validation(dv_origem)
dv_origem.add(f"J{primeira}:J{ultima}")

dv_status = DataValidation(type="list", formula1=f'"{COTADO},{ESTIMADO}"', allow_blank=False)
ws.add_data_validation(dv_status)
dv_status.add(f"S{primeira}:S{ultima}")

# Larguras das Colunas da BOM
larguras_bom = [5, 22, 40, 18, 18, 12, 8, 10, 13, 16, 7, 7, 7, 7, 13, 13, 13, 13, 12, 52, 16]
for i, w in enumerate(larguras_bom, start=1):
    ws.column_dimensions[get_column_letter(i)].width = w

# Congelar Painéis e Filtros
ws.freeze_panes = ws.cell(HDR + 1, 4)
ws.auto_filter.ref = f"A{HDR}:U{ultima}"


# ==============================================================================
# ABA 3: NOTAS DE ENGENHARIA (CADERNO TÉCNICO)
# ==============================================================================
ns = wb.create_sheet("Notas")
ns.views.sheetView[0].showGridLines = True

ns.row_dimensions[1].height = 20
ns["A1"] = "CADERNO DE ENGENHARIA: NOTAS, PREMISSAS E DIRETRIZES TÉCNICAS"
ns["A1"].font = F_TITLE

ns.row_dimensions[2].height = 16
ns["A2"] = "Documentação das premissas de projeto, regras de transição entre bancada e luva vestível, e decisões de hardware."
ns["A2"].font = F_SUBTITLE

secoes_notas = [
    ("1. PREMISSAS DE ALIMENTAÇÃO E ARQUITETURA", [
        ("Bancada vs. Wearable", "Nos cenários de bancada (1 dedo - U1 e P1), a alimentação é fornecida diretamente pelo barramento USB de 5V do computador, simplificando os testes de aquisição. A bateria Li-Ion 18650, módulo carregador TP4056 e regulador boost MT3608 só são ativados nos cenários de 3 dedos (luva vestível autônoma)."),
        ("Estimativa de Ímãs N52", "Foi adotada a cotação preliminar de 4 ímãs por dedo (disco 5×3 mm). A quantidade exata e o arranjo geométrico de sobreposição dipolar serão definidos após a modelagem paramétrica da microestrutura cut-cell no Fusion 360."),
        ("Atuadores Vibrotáteis ERM", "Previsto 1 motor ERM coin (8×4 mm) por dedo ativo + 1 unidade extra de reserva técnica em bancada."),
        ("Recursos Próprios L-VIS", "Filamento TPU flexível 95A, protoboards, jumpers de sinal, cabos micro-USB e resistores THT são supridos gratuitamente pela infraestrutura do Laboratório L-VIS.")
    ]),
    ("2. ROTEIRO DE TRANSIÇÃO (1 DEDO ➔ 3 DEDOS)", [
        ("Reaproveitamento de Lotes", "Os kits de ímãs N52 (20 un.), transistores 2N7000 (50 un.) e diodos 1N4148 (200 un.) contêm peças suficientes para abastecer todos os 3 dedos. A migração de U1 para U3 requer apenas a compra dos sensores adicionais e do circuito de alimentação."),
        ("Microcontroladores", "O ESP32 DevKit V1 adquirido na Fase 1 continuará operando permanentemente como nó de validação em bancada, enquanto o ESP32-S3 Nano assumirá a eletrônica embarcada no punho da luva.")
    ]),
    ("3. ITENS A COTAR / PENDÊNCIAS TÉCNICAS", [
        ("Sensibilidade de Gate 2N7000", "O transistor 2N7000 possui tensão de limiar de gate (Vgs_th) típica entre 2,0V e 3,0V. Deve-se validar se a saída lógica de 3,3V do ESP32 satura o canal de forma plena para conduzir os ~70mA do motor ERM. Caso contrário, substituir pelo AO3400A (nível lógico garantido em 2,5V) ou bipolar BC337."),
        ("Especificação ESP32-S3 Nano", "Definir entre o modelo Waveshare ESP32-S3 Nano ou Arduino Nano ESP32 em função de dimensões físicas e pinagem."),
        ("Multiplexador TCA9548A", "O CI TLV493D-A1B6 suporta apenas 2 endereços I2C selecionáveis. O TCA9548A é indispensável na luva de 3 dedos para isolar os barramentos SDA/SCL de cada falange.")
    ]),
    ("4. REGISTRO DE DECISÕES DE HARDWARE", [
        ("Módulo IRF520 Removido", "O IRF520 não é um MOSFET de nível lógico e necessita de Vgs > 5V para conduzir corrente significativa, operando de forma instável ou ineficiente com o ESP32."),
        ("Ímã 5×1 mm Descartado", "O volume magnético do disco 5×1 mm é ~30% menor que o modelo de referência (4,76×1,58 mm), reduzindo a densidade de fluxo e a sensibilidade do eFlesh. Adotou-se o disco 5×3 mm como padrão de alta sensibilidade."),
        ("Breakouts vs. PCB SMD", "Para compatibilizar prazos e orçamento, a fase de bancada inicia com breakouts Qwiic prontos. A PCB customizada no KiCad será desenvolvida para a luva final.")
    ])
]

row_n = 4
for sec_tit, itens_sec in secoes_notas:
    ns.row_dimensions[row_n].height = 22
    cell_sec = ns.cell(row_n, 1, sec_tit)
    cell_sec.font = F_SECTION
    row_n += 1
    
    for tit_item, txt_item in itens_sec:
        ns.row_dimensions[row_n].height = 24
        c_i = ns.cell(row_n, 1, f"• {tit_item}:")
        c_i.font = F_BOLD
        c_i.alignment = Alignment(horizontal="left", vertical="center")
        
        ns.merge_cells(start_row=row_n, start_column=2, end_row=row_n, end_column=4)
        c_t = ns.cell(row_n, 2, txt_item)
        c_t.font = F_REGULAR
        c_t.alignment = ALIGN_LEFT
        row_n += 1
        
    row_n += 1

ns.column_dimensions["A"].width = 30
ns.column_dimensions["B"].width = 40
ns.column_dimensions["C"].width = 40
ns.column_dimensions["D"].width = 40

# Salvar Planilha Final
wb.save(OUT)
print(f"Planilha estética e profissional gerada com sucesso em: {OUT}")
