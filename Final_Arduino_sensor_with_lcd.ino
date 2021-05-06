#include <LiquidCrystal.h> // includes the LiquidCrystal Library
LiquidCrystal lcd(1, 2, 4, 5, 6, 7); // Creates an LCD object. Parameters: (rs,enable, d4, d5, d6, d7)
const int trigPin = 9;
const int echoPin = 10;
long duration;
int distanceCm, distanceInch,percentage;

void setup() {
  lcd.begin(16,2); // Initializes the interface to the LCD screen, and specifies the dimensions (width and height) of the display
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
  }
void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distanceCm= duration*0.034/2;
  distanceInch = duration*0.0133/2;
  percentage  = (17-distanceCm)*100/17;
  lcd.setCursor(0,0); // Sets the location at which subsequent text written to the LCD will be displayed
  lcd.print("                    "); //Print blanks to clear the row
  lcd.print("Percentage: "); // Prints string "Distance" on the LCD
  if(percentage<0)
  {
  lcd.print("0");
  }
  else
  {
  lcd.print(percentage); // Prints the distance value from the sensor
  //lcd.print(" %");
  }
  delay(250);
  

  Serial.println(duration);
  Serial.println(distanceCm);
  Serial.println(distanceInch);
  delay(10);
}
