#include <WiFi.h>

const char* ssid = "wiredliving";
const char* password = "livingwired";


IPAddress server(192,168,12,1);
IPAddress gateway; // IDK if this works but it might be easy way to get PI address

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
  Serial.println(gateway);

  if (client.connect(gateway, 18000)) {
    Serial.println("Connected to server");
    client.println("GET_STATE");
    
  }

  while (client.connected()) {
    if (client.available()) {
      char c = client.read();
      Serial.print(c); // Need a termination character use \n and stop reading on newline
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
