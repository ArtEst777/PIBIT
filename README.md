# 🧤 PIBIT — Miniaturização e Integração de Sensores Táteis Magnéticos eFlesh em uma Luva

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Instituição: UnB](https://img.shields.io/badge/Institui%C3%A7%C3%A3o-UnB-green.svg)](https://unb.br/)
[![Laboratório: L--VIS](https://img.shields.io/badge/Laborat%C3%B3rio-L--VIS-purple.svg)](https://github.com/L-VIS)

> *Título provisório — o nome definitivo ainda será escolhido.*
>
> **Programa**: PIBIT (Iniciação em Desenvolvimento Tecnológico e Inovação)  
> **Laboratório**: L-VIS — Laboratório de Visualização, Interação e Simulação  
> **Instituição**: Universidade de Brasília (UnB)  
> **Autor**: Artur Ferreira Gonçalves — Engenharia Mecatrônica, UnB ([@ArtEst777](https://github.com/ArtEst777))  
> **Orientador**: Prof. Dr. Felix  
> **Período**: 12 meses (início: Julho/2026)  
> **Fase atual**: Pré-prototipagem (Mês 1–2)  

---

## 🎯 Objetivo

Miniaturizar, caracterizar e integrar sensores táteis magnéticos **eFlesh** (Pattabiraman et al., NYU) em escala de ponta de dedo (**15×15×10 mm**), instalando-os nos dedos **polegar, indicador e médio** de uma luva vestível, com **feedback vibrotátil local no mundo real**.

O eFlesh original foi demonstrado em almofadas de 40×40 mm; a miniaturização para a escala anatômica de uma polpa digital humana (~15×15 mm) mantendo a sensibilidade e a integração de três sensores numa luva vestível constituem a lacuna tecnológica e a contribuição central deste projeto.

---

## 🌍 Escopo do Feedback: Mundo Real

Por restrição de tempo e recursos na fase atual, **o projeto não utiliza ROS2, Unity nem outras plataformas de RV**. A malha de sensoriamento e controle é **física, embarcada e local**:

1. O usuário toca ou aperta um **objeto real**.
2. A microestrutura de TPU 95A (*cut-cell*) do eFlesh se deforma, deslocando o ímã de neodímio N52.
3. O magnetômetro 3D Infineon TLV493D mede a variação tridimensional do campo magnético ($\Delta B_x, \Delta B_y, \Delta B_z$).
4. O microcontrolador ESP32 estima a força em tempo real (via MLP com regressão polinomial como alternativa rápida).
5. O ESP32 aciona o motor vibrotátil ERM correspondente via PWM com intensidade proporcional à força de aperto ou deslizamento.

Tarefas de validação: **aperto controlado**, **detecção de deslizamento** e **pinça fina** com objetos reais.

> **Preparação para integração futura:** A arquitetura do firmware é estritamente modular (*aquisição → estimativa de força → atuação háptica*), preservando as interfaces de rede sem fio (Wi-Fi e BLE) do ESP32 para transmissão de dados via UDP para Unity, ROS2 ou motores de Realidade Virtual em etapas futuras.

---

## 🔬 Arquitetura do Sistema

```
                        OBJETO REAL
                             │ toque / compressão mecânica
                             ▼
 ┌──────────────────────────────────────────────┐       ┌──────────────────────────────┐
 │       eFlesh Miniaturizado (TPU 95A)         │       │    Motor ERM 8×4 mm (3 V)    │
 │       + Ímã N52 4,76×1,58 mm (ou 5×3 mm)     │       │  no dorso do dedo ou palma   │
 └──────────────────────┬───────────────────────┘       │    (15–30 mm do sensor)      │
                        │ ΔB (Bx, By, Bz)               └──────────────▲───────────────┘
                        ▼                                              │ vibração háptica
 ┌──────────────────────────────────────────────┐                      │
 │ 3× TLV493D-A1B6 (na lateral da falange)      │       ┌──────────────┴───────────────┐
 └──────────────────────┬───────────────────────┘       │    Driver MOSFET + Diodo     │
                        │ Barramento I2C                │    Flyback 1N4148            │
                        ▼                               └──────────────▲───────────────┘
 ┌──────────────────────────────────────────────┐                      │ GPIO PWM
 │  Multiplexador I2C TCA9548A                  │                      │
 │  (Necessário: TLV493D possui só 2 endereços) │                      │
 └──────────────────────┬───────────────────────┘                      │
                        ▼                                              │
 ┌─────────────────────────────────────────────────────────────────────┴───────────────┐
 │ Microcontrolador ESP32 DevKit V1 (bancada) ➔ ESP32-S3 Nano (luva final)             │
 │ Pipeline: Leitura I2C ➔ Subtração de Baseline ➔ Estimativa de Força ➔ Modulação PWM │
 └─────────────────────────────────────────────────────────────────────────────────────┘
                        │
                        ┆ (Futura Expansão) Telemetria Wi-Fi / BLE ➔ UDP ➔ Unity / ROS2
```

---

## 🛠️ Decisões de Engenharia Principais

| Item | Decisão | Justificativa Técnica |
| :--- | :--- | :--- |
| **Sensor Magnético** | TLV493D-A1B6 | Ampla disponibilidade em breakout, 3,3 V nativo, biblioteca consolidada |
| **Comunicação I2C** | TCA9548A | O TLV493D tem apenas 2 endereços configuráveis; 3 dedos exigem multiplexação |
| **Ímãs de Neodímio** | N52 4,76×1,58 mm (ou 5×3 mm) | O modelo 5×1 mm tem 30% menos volume; 4,76×1,58 mm é o padrão do artigo original |
| **Atuador Háptico** | ERM no dorso ou palma | A 3 mm, o motor gera 5–20 mT (ruído crítico no eFlesh); a 15–30 mm o ruído cai drasticamente |
| **Modelagem CAD** | Cut-cell personalizada | A treliça de octeto padrão é rígida demais; a cut-cell permite compressão controlada |
| **Algoritmo de Força**| MLP (2×128 nós) + Regressão | MLP lida com acoplamento não-linear (1/d³); regressão de 2º grau (Barthel) é alternativa rápida |
| **Feedback** | Mundo real (malha local) | Foco em viabilidade e entrega robusta dentro do prazo do PIBIT |
| **Eletrônica** | Breakouts ➔ PCB KiCad | Breakouts na bancada inicial; PCB customizada projetada em KiCad para a luva final |

---

## 💰 Custos por Cenário ([BOM/BOM.xlsx](BOM/BOM.xlsx))

A lista de materiais foi detalhada em 4 cenários com fórmulas automáticas por pacote (sem frete):

| Cenário | 1 Dedo (Bancada Inicial) | 3 Dedos (Luva Completa) |
| :--- | :---: | :---: |
| **Placa Universal** (Montagem Manual com Breakouts) | **R$ 195,07** | **R$ 421,73** |
| **PCB Customizada** (Placa Própria KiCad com TLV493D SMD) | **R$ 338,14** | **R$ 472,08** |

*Valores detalhados na planilha [`BOM/BOM.xlsx`](BOM/BOM.xlsx). Para recalcular a planilha com novos preços: `py BOM/gerar_bom.py BOM/BOM.xlsx`.*

---

## 📦 Estrutura do Repositório e Documentos

```text
├── BOM/
│   ├── BOM.xlsx                                            # Planilha orçamentária executiva (4 cenários e fórmulas)
│   └── gerar_bom.py                                        # Script gerador da planilha BOM com validação automática
├── Datasheet/
│   └── infineon-tlv493d-a1b6-datasheet-en.pdf              # Datasheet do sensor magnético 3D TLV493D
├── docs/
│   ├── PROJETO_PIBIT.md                                    # Proposta técnica e registro detalhado de decisões
│   ├── Catalogo_Fontes_PIBIT.xlsx                          # Catálogo com 99 fontes bibliográficas categorizadas
│   ├── Revisão Bibliográfica — eFlesh miniaturizado...pdf   # Síntese bibliográfica e funil temático (13 páginas)
│   └── Roteiro de estudo MLP para o PIBIT.pdf              # Roteiro de capacitação em 4 semanas (MLP e regressão)
├── src/                                                    # Código-fonte e testes de bancada (disponível também como scr/)
│   ├── Sensor_ERM/                                         # Testes do atuador vibrotátil ERM via PWM
│   │   ├── test_erm_pwm.ino                                # Firmware de teste (rampas e padrões hápticos)
│   │   └── README.md                                       # Circuito do driver MOSFET e precauções
│   └── Sensor_Magnetometro/                                # Testes do magnetômetro 3D TLV493D
│       ├── test_tlv493d_i2c.ino                            # Firmware de streaming triaxial e baseline ΔB
│       └── README.md                                       # Pinagem I2C e visualização no Serial Plotter
├── pibit-latex/                                            # Modelo oficial do relatório final em LaTeX (padrão ABNT / UnB)
│   ├── main.tex                                            # Arquivo mestre do relatório (configurações e cabeçalho)
│   ├── preambulo.tex                                       # Pacotes, formatação ABNT, Arial 12 e regras tipográficas
│   ├── referencias.bib                                     # Base de dados bibliográfica BibTeX com fontes verificadas
│   ├── siglas.tex                                          # Lista dinâmica de abreviaturas e siglas (pacote acro)
│   ├── secoes/                                             # Capítulos do relatório (00-resumo a 08-apêndices)
│   └── LEIAME.md                                           # Guia de compilação no Overleaf e orientações de escrita
├── Domunetos e Artigos/                                    # Teses e artigos de apoio (PDFs pesados ignorados no Git)
├── .gitignore                                              # Proteção contra binários pesados e temporários
├── LICENSE                                                 # Licença MIT
└── README.md                                               # Este documento
```

---

## 📚 Documentos de Pesquisa e Referências

### Documentos Internos do Projeto ([`docs/`](docs/))
* [`docs/Catalogo_Fontes_PIBIT.xlsx`](docs/Catalogo_Fontes_PIBIT.xlsx): Base bibliográfica com **99 fontes** indexadas por tema, categoria (artigos, teses, datasheets, códigos abertos) e prioridade de leitura.
* [`docs/Revisão Bibliográfica — eFlesh miniaturizado para luva de RV.pdf`](docs/Revisão%20Bibliogr%C3%A1fica%20%E2%80%94%20eFlesh%20miniaturizado%20para%20luva%20de%20RV.pdf): Revisão crítica da evolução *ReSkin ➔ AnySkin ➔ eFlesh*, análise de microestruturas cut-cell, compensação de drift térmico e debate entre redes neurais MLP vs. regressão de 2º grau.
* [`docs/Roteiro de estudo MLP para o PIBIT.pdf`](docs/Roteiro%20de%20estudo%20MLP%20para%20o%20PIBIT.pdf): Roteiro de estudos práticos em 4 semanas para implementação de modelos de força no ESP32.

### Repositório Oficial do eFlesh
* Código-fonte, modelos e dados públicos da NYU: [github.com/notvenky/eFlesh](https://github.com/notvenky/eFlesh)

### Artigos Fundamentais
* **eFlesh**: Pattabiraman et al., *eFlesh: Highly customizable Magnetic Touch Sensing using Cut-Cell Microstructures*, NYU (2025). [arXiv:2506.09994](https://arxiv.org/abs/2506.09994).
* **Cut-Cells**: Tozoni, D. et al., *Cut-cell microstructures for two-scale structural optimization*, Computer Graphics Forum, v. 43, n. 5 (2024).
* **AnySkin**: Bhirangi, R. et al., *AnySkin: Versatile and replaceable tactile skin*, CoRL (2024).
* **Regressão eFlesh**: Barthel, Felix, *Entwicklung eines regressionsbasierten Modells zur Echtzeit-Kraftschätzung für den eFlesh-Taktilsensor*, HTWK Leipzig (2026).

---

## 👥 Equipe e Orientação

* **Pesquisador**: Artur Ferreira Gonçalves — Graduando em Engenharia Mecatrônica ([@ArtEst777](https://github.com/ArtEst777))
* **Orientador**: Prof. Dr. Felix — Universidade de Brasília (UnB)
* **Laboratório**: L-VIS — Laboratório de Visualização, Interação e Simulação (UnB)
* **Colaboração e Pesquisa**: Igor Rafael de Carvalho Oliveira (autor do roteiro de estudo e catálogo de fontes)

---

## 📄 Licença

Este projeto é disponibilizado sob a licença **MIT**. Consulte o arquivo [`LICENSE`](LICENSE) para mais detalhes.
