
const int pwmin_L = 2;  // Left
const int pwmout_L = 5;  // Left

const int pwmin_R =  3;  // Right
const int pwmout_R = 6;  // Right


// this constant won't change:
// code word for forward, backwards, right and left from respi

const int enableA = 52;
const int enableB = 53;
const int x = 51;

// direction pins
const int motora1 = 22;
const int motora2 = 24;
const int motora3 = 26;
const int motora4 = 28;

const int motorb1 = 30;
const int motorb2 = 32;
const int motorb3 = 34;
const int motorb4 = 36;



void setup() {
  
  pinMode(pwmin_R,INPUT);
  pinMode(pwmin_L,INPUT);
  pinMode(enableA, INPUT);
  pinMode(enableB, INPUT);
  pinMode(x, INPUT);

  pinMode(pwmout_R,OUTPUT);
  pinMode(pwmout_L,OUTPUT);
  
  pinMode(motora1, OUTPUT);
  pinMode(motora2, OUTPUT);
  pinMode(motora3, OUTPUT);
  pinMode(motora4, OUTPUT);

  pinMode(motorb1, OUTPUT);
  pinMode(motorb2, OUTPUT);
  pinMode(motorb3, OUTPUT);
  pinMode(motorb4, OUTPUT);


  Serial.begin(9600);
}

void loop() {
  
  // respi input 
  int pwminput_L = map(analogRead(pwmin_L), 0, 100, 0 , 255);
  int pwminput_R = map(analogRead(pwmin_R), 0, 100, 0 , 255);

  int A = digitalRead(enableA);
  int B = digitalRead(enableB);

  // pwm from respi to arduino to motor
  analogWrite(pwmout_L,pwminput_L);
  analogWrite(pwmout_R,pwminput_R);

//      FORWARD

  if (A == LOW && B == LOW){
    
    digitalWrite(motora1, HIGH);
    digitalWrite(motora2, LOW);
    digitalWrite(motora3, HIGH);
    digitalWrite(motora4, LOW);

    digitalWrite(motorb1, HIGH);
    digitalWrite(motorb2, LOW);
    digitalWrite(motorb3, HIGH);
    digitalWrite(motorb4, LOW);
  }


//      LEFT
  else if (A == HIGH && B == LOW){
    
    digitalWrite(motora1, LOW);
    digitalWrite(motora2, HIGH);
    digitalWrite(motora3, LOW);
    digitalWrite(motora4, HIGH);

    digitalWrite(motorb1, HIGH);
    digitalWrite(motorb2, LOW);
    digitalWrite(motorb3, HIGH);
    digitalWrite(motorb4, LOW);


  }

  
  //      RIGHT
  else if (A == LOW && B == HIGH){
    
    digitalWrite(motora1, HIGH);
    digitalWrite(motora2, LOW);
    digitalWrite(motora3, HIGH);
    digitalWrite(motora4, LOW);

    digitalWrite(motorb1, LOW);
    digitalWrite(motorb2, HIGH);
    digitalWrite(motorb3, LOW);
    digitalWrite(motorb4, HIGH);



  }

  
  //       reverse
  else if (A == HIGH && B == HIGH){
    
    digitalWrite(motora1, LOW);
    digitalWrite(motora2, HIGH);
    digitalWrite(motora3, LOW);
    digitalWrite(motora4, HIGH);

    digitalWrite(motorb1, LOW);
    digitalWrite(motorb2, HIGH);
    digitalWrite(motorb3, LOW);
    digitalWrite(motorb4, HIGH);

  } else {
    digitalWrite(motora1, LOW);
    digitalWrite(motora2, LOW);
    digitalWrite(motora3, LOW);
    digitalWrite(motora4, LOW);

    digitalWrite(motorb1, LOW);
    digitalWrite(motorb2, LOW);
    digitalWrite(motorb3, LOW);
    digitalWrite(motorb4, LOW);

  }

  delay(3000);

  while(digitalRead(x)){

    digitalWrite(motora1, LOW);
    digitalWrite(motora2, LOW);
    digitalWrite(motora3, LOW);
    digitalWrite(motora4, LOW);

    digitalWrite(motorb1, LOW);
    digitalWrite(motorb2, LOW);
    digitalWrite(motorb3, LOW);
    digitalWrite(motorb4, LOW);
  };

  

}
