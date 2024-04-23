#include "WifiCam.hpp"
#include <WiFi.h>
#include <HTTPClient.h>

static const char* WIFI_SSID = "espwifi";
static const char* WIFI_PASS = "espwifinet";
const char* thingSpeakServer = "api.thingspeak.com";
const String apiKey = "7STBSKX320PDR7HK";
const unsigned long channelID = 2516688; // Your ThingSpeak channel ID

esp32cam::Resolution initialResolution;

WebServer server(80);

void setup() {
  Serial.begin(115200);
  Serial.println();
  delay(2000);

  WiFi.persistent(false);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  if (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.printf("WiFi failure %d\n", WiFi.status());
    delay(5000);
    ESP.restart();
  }
  Serial.println("WiFi connected");

  {
    using namespace esp32cam;

    initialResolution = Resolution::find(1024, 768);

    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(initialResolution);
    cfg.setJpeg(80);

    bool ok = Camera.begin(cfg);
    if (!ok) {
      Serial.println("camera initialize failure");
      delay(5000);
      ESP.restart();
    }
    Serial.println("camera initialize success");
  }

  Serial.println("camera starting");
  Serial.print("http://");
  Serial.println(WiFi.localIP());

  addRequestHandlers();
  server.begin();
}

void loop() {
  // Check if a client has connected
  server.handleClient();

  // Prepare data to send to ThingSpeak
  String dataToSend = "*";
  String inputString = "person";
  for (int i = 0; i < inputString.length(); i++) {
    dataToSend += inputString[i];
    dataToSend += "-";
    dataToSend += (String)inputString[i];
    if (i < inputString.length() - 1) {
      dataToSend += "-";
    }
  }

  // Send data to ThingSpeak
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = "http://" + String(thingSpeakServer) + "/update?api_key=" + apiKey + "&field1=" + dataToSend + "&field2=" + String(channelID);
    http.begin(url);
    int httpCode = http.GET(); //Send the request
    http.end(); //Close connection
    if (httpCode == 200) {
      Serial.println("Data sent to ThingSpeak successfully");
    } else {
      Serial.println("Error sending data to ThingSpeak");
    }
  } else {
    Serial.println("WiFi Disconnected. Unable to send data to ThingSpeak");
  }

  delay(5000); // Wait for 5 seconds before sending data again
}
