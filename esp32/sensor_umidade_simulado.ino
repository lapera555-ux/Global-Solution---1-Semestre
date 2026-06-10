/*
  AgroENSO Risk IA - ESP32 simulado
  Esta camada representa a validação local de campo.
  O ESP32 não mede El Niño. Ele simula leituras de umidade do solo e temperatura.
*/

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("AgroENSO Risk IA - ESP32 simulado iniciado");
}

void loop() {
  int umidade = random(14, 43);
  int temperatura = random(26, 39);

  Serial.print("umidade_solo_pct=");
  Serial.print(umidade);
  Serial.print("; temperatura_local_c=");
  Serial.print(temperatura);

  if (umidade < 20) {
    Serial.println("; status=solo seco");
  } else if (umidade < 28) {
    Serial.println("; status=atencao");
  } else {
    Serial.println("; status=adequado");
  }

  delay(3000);
}
