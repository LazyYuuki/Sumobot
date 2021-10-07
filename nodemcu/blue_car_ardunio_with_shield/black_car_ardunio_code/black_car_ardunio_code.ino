#include <AFMotor.h>

AF_DCMotor motor1(1);
AF_DCMotor motor2(2);

AF_DCMotor motor3(3);
AF_DCMotor motor4(4);

void setup() {
  // put your setup code here, to run once:
  // Start up serial connection
  Serial.begin(115200); // baud rate
}

void loop() {
  int action = random(0,10);
  Serial.println(action);
  delay(random(0,2000));
  switch (action) {
    case 0:
      motor1.setSpeed(0); //I'm not sure if the motor is turning left or not
      motor1.run(FORWARD); //If it is not, change this function to run(BACKWARD)
      motor2.setSpeed(0); //I'm not sure if the motor is turning left or not
      motor2.run(FORWARD); //If it is not, change this function to run(BACKWARD)
      motor3.setSpeed(0); //I'm not sure if the motor is turning left or not
      motor3.run(FORWARD); //If it is not, change this function to run(BACKWARD)
      motor4.setSpeed(0); //I'm not sure if the motor is turning left or not
      motor4.run(FORWARD); //If it is not, change this function to run(BACKWARD)
      break;
    default:
      // turn left
      motor1.setSpeed(200); //I'm not sure if the motor is turning left or not
      motor1.run(random(0,2) ? FORWARD : BACKWARD); //If it is not, change this function to run(BACKWARD)
      motor2.setSpeed(200); //I'm not sure if the motor is turning left or not
      motor2.run(random(0,2) ? FORWARD : BACKWARD); //If it is not, change this function to run(BACKWARD)
      motor3.setSpeed(200); //I'm not sure if the motor is turning left or not
      motor3.run(random(0,2) ? FORWARD : BACKWARD); //If it is not, change this function to run(BACKWARD)
      motor4.setSpeed(200); //I'm not sure if the motor is turning left or not
      motor4.run(random(0,2) ? FORWARD : BACKWARD); //If it is not, change this function to run(BACKWARD)
      break;
  }
}
