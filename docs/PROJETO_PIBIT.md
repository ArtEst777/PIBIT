# PROJETO PIBIT — Miniaturização e Integração de Sensores Táteis Magnéticos eFlesh Aplicados a uma Luva

- **Autor**: Artur Ferreira Gonçalves (graduando em Engenharia Mecatrônica, UnB)
- **Laboratório**: L-VIS — Laboratório de Visualização, Interação e Simulação (UnB)
- **Período**: 12 meses
- **Data**: Outubro/2026

---

## 1. Contexto e problema

Luvas de realidade virtual (RV) permitem capturar os movimentos das mãos, mas raramente medem forças de contato nas pontas dos dedos. Sem feedback tátil, o usuário não percebe rigidez, textura ou deslizamento de objetos, o que limita a imersão e dificulta aplicações em treinamento de habilidades motoras finas (cirurgia, manutenção). Sensores flexíveis resistivos, comuns em luvas de baixo custo, sofrem com histerese, deriva e falta de repetibilidade.

## 2. Estado da arte: sensor eFlesh

Pattabiraman et al. (2025) propuseram o eFlesh: um sensor tátil magnético fabricado inteiramente por impressão 3D, com microestruturas cut-cell, ímãs de neodímio e um magnetômetro de efeito Hall. Quando a superfície do sensor é deformada, o campo magnético varia; uma rede neural simples (MLP) estima força normal (RMSE 0,27 N), força cisalhante (0,12 N) e ponto de contato (0,5 mm). O eFlesh é de baixo custo (< US$ 5), fácil de fabricar e altamente customizável.

## 3. Oportunidade científica

O eFlesh foi demonstrado em almofadas de 40×40 mm, incompatíveis com a área de uma ponta de dedo humana (~15×15 mm). A miniaturização para essa escala mantendo a sensibilidade não foi relatada. Além disso, a integração de múltiplos sensores (três) em uma luva é inédita e representa um avanço para interfaces tátil-motoras.

## 4. Aplicação proposta

Este projeto aplicará o conceito eFlesh à luva já desenvolvida pelo proponente no L-VIS (plataforma ESP32). Serão fabricados três sensores miniaturizados (15×15×10 mm), posicionados nas pontas dos dedos indicador, médio e polegar. A luva passará a estimar, em tempo real, as forças de contato exercidas durante a **manipulação de objetos reais**, permitindo tarefas de aperto controlado, detecção de deslizamento e pinça fina.

### 4.1 Escopo do feedback: mundo real

Por limitação de tempo e de recursos, **esta fase não utiliza ROS2, Unity nem outra plataforma de RV**. O feedback é físico, em malha fechada local:

```
objeto real → deformação do eFlesh → ΔB no TLV493D → estimativa de força no ESP32 → PWM no motor ERM → percepção do usuário
```

Todo o processamento ocorre no próprio microcontrolador, sem depender de computador externo.

### 4.2 Preparação para integração futura

Para permitir uma implementação futura em RV:

- O firmware será organizado em módulos independentes (**aquisição → estimativa → atuação**), de modo que a saída de força possa ser enviada a outro destino sem reescrever as demais camadas.
- O ESP32 / ESP32-S3 mantém Wi-Fi e BLE disponíveis para uma futura comunicação UDP com Unity, ROS2 ou outro ambiente.
- Os dados de caracterização serão salvos em formato aberto (CSV), reutilizável por qualquer plataforma.

## 5. Objetivos e método

**Objetivo geral**: miniaturizar, caracterizar e integrar sensores eFlesh para pontas de dedo, validando seu desempenho em uma luva com feedback vibrotátil no mundo real.

**Método resumido (revisado):**

- **CAD**: redesenho das microestruturas (célula de 6 mm, vigas de 0,3 mm) no Fusion 360 + script Python, com célula cut-cell personalizada. A treliça de octeto padrão do Fusion 360 é rígida demais e não permite a deformação controlada necessária ao sensoriamento.
- **Fabricação**: impressão 3D em TPU 95A, inserção de ímãs N52 (4,76×1,58 mm, modelo original do artigo; alternativamente 5×3 mm para maior sensibilidade) e magnetômetro TLV493D-A1B6 (substituiu o MLX90393 por disponibilidade e compatibilidade com 3,3 V).
- **Caracterização em bancada**: força normal 0–15 N, cisalhante 0–8 N, localização em malha 10×10 mm.
- **Calibração**: treinamento de MLPs para estimativa de força e posição (validação temporal).
- **Integração**: firmware ESP32 com leitura multiplexada I2C via TCA9548A (o TLV493D possui apenas 2 endereços, insuficiente para 3 sensores) e experimentos com objetos reais (aperto controlado, deslizamento e pinça fina).
- **Atuação háptica**: motores ERM (8×4 mm, 3 V) no dorso do dedo ou na palma. A 3 mm do sensor, o campo do motor (5–20 mT) é comparável ao sinal do eFlesh (10–25 mT), o que inviabiliza a leitura. A 15–30 mm, a interferência cai para níveis aceitáveis.

