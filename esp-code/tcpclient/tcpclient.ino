#include <WiFi.h>

const char* ssid = "wiredliving";
const char* password = "livingwired";

// https://docs.arduino.cc/libraries/wifi/#Client%20class

// The server has a gateway address of 192.168.12.1
// Use gateway instead
// IPAddress server(192,168,12,1);
IPAddress gateway;

WiFiClient client;

void setup() {
  Serial.begin(115200);

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

  if (client.connect(gateway, 18000)) {
    Serial.println("Connected to server");
    client.println("GET_STATE");
  }

  String str = "";
  while (client.connected()) {
    if (client.available()) {
      char c = client.read();
      //Serial.print(c);
      str += c;
      if (c == '\n') {
        Serial.println("Got String Back: ");
        Serial.println(str);
      }
    }
  }

  Serial.println("Completed Setup");
}

void loop() {
  // put your main code here, to run repeatedly:

  //gateway = WiFi.gatewayIP(); // Again IDK if this works as intended

  //client.connect(gateway, 18000);
  // client.connect(server, 18000);
}
