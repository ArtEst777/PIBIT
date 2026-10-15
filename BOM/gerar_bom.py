"""Gera BOM/BOM.xlsx do projeto PIBIT com 4 cenários de montagem.

Cenários:
  U1 = Placa universal, 1 dedo (início / bancada)
  U3 = Placa universal, 3 dedos (objetivo final)
  P1 = PCB customizada, 1 dedo
  P3 = PCB customizada, 3 dedos
"""
import math
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = sys.argv[1] if len(sys.argv) > 1 else "BOM.xlsx"
TAXA_USD = 5.60

COMPRAR = "Comprar"
LVIS = "L-VIS (grátis)"
LVIS_CONF = "L-VIS (confirmar)"
ALT = "Alternativa (fora do total)"
COTADO = "Cotado"
ESTIMADO = "Estimado"

# (categoria, componente, modelo, fornecedor, preco_pacote, moeda, unid_pacote,
#  origem, U1, U3, P1, P3, confianca, notas, link)
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
     "Versão PCB. Tamanho do pacote (50 un.) a confirmar.",
     "https://lista.mercadolivre.com.br/ao3400a-sot-23"),
    ("2. Atuação háptica", "Diodo de sinal 1N4148 (THT, kit 200 un.) — flyback",
     "1N4148", "Mercado Livre", 22.00, "BRL", 200, COMPRAR, 1, 3, 0, 0, COTADO,
     "Versão manual. Em antiparalelo com cada motor.",
     "https://www.mercadolivre.com.br/diodo-de-sinal-1n4148-kit-200-pecas/p/MLB2072206267"),
    ("2. Atuação háptica", "Diodo de sinal 1N4148W (SOD-123, SMD) — flyback",
     "1N4148W", "Mercado Livre / AliExpress", 15.00, "BRL", 100, COMPRAR, 0, 0, 1, 3, ESTIMADO,
     "Versão PCB.",
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
     "Fase 1 (bancada, 1 dedo). Alimentada pelo USB.",
     "https://www.robocore.net/wifi/esp32-wifi-bluetooth"),
    ("3. Processamento e alimentação", "Placa ESP32-S3 Nano (compacta, dual-core LX7)",
     "ESP32-S3 Nano", "A definir", 90.00, "BRL", 1, COMPRAR, 0, 1, 0, 1, ESTIMADO,
     "Fase 2 (luva, 3 dedos). Preço varia muito por fabricante (Waveshare x Arduino).",
     ""),
    ("3. Processamento e alimentação", "Bateria Li-Ion 18650, 3,7 V, recarregável",
     "BATVTRLIPO3V7", "HU Infinito", 13.40, "BRL", 1, COMPRAR, 0, 1, 0, 1, COTADO,
     "Só na luva (3 dedos); a bancada usa USB.",
     "https://www.huinfinito.com.br/module/iqitsearch/searchiqit?s=BATERIA+L%C3%8DTIO+3%2C7V+%2818650+-+RECARREG%C3%81VEL%29"),
    ("3. Processamento e alimentação", "Suporte para 1 bateria 18650",
     "BATPLIPO3V701", "HU Infinito", 3.90, "BRL", 1, COMPRAR, 0, 1, 0, 1, COTADO,
     "Só suporte mecânico; não carrega nem protege a bateria.",
     "https://www.huinfinito.com.br/baterias-acessorios/1356-suporte-01-bateria-litio-37v-18650-canoa-preto.html"),
    ("3. Processamento e alimentação", "Módulo carregador TP4056 com proteção (USB-C)",
     "TP4056", "Mercado Livre / AliExpress", 8.00, "BRL", 1, COMPRAR, 0, 1, 0, 1, ESTIMADO,
     "Carga e proteção contra sobrecarga/descarga da 18650.",
     ""),
    ("3. Processamento e alimentação", "Módulo elevador de tensão (boost) 5 V, ex.: MT3608",
     "MT3608", "Mercado Livre / AliExpress", 8.00, "BRL", 1, COMPRAR, 0, 1, 0, 1, ESTIMADO,
     "Gera 5 V estáveis para a placa a partir da bateria (3,0–4,2 V).",
     ""),

    # 4. Montagem e interconexão
    ("4. Montagem e interconexão", "Placa de circuito universal (perfurada), ~5×7 cm",
     "Perfboard", "Mercado Livre / loja local", 10.00, "BRL", 1, COMPRAR, 1, 2, 0, 0, ESTIMADO,
     "Versão manual. Verificar se há no L-VIS.",
     ""),
    ("4. Montagem e interconexão", "Fabricação de PCB (lote mínimo 5 un., com frete e impostos)",
     "PCB 2 camadas", "JLCPCB / PCBWay", 120.00, "BRL", 1, COMPRAR, 0, 0, 1, 1, ESTIMADO,
     "Versão PCB. Um lote de 5 placas atende 1 ou 3 dedos. Projeto no KiCad.",
     ""),
    ("4. Montagem e interconexão", "Capacitor cerâmico SMD 0805 100 nF (kit 100 un.)",
     "0805 100 nF", "Mercado Livre", 19.00, "BRL", 100, COMPRAR, 0, 0, 1, 1, COTADO,
     "Versão PCB. Desacoplamento de cada CI.",
     "https://www.mercadolivre.com.br/100x-capacitor-multicamada-smd-100nf-50v-10-x7r-0805/p/MLB47645304"),
    ("4. Montagem e interconexão", "Capacitor cerâmico THT 100 nF",
     "100 nF THT", "L-VIS", 0.00, "BRL", 1, LVIS_CONF, 2, 4, 0, 0, ESTIMADO,
     "Versão manual. Desacoplamento junto aos módulos.",
     ""),
    ("4. Montagem e interconexão", "Barra de pinos macho 1×40, 2,54 mm",
     "Barra 1×40", "HU Infinito", 3.58, "BRL", 1, COMPRAR, 1, 2, 1, 2, COTADO,
     "",
     "https://www.huinfinito.com.br/conectores/734-conector-barra-de-pinos-macho-1x40x20-180-graus.html"),
    ("4. Montagem e interconexão", "Conector JST macho/fêmea (kit 10 pares)",
     "JST", "Mercado Livre", 28.90, "BRL", 10, COMPRAR, 0, 4, 2, 4, COTADO,
     "Ligação destacável entre a placa do pulso e os dedos. Na bancada com 1 dedo, jumpers bastam.",
     "https://www.mercadolivre.com.br/plug-conector-jst-da-bateria-lipo-10-pares-macho-e-femea/p/MLB2081705943"),
    ("4. Montagem e interconexão", "Fio flexível fino (cabinho 26–30 AWG, várias cores)",
     "Cabinho 28 AWG", "Mercado Livre / loja local", 15.00, "BRL", 1, COMPRAR, 1, 1, 1, 1, ESTIMADO,
     "Fiação até as pontas dos dedos; precisa ser flexível para não romper.",
     ""),
    ("4. Montagem e interconexão", "Protoboard, jumpers e cabo USB",
     "—", "L-VIS", 0.00, "BRL", 1, LVIS, 1, 1, 1, 1, COTADO,
     "Disponível no laboratório.",
     ""),

    # 5. Fabricação mecânica
    ("5. Fabricação mecânica", "Filamento TPU 95A flexível 1,75 mm, 1 kg",
     "TPU 95A", "L-VIS", 149.00, "BRL", 1, LVIS, 1, 1, 1, 1, COTADO,
     "Disponível no L-VIS (preço só como referência). Impressão do eFlesh.",
     "https://www.mercadolivre.com.br/filamento-tpu-flexivel-175mm-1kg-para-impressora-3d-cor-natural-transparente/p/MLB64157424"),
    ("5. Fabricação mecânica", "Luva base e case impresso (PLA) para a eletrônica",
     "—", "L-VIS", 0.00, "BRL", 1, LVIS_CONF, 1, 1, 1, 1, ESTIMADO,
     "Reaproveita a luva do projeto LVIS; case impresso no laboratório.",
     ""),
]