## 6. Resultados esperados

- Primeiro sensor eFlesh miniaturizado (15×15 mm) funcional.
- Curvas de caracterização e métricas de erro (RMSE) para diferentes rigidezes.
- Luva com três pontos de tato magnético e feedback vibrotátil em malha fechada local, inédita no Brasil.
- Firmware modular pronto para integração futura com RV.
- Repositório público (modelos CAD, firmware, scripts de ML) e submissão de resumo ao SBR 2026.

## 7. Discrepâncias em relação ao plano original

Durante a pré-prototipagem (Mês 1–2), foram identificadas discrepâncias técnicas que exigiram revisão do escopo.

**Tabela 1 — Discrepâncias entre o plano original e o plano revisado**

| Item | Plano original | Plano revisado | Justificativa |
| :--- | :--- | :--- | :--- |
| Sensor | MLX90393 ou TLV493D | TLV493D-A1B6 | Maior disponibilidade em breakout, operação em 3,3 V, biblioteca consolidada |
| Endereços I2C | Não especificado | Apenas 2 endereços → TCA9548A obrigatório | O datasheet do TLV493D (seção 2.1.1) confirma apenas 2 endereços configuráveis |
| Ímãs | N52 5×1 mm | N52 4,76×1,58 mm (artigo) ou 5×3 mm | O ímã de 5×1 mm tem volume ~30% menor; a sensibilidade reduzida pode não atingir RMSE de 0,27 N |
| Microcontrolador | ESP32 DevKit V1 | DevKit V1 (bancada) + ESP32-S3 Nano (final) | O DevKit é grande para wearable; o S3 Nano é menor, mais leve e tem dual-core LX7 |
| Atuador háptico | ERM na ponta do dedo | ERM no dorso do dedo ou na palma | Interferência magnética: a 3 mm, o campo do ERM (5–20 mT) é comparável ao sinal do eFlesh (10–25 mT) |
| Modelagem CAD | Cut-cell (Tozoni et al.) | Cut-cell personalizada no Fusion 360 | A treliça de octeto padrão é rígida e isotrópica; a célula personalizada (4 placas + cortes) permite deformação controlada |
| Calibração | Regressão polinomial | MLP (2 camadas, 128 neurônios) + regressão como alternativa | Não linearidades do campo (1/d³), acoplamento entre eixos e deriva térmica exigem MLP |
| **Plataforma de feedback** | **Integração com Unity / RV** | **Feedback no mundo real, malha local no ESP32** | **Tempo e recursos limitados; integração com RV (Unity/ROS2) preservada como etapa futura** |
| Orçamento | R$ 855 (3 dedos) | R$ 197 (1 dedo) → R$ 264 (com bateria) | Abordagem faseada: validar 1 dedo antes de escalar para 3; itens gratuitos no L-VIS |
| Relatório | 100% submetido | 75% (14 correções pendentes) | Auditoria identificou erros de unidade (mT vs. Gauss) e omissões |
| Posição do sensor | Não especificada | Lateral da falange distal | A face de contato deve ficar livre para o eFlesh; o breakout fica na lateral |

## 8. Nota sobre o teste de bancada e a fabricação de PCB

Não foi possível, neste momento, realizar o teste de bancada com os modelos do artigo oficial do eFlesh. O motivo principal é a restrição orçamentária temporária para comprar ou fabricar as PCBs necessárias aos magnetômetros em versão SMD (MLX90393 ou TLV493D em encapsulamento QFN/TSOP-6). Essas placas exigiriam montagem especializada ou compra de módulos importados, com custo incompatível com a fase atual do projeto.

Como alternativa viável, optou-se por módulos breakout do TLV493D, que permitem validar a leitura I2C, a calibração de baseline e o firmware sem PCB customizada. Essa abordagem mantém o cronograma ativo e permite caracterizar o sensor com os recursos disponíveis.

O proponente concluiu recentemente um curso de KiCad, o que o capacita a projetar, em etapa futura, uma PCB própria para a versão final da luva. Isso reduzirá custos, eliminará a dependência de módulos importados e permitirá integrar o magnetômetro de forma mais compacta na ponta do dedo.

