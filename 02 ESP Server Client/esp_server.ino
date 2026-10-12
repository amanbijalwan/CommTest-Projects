#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASS";

WebServer server(80);
WiFiServer tcpServer(5000);

void handleRoot() {
  String cmd = server.arg("cmd");
  String response;
  if (cmd == "status") {
    response = "Server status: running fine.";
  } else {
    response = "Server echo: " + cmd;
  }
  server.send(200, "text/plain", response);
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected, IP: " + WiFi.localIP().toString());

  // Web server
  server.on("/", HTTP_GET, []() {
    server.send(200, "text/html",
      "<form action='/' method='GET'>"
      "Command: <input name='cmd'>"
      "<input type='submit'>"
      "</form>");
  });
  server.on("/", HTTP_POST, handleRoot);
  server.begin();

  // TCP server
  tcpServer.begin();
}

void loop() {
  server.handleClient();

  WiFiClient client = tcpServer.available();
  if (client) {
    while (client.connected()) {
      if (client.available()) {
        String cmd = client.readStringUntil('\n');
        cmd.trim();
        String response;
        if (cmd == "status") {
          response = "Server status: running fine.\n";
        } else {
          response = "Server echo: " + cmd + "\n";
        }
        client.print(response);
      }
    }
    client.stop();
  }
}