CENARIOS = [
    ("U1", "Placa universal — 1 dedo", "Início: validação em bancada (ESP32 DevKit, USB)"),
    ("U3", "Placa universal — 3 dedos", "Objetivo final, montagem manual (ESP32-S3 Nano, bateria)"),
    ("P1", "PCB customizada — 1 dedo", "Início com PCB própria do dedo (KiCad)"),
    ("P3", "PCB customizada — 3 dedos", "Objetivo final com PCB própria"),
]

# ---------- estilos ----------
AZUL = PatternFill("solid", fgColor="1F4E78")
AZUL_CLARO = PatternFill("solid", fgColor="DDEBF7")
CINZA = PatternFill("solid", fgColor="F2F2F2")
AMARELO = PatternFill("solid", fgColor="FFF2CC")
VERDE = PatternFill("solid", fgColor="E2EFDA")
BRANCO_B = Font(bold=True, color="FFFFFF")
NEGRITO = Font(bold=True)
FINA = Side(style="thin", color="BFBFBF")
BORDA = Border(left=FINA, right=FINA, top=FINA, bottom=FINA)
BRL = '"R$" #,##0.00'
QUEBRA = Alignment(wrap_text=True, vertical="top")
CENTRO = Alignment(horizontal="center", vertical="top", wrap_text=True)

