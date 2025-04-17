#include <WiFi.h>

const char* ssid = "wiredliving";
const char* password = "livingwired";

const String GET_STR = "GET_STATE";
const String ON_STR = "SET_ON";
const String OFF_STR = "SET_OFF";

bool current_state = false;

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

  while(WiFi.status() != WL_CONNECTED){
    Serial.print(".");
    delay(100);
  }

  Serial.println("\nConnected to the WiFi network");
  Serial.print("Local ESP32 IP: ");
  Serial.println(WiFi.localIP());

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

void loop() {
  // put your main code here, to run repeatedly
  //Serial.println(client.connected());
  //delay(100);

  String msg_str = "";
  while (client.connected()) {
    if (client.available()) {
      char c = client.read();
      msg_str += c;
      if (c == '\n') {
        Serial.println("Recieved String: ");
        Serial.println(msg_str);
        if (msg_str.indexOf(GET_STR) >= 0) {
          client.println(current_state); // Maybe format this message nicer
        } else if (msg_str.equals(ON_STR)) {
          current_state = true;
          digitalWrite(19, LOW);
          client.println(current_state);
        } else if (msg_str.equals(OFF_STR)) {
          current_state = false;
          digitalWrite(19, HIGH);
          client.println(current_state);
        } else {
          Serial.println("Invalid Request");
        }
        msg_str = ""; // After we hit newline and process, reset string for next message
      }
    }
  }

  //Serial.println("Disconnected from server");
}
