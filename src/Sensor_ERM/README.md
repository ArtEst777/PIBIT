# 📳 Módulo de Atuação Háptica: Sensor_ERM

Esta pasta contém o firmware de teste e documentação de integração dos atuadores vibrotáteis **ERM Coin (8×4 mm e 10 mm, 3 V)** para feedback sensorial no mundo real.

---

## 🔌 Esquemático do Circuito Driver (MOSFET Canal N)

Como o microcontrolador ESP32 opera com sinais de controle em 3,3 V e corrente máxima por GPIO de apenas ~12 a 20 mA, os motores ERM (que consomem de 50 a 90 mA) **não podem** ser ligados diretamente no pino do ESP32.

Utiliza-se uma topologia de chaveamento *Low-Side* com transistor MOSFET:

```text
       VCC (+3.3V ou Bateria 3.7V)
                  │
                  ├───┐
                  │   │
              [Motor ERM] [Diodo 1N4148] (Cátodo/faixa no VCC)
                  │   │
                  ├───┘
                  │
                Drain
                ┌───┐
 GPIO 18 ──[100R]───┤   │ MOSFET Canal N (AO3400A ou 2N7000)
                └───┘
                Source
                  │
                 GND

 * Resistor de 10k entre Gate e GND (Pull-down de proteção no boot)
```

---

## ⚠️ Cuidados de Engenharia (Interferência Eletromagnética)
Conforme documentado no projeto PIBIT:
* A uma distância de **3 mm**, o campo eletromagnético gerado pelo enrolamento e imã interno do ERM em rotação atinge de **5 a 20 mT**, o que corrompe as leituras do eFlesh (que opera na faixa de 10 a 25 mT).
* O atuador ERM deve ser fisicamente posicionado no **dorso do dedo** ou na **palma da mão** (distância de **15 a 30 mm** do magnetômetro), onde a atenuação de campo magnético por queda cúbica ($1/d^3$) reduz o ruído para níveis insignificantes.

---

## 🚀 Como Executar o Teste
1. Abra o arquivo [`test_erm_pwm.ino`](test_erm_pwm.ino) no **Arduino IDE** ou **VS Code com PlatformIO**.
2. Selecione a placa **ESP32 Dev Module** (ou **ESP32-S3 Dev Module**).
3. Conecte o ESP32 via USB e faça o upload a **115200 bauds**.
4. Observe a resposta mecânica de vibração durante a rampa linear e pulsos de textura tátil.