wb = Workbook()

# ================= Aba Componentes =================
ws = wb.active
ws.title = "Componentes"

cab = ["ID", "Categoria", "Componente", "Modelo / Part Number", "Fornecedor",
       "Preço do pacote (orig.)", "Moeda", "Unid. por pacote", "Preço do pacote (R$)",
       "Origem", "Qtd U1", "Qtd U3", "Qtd P1", "Qtd P3",
       "Custo U1 (R$)", "Custo U3 (R$)", "Custo P1 (R$)", "Custo P3 (R$)",
       "Preço", "Notas", "Link"]
ws.append(["BOM — PIBIT eFlesh: lista de componentes por cenário"])
ws["A1"].font = Font(bold=True, size=14)
ws.append(["Qtd = unidades necessárias. Custo = pacotes necessários × preço do pacote, só para itens com Origem = \"Comprar\". "
           "Linhas amarelas = preço estimado (confirmar). Taxa USD na aba Resumo."])
ws.merge_cells("A2:U2")
ws["A2"].alignment = QUEBRA
ws.row_dimensions[2].height = 30
ws.append(cab)
HDR = 3
for c in range(1, len(cab) + 1):
    cell = ws.cell(HDR, c)
    cell.fill = AZUL
    cell.font = BRANCO_B
    cell.alignment = CENTRO
    cell.border = BORDA

primeira = HDR + 1
for i, it in enumerate(ITENS):
    (cat, comp, mod, forn, preco, moeda, unid, origem, u1, u3, p1, p3, conf, notas, link) = it
    r = primeira + i
    ws.cell(r, 1, i + 1)
    ws.cell(r, 2, cat)
    ws.cell(r, 3, comp)
    ws.cell(r, 4, mod)
    ws.cell(r, 5, forn)
    ws.cell(r, 6, preco)
    ws.cell(r, 7, moeda)
    ws.cell(r, 8, unid)
    ws.cell(r, 9, f'=IF(G{r}="USD",F{r}*Resumo!$C$4,F{r})')
    ws.cell(r, 10, origem)
    for j, q in enumerate((u1, u3, p1, p3)):
        ws.cell(r, 11 + j, q)
        qcol = get_column_letter(11 + j)
        ws.cell(r, 15 + j,
                f'=IF(AND($J{r}="{COMPRAR}",{qcol}{r}>0),ROUNDUP({qcol}{r}/$H{r},0)*$I{r},0)')
    ws.cell(r, 19, conf)
    ws.cell(r, 20, notas)
    ws.cell(r, 21, link)
    if link:
        ws.cell(r, 21).hyperlink = link
        ws.cell(r, 21).font = Font(color="0563C1", underline="single")

    fill = AMARELO if conf == ESTIMADO else (CINZA if origem != COMPRAR else None)
    for c in range(1, len(cab) + 1):
        cell = ws.cell(r, c)
        cell.border = BORDA
        cell.alignment = CENTRO if c in (1, 7, 8, 10, 11, 12, 13, 14, 19) else QUEBRA
        if fill:
            cell.fill = fill
    for c in (6,):
        ws.cell(r, c).number_format = '#,##0.00'
    for c in (9, 15, 16, 17, 18):
        ws.cell(r, c).number_format = BRL

ultima = primeira + len(ITENS) - 1
rt = ultima + 1
ws.cell(rt, 3, "TOTAL (sem frete)").font = NEGRITO
for j in range(4):
    col = get_column_letter(15 + j)
    c = ws.cell(rt, 15 + j, f"=SUM({col}{primeira}:{col}{ultima})")
    c.number_format = BRL
    c.font = NEGRITO
