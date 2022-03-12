// Motor A connections
//1,2 is for left front, 3,4 is for right front
//7,8 is for left back, 5,6 is for right back
int inRF1 = 25; // D2
int inRF2 = 26; // D3
int inLF1 = 32; // D0
int inLF2 = 33; // D1
int inRB1 = 14; // D6
int inRB2 = 27; // D5
int inLB1 = 12; // D7
int inLB2 = 13; // D8

//Functions for wheels to not moving
void leftFrontStp(){
  analogWrite(inLF1, 0);
  analogWrite(inLF2, 0);
}

void rightFrontStp(){
  analogWrite(inRF1, 0);
  analogWrite(inRF2, 0);
}

void leftBackStp(){
  analogWrite(inLB1, 0);
  analogWrite(inLB2, 0);
}

void rightBackStp(){
  analogWrite(inRB1, 0);
  analogWrite(inRB2, 0);
}

//functions for 4 wheels to move forwards and backwards
void leftFrontFd(){
  analogWrite(inLF1, 600);
  analogWrite(inLF2, 0);
}

void rightFrontFd(){
  analogWrite(inRF1, 600);
  analogWrite(inRF2, 0);
}

void leftBackFd(){
  analogWrite(inLB1, 600);
  analogWrite(inLB2, 0);
}

void rightBackFd(){
  analogWrite(inRB1, 600);
  analogWrite(inRB2, 0);
}

void leftFrontBd(){
  analogWrite(inLF1, 0);
  analogWrite(inLF2, 600);
}

void rightFrontBd(){
  analogWrite(inRF1, 0);
  analogWrite(inRF2, 600);
}

void leftBackBd(){
  analogWrite(inLB1, 0);
  analogWrite(inLB2, 600);
}

void rightBackBd(){
  analogWrite(inRB1, 0);
  analogWrite(inRB2, 600);
}

//THIS WILL BE THE ACTUAL FUNCTION THAT WE CAN USE

void moveFdS0(){
  analogWrite(inLF1, 600);
  analogWrite(inLF2, 0);
  analogWrite(inRF1, 600);
  analogWrite(inRF2, 0);
  analogWrite(inLB1, 600);
  analogWrite(inLB2, 0);
  analogWrite(inRB1, 600);
  analogWrite(inRB2, 0);
}

void moveBdS0(){
  analogWrite(inLF1, 0);
  analogWrite(inLF2, 600);
  analogWrite(inRF1, 0);
  analogWrite(inRF2, 600);
  analogWrite(inLB1, 0);
  analogWrite(inLB2, 600);
  analogWrite(inRB1, 0);
  analogWrite(inRB2, 600);
}

void roundArena(){
  analogWrite(inLF1, 0);
  analogWrite(inLF2, 600);
  analogWrite(inRF1, 0);
  analogWrite(inRF2, 300); // control
  analogWrite(inLB1, 0);
  analogWrite(inLB2, 300); // control 2
  analogWrite(inRB1, 0);
  analogWrite(inRB2, 600);
}

void allStop(){
  analogWrite(inLF1, 0);
  analogWrite(inLF2, 0);
  analogWrite(inRF1, 0);
  analogWrite(inRF2, 0);
  analogWrite(inLB1, 0);
  analogWrite(inLB2, 0);
  analogWrite(inRB1, 0);
  analogWrite(inRB2, 0);
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
