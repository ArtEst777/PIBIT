# 🧲 Módulo de Sensoriamento Magnético 3D: Sensor_Magnetometro

Esta pasta contém o firmware de teste e documentação de integração do magnetômetro tridimensional **Infineon TLV493D-A1B6** para a transdução tátil do **eFlesh** em microestruturas de TPU.

---

## 📌 Pinagem e Conexão I2C com o ESP32

O sensor opera nativamente em níveis lógicos de **3,3 V** (compatibilidade direta com o ESP32, sem necessidade de conversores de nível lógico).

| Pino Sensor | Pino ESP32 (DevKit / Nano) | Função | Observação |
| :--- | :--- | :--- | :--- |
| **VDD / 3V3** | 3V3 | Alimentação | $2,7\text{ V}$ a $3,5\text{ V}$ |
| **GND** | GND | Referência de Terra | Comum |
| **SDA** | GPIO 21 (ou definido no software) | Dados I2C | Resistor de pull-up $4,7\text{ k}\Omega$ |
| **SCL** | GPIO 22 (ou definido no software) | Clock I2C | Resistor de pull-up $4,7\text{ k}\Omega$ |

---

## 🔍 Endereçamento I2C e Multiplexação
* O CI TLV493D-A1B6 possui apenas **2 endereços de barramento** configuráveis por hardware (`0x5E` ou `0x35`).
* Na fase de bancada com **1 dedo**, o sensor é ligado diretamente aos pinos SDA/SCL do ESP32.
* Na luva completa com **3 dedos**, os 3 sensores serão conectados através de um multiplexador I2C **TCA9548A** (endereço `0x70`), permitindo selecionar o canal do dedo desejado via comando `Wire.write(1 << canal)`.

---

## 📊 Calibração de Baseline e Sinal Útil ($\Delta \vec{B}$)
Ao ligar a luva, o código faz a amostragem em repouso do campo magnético inicial:
$$\vec{B}_0 = (B_{x0}, B_{y0}, B_{z0})$$

Quando a polpa de TPU sofre compressão mecânica, o ímã N52 se desloca em relação ao chip, gerando a variação:
$$\Delta B_x = B_x - B_{x0}, \quad \Delta B_y = B_y - B_{y0}, \quad \Delta B_z = B_z - B_{z0}$$
$$\|\Delta \vec{B}\| = \sqrt{\Delta B_x^2 + \Delta B_y^2 + \Delta B_z^2}$$

Esse vetor $\Delta \vec{B}$ é o vetor de entrada fornecido à rede neural MLP ou ao modelo de regressão para estimar a força normal e tangencial em Newtons.

---

## 🚀 Como Executar o Teste
1. Abra o arquivo [`test_tlv493d_i2c.ino`](test_tlv493d_i2c.ino) na Arduino IDE.
2. Certifique-se de que a taxa da Serial está em **115200 bauds**.
3. Abra as ferramentas **Serial Plotter** (`Ctrl + Shift + L` na Arduino IDE) para visualizar em tempo real os gráficos de deformação magnética ao apertar a polpa do eFlesh!