Essa limitação não inviabiliza o projeto; apenas reorganiza a sequência de execução: a validação com breakouts antecede a integração em PCB customizada, que será desenvolvida quando houver orçamento e após a validação funcional dos sensores.

## 9. Status atual do projeto

**Fase atual**: pré-prototipagem (Mês 1–2)

1. **Escopo**: 3 dedos (polegar, indicador, médio), para viabilidade em 12 meses. Foco na miniaturização do eFlesh e no feedback vibrotátil no mundo real via motores ERM.
2. **Sensoriamento**: TLV493D-A1B6 (magnetômetro 3D, I2C, 3,3 V). Módulos breakout no AliExpress (R$ 37/unidade); 3 unidades para diluir o frete. Multiplexador TCA9548A necessário (apenas 2 endereços I2C).
3. **Atuação háptica**: motor ERM 8×4 mm, 3 V (HU Infinito, R$ 5), no dorso do dedo ou na palma (15–30 mm do sensor). Validação experimental prevista para o Mês 6.
4. **Processamento**: ESP32 DevKit V1 (Fase 1, bancada, R$ 43) e ESP32-S3 Nano (Fase 2, luva final). Ambos com I2C e PWM; Wi-Fi/BLE reservados para integração futura com RV.
5. **Modelagem CAD**: cut-cell personalizada no Fusion 360 (célula de 6 mm, placas de 0,3 mm, cortes circulares de 2 mm). Guia passo a passo documentado.
6. **BOM e custos**: R$ 197 (1 dedo) → R$ 264 (com bateria LiPo e case). Filamento TPU, resistores, protoboard e cabos USB disponíveis gratuitamente no L-VIS.
7. **Documentação**: relatório técnico 75% pronto, com 14 correções identificadas em 4 níveis de dificuldade. Correções críticas: unidades (mT vs. Gauss), calibração (MLP vs. regressão), endereços I2C e interferência do ERM.
8. **Base teórica**: eletromagnetismo estudado (8 módulos): campo magnético (B em mT), queda com 1/d³, efeito Hall, conversão LSB→mT, baseline (ΔB), cadeia força→deslocamento→campo, interferência do ERM, Lei de Faraday.
9. **Próximos passos**:
   1. Finalizar as correções do relatório
   2. Comprar os materiais do teste de 1 dedo
   3. Recriar a cut-cell no Fusion 360
   4. Montar o circuito na protoboard
   5. Validar a leitura do sensor
   6. Testar a interferência do ERM
   7. Integrar no dedo

## 10. Perfil do proponente

- Estudante de Engenharia Mecatrônica (UnB, 10º período).
- Gestor de equipe no projeto LVIS (Luva de Realidade Virtual), com 7 membros.
- Experiência em All Blue (AUVs), Biomecatrônica e Ubuntu (ações afirmativas).
- Monitor de Laboratório de Eletrônica (UnB, 2025).
- Estagiário no Grupo Mahvla — Control (AutoCAD, automação documental).
- Curso de KiCad concluído recentemente.
- Idiomas: inglês avançado, espanhol avançado, mandarim básico.
- Mais de 900 horas em atividades de extensão.
- Apresentação oral: "Luva de Realidade Virtual de Baixo Custo" (LVIS, 2025).

## 11. Referências

BHIRANGI, R.; DEFRANCO, A.; ADKINS, J.; et al. AnySkin: Versatile and replaceable tactile skin. Conference on Robot Learning (CoRL), 2024.

PATTABIRAMAN, V.; HUANG, Z.; PANOZZO, D.; ZORIN, D.; PINTO, L.; BHIRANGI, R. eFlesh: Highly customizable Magnetic Touch Sensing using Cut-Cell Microstructures. arXiv preprint arXiv:2506.09994, 2025.

TOZONI, D.; HUANG, Z.; PANOZZO, D.; ZORIN, D. Cut-cell microstructures for two-scale structural optimization. Computer Graphics Forum, v. 43, n. 5, 2024.

YIN, J.; et al. Learning in-hand translation using tactile skin with shear and normal force sensing. IEEE Robotics and Automation Letters, 2024.

INFINEON. TLV493D-A1B6 3D Magnetic Sensor Datasheet. Rev. 1.1, 2019.

ESPRESSIF. ESP32 Datasheet. Version 2.1, 2018.

## 12. Observação final

As discrepâncias da Tabela 1 não comprometem os objetivos do projeto; ao contrário, são decisões de engenharia fundamentadas em análise de datasheets e testes preliminares de viabilidade. O escopo foi ajustado para garantir que o protótipo seja funcional, validado experimentalmente e documentado de forma reproduzível, características valorizadas em projetos PIBIT/PIBIC e em publicações científicas.
