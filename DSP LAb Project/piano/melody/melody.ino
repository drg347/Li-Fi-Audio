int speakerPin = 11;
void setup() {
  Serial.begin(9600);
  pinMode(speakerPin, OUTPUT);
}

int c = 0;
int noteDuration = 1000/8;
void loop() {
  int num=0;
  //digitalWrite(speakerPin, HIGH);
  if(Serial.available() > 0) {
    for (int i=2; i>=0; i--){
      c = Serial.read();
      c = c - '0';
      num = num+c*pow(10,i);
    }
    num += 1;
    tone(speakerPin, num, noteDuration);
    delay(noteDuration *1.5);
  }
  
  else {
    noTone(8);
    delay(noteDuration *1.5);
  }
}

