# 🧤 Luva Háptica L-VIS com Sensoriamento eFlesh

> **Projeto de Iniciação em Desenvolvimento Tecnológico e Inovação (PIBITI / PIBIT)**  
> **Laboratório**: L-VIS – Laboratório de Visualização, Interação e Simulação  
> **Instituição**: Universidade de Brasília (UnB)  
> **Desenvolvedor**: Artur Gonçalves ([@ArtEst777](https://github.com/ArtEst777))  

---

## 🎯 Visão Geral

Este projeto tem como objetivo o desenvolvimento de uma **luva háptica vestível de baixo custo com malha sensorial fechada (*closed-loop*)**, integrando:

1. **Sensoriamento Tátil Tridimensional (*eFlesh*)**: Pontas dos dedos instrumentadas com microestruturas elásticas flexíveis (*cut-cell*) impressas em 3D (TPU), ímãs de neodímio N52 e magnetômetros tridimensionais (Infineon TLV493D-A1B6). O sistema mede deformações mecânicas e estima forças normais e cisalhamento triaxial em tempo real.
2. **Feedback Vibrotátil Ativo**: Motores ERM (*coin*) acionados via modulação PWM por drivers MOSFET para sintetizar texturas, contato e pressão de preensão.
3. **Telemetria Sem Fio**: Microcontrolador ESP32 para aquisição via barramento I2C, controle dos motores e envio de dados sem fio (Wi-Fi / BLE) para aplicações em Realidade Virtual (Unity/Godot) e robótica.

---

## 🔬 Arquitetura do Sistema

```
                      ┌───────────────────────────────────────┐
                      │             USUÁRIO / OBJETO          │
                      └───────┬───────────────────────▲───────┘
          Toque / Compressão  │                       │ Vibração / Háptica
                              ▼                       │
                   ┌─────────────────────┐ ┌──────────┴──────────┐
                   │    eFlesh (TPU)     │ │   Atuadores ERM     │
                   │ + Ímã Neodímio N52  │ │   (8x4mm / 10mm)    │
                   └──────────┬──────────┘ └──────────▲──────────┘
             Variação de B    │                       │ Sinal PWM
                              ▼                       │
                   ┌─────────────────────┐ ┌──────────┴──────────┐
                   │  Infineon TLV493D   │ │   Drivers MOSFET    │
                   │  (Magnetômetro 3D)  │ │   (AO3400A / 2N7000)│
                   └──────────┬──────────┘ └──────────▲──────────┘
                     Barramento I2C                   │ GPIO PWM
                              │                       │
                      ┌───────▼───────────────────────┴───────┐
                      │          Microcontrolador ESP32       │
                      │       (Leitura, Regressão e PWM)      │
                      └───────────────────┬───────────────────┘
                                          │ Wi-Fi / Bluetooth
                                          ▼
                      ┌───────────────────────────────────────┐
                      │   Ambiente Virtual / ROS2 / Unity     │
                      └───────────────────────────────────────┘
```

---

## 📦 Estrutura do Repositório

```text
├── BOM/
│   └── BOM.xlsx                     # Lista técnica de materiais, custos e fornecedores
├── Datasheet/
│   └── infineon-tlv493d-...pdf       # Folha de dados do magnetômetro 3D Infineon
├── Domunetos e Artigos/             # Artigos de referência científica e teses correlatas
│   └── (Arquivos em PDF ignorados no Git para otimização de espaço)
├── .gitignore                       # Filtro de arquivos binários e temporários
└── README.md                        # Este documento
```

---

## 🛠️ Especificação de Hardware e Custos

Conforme detalhado no arquivo [`BOM/BOM.xlsx`](BOM/BOM.xlsx), foram planejadas opções modulares de montagem:

* **Sensoriamento**: Infineon TLV493D-A1B6 (TSOP-6 / Módulos Qwiic) + Ímãs N52 ($5\times 1\text{ mm}$ e $5\times 3\text{ mm}$).
* **Atuação Háptica**: Minimotores de vibração excêntrica tipo moeda (ERM 3V) + Transistores MOSFET AO3400A / 2N7000 + Diodos 1N4148.
* **Processamento**: ESP32 DevKit V1 / ESP32-WROOM-32U alimentado por célula Li-Ion 18650 ($3.7\text{ V}$).
* **Estrutura Mecânica**: Filamento TPU flexível 95A para impressão 3D das polpas digitais e suporte.

---

## 📚 Principais Referências

1. **eFlesh**: Pattabiraman et al., *eFlesh: Highly customizable Magnetic Touch Sensing using Cut-Cell Microstructures*, NYU (2024–2025).
2. **Regressão e Calibração eFlesh**: Barthel, Felix. *Entwicklung eines regressionsbasierten Modells zur Echtzeit-Kraftschätzung für den eFlesh-Taktilsensor*, HTWK Leipzig (2026).
3. **CyberGlove-HT**: Lopes, Élio. *CyberGlove para Interação com Ambientes Imersivos*, Instituto Politécnico de Tomar (2019).
4. **Simulação de Texturas Táteis**: De Brida, Leonardo. *Avaliação da eficácia de uma Luva Tátil em simulação de texturas*, UFSC (2024).

---

## 👨‍💻 Autor e Contato

* **Desenvolvedor**: Artur Gonçalves
* **GitHub**: [@ArtEst777](https://github.com/ArtEst777)
* **Laboratório**: [L-VIS - Laboratório de Visualização e Interação (UnB)](https://github.com/L-VIS)
