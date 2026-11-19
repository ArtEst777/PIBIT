# -*- coding: utf-8 -*-
"""Gera BOM/BOM.xlsx do projeto PIBIT com design estético, profissional e executivo (v4.0).

Compatível com a pesquisa de preços v4.0 e otimizado para logística em Brasília - DF.

Cenários:
  U1 = Placa universal, 1 dedo (início / bancada de testes)
  U3 = Placa universal, 3 dedos (objetivo final montagem manual em perfboard)
  P1 = PCB customizada, 1 dedo (bancada com placa SMD KiCad)
  P3 = PCB customizada, 3 dedos (objetivo final integrado SMD vestível)

Opções Comparativas (3 Dedos):
  Opção A = PCB Customizada SMD (CIs avulsos TLV493D-A1B6 + ESP32-WROOM-32U + MOSFETs SMD)
  Opção B = Prototipagem em Placa Perfurada (Módulos breakout Qwiic TLV493D + ESP32 DevKit V1 RoboCore)
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

# Tipografia e Paleta de Cores Executiva (Slate / Navy / Emerald / Amber)
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
F_TITLE = Font(name=FONT_FAMILY, size=15, bold=True, color="0F172A")
F_SUBTITLE = Font(name=FONT_FAMILY, size=9.5, italic=True, color="475569")
F_SECTION = Font(name=FONT_FAMILY, size=11, bold=True, color="0F172A")
F_HEADER = Font(name=FONT_FAMILY, size=9, bold=True, color="FFFFFF")
F_CAT = Font(name=FONT_FAMILY, size=9.5, bold=True, color="1E293B")
F_REGULAR = Font(name=FONT_FAMILY, size=9, color="1E293B")
F_BOLD = Font(name=FONT_FAMILY, size=9, bold=True, color="1E293B")
F_LINK = Font(name=FONT_FAMILY, size=8.5, color="0284C7", underline="single")
F_TOTAL = Font(name=FONT_FAMILY, size=9.5, bold=True, color="0F172A")

# Fontes KPI
F_KPI_LABEL = Font(name=FONT_FAMILY, size=8, bold=True, color="475569")
F_KPI_CODE = Font(name=FONT_FAMILY, size=9.5, bold=True, color="0F172A")
F_KPI_VAL = Font(name=FONT_FAMILY, size=14, bold=True, color="0F172A")
F_KPI_DESC = Font(name=FONT_FAMILY, size=8, italic=True, color="64748B")

# Bordas
THIN_GRAY = Side(style="thin", color="CBD5E1")
THICK_NAVY = Side(style="medium", color="1E3A5F")
DOUBLE_BOTTOM = Side(style="double", color="1E3A5F")

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

# Definição dos Itens da BOM v4.0 (28 Itens com Logística Brasília - DF)
# Tupla: (Categoria, Componente, Modelo, Fornecedor, Preço, Moeda, Qtd/Pct, Origem, U1, U3, P1, P3, Status, Notas, Link)
ITENS = [
    # 1. Atuadores Vibrotáteis ERM
    ("1. Atuadores Vibrotáteis ERM", "Motor de Vibração Chato com Fio 8x4mm (ERM Coin 3V)",
     "Motor 8x4mm C/ Fio", "HU Infinito (Correios DF)", 8.50, "BRL", 1, COMPRAR, 2, 4, 2, 4, COTADO,
     "Fornecedor nacional direto. 1 un/dedo + 1 reserva técnica. Despacho Correios (Sedex/PAC) para Brasília.",
     "https://www.huinfinito.com.br/motores/1391-motor-de-vibracao-chato-com-fio-8x4mm.html"),
    ("1. Atuadores Vibrotáteis ERM", "Motor ERM Coin 8x2.0mm com FPC (Baixo Consumo 35mA)",
     "JYC0820FL", "DigiKey (UPS Express)", 1.43, "USD", 1, ALT, 0, 0, 0, 0, COTADO,
     "Alternativa ultra-fina (2.0mm) e baixo consumo (35mA). Importação DigiKey (DDP com tributos pagos).",
     "https://www.digikey.com.br/pt/products/detail/jinlong-machinery-electronics-inc/JYC0820FL001G/14311822"),
    ("1. Atuadores Vibrotáteis ERM", "Kit Motor Vibracall Moeda 10mm 3V (5 Unidades 1027)",
     "Vibracall 10mm (1027)", "Mercado Livre Full (DF 24-48h)", 25.00, "BRL", 5, ALT, 0, 0, 0, 0, COTADO,
     "Opção com entrega FULL no Mercado Livre (24h a 48h em Brasília via CD Santa Maria/DF).",
     "https://lista.mercadolivre.com.br/motor-vibracall-moeda-10mm"),

    # 2. Acionamento ERM & Prototipagem
    ("2. Acionamento ERM & Prototipagem", "MOSFET Canal N Through-Hole 60V 115mA (TO-92)",
     "2N7000 / BS170", "RoboCore (Jadlog DF 2-3d)", 1.20, "BRL", 1, COMPRAR, 1, 3, 0, 0, COTADO,
     "Versão bancada/perfboard. RoboCore despacha para DF em 2-3 dias; disponível também em lojas na W3 Sul (DF).",
     "https://www.robocore.net/transistor/transistor-mosfet-2n7000"),
    ("2. Acionamento ERM & Prototipagem", "MOSFET Canal N SMD 30V 5.8A (SOT-23)",
     "AO3400A / 2N7002", "Mercado Livre / AliExpress", 0.50, "BRL", 1, COMPRAR, 0, 0, 1, 3, COTADO,
     "Versão PCB SMD. Condução plena garantida com sinal de 2,5V/3,3V diretamente do pino GPIO do ESP32.",
     "https://lista.mercadolivre.com.br/ao3400a-sot-23"),
    ("2. Acionamento ERM & Prototipagem", "Díodo de Proteção Flyback 1N4148 (THT / SOD-27)",
     "1N4148 THT", "Eletrogate (Sedex DF 2-3d) / L-VIS", 0.30, "BRL", 1, COMPRAR, 1, 3, 0, 0, COTADO,
     "Versão manual. Proteção indutiva em antiparalelo com cada motor. Disponível no estoque do laboratório L-VIS (UnB).",
     "https://www.eletrogate.com/diodo-1n4148"),
    ("2. Acionamento ERM & Prototipagem", "Díodo de Proteção Flyback SMD (1N4148W SOD-123)",
     "1N4148W SMD", "Mercado Livre / AliExpress", 0.30, "BRL", 1, COMPRAR, 0, 0, 1, 3, COTADO,
     "Versão PCB SMD. Diodo ultra-rápido de proteção para montagem em superfície.",
     "https://lista.mercadolivre.com.br/1n4148w-sod-123"),
    ("2. Acionamento ERM & Prototipagem", "Resistor 220 Ω / 100 Ω 1/4W (Limitador de Gate PWM)",
     "Resistor 100R THT", "Eletrogate / L-VIS UnB", 0.10, "BRL", 1, LVIS, 1, 3, 0, 0, COTADO,
     "Versão manual. Disponível gratuitamente no L-VIS (UnB) ou fornecido pela Eletrogate.",
     "https://www.eletrogate.com/resistor-100r-1-4w"),
    ("2. Acionamento ERM & Prototipagem", "Resistor 10k Ω 1/4W (Pull-down de Gate)",
     "Resistor 10k THT", "Eletrogate / L-VIS UnB", 0.10, "BRL", 1, LVIS, 1, 3, 0, 0, COTADO,
     "Versão manual. Mantém gate em nível baixo durante boot do ESP32. Grátis no L-VIS (UnB).",
     "https://www.eletrogate.com/resistor-10k-1-4w"),
    ("2. Acionamento ERM & Prototipagem", "Módulo Driver MOSFET IRF520 PWM para Arduino",
     "Módulo IRF520", "Eletrogate / Mercado Livre", 12.50, "BRL", 1, ALT, 0, 0, 0, 0, COTADO,
     "Alternativa modular rápida. Vgs de saturação elevado (>5V); transistores 2N7000/AO3400A são preferíveis.",
     "https://www.eletrogate.com/modulo-driver-mosfet-irf520"),
    ("2. Acionamento ERM & Prototipagem", "Placa de Circuito Impresso Universal Perfurada (Perfboard 2.54mm)",
     "Perfboard 5x7cm / 10x10cm", "Eletrogate (2-3d DF) / Feira Importados", 15.00, "BRL", 1, COMPRAR, 1, 1, 0, 0, COTADO,
     "Circuito central no dorso da mão. Eletrogate entrega em 2-3 dias no DF; disponível também na Feira dos Importados.",
     "https://www.eletrogate.com/placa-de-circuito-impresso-ilhada-dupla-face-5x7cm"),

    # 3. Sensoriamento eFlesh
    ("3. Sensoriamento eFlesh", "Módulo Magnetômetro 3D TLV493D STEMMA QT / Qwiic",
     "Módulo TLV493D Qwiic", "AliExpress (Remessa Conforme DF)", 36.99, "BRL", 1, COMPRAR, 1, 3, 0, 0, COTADO,
     "Versão prototipagem manual. Comprar 3 un dilui o frete. Remessa Conforme com entrega DF pelos Correios.",
     "https://pt.aliexpress.com/item/1005008497289675.html"),
    ("3. Sensoriamento eFlesh", "CI Magnetômetro 3D TLV493D-A1B6 (TSOP-6)",
     "TLV493DA1B6HTSA1", "DigiKey / Mouser", 1.80, "USD", 1, COMPRAR, 0, 0, 2, 4, COTADO,
     "Versão PCB KiCad. Inclui 1 un de reserva para retrabalho de solda. Envio expresso DDP.",
     "https://www.digikey.com.br/pt/products/detail/infineon-technologies/TLV493DA1B6HTSA1/5802095"),
    ("3. Sensoriamento eFlesh", "20 Peças Imã De Neodímio Super Forte N52 Pastilha 5mm X 1mm (ou 5x3mm)",
     "N52 Disco 5x1mm", "Mercado Livre Full (DF 24-48h)", 21.85, "BRL", 20, COMPRAR, 4, 12, 4, 12, COTADO,
     "Kit com 20 un. Entrega Full para Brasília (24h a 48h via CD Santa Maria/DF). 4 ímãs por dedo na cut-cell.",
     "https://lista.mercadolivre.com.br/ima-neodimio-n52-5x1mm"),
    ("3. Sensoriamento eFlesh", "Ímã de Neodímio N52 Disco 3/16\" x 1/16\" (10 Unidades)",
     "N52 3/16\"x1/16\"", "K&J Magnetics (EUA)", 5.00, "USD", 10, ALT, 0, 0, 0, 0, COTADO,
     "Modelo de referência do artigo original eFlesh. Alternativa para calibração laboratorial comparativa.",
     "https://www.kjmagnetics.com/d31-n52-neodymium-disc-magnet"),
    ("3. Sensoriamento eFlesh", "Módulo Multiplexador I2C TCA9548A (8 Canais)",
     "TCA9548A", "Eletrogate / Mercado Livre", 20.00, "BRL", 1, COMPRAR, 0, 1, 0, 1, ESTIMADO,
     "Obrigatório para 3 dedos: o sensor TLV493D possui apenas 2 endereços I2C selecionáveis.",
     "https://www.eletrogate.com/modulo-multiplexador-i2c-tca9548a"),

    # 4. Processamento & Alimentação
    ("4. Processamento & Alimentação", "Placa de Desenvolvimento ESP32 WiFi + Bluetooth DevKit V1",
     "ESP32 DevKit V1", "RoboCore (Oficial SP->DF 2-3d)", 49.90, "BRL", 1, COMPRAR, 1, 1, 1, 0, COTADO,
     "Fornecedor oficial nacional. Despacho Jadlog/Sedex para Brasília em 2-3 dias. Bancada USB e testes.",
     "https://www.robocore.net/wifi/esp32-wifi-bluetooth"),
    ("4. Processamento & Alimentação", "Módulo ESP32-WROOM-32U com Conector U.FL (SMD para PCB)",
     "ESP32-WROOM-32U", "RoboCore / Mercado Livre", 32.00, "BRL", 1, COMPRAR, 0, 0, 0, 1, COTADO,
     "Módulo SMD oficial RoboCore para PCB customizada do punho. Permite antena articulada externa.",
     "https://www.robocore.net/wifi/modulo-esp32-wroom-32u"),
    ("4. Processamento & Alimentação", "Placa ESP32-S3 Nano (Compacta Dual-Core LX7)",
     "ESP32-S3 Nano", "Eletrogate / Waveshare", 90.00, "BRL", 1, ALT, 0, 0, 0, 0, ESTIMADO,
     "Alternativa ultra-compacta pronta para luva vestível.",
     "https://www.eletrogate.com/modulo-esp32-s3"),
    ("4. Processamento & Alimentação", "Bateria LiPo 3.7V 1050mAh (com Circuito de Proteção)",
     "LiPo 3.7V 1050mAh", "RoboCore (LiPo Certificada DF)", 38.00, "BRL", 1, COMPRAR, 0, 1, 0, 1, COTADO,
     "RoboCore oficial com proteção PCM contra curto/sobrecarga. Transporte rodoviário homologado DF.",
     "https://www.robocore.net/baterias/bateria-lipo-3-7v-1050mah"),
    ("4. Processamento & Alimentação", "Módulo Carregador de Bateria TP4056 USB-C",
     "TP4056 USB-C", "Eletrogate (USB-C)", 8.50, "BRL", 1, COMPRAR, 0, 1, 0, 1, COTADO,
     "Gerenciamento de recarga LiPo com conector Type-C e proteção contra subtensão.",
     "https://www.eletrogate.com/modulo-carregador-de-baterias-tp4056-usb-c"),
    ("4. Processamento & Alimentação", "Módulo Regulador de Tensão Boost 5V (MT3608)",
     "MT3608", "Eletrogate / Mercado Livre", 8.50, "BRL", 1, COMPRAR, 0, 1, 0, 1, ESTIMADO,
     "Eleva e estabiliza os 3.7V da bateria em 5.0V constante para o barramento do ESP32.",
     "https://www.eletrogate.com/modulo-regulador-de-tensao-step-up-mt3608"),

    # 5. Passivos & Conectores PCB
    ("5. Passivos & Conectores PCB", "Capacitor Cerâmico SMD 0805 100nF (0.1µF 50V)",
     "Capacitor 0805 100nF", "Mercado Livre Full (DF)", 0.20, "BRL", 1, COMPRAR, 0, 0, 2, 6, COTADO,
     "Versão PCB SMD. Filtro de desacoplamento local em cada magnetômetro.",
     "https://lista.mercadolivre.com.br/capacitor-smd-0805-100nf"),
    ("5. Passivos & Conectores PCB", "Resistor SMD 0805 4.7k Ω (Pull-up I2C)",
     "Resistor 0805 4.7k", "Mercado Livre Full (DF)", 0.10, "BRL", 1, COMPRAR, 0, 0, 2, 2, COTADO,
     "Versão PCB SMD. Resistores de pull-up para barramentos I2C.",
     "https://lista.mercadolivre.com.br/resistor-smd-0805-4k7"),
    ("5. Passivos & Conectores PCB", "Barra de Pinos Macho 1x40 2.54mm",
     "Barra de Pinos 1x40", "RoboCore / W3 Sul Brasília", 2.50, "BRL", 1, COMPRAR, 1, 2, 1, 1, COTADO,
     "Interconexões de bancada. Disponível na RoboCore, Eletrogate ou lojas na W3 Sul (DF).",
     "https://www.robocore.net/conectores/barra-de-pinos-1x40-180-macho"),
    ("5. Passivos & Conectores PCB", "Conector JST-SH 4 Pinos 1.0mm (Fêmea + Cabo) / JST PH",
     "JST-SH 4P 1.0mm", "Mercado Livre / AliExpress", 3.50, "BRL", 1, COMPRAR, 0, 3, 1, 3, COTADO,
     "Chicotes destacáveis para fiação das articulações dos dedos sem fadiga de solda.",
     "https://lista.mercadolivre.com.br/conector-jst-sh-1.0mm"),
    ("5. Passivos & Conectores PCB", "Fio Flexível Extrafino Siliconado 28–30 AWG",
     "Fio Silicone 28/30 AWG", "Eletrogate / Mercado Livre", 15.00, "BRL", 1, COMPRAR, 1, 1, 1, 1, COTADO,
     "Cabinho de silicone flexível indispensável para não travar a movimentação dos dedos.",
     "https://www.eletrogate.com/fio-silicone-awg30"),
    ("5. Passivos & Conectores PCB", "Fabricação de PCB Customizada (Lote 5 un. KiCad 2 camadas)",
     "PCB 2 Camadas", "JLCPCB / PCBWay", 120.00, "BRL", 1, COMPRAR, 0, 0, 1, 1, ESTIMADO,
     "Versão KiCad. Lote com 5 placas atende os 3 dedos com sobras para testes.",
     "https://jlcpcb.com/"),
    ("5. Passivos & Conectores PCB", "Protoboard, Jumpers Flexíveis e Cabos USB de Bancada",
     "Protoboard + Jumpers", "L-VIS UnB", 0.00, "BRL", 1, LVIS, 1, 1, 1, 1, COTADO,
     "Disponíveis para uso irrestrito no laboratório L-VIS (UnB).",
     ""),

    # 6. Insumos de Fabricação & Montagem
    ("6. Insumos de Fabricação & Montagem", "Filamento Flexível TPU 95A 1.75mm (Carretel 500g)",
     "TPU 95A 500g", "3D Fila / ML Full (DF 24-48h)", 89.00, "BRL", 1, COMPRAR, 1, 1, 1, 1, COTADO,
     "3D Fila original. Entrega expressa para Brasília (24h a 48h via ML Full). Impressão das polpas eFlesh.",
     "https://www.3dfila.com.br/filamento-tpu-flexivel-1-75mm"),
    ("6. Insumos de Fabricação & Montagem", "Cola Instantânea Cianoacrilato (Super Bonder 3g para Ímãs)",
     "Super Bonder 3g", "Papelaria DF / ML Full", 6.50, "BRL", 1, COMPRAR, 1, 1, 1, 1, COTADO,
     "Fixação dos ímãs de neodímio nos alojamentos internos de TPU. Compra imediata em papelarias/ferragens no DF.",
     "https://lista.mercadolivre.com.br/cola-super-bonder-3g"),
    ("6. Insumos de Fabricação & Montagem", "Luva Têxtil Base e Acessórios Mecânicos em PLA",
     "Luva Têxtil + PLA", "L-VIS UnB", 0.00, "BRL", 1, LVIS, 1, 1, 1, 1, COTADO,
     "Luva base de tecido e case rígido em PLA impressos nas impressoras 3D do L-VIS.",
     ""),
]

CENARIOS = [
    ("U1", "Placa Universal • 1 Dedo", "Bancada Inicial (ESP32 DevKit, USB, Breakout Qwiic)", FILL_KPI_U1),
    ("U3", "Placa Universal • 3 Dedos", "Objetivo Final Manual (ESP32 DevKit, Bateria, TCA9548A)", FILL_KPI_U3),
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

rs["A2"] = "PIBIT / L-VIS (UnB)  •  LUVA TÁTIL eFLESH (v4.0)"
rs["A2"].font = Font(name=FONT_FAMILY, size=15, bold=True, color="0F172A")

rs["A3"] = "Painel Executivo de Custos, Comparativo de Cenários e Logística Brasília - DF"
rs["A3"].font = Font(name=FONT_FAMILY, size=9.5, italic=True, color="475569")

rs["A4"] = "Autor: Artur Ferreira Gonçalves | Laboratório: L-VIS (UnB) | Orientação: Prof. Dr. Felix | Atualização: Novembro/2026 (v4.0)"
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

rs["D6"] = "(Célula editável — atualiza custos em US$ automaticamente em todas as abas)"
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
    
    # Bordas e cores do card
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
rs["A14"] = "1. COMPARATIVO DETALHADO DOS CENÁRIOS DE ENGENHARIA"
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
    "Baixa (Validação Rápida em Bancada)",
    "Média (Montagem Manual Completa 3 Dedos)",
    "Média-Alta (Soldagem SMD Bancada KiCad)",
    "Alta (Integração Total na Luva Vestível)"
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

# Tabela 2: Resumo Comparativo Opção A vs Opção B (Pesquisa de Preços v4.0)
r_opcoes_title = 22
rs.row_dimensions[r_opcoes_title].height = 22
rs[f"A{r_opcoes_title}"] = "2. COMPARATIVO DE ARQUITETURAS DE 3 DEDOS (PESQUISA v4.0)"
rs[f"A{r_opcoes_title}"].font = F_SECTION

cab_opcoes = ["Opção", "Arquitetura de Montagem", "Atuadores (3 Dedos)", "Acionamento de Potência", "Sensoriamento & Processamento", "Custo Estimado (R$)"]
rs.row_dimensions[r_opcoes_title + 1].height = 22
for col_idx, text in enumerate(cab_opcoes, start=1):
    cell = rs.cell(r_opcoes_title + 1, col_idx, text)
    cell.fill = FILL_HEADER_SEC
    cell.font = F_HEADER
    cell.alignment = ALIGN_HEADER
    cell.border = BORDER_HEADER

opcoes_dados = [
    ("Opção A", "PCB Customizada (CIs Avulsos SMD + KiCad)",
     "3x ERM 8x4mm HU Infinito (ou JYC0820FL)",
     "3x MOSFETs AO3400A SOT-23 + Díodos 1N4148W",
     "3x TLV493D-A1B6 SMD + ESP32-WROOM-32U + LiPo 1050mAh",
     "=D19"),  # Liga diretamente ao Cenário P3 (PCB 3 dedos)
    ("Opção B", "Prototipagem em Placa Perfurada (Módulos Breakout)",
     "3x ERM 8x4mm HU Infinito com Fio",
     "3x MOSFETs 2N7000 TO-92 + Díodos 1N4148 + Perfboard",
     "3x Módulos TLV493D Qwiic + ESP32 DevKit V1 RoboCore + LiPo",
     "=D17")   # Liga diretamente ao Cenário U3 (Universal 3 dedos)
]

for idx, op in enumerate(opcoes_dados):
    r = r_opcoes_title + 2 + idx
    rs.row_dimensions[r].height = 22
    for c_idx, val in enumerate(op[:5], start=1):
        cell = rs.cell(r, c_idx, val)
        cell.font = F_BOLD if c_idx == 1 else F_REGULAR
        cell.alignment = ALIGN_CENTER if c_idx == 1 else ALIGN_LEFT
        cell.border = BORDER_CELL
        if idx % 2 == 1:
            cell.fill = FILL_ZEBRA
            
    c_val = rs.cell(r, 6, op[5])
    c_val.font = F_BOLD
    c_val.alignment = ALIGN_RIGHT
    c_val.number_format = FMT_CURRENCY
    c_val.fill = FILL_CARD_BG
    c_val.border = BORDER_CELL

# Tabela 3: Custos por Subsistema de Engenharia
r_cat_title = r_opcoes_title + 5
rs.row_dimensions[r_cat_title].height = 22
rs[f"A{r_cat_title}"] = "3. DISTRIBUIÇÃO DE CUSTOS POR SUBSISTEMA DE ENGENHARIA"
rs[f"A{r_cat_title}"].font = F_SECTION

cab_cats = ["Subsistema de Engenharia", "U1: Univ. 1 Dedo", "U3: Univ. 3 Dedos", "P1: PCB 1 Dedo", "P3: PCB 3 Dedos"]
rs.row_dimensions[r_cat_title + 1].height = 20
for c_idx, t in enumerate(cab_cats, start=1):
    cell = rs.cell(r_cat_title + 1, c_idx, t)
    cell.fill = FILL_HEADER_PRI
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

# Seção 4: Guia de Aquisição e Logística Brasília - DF
r_guia = r_tot_cat + 2
rs.row_dimensions[r_guia].height = 20
rs[f"A{r_guia}"] = "4. DIRETRIZES DE AQUISIÇÃO E LOGÍSTICA PARA BRASÍLIA - DF"
rs[f"A{r_guia}"].font = F_SECTION

diretrizes_df = [
    ("Mercado Livre Full (DF 24-48h)", "Priorizar anúncios com selo Full para Brasília. Os produtos saem dos centros de distribuição do DF (Santa Maria/DF) e Goiás (Anápolis), com entrega garantida em 24h a 48h úteis. Ideal para: ímãs N52 pastilha, cola instantânea, cabos e filamento TPU."),
    ("RoboCore (Despacho SP ➔ DF 2-3d)", "Fornecedor nacional oficial com envio ágil para Brasília via Jadlog Express ou Sedex (2 a 3 dias úteis). Recomendado para componentes críticos de qualidade: ESP32 DevKit V1 original, módulo SMD ESP32-WROOM-32U e bateria LiPo 1050mAh homologada."),
    ("Eletrogate (Despacho Rápido 2-3d)", "Excelente catálogo com entrega rápida no DF via transportadora. Ideal para o módulo carregador TP4056 USB-C, multiplexador I2C TCA9548A, módulos boost MT3608 e placas universais perfuradas (perfboards)."),
    ("HU Infinito (Correios Sedex DF)", "Fornecedor de referência para o motor ERM mini moeda 8x4mm com fios. Despachado via Correios com código de rastreamento para Brasília."),
    ("Comércio Local em Brasília (Sem Frete)", "Lojas de componentes eletrônicos na Comercial da W3 Sul (ex: 508 Sul e 708 Sul) e Feira dos Importados de Brasília (SIA): transistores 2N7000 avulsos, diodos 1N4148, resistores, protoboards e barras de pinos para reposição imediata de bancada."),
    ("Infraestrutura Laboratório L-VIS (UnB)", "Protoboards de bancada, jumpers flexíveis, resistores 1/4W, cabos micro-USB e impressoras 3D são fornecidos diretamente pelo laboratório na UnB (custo R$ 0,00 para o projeto).")
]

for idx, (titulo_d, desc_d) in enumerate(diretrizes_df):
    r_d = r_guia + 1 + idx
    rs.row_dimensions[r_d].height = 22
    c_t = rs.cell(r_d, 1, f"• {titulo_d}: ")
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
ws["A1"] = "BOM — ESPECIFICAÇÃO COMPLETA DE MATERIAIS E COMPONENTES (v4.0)"
ws["A1"].font = F_TITLE

ws.row_dimensions[2].height = 16
ws["A2"] = "Projeto PIBIT / L-VIS (UnB) | Otimizado para logística em Brasília - DF | Detalhamento técnico por subsistema"
ws["A2"].font = F_SUBTITLE

# Linha 4: Super-Cabeçalho (Agrupador Visual)
ws.row_dimensions[4].height = 18

super_headers = [
    ("A4:E4", "ESPECIFICAÇÃO DO COMPONENTE", FILL_HEADER_PRI),
    ("F4:I4", "PREÇO DO LOTE / PACOTE", FILL_HEADER_SEC),
    ("J4:J4", "ORIGEM", FILL_HEADER_PRI),
    ("K4:N4", "QUANTIDADES DEMANDADAS", FILL_HEADER_SEC),
    ("O4:R4", "CUSTOS POR CENÁRIO (R$)", FILL_HEADER_PRI),
    ("S4:U4", "STATUS, LOGÍSTICA DF & LINKS", FILL_HEADER_SEC),
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
    "ID", "Subsistema", "Componente / Descrição Técnica", "Modelo / Part Number", "Fornecedor / Logística DF",
    "Preço Orig.", "Moeda", "Qtd/Pct", "Preço Pct (R$)",
    "Origem", "U1", "U3", "P1", "P3",
    "Custo U1 (R$)", "Custo U3 (R$)", "Custo P1 (R$)", "Custo P3 (R$)",
    "Status Preço", "Notas Técnicas & Logística Brasília - DF", "Link do Produto / Loja"
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
        # Arredondamento para cima em pacotes
        ws.cell(r, 15 + j, f'=IF(AND($J{r}="{COMPRAR}",{qcol}{r}>0),ROUNDUP({qcol}{r}/$H{r},0)*$I{r},0)')
        
    ws.cell(r, 19, conf)
    ws.cell(r, 20, notas)
    ws.cell(r, 21, "Acessar Loja" if link else "—")
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
larguras_bom = [5, 24, 42, 20, 24, 12, 8, 10, 13, 16, 7, 7, 7, 7, 13, 13, 13, 13, 12, 52, 16]
for i, w in enumerate(larguras_bom, start=1):
    ws.column_dimensions[get_column_letter(i)].width = w

# Congelar Painéis
ws.freeze_panes = ws.cell(HDR + 1, 4)


# ==============================================================================
# ABA 3: NOTAS (CADERNO DE ENGENHARIA & LOGÍSTICA DF)
# ==============================================================================
ns = wb.create_sheet("Notas")
ns.views.sheetView[0].showGridLines = True

ns.row_dimensions[1].height = 20
ns["A1"] = "CADERNO DE ENGENHARIA: NOTAS, DIRETRIZES TÉCNICAS E LOGÍSTICA DF (v4.0)"
ns["A1"].font = F_TITLE

ns.row_dimensions[2].height = 16
ns["A2"] = "Premissas do projeto eFlesh / L-VIS (UnB), roteiro de montagem e mapeamento de fornecedores em Brasília."
ns["A2"].font = F_SUBTITLE

secoes_notas = [
    ("1. PREMISSAS DE ALIMENTAÇÃO E ARQUITETURA", [
        ("Bancada USB vs. Bateria Vestível", "Nos cenários de bancada (1 dedo - U1 e P1), a alimentação é fornecida pelo barramento USB do computador (5V / 500mA), acelerando os ensaios de calibração. A bateria LiPo 3.7V 1050mAh, módulo carregador TP4056 USB-C e regulador boost MT3608 são acionados nos cenários de 3 dedos para autonomia sem fios."),
        ("Estimativa de Ímãs N52 na Cut-Cell", "Adotou-se a cotação de 4 ímãs por dedo (pastilhas N52 5x1mm ou 5x3mm). Um único kit com 20 unidades adquirido no Mercado Livre Full (R$ 21,85) cobre plenamente os 3 dedos e fornece 8 ímãs sobressalentes para calibração."),
        ("Atuadores Vibrotáteis ERM", "Previsto 1 motor ERM coin (8x4mm) por dedo ativo + 1 unidade extra de reserva técnica em bancada. O motor deve ser encapsulado no dorso da falange para evitar interferência mecânica com o magnetômetro."),
        ("Recursos Próprios L-VIS (UnB)", "Protoboards de bancada, jumpers flexíveis de sinal, cabos micro-USB e resistores THT são supridos gratuitamente pela infraestrutura do Laboratório L-VIS (custo zero).")
    ]),
    ("2. ROTEIRO DE TRANSIÇÃO (1 DEDO ➔ 3 DEDOS)", [
        ("Reaproveitamento de Insumos", "Os pacotes de ímãs N52 (kit 20 un), resistores, conectores JST e filamento TPU adquiridos na Fase 1 atendem todos os 3 dedos. A transição de U1 para U3 requer apenas a compra dos sensores adicionais e do circuito de bateria."),
        ("Multiplexador TCA9548A", "O CI TLV493D-A1B6 suporta apenas 2 endereços I2C selecionáveis. O TCA9548A é indispensável na luva de 3 dedos para isolar os barramentos SDA/SCL de cada falange."),
        ("Acionamento por Transistor", "O MOSFET 2N7000 (TO-92) é empregado na montagem manual em perfboard, enquanto o AO3400A (SOT-23) é o padrão da PCB KiCad SMD, garantindo condução plena com sinal de 3,3V do ESP32.")
    ]),
    ("3. MAPEAMENTO LOGÍSTICO & FORNECEDORES PARA BRASÍLIA - DF", [
        ("Mercado Livre Full (CD Santa Maria/DF e Anápolis)", "Entrega em 24h a 48h úteis em Brasília. Ideal para compras de ímãs N52, filamento TPU 3D Fila, cola cianoacrilato e cabos de silicone."),
        ("RoboCore (Despacho Expresso Jadlog / Sedex)", "Prazo de 2 a 3 dias úteis para o DF. Fornecedor nacional homologado para o ESP32 DevKit V1, módulo SMD ESP32-WROOM-32U e baterias LiPo com proteção PCM."),
        ("Eletrogate (Despacho Sedex / Transportadora)", "Prazo de 2 a 4 dias úteis para o DF. Melhor opção nacional para o TP4056 USB-C, multiplexador TCA9548A, módulos MT3608 e placas perfuradas."),
        ("HU Infinito (Correios Sedex / PAC DF)", "Fornecedor exclusivo para o mini motor ERM 8x4mm com fio no Brasil. Entrega em Brasília de 3 a 5 dias úteis."),
        ("Lojas Físicas de Eletrônica em Brasília (Sem Frete)", "Comercial da W3 Sul (508 Sul / 708 Sul) e Feira dos Importados (SIA): transistores 2N7000, diodos 1N4148, resistores, protoboards e barras de pinos para reposição imediata de bancada.")
    ]),
    ("4. REGISTRO DE DECISÕES DE ENGENHARIA", [
        ("Conector USB-C no TP4056", "Padronizado conector Type-C moderno para simplificar a recarga da luva com cabos de smartphones comuns."),
        ("Fio Siliconado Ultra-flexível (28-30 AWG)", "Cabos comuns de cobre rígido quebram rapidamente com o movimento repetitivo das articulações dos dedos; o cabinho com capa de silicone é essencial para durabilidade da luva vestível."),
        ("Fixação dos Ímãs no TPU", "Utilização de cianoacrilato (Super Bonder) com pré-limpeza da cavidade impressa em 3D garante ancoragem permanente dos ímãs na cut-cell.")
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
        c_i = ns.cell(row_n, 1, f"• {tit_item}: ")
        c_i.font = F_BOLD
        c_i.alignment = Alignment(horizontal="left", vertical="center")
        
        ns.merge_cells(start_row=row_n, start_column=2, end_row=row_n, end_column=4)
        c_t = ns.cell(row_n, 2, txt_item)
        c_t.font = F_REGULAR
        c_t.alignment = ALIGN_LEFT
        row_n += 1
        
    row_n += 1

ns.column_dimensions["A"].width = 32
ns.column_dimensions["B"].width = 42
ns.column_dimensions["C"].width = 42
ns.column_dimensions["D"].width = 42

# Salvar Planilha Final
wb.save(OUT)
print(f"Planilha executiva v4.0 gerada com sucesso em: {OUT}")
