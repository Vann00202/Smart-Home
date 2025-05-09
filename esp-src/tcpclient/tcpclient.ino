#include <WiFi.h>

const char* ssid = "wiredliving";
const char* password = "livingwired";

const String GET_STR = "GET_STATE";
const String ON_STR = "SET_ON";
const String OFF_STR = "SET_OFF";
const String TOGGLE_STR = "TOGGLE";


// https://docs.arduino.cc/libraries/wifi/#Client%20class

// The server has a gateway address of 192.168.12.1
// Use gateway instead
// IPAddress server(192,168,12,1);
IPAddress gateway;

WiFiClient client;

void setup() {
  Serial.begin(115200);

  // Pin Setup
  pinMode(19, OUTPUT);
  pinMode(32, OUTPUT); // common anode needs to be rewired on over to 32 from 35 or shorted to 32

  pinMode(23, OUTPUT); //RED
  pinMode(22, OUTPUT); //GREEN
  pinMode(16, OUTPUT); //BLUE

  // Set outlet off
  digitalWrite(19, HIGH); 


  delay(5000);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi network...");

  // Light Red
  digitalWrite(32, HIGH);
  digitalWrite(23, LOW);
  digitalWrite(22, HIGH);
  digitalWrite(16, HIGH);
}

void connect() {
  if (WiFi.status() != WL_CONNECTED) {
    while(WiFi.status() != WL_CONNECTED){
      Serial.print(".");
      delay(100);
      // Light Red
      digitalWrite(32, HIGH);
      digitalWrite(23, LOW);
      digitalWrite(22, HIGH);
      digitalWrite(16, HIGH);
      delay(100);
      // Light Off
      digitalWrite(32, LOW);
      digitalWrite(23, LOW);
      digitalWrite(22, LOW);
      digitalWrite(16, LOW);
    }

    Serial.println("\nConnected to the WiFi network");
    Serial.print("Local ESP32 IP: ");
    Serial.println(WiFi.localIP());
    // Light Blue
    digitalWrite(32, HIGH);
    digitalWrite(23, HIGH);
    digitalWrite(22, HIGH);
    digitalWrite(16, LOW);
    gateway = WiFi.gatewayIP();
    Serial.print("Gateway IP Address: ");
    Serial.println(gateway);

    while (!client.connect(gateway, 18000)) {
      Serial.println("Connecting to server");
      delay(1000);
    }
    Serial.println("Connected to server");

    Serial.println("Completed Setup");
  }
}

void loop() {
  // put your main code here, to run repeatedly
  //Serial.println(client.connected());
  //delay(100);
  connect();

  String msg_str = "";
  while (client.connected()) {
    if (client.available()) {
      char c = client.read();
      msg_str += c;
      if (c == '\n') {
        Serial.println("Recieved String: ");
        Serial.println(msg_str);
        if (msg_str.indexOf(GET_STR) >= 0) {
          client.println(!digitalRead(19));
        } else if (msg_str.indexOf(ON_STR) >= 0) {
          digitalWrite(19, LOW);
          client.println(!digitalRead(19));
        } else if (msg_str.indexOf(OFF_STR) >= 0) {
          digitalWrite(19, HIGH);
          client.println(!digitalRead(19));
        } else if (msg_str.indexOf(TOGGLE_STR) >= 0) {
          digitalWrite(19, !digitalRead(19));
          client.println(!digitalRead(19));
        } else {
          Serial.println("Invalid Request");
        }
        msg_str = ""; // After we hit newline and process, reset string for next message
      }
    }
  }

  Serial.println("Disconnected from server");
}
