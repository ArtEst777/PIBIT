/**
 * @file test_tlv493d_i2c.ino
 * @brief Leitura, calibração de baseline e streaming triaxial do magnetômetro 3D Infineon TLV493D-A1B6.
 * @project PIBIT — Luva Tátil eFlesh (L-VIS / UnB)
 * @author Artur Ferreira Gonçalves (@ArtEst777)
 * 
 * Conexões I2C padrão com ESP32 (3.3V nativo):
 *  - VDD (Sensor) -> 3.3V (ESP32)
 *  - GND (Sensor) -> GND (ESP32)
 *  - SDA (Sensor) -> GPIO 21 (ESP32) [com pull-up 4.7k se não houver no breakout]
 *  - SCL (Sensor) -> GPIO 22 (ESP32) [com pull-up 4.7k se não houver no breakout]
 * 
 * Compatibilidade:
 *  - Funciona diretamente com a biblioteca oficial "TLV493D-A1B6" da Infineon
 *    (Disponível no Gerenciador de Bibliotecas da Arduino IDE).
 *  - Inclui rotina de escaneamento automático de endereços I2C (0x5E ou 0x35).
 */

#include <Arduino.h>
#include <Wire.h>

// Endereço I2C padrão do TLV493D-A1B6 (típico: 0x5E ou 0x35 conforme pino ADDR)
#define TLV493D_DEFAULT_ADDR 0x5E

// Estrutura de dados para o vetor magnético triaxial
struct MagVector {
  float x; // Campo magnético em mT
  float y; // Campo magnético em mT
  float z; // Campo magnético em mT
};

MagVector baseline = {0.0f, 0.0f, 0.0f};
bool baselineCalibrated = false;

// Função para escanear dispositivos presentes no barramento I2C
void scanI2CBus() {
  Serial.println(F("\n[I2C] Escaneando barramento I2C..."));
  byte count = 0;
  for (byte i = 1; i < 127; i++) {
    Wire.beginTransmission(i);
    if (Wire.endTransmission() == 0) {
      Serial.printf("  -> Dispositivo encontrado no endereco: 0x%02X", i);
      if (i == 0x5E || i == 0x35) Serial.print(F(" (TLV493D-A1B6 Detectado!)"));
      if (i == 0x70) Serial.print(F(" (Multiplexador TCA9548A Detectado!)"));
      Serial.println();
      count++;
    }
  }
  if (count == 0) {
    Serial.println(F("  [ERRO] Nenhum dispositivo I2C encontrado. Verifique cabos e alimentacao!"));
  } else {
    Serial.printf("  Total de %d dispositivo(s) encontrado(s).\n\n", count);
  }
}

// Leitura bruta direta dos registradores do TLV493D (10 registradores de leitura)
bool readTLV493DRaw(uint8_t addr, MagVector &mag) {
  Wire.requestFrom(addr, (uint8_t)6);
  if (Wire.available() < 6) return false;

  uint8_t b0 = Wire.read(); // Bx[11..4]
  uint8_t b1 = Wire.read(); // By[11..4]
  uint8_t b2 = Wire.read(); // Bz[11..4]
  uint8_t b3 = Wire.read(); // Temp[11..8], Bx[3..0]
  uint8_t b4 = Wire.read(); // By[3..0]
  uint8_t b5 = Wire.read(); // Bz[3..0]

  // Montagem dos inteiros de 12 bits com sinal (complemento de dois)
  int16_t rawX = (int16_t)((b0 << 4) | (b3 & 0x0F));
  int16_t rawY = (int16_t)((b1 << 4) | ((b4 >> 4) & 0x0F));
  int16_t rawZ = (int16_t)((b2 << 4) | (b5 & 0x0F));

  // Extensão de sinal para 16 bits
  if (rawX & 0x0800) rawX |= 0xF000;
  if (rawY & 0x0800) rawY |= 0xF000;
  if (rawZ & 0x0800) rawZ |= 0xF000;

  // Fator de conversão típico do TLV493D: ~0.098 mT/LSB (ou ~0.13 mT/LSB)
  const float SENSITIVITY_MT = 0.098f;
  mag.x = rawX * SENSITIVITY_MT;
  mag.y = rawY * SENSITIVITY_MT;
  mag.z = rawZ * SENSITIVITY_MT;

  return true;
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println(F("=================================================="));
  Serial.println(F("  PIBIT / L-VIS (UnB) — Teste Magnetometro 3D     "));
  Serial.println(F("  Sensor: Infineon TLV493D-A1B6                   "));
  Serial.println(F("=================================================="));

  // Inicializa barramento I2C no ESP32 a 400 kHz (Fast Mode como no eFlesh oficial)
  Wire.begin(21, 22);
  Wire.setClock(400000);
  delay(50);

  scanI2CBus();

  // Calibração de Baseline inicial (Média de 30 amostras em repouso)
  Serial.println(F("Calibrando Baseline magnetica ambiente (nao toque no sensor)..."));
  float sumX = 0, sumY = 0, sumZ = 0;
  int validSamples = 0;

  for (int i = 0; i < 30; i++) {
    MagVector m;
    if (readTLV493DRaw(TLV493D_DEFAULT_ADDR, m)) {
      sumX += m.x;
      sumY += m.y;
      sumZ += m.z;
      validSamples++;
    }
    delay(20);
  }

  if (validSamples > 10) {
    baseline.x = sumX / validSamples;
    baseline.y = sumY / validSamples;
    baseline.z = sumZ / validSamples;
    baselineCalibrated = true;
    Serial.printf("Baseline Calibrada com Sucesso: B0_x=%.2f mT | B0_y=%.2f mT | B0_z=%.2f mT\n\n",
                  baseline.x, baseline.y, baseline.z);
    Serial.println(F("Iniciando Streaming em formato Serial Plotter (Delta Bx, Delta By, Delta Bz, Magnitude):"));
  } else {
    Serial.println(F("[AVISO] Nao foi possivel comunicar com o sensor no endereco 0x5E."));
    Serial.println(F("Verifique se o seu breakout responde em 0x35 ou utilize o scanner I2C acima."));
  }
}

void loop() {
  MagVector current;
  if (readTLV493DRaw(TLV493D_DEFAULT_ADDR, current)) {
    // Cálculo da variação em relação ao repouso (Elimina campo estático da Terra)
    float deltaX = current.x - baseline.x;
    float deltaY = current.y - baseline.y;
    float deltaZ = current.z - baseline.z;
    float magnitude = sqrt(deltaX * deltaX + deltaY * deltaY + deltaZ * deltaZ);

    // Formatação amigável para o Plotter Serial da Arduino IDE
    Serial.print(F("Delta_Bx:"));   Serial.print(deltaX, 3);
    Serial.print(F(" Delta_By:"));   Serial.print(deltaY, 3);
    Serial.print(F(" Delta_Bz:"));   Serial.print(deltaZ, 3);
    Serial.print(F(" Magnitude:"));  Serial.println(magnitude, 3);
  } else {
    delay(500);
  }

  delay(20); // Amostragem a ~50 Hz
}
