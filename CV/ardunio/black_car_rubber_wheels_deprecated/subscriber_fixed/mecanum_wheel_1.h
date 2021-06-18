// Motor A connections
//1,2 is for left front, 3,4 is for right front
//7,8 is for left back, 5,6 is for right back
int inRF1 = D2;
int inRF2 = D3;
int inLF1 = D0;
int inLF2 = D1;
int inRB1 = D8;
int inRB2 = D7;
int inLB1 = D5;
int inLB2 = D6;

//Functions for wheels to not moving
void leftFrontStp(){
  digitalWrite(inLF1, LOW);
  digitalWrite(inLF2, LOW);
}

void rightFrontStp(){
  digitalWrite(inRF1, LOW);
  digitalWrite(inRF2, LOW);
}

void leftBackStp(){
  digitalWrite(inLB1, LOW);
  digitalWrite(inLB2, LOW);
}

void rightBackStp(){
  digitalWrite(inRB1, LOW);
  digitalWrite(inRB2, LOW);
}

//functions for 4 wheels to move forwards and backwards
void leftFrontFd(){
  digitalWrite(inLF1, HIGH);
  digitalWrite(inLF2, LOW);
}

void rightFrontFd(){
  digitalWrite(inRF1, HIGH);
  digitalWrite(inRF2, LOW);
}

void leftBackFd(){
  digitalWrite(inLB1, HIGH);
  digitalWrite(inLB2, LOW);
}

void rightBackFd(){
  digitalWrite(inRB1, HIGH);
  digitalWrite(inRB2, LOW);
}

void leftFrontBd(){
  digitalWrite(inLF1, LOW);
  digitalWrite(inLF2, HIGH);
}

void rightFrontBd(){
  digitalWrite(inRF1, LOW);
  digitalWrite(inRF2, HIGH);
}

void leftBackBd(){
  digitalWrite(inLB1, LOW);
  digitalWrite(inLB2, HIGH);
}

void rightBackBd(){
  digitalWrite(inRB1, LOW);
  digitalWrite(inRB2, HIGH);
}

//THIS WILL BE THE ACTUAL FUNCTION THAT WE CAN USE

void moveFdSlow(){
  analogWrite(inLF1, 600);
  analogWrite(inLF2, 0);
  analogWrite(inRF1, 600);
  analogWrite(inRF2, 0);
  analogWrite(inLB1, 600);
  analogWrite(inLB2, 0);
  analogWrite(inRB1, 600);
  analogWrite(inRB2, 0);
}

void moveBdSlow(){
  analogWrite(inLF1, 0);
  analogWrite(inLF2, 600);
  analogWrite(inRF1, 0);
  analogWrite(inRF2, 600);
  analogWrite(inLB1, 0);
  analogWrite(inLB2, 600);
  analogWrite(inRB1, 0);
  analogWrite(inRB2, 600);
}

void allStop(){
	digitalWrite(inLF1, LOW);
	digitalWrite(inLF2, LOW);
	digitalWrite(inRF1, LOW);
	digitalWrite(inRF2, LOW);
	digitalWrite(inLB1, LOW);
	digitalWrite(inLB2, LOW);
	digitalWrite(inRB1, LOW);
	digitalWrite(inRB2, LOW);
}

void moveForwards(){
  leftFrontFd();
  rightFrontFd();
  leftBackFd();
  rightBackFd();
}

void moveBackwards(){
  leftFrontBd();
  rightFrontBd();
  leftBackBd();
  rightBackBd();
}

void moveRight(){
  rightFrontFd();
  leftBackFd();
  rightBackBd();
  leftFrontBd();
}

void moveLeft(){
  rightBackFd();
  leftFrontFd();
  rightFrontBd();
  leftBackBd();
}

void turnClockwise(){
  leftFrontFd();
  leftBackFd();
  rightFrontBd();
  leftBackBd();
}

void turnAntiClockwise(){
  leftFrontBd();
  leftBackBd();
  rightFrontFd();
  leftBackFd();
}


void diagonalDownLeft(){
  leftFrontBd();
  rightBackBd();
  leftBackStp();
  rightFrontStp();
}

void diagonalUpRight(){
  leftFrontFd();
  rightBackFd();
  leftBackStp();
  rightFrontStp();
}

void diagonalUpLeft(){
  rightFrontFd();
  leftBackFd();
  rightBackStp();
  leftFrontStp();
}

void diagonalDownRight(){
  rightFrontBd();
  leftBackBd();
  rightBackStp();
  leftFrontStp();
}