for c in range(1, len(cab) + 1):
    ws.cell(rt, c).fill = AZUL_CLARO
    ws.cell(rt, c).border = BORDA

dv = DataValidation(type="list", formula1=f'"{COMPRAR},{LVIS},{LVIS_CONF},{ALT}"', allow_blank=False)
ws.add_data_validation(dv)
dv.add(f"J{primeira}:J{ultima}")
dv2 = DataValidation(type="list", formula1=f'"{COTADO},{ESTIMADO}"', allow_blank=False)
ws.add_data_validation(dv2)
dv2.add(f"S{primeira}:S{ultima}")

larguras = [5, 20, 42, 18, 20, 12, 8, 10, 13, 16, 7, 7, 7, 7, 12, 12, 12, 12, 10, 50, 40]
for i, w in enumerate(larguras, 1):
    ws.column_dimensions[get_column_letter(i)].width = w
ws.freeze_panes = ws.cell(HDR + 1, 4)
ws.auto_filter.ref = f"A{HDR}:U{ultima}"

# ================= Aba Resumo =================
rs = wb.create_sheet("Resumo", 0)
rs["A1"] = "BOM — PIBIT eFlesh: resumo de custos"
rs["A1"].font = Font(bold=True, size=14)
rs["A2"] = "Valores sem frete e sem impostos de importação (exceto a fabricação de PCB, que já os inclui na estimativa)."
rs["A2"].font = Font(italic=True)
rs["A4"] = "Taxa de câmbio"
rs["B4"] = "R$ / US$ (editável)"
rs["C4"] = TAXA_USD
rs["C4"].fill = AMARELO
rs["C4"].number_format = '#,##0.00'
rs["A4"].font = NEGRITO

rs.append([])
cab_r = ["Cenário", "Descrição", "Uso", "Total (R$)", "Itens com preço estimado (R$)", "Itens cotados (R$)"]
rs.append(cab_r)
hr = rs.max_row
for c in range(1, len(cab_r) + 1):
    cell = rs.cell(hr, c)
    cell.fill = AZUL
    cell.font = BRANCO_B
    cell.alignment = CENTRO
    cell.border = BORDA

rng = lambda col: f"Componentes!${col}${primeira}:${col}${ultima}"
for k, (cod, nome, uso) in enumerate(CENARIOS):
    r = hr + 1 + k
    col = get_column_letter(15 + k)
    rs.cell(r, 1, cod)
    rs.cell(r, 2, nome)
    rs.cell(r, 3, uso)
    rs.cell(r, 4, f"=SUM({rng(col)})")
    rs.cell(r, 5, f'=SUMIF({rng("S")},"{ESTIMADO}",{rng(col)})')
    rs.cell(r, 6, f"=D{r}-E{r}")
    for c in range(1, 7):
        rs.cell(r, c).border = BORDA
        rs.cell(r, c).alignment = QUEBRA
    for c in (4, 5, 6):
        rs.cell(r, c).number_format = BRL
    rs.cell(r, 4).font = NEGRITO
    rs.cell(r, 4).fill = VERDE

# custo por categoria
rs.append([])
rs.append(["Custo por categoria"])
rs.cell(rs.max_row, 1).font = Font(bold=True, size=12)
rs.append(["Categoria", "", "", "U1 (R$)", "U3 (R$)", "P1 (R$)", "P3 (R$)"])
hc = rs.max_row
for c in range(1, 8):
    cell = rs.cell(hc, c)
    cell.fill = AZUL
    cell.font = BRANCO_B
    cell.alignment = CENTRO
    cell.border = BORDA
cats = []
for it in ITENS:
    if it[0] not in cats:
        cats.append(it[0])
for k, cat in enumerate(cats):
    r = hc + 1 + k
    rs.cell(r, 1, cat)
    rs.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
    for j in range(4):
        col = get_column_letter(15 + j)
        c = rs.cell(r, 4 + j, f'=SUMIF({rng("B")},$A{r},{rng(col)})')
        c.number_format = BRL
    for c in range(1, 8):
        rs.cell(r, c).border = BORDA

