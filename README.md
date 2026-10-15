# 🧤 PIBIT — Miniaturização e Integração de Sensores Táteis Magnéticos eFlesh em uma Luva

> **Programa**: PIBIT (Iniciação em Desenvolvimento Tecnológico e Inovação)
> **Laboratório**: L-VIS — Laboratório de Visualização, Interação e Simulação (UnB)
> **Autor**: Artur Ferreira Gonçalves — Engenharia Mecatrônica, UnB ([@ArtEst777](https://github.com/ArtEst777))
> **Período**: 12 meses (início: Outubro/2026)
> **Fase atual**: Pré-prototipagem (Mês 1–2)

---

## 🎯 Objetivo

Miniaturizar, caracterizar e integrar sensores táteis magnéticos **eFlesh** (Pattabiraman et al.) em escala de ponta de dedo (**15×15×10 mm**), instalando-os nos dedos **polegar, indicador e médio** de uma luva, com **feedback vibrotátil no mundo real**.

O eFlesh original foi demonstrado em almofadas de 40×40 mm; a miniaturização para a ponta de um dedo humano (~15×15 mm) mantendo a sensibilidade, e a integração de três sensores em uma luva, ainda não foram relatadas.

---

## 🌍 Escopo do feedback: mundo real

Por limitação de tempo e de recursos, **esta fase do projeto não usa ROS2, Unity nem outra plataforma de RV**. A malha de feedback é **física e local**:

1. O usuário toca ou aperta um **objeto real**.
2. O eFlesh se deforma e o TLV493D mede a variação do campo magnético (ΔB).
3. O ESP32 estima a força (MLP, com regressão como alternativa) **no próprio microcontrolador**.
4. O ESP32 aciona o motor ERM correspondente com intensidade PWM proporcional à força, ao contato ou ao deslizamento.

Tarefas de validação: **aperto controlado**, **detecção de deslizamento** e **pinça fina** com objetos reais.

> **Integração futura (fora do escopo atual):** o firmware será modular, separando *aquisição → estimativa → atuação*, e o ESP32 mantém Wi-Fi/BLE disponíveis. Assim, uma etapa posterior poderá enviar os dados por UDP para Unity, ROS2 ou outro ambiente de RV sem refazer o hardware.

---

## 🔬 Arquitetura (fase atual)

```
          Objeto real
               │ toque / compressão
               ▼
 ┌──────────────────────────────┐       ┌──────────────────────────────┐
 │ eFlesh (TPU 95A, cut-cell)   │       │ Motor ERM 8×4 mm, 3 V        │
 │ + ímã N52 4,76×1,58 mm       │       │ no dorso do dedo / palma     │
 │   (alternativa: 5×3 mm)      │       │ (15–30 mm do sensor)         │
 └──────────────┬───────────────┘       └──────────────▲───────────────┘
                │ ΔB (Bx, By, Bz)                      │ vibração
                ▼                                      │
 ┌──────────────────────────────┐       ┌──────────────┴───────────────┐
 │ 3× TLV493D-A1B6 (breakout)   │       │ Driver MOSFET + diodo        │
 │ na lateral da falange distal │       │ flyback                      │
 └──────────────┬───────────────┘       └──────────────▲───────────────┘
                │ I2C                                  │ PWM
                ▼                                      │
 ┌──────────────────────────────┐                      │
 │ Multiplexador TCA9548A       │                      │
 │ (TLV493D: só 2 endereços)    │                      │
 └──────────────┬───────────────┘                      │
                ▼                                      │
 ┌─────────────────────────────────────────────────────┴───────┐
 │ ESP32 DevKit V1 (bancada) → ESP32-S3 Nano (luva final)      │
 │ leitura → baseline ΔB → estimativa de força → PWM           │
 └─────────────────────────────────────────────────────────────┘
                │
                ┆  (futuro) Wi-Fi / BLE → UDP → Unity / ROS2 / RV
```

---

## 🛠️ Decisões de engenharia principais

| Item | Decisão | Motivo |
| :--- | :--- | :--- |
| Sensor | TLV493D-A1B6 | Disponível em breakout, opera em 3,3 V, biblioteca consolidada |
| Barramento | TCA9548A | O TLV493D só tem 2 endereços I2C, insuficiente para 3 sensores |
| Ímã | N52 4,76×1,58 mm (ou 5×3 mm) | O 5×1 mm tem ~30% menos volume e pode não atingir o RMSE desejado |
| Atuador | ERM no dorso do dedo ou na palma | A 3 mm, o campo do ERM (5–20 mT) é comparável ao sinal do eFlesh (10–25 mT) |
| CAD | Cut-cell personalizada (Fusion 360 + Python) | A treliça de octeto padrão é rígida e isotrópica demais |
| Calibração | MLP (2 camadas, 128 neurônios) + regressão como alternativa | Não linearidade (1/d³), acoplamento entre eixos e deriva térmica |
| Feedback | Mundo real, malha local no ESP32 | Tempo e recursos; integração com RV fica para etapa futura |
| PCB | Breakouts agora, PCB própria (KiCad) depois | Restrição orçamentária para fabricar e montar SMD |

A análise completa está em [`docs/PROJETO_PIBIT.md`](docs/PROJETO_PIBIT.md).

---

## 📦 Estrutura do repositório

```text
├── BOM/
│   └── BOM.xlsx            # Lista de materiais e custos
├── Datasheet/              # Datasheets (PDFs não versionados)
├── Domunetos e Artigos/    # Referências (PDFs não versionados)
├── docs/
│   └── PROJETO_PIBIT.md    # Documento detalhado do projeto
├── .gitignore
└── README.md
```

---

## 🗺️ Próximos passos

1. Finalizar as correções do relatório técnico (14 pendentes)
2. Comprar os materiais do teste de 1 dedo
3. Recriar a cut-cell no Fusion 360
4. Montar o circuito na protoboard
5. Validar a leitura do sensor (baseline e ΔB)
6. Testar a interferência do ERM em função da distância
7. Integrar o sensor no dedo, com feedback vibrotátil local

---

## 📚 Referências principais

- PATTABIRAMAN, V. et al. *eFlesh: Highly customizable Magnetic Touch Sensing using Cut-Cell Microstructures*. arXiv:2506.09994, 2025.
- TOZONI, D. et al. *Cut-cell microstructures for two-scale structural optimization*. Computer Graphics Forum, 2024.
- BHIRANGI, R. et al. *AnySkin: Versatile and replaceable tactile skin*. CoRL, 2024.
- BARTHEL, F. *Entwicklung eines regressionsbasierten Modells zur Echtzeit-Kraftschätzung für den eFlesh-Taktilsensor*. HTWK Leipzig, 2026.
- INFINEON. *TLV493D-A1B6 3D Magnetic Sensor Datasheet*.
