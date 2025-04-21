void setup() {
  Serial.begin(115200);
  // put your setup code here, to run once:
  pinMode(19, OUTPUT);

  pinMode(32, OUTPUT); // common anode needs to be rewired on over to 32 from 35 or shorted to 32

  pinMode(23, OUTPUT); //RED
  pinMode(22, OUTPUT); //GREEN
  pinMode(16, OUTPUT); //BLUE
}


  // RELAY CODE
  
  // Outlet off
  digitalWrite(19, HIGH); 
 
  // Outlet On
  digitalWrite(19, LOW);

  // LIGHT CODE

  // Light on (white)
  digitalWrite(32, HIGH); 
  digitalWrite(23, LOW);
  digitalWrite(22, LOW);
  digitalWrite(16, LOW);

  // Light Red
  digitalWrite(32, HIGH);
  digitalWrite(23, LOW);
  digitalWrite(22, HIGH);
  digitalWrite(16,HIGH);

  // Light Green
  digitalWrite(32, HIGH);
  digitalWrite(23, HIGH);
  digitalWrite(22, LOW);
  digitalWrite(16, HIGH);


  // Light Blue
  digitalWrite(32, HIGH);
  digitalWrite(23, HIGH);
  digitalWrite(22, HIGH);
  digitalWrite(16, LOW);

  // Light Off
  digitalWrite(32, LOW);
  digitalWrite(23, LOW);
  digitalWrite(22, LOW);
  digitalWrite(16, LOW);



