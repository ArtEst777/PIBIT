/**
 * @file test_erm_pwm.ino
 * @brief Teste e caracterização de atuadores vibrotáteis ERM (Coin 8x4mm / 10mm) com ESP32.
 * @project PIBIT — Luva Tátil eFlesh (L-VIS / UnB)
 * @author Artur Ferreira Gonçalves (@ArtEst777)
 * 
 * Circuito de Acionamento (Driver MOSFET N):
 *  - GPIO 18 (ESP32) -> Resistor 100R -> Gate do MOSFET (AO3400A ou 2N7000)
 *  - Resistor 10k entre Gate e GND (Pull-down de proteção no boot)
 *  - Source do MOSFET -> GND
 *  - Drain do MOSFET -> Terminal Negativo (-) do Motor ERM
 *  - Terminal Positivo (+) do Motor ERM -> 3.3V (ou 3.7V da bateria)
 *  - Diodo 1N4148 em paralelo com o motor (Cátodo/faixa no +, Ânodo no Drain)
 */

#include <Arduino.h>

// Configuração do pino e canal PWM (ESP32 LEDC)
const int PIN_MOTOR_ERM = 18;       // GPIO conectado ao Gate do MOSFET
const int PWM_FREQ = 1000;          // 1 kHz (ótima resposta para ERM DC)
const int PWM_RESOLUTION = 8;       // 8 bits: valores de 0 a 255
const int PWM_CHANNEL = 0;          // Canal LEDC (0 a 15)

// Função auxiliar para ajustar intensidade (0 a 100%)
void setVibrationIntensity(float percentage) {
  percentage = constrain(percentage, 0.0f, 100.0f);
  int duty = map((int)(percentage * 10), 0, 1000, 0, 255);
  ledcWrite(PIN_MOTOR_ERM, duty);
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println(F("=================================================="));
  Serial.println(F("  PIBIT / L-VIS (UnB) — Teste de Atuador ERM     "));
  Serial.println(F("=================================================="));
  
  // Configuração do periférico LEDC PWM no ESP32
  #if ESP_IDF_VERSION >= ESP_IDF_VERSION_VAL(5, 0, 0)
    // Para ESP32 Core v3.x+ (ESP-IDF 5.x)
    ledcAttach(PIN_MOTOR_ERM, PWM_FREQ, PWM_RESOLUTION);
  #else
    // Para ESP32 Core v2.x legado
    ledcSetup(PWM_CHANNEL, PWM_FREQ, PWM_RESOLUTION);
    ledcAttachPin(PIN_MOTOR_ERM, PWM_CHANNEL);
  #endif

  setVibrationIntensity(0);
  Serial.println(F("Motor inicializado em estado DESLIGADO."));
  Serial.println(F("Iniciando rotina de testes de padrões hápticos..."));
}

void loop() {
  // Teste 1: Rampa linear de aceleração (0% a 100%)
  Serial.println(F("\n[Teste 1] Rampa crescente de força (0% -> 100%)..."));
  for (int pct = 0; pct <= 100; pct += 5) {
    setVibrationIntensity(pct);
    Serial.printf("Intensidade: %d%%\n", pct);
    delay(100);
  }
  delay(500);
  setVibrationIntensity(0);
  delay(1000);

  // Teste 2: Pulso curto (Simulação de toque / clique discreto)
  Serial.println(F("\n[Teste 2] Pulsos curtos (Detecção de Contato / Clique)..."));
  for (int i = 0; i < 3; i++) {
    setVibrationIntensity(80);
    delay(40); // 40 ms de pulso rápido
    setVibrationIntensity(0);
    delay(250);
  }
  delay(1000);

  // Teste 3: Padrão de textura (pulsos modulados tipo De Brida, 2024)
  Serial.println(F("\n[Teste 3] Simulação de Textura Áspera (Tremor de deslizamento)..."));
  for (int i = 0; i < 15; i++) {
    setVibrationIntensity(60);
    delay(20);
    setVibrationIntensity(10);
    delay(20);
  }
  setVibrationIntensity(0);
  
  Serial.println(F("\nCiclo concluído. Aguardando 4 segundos para reiniciar..."));
  delay(4000);
}
