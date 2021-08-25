int inRF1 = D2;
int inRF2 = D3;
int inRB1 = D0;
int inRB2 = D1;

void rightFrontStp(){
  digitalWrite(inRF1, LOW);
  digitalWrite(inRF2, LOW);
}

void rightBackStp(){
  digitalWrite(inRB1, LOW);
  digitalWrite(inRB2, LOW);
}

void rightFrontFd(){
  digitalWrite(inRF1, HIGH);
  digitalWrite(inRF2, LOW);
}

void rightBackFd(){
  digitalWrite(inRB1, HIGH);
  digitalWrite(inRB2, LOW);
}

void rightFrontBd(){
  digitalWrite(inRF1, LOW);
  digitalWrite(inRF2, HIGH);
}

void rightBackBd(){
  digitalWrite(inRB1, LOW);
  digitalWrite(inRB2, HIGH);
}

void setup() {
  // put your setup code here, to run once:
  pinMode(inRF1, OUTPUT);
  pinMode(inRF2, OUTPUT);
    pinMode(inRB1, OUTPUT);
  pinMode(inRB2, OUTPUT);
    digitalWrite(inRF1, LOW);
  digitalWrite(inRF2, LOW);
  digitalWrite(inRB1, LOW);
  digitalWrite(inRB2, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  rightFrontFd();
  rightBackFd();
  

}
