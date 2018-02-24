// Including the ESP8266 WiFi library
#include <ESP8266WiFi.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <WiFiUDP.h>

// Replace with your network details
const char* ssid = "Your_Router_SSID";
const char* password = "Your_Router_Password";
boolean wifiConnected = false;
// Data wire is plugged into pin D1 on the ESP8266 12-E - GPIO 0
#define ONE_WIRE_BUS 0

IPAddress broadcastIp(192,168,1,255);

// UDP variables
unsigned int localPort = 8888;
WiFiUDP UDP;
boolean udpConnected = false;
char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //buffer to hold incoming packet,

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature DS18B20(&oneWire);
char temperatureCString[6];
char temperatureFString[6];

// Web Server on port 80
WiFiServer server(80);

// only runs once on boot
void setup() {
  // Initializing serial port for debugging purposes
  Serial.begin(115200);
  delay(10);
// Initialise wifi connection
wifiConnected = connectWifi();

// only proceed if wifi connection successful
  if(wifiConnected){
  udpConnected = connectUDP();
    if (udpConnected){
  
    }
  }
  DS18B20.begin(); // IC Default 9 bit. If you have troubles consider upping it 12. Ups the delay giving the IC more time to process the temperature measurement
  
}



// runs over and over again
void loop() {
  getTemperature();
  //Serial.println(temperatureCString);
  
   // check if the WiFi and UDP connections were successful
if(wifiConnected){
  if(udpConnected){
  getUDP();
  //Start broadcast of Temperature
      if(String(packetBuffer) == "BehindTheSciences.com") //If start packet is received
      {
        while(String(packetBuffer) != "STOP") //Stops transmitting Temperature Data if "STOP" is received on UDP
        {
          getTemperature();
          memset(packetBuffer, 0, sizeof(packetBuffer));
          UDP.beginPacket(broadcastIp, 64123);
          
          UDP.write(temperatureCString);
          UDP.endPacket();
          delay(5000);
          getUDP();
          Serial.println(String(packetBuffer));
        }
      }
    }
delay(10);   

  }
   
}

//Get UDP Data
void getUDP(){
  int packetSize = UDP.parsePacket();
  if(packetSize)
    {
      Serial.println("");
      Serial.print("Received packet of size ");
      Serial.println(packetSize);
      Serial.print("From ");
      IPAddress remote = UDP.remoteIP();
      for (int i =0; i < 4; i++)
        {
          Serial.print(remote[i], DEC);
          if (i < 3)
            {
              Serial.print(".");
            }
        }
      Serial.print(", port ");
      Serial.println(UDP.remotePort());
      
      // read the packet into packetBufffer
      UDP.read(packetBuffer,UDP_TX_PACKET_MAX_SIZE);
      Serial.println("Contents:");
      Serial.print(packetBuffer);
    }
}


// connect to UDP – returns true if successful or false if not
boolean connectUDP()
{
  boolean state = false;

  Serial.println("");
  Serial.println("Connecting to UDP");

  if(UDP.begin(localPort) == 1)
    {
    Serial.println("Connection successful");
    state = true;
    }
  else
    {
    Serial.println("Connection failed");
    }

  return state;
}
// connect to wifi – returns true if successful or false if not
boolean connectWifi()
{
  boolean state = true;
  int i = 0;
  WiFi.begin(ssid, password);
  Serial.println("");
  Serial.println("Connecting to WiFi");

  // Wait for connection
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.print(".");
    if (i > 10)
      {
      state = false;
      break;
      }
    i++;
  }
  if (state)
    {
    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    }
  else 
    {
    Serial.println("");
    Serial.println("Connection failed.");
    }
  return state;
}

//Get Temperature of 18D20
void getTemperature() 
{
  float tempC;
  float tempF;
  do {
    DS18B20.requestTemperatures(); 
    tempC = DS18B20.getTempCByIndex(0);
    dtostrf(tempC, 2, 2, temperatureCString);
    tempF = DS18B20.getTempFByIndex(0);
    dtostrf(tempF, 3, 2, temperatureFString);
    delay(100);
  } while (tempC == 85.0 || tempC == (-127.0));
}
