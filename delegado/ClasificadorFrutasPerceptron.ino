void setup() {
  pinMode(13, OUTPUT); // Configurar el pin 13 como salida
  Serial.begin(9600); // Iniciar la comunicación serie a 9600 baudios
}

void loop() {
  if (Serial.available() > 0) { // Si hay datos disponibles en el puerto serie
    char c = Serial.read(); // Leer el caracter recibido
    if (c == '1') { // Si el caracter es '1'
      digitalWrite(13, HIGH); // Encender el LED 13
    }
    else if (c == '0') { // Si el caracter es '0'
      digitalWrite(13, LOW); // Apagar el LED 13
    }
  }
}