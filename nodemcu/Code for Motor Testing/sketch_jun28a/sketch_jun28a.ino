// Motor A connections
//1,2 is for left front, 3,4 is for right front
//7,8 is for left back, 5,6 is for right back
int inRF1 = 13;
int inRF2 = 12;

int inRB2 = 14;
int inLF1 = 27;

int inLF2 = 25;
int inRB1 = 26;

int inLB1 = 32;
int inLB2 = 33;

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
  leftBackFd();
  leftFrontBd();
  rightFrontFd();
  rightBackBd();
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
  rightBackBd();
}

void turnAntiClockwise(){
  leftFrontBd();
  leftBackBd();
  rightFrontFd();
  rightBackFd();
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

void setup(){
  pinMode(inLF1, OUTPUT);
  pinMode(inLF2, OUTPUT);
  pinMode(inRF1, OUTPUT);
  pinMode(inRF2, OUTPUT);
  pinMode(inLB1, OUTPUT);
  pinMode(inLB2, OUTPUT);
  pinMode(inRB1, OUTPUT);
  pinMode(inRB2, OUTPUT);

  // Turn off motors - Initial state
  digitalWrite(inLF1, LOW);
  digitalWrite(inLF2, LOW);
  digitalWrite(inRF1, LOW);
  digitalWrite(inRF2, LOW);
  digitalWrite(inLB1, LOW);
  digitalWrite(inLB2, LOW);
  digitalWrite(inRB1, LOW);
  digitalWrite(inRB2, LOW);
}

void loop(){
  moveForwards();
}