rs.append([])
rs.append(["Como ler"])
rs.cell(rs.max_row, 1).font = Font(bold=True, size=12)
for linha in [
    "• Placa universal = montagem manual com módulos breakout soldados em placa perfurada.",
    "• PCB customizada = CI TLV493D SMD e componentes 0805/SOT-23 em placa própria do dedo (KiCad).",
    "• 1 dedo = início do projeto (bancada). 3 dedos = objetivo final (polegar, indicador, médio).",
    "• Itens do L-VIS e alternativas aparecem na lista, mas não entram no total.",
    "• Kits (ímãs, diodos, MOSFETs) são comprados por pacote: um pacote pode atender vários cenários.",
    "• Quem já comprou o cenário de 1 dedo não paga o total de 3 dedos de novo: veja a aba Notas.",
]:
    rs.append([linha])

for col, w in zip("ABCDEFG", [12, 28, 52, 14, 18, 14, 14]):
    rs.column_dimensions[col].width = w

# ================= Aba Notas =================
ns = wb.create_sheet("Notas")
ns["A1"] = "Notas, premissas e pendências"
ns["A1"].font = Font(bold=True, size=14)
notas = [
    ("Premissas", ""),
    ("", "Bancada (1 dedo) é alimentada pelo USB; bateria, carregador e boost só entram nos cenários de 3 dedos."),
    ("", "Quantidade de ímãs por dedo (4) é provisória; depende do CAD da cut-cell miniaturizada."),
    ("", "Motores ERM: 1 por dedo + 1 de reserva."),
    ("", "TPU, resistores THT, protoboard, jumpers e cabos USB são do L-VIS (custo zero)."),
    ("", "Frete não incluído. AliExpress/DigiKey podem ter taxa de importação."),
    ("Evolução de 1 para 3 dedos", ""),
    ("", "Passar de U1 para U3 reaproveita kits já comprados (ímãs, 2N7000, 1N4148). O custo incremental é menor que a diferença dos totais."),
    ("", "O ESP32 DevKit (bancada) continua útil para testes depois que a luva usar o ESP32-S3 Nano."),
    ("Pendências", ""),
    ("", "Confirmar preços estimados (linhas amarelas): TCA9548A, AO3400A, 1N4148W, kit 0805, ESP32-S3 Nano, TP4056, MT3608, placa universal, PCB, fio."),
    ("", "Definir modelo exato do ESP32-S3 Nano (Waveshare, Arduino Nano ESP32 etc.)."),
    ("", "Validar o 2N7000 com gate em 3,3 V; se não conduzir bem, usar AO3400A em adaptador SOT-23 ou transistor BJT (BC337/2N2222)."),
    ("", "Kit de motores Vibracall 10 mm (5 un.) já em estoque pode servir de reserva para os primeiros testes."),
    ("Mudanças em relação à BOM anterior", ""),
    ("", "Removido módulo IRF520: não é de nível lógico e conduz mal com 3,3 V do ESP32."),
    ("", "Removido ímã 5×1 mm: volume ~30% menor, sensibilidade possivelmente insuficiente (ver docs/PROJETO_PIBIT.md)."),
    ("", "Removidos motor JYC0820FL e ESP32-WROOM-32U (opcionais sem uso no plano atual)."),
    ("", "Adicionados TCA9548A, ESP32-S3 Nano, carregador TP4056, boost 5 V, placa universal, fabricação de PCB e fio flexível."),
    ("", "Corrigida a nota do suporte 18650: ele não é carregador nem tem proteção."),
]
for a, b in notas:
    ns.append([a, b])
    r = ns.max_row
    if a:
        ns.cell(r, 1).font = Font(bold=True, size=12)
    ns.cell(r, 2).alignment = QUEBRA
ns.column_dimensions["A"].width = 30
ns.column_dimensions["B"].width = 120

wb.save(OUT)

# ---------- totais calculados em Python (para conferência) ----------
tot = [0.0] * 4
est = [0.0] * 4
for it in ITENS:
    preco, moeda, unid, origem = it[4], it[5], it[6], it[7]
    if origem != COMPRAR:
        continue
    pbrl = preco * TAXA_USD if moeda == "USD" else preco
    for j, q in enumerate(it[8:12]):
        if q > 0:
            v = math.ceil(q / unid) * pbrl
            tot[j] += v
            if it[12] == ESTIMADO:
                est[j] += v
for (cod, nome, _), t, e in zip(CENARIOS, tot, est):
    print(f"{cod} {nome:28s} total R$ {t:8.2f}  (estimado R$ {e:7.2f})")
