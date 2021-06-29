#include <AFMotor.h>

AF_DCMotor motor1(1);
AF_DCMotor motor2(2);

AF_DCMotor motor3(3);
AF_DCMotor motor4(4);

void setup() {
  // put your setup code here, to run once:
  // Start up serial connection
  Serial.begin(9600); // baud rate
}

void loop() {
  if (Serial.available()) {
    //    Serial.println(Serial.parseInt());
    int action = Serial.parseInt();
    Serial.println(action);
//    if (action == 1) {
//      motor1.setSpeed(200); //I'm not sure if the motor is turning left or not
//      motor1.run(FORWARD); //If it is not, change this function to run(BACKWARD)
//      motor2.setSpeed(200); //I'm not sure if the motor is turning left or not
//      motor2.run(FORWARD); //If it is not, change this function to run(BACKWARD)
//      motor3.setSpeed(0); //I'm not sure if the motor is turning left or not
//      motor3.run(FORWARD); //If it is not, change this function to run(BACKWARD)
//      motor4.setSpeed(0); //I'm not sure if the motor is turning left or not
//      motor4.run(FORWARD); //If it is not, change this function to run(BACKWARD)
//    }
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
          case 1:
            // turn left
            motor1.setSpeed(200); //I'm not sure if the motor is turning left or not
            motor1.run(FORWARD); //If it is not, change this function to run(BACKWARD)
            motor2.setSpeed(200); //I'm not sure if the motor is turning left or not
            motor2.run(FORWARD); //If it is not, change this function to run(BACKWARD)
            motor3.setSpeed(200); //I'm not sure if the motor is turning left or not
            motor3.run(FORWARD); //If it is not, change this function to run(BACKWARD)
            motor4.setSpeed(200); //I'm not sure if the motor is turning left or not
            motor4.run(FORWARD); //If it is not, change this function to run(BACKWARD)
            break;
          default:
            motor1.setSpeed(0); //I'm not sure if the motor is turning left or not
            motor1.run(FORWARD); //If it is not, change this function to run(BACKWARD)
            motor2.setSpeed(0); //I'm not sure if the motor is turning left or not
            motor2.run(FORWARD); //If it is not, change this function to run(BACKWARD)
            motor3.setSpeed(0); //I'm not sure if the motor is turning left or not
            motor3.run(FORWARD); //If it is not, change this function to run(BACKWARD)
            motor4.setSpeed(0); //I'm not sure if the motor is turning left or not
            motor4.run(FORWARD); //If it is not, change this function to run(BACKWARD)
            break;
        }

    //    if (Serial.readString() == 'H') {
    //      motor1.setSpeed(200); //I'm not sure if the motor is turning left or not
    //      motor1.run(FORWARD); //If it is not, change this function to run(BACKWARD)
    //    }
  }
}
