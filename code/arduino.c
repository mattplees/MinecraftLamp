//
//  Adafruit Trinket with NeoPixel Night Light.
//  Meant to be embedded in a Minecraft Ore cube.
//
//  Wire a pushbutton from GPIO #3 to GND.
//  NeoPixel DI connects to GPIO #2
//  NeoPixel power to +5V and GND to GND (or GPIO #1 as a convenience.)
//

#include <Adafruit_NeoPixel.h>
#ifdef __AVR_ATtiny85__ // Trinket, Gemma, etc.
 #include <avr/power.h>
#endif

#define PIN_DOUT 2  // #2 is connected to the DI pin on the NeoPixel
#define PIN_GND  1  // #1 is used as GND for the NeoPixel, for convenience.
#define PIN_BUTTON_A 3

// Initialize a string of one LED on pin #2
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(1, PIN_DOUT);

#define N_COLORS  (8)
uint32_t colors[N_COLORS]  =
{
  0xFF0000,  // Red  (Redstone)
  0x7FFFFF,  // Cyan  (Diamond)
  0xFF3F00,  // Orange  (Copper)
  0x00FF00,  // Green  (Emerald)
  0x0000FF,  // Blue  (Lapis Lazuli)
  0xFF7F00,  // Yellow  (Gold)
  0xFF00FF,  // Magenta
  0xFFFFFF,  // White
};

int nColor = 0;
uint32_t fadeTime;
uint32_t t;
uint32_t pressTime;
int buttonState = 0;  // 0=released, 1=debounce, 2=pressed

uint8_t r = 0;
uint8_t g = 0;
uint8_t b = 0;
uint8_t r1 = 0;
uint8_t g1 = 0;
uint8_t b1 = 0;

void advanceColor() {
    nColor++;    // Next color
    if (nColor >= N_COLORS)
      nColor = 0;

   uint32_t color = colors[nColor];
   r1 = 0xFF & (color >> 16);
   g1 = 0xFF & (color >> 8);
   b1 = 0xFF & (color);
}

void refreshColor() {
  if (r < r1)
    r = r + 1;
  else if (r > r1)
    r = r - 1;

  if (g < g1)
    g = g + 1;
  else if (g > g1)
    g = g - 1;

  if (b < b1)
    b = b + 1;
  else if (b > b1)
    b = b - 1;

    uint32_t color = r;
    color = (color << 8) | g;
    color = (color << 8) | b;
    pixels.setPixelColor(0, color);
    pixels.show();
}

void setup() {
#ifdef __AVR_ATtiny85__ // Trinket, Gemma, etc.
  if(F_CPU == 16000000) clock_prescale_set(clock_div_1);
#endif

  // Set button pin as input:
  pinMode(PIN_BUTTON_A, INPUT_PULLUP);
  // Setting input pins to high turns on internal pull-up resistors:
  digitalWrite(PIN_BUTTON_A, HIGH);

  // Set GND pin for NeoPixel as output and LOW:
  pinMode(PIN_GND, OUTPUT);
  digitalWrite(PIN_GND, LOW);

  pixels.begin();
  //pixels.setBrightness(85); // 1/3 brightness
  pixels.setBrightness(255);  // Full brightness

  advanceColor();
  fadeTime = millis();
  refreshColor();
}

void loop() {

  t = millis();

  // Must debounce the button on Pin #3 in case we're
  // powered off USB of an actual computer.
  // The USB host will pulse the data line and fake us out otherwise.
  if (digitalRead(PIN_BUTTON_A) == LOW)
  {
    if (buttonState == 0)
    {
      pressTime = t;
      buttonState = 1;
    }
    else if ((buttonState == 1) && ((t - pressTime) >= 60))
    {
      advanceColor();
      buttonState = 2;
    }
  }
  else
  {
    buttonState = 0;
  }

  if ((t - fadeTime) > 3) {
    refreshColor();
    fadeTime = t;
  }
}