/*
  Firmware version: "2.0.4"
  -------------------------------------------------------------------------------------
  Adapted example from HX711 library for `serial-weighing-scale`. Lars Rollik, nov2021.
  github.com/larsrollik/serial-weighing-scale
  -------------------------------------------------------------------------------------
  HX711_ADC
  Arduino library for HX711 24-Bit Analog-to-Digital Converter for Weight Scales
  Olav Kallhovd sept2017
  -------------------------------------------------------------------------------------
*/

#include <HX711_ADC.h>

// DEFINITIONS
#define CMD Serial
#define HX711_DOUT 2      // DATA
#define HX711_SCK 3       // CLOCK
#define SAMPLES_IN_USE 1  // number of samples to average for measurement, less will cause more noise but faster response
// #define CALIBRATION_FACTOR -3150  // CHANGE THIS VALUE FROM CALIBRATION RESULT  // scale 1
#define CALIBRATION_FACTOR -2630  // CHANGE THIS VALUE FROM CALIBRATION RESULT  // scale 2
#define SCALING_FACTOR 1.0
#define STABILIZING_TIME 2000  // precision right after power-up can be improved by adding a few seconds of stabilizing time
#define PERFORM_TARE true      // set to false if you don't want tare to be performed in the next step
#define DEBUG_PRINT false
#define ID_STRING "<SerialWeighingScale>"
#define BUFFER_SIZE 10

// INSTANCE of LoadCell object
HX711_ADC LoadCell(HX711_DOUT, HX711_SCK);

float buffer[BUFFER_SIZE];
uint8_t bufIndex = 0;
bool bufFilled = false;
// Sampling flag set by ISR
volatile bool sampleFlag = false;

void setup() {
  // establish communication
  CMD.begin(115200);

  // initialize the scale
  LoadCell.begin();
  LoadCell.start(STABILIZING_TIME, PERFORM_TARE);
  LoadCell.setSamplesInUse(SAMPLES_IN_USE);
  LoadCell.setGain(128);

  if (LoadCell.getTareTimeoutFlag()) {
    logMessage("Timeout, check MCU>HX711 wiring and pin designations");
    while (1)
      ;
  } else {
    LoadCell.setCalFactor(CALIBRATION_FACTOR);
  }

  while (!CMD)
    ;

  identifyMyself();

  if (DEBUG_PRINT)
    logMessage("ready");

  // Initialize buffer
  for (int i = 0; i < BUFFER_SIZE; i++) {
    buffer[i] = 0;
  }

  // --- Timer1 Setup for 100ms interrupts ---
  noInterrupts();  // Disable interrupts during setup

  TCCR1A = 0;  // Clear Timer/Counter Control Registers
  TCCR1B = 0;
  TCNT1 = 0;  // Clear timer counter

  // Set compare match register for 100ms interval
  // Formula: OCR1A = (16*10^6) / (prescaler * frequency) - 1
  // For 10Hz (100ms): OCR1A = 16,000,000 / (64 * 10) - 1 = 24,999
  OCR1A = 24999;
  TCCR1B |= (1 << WGM12);               // CTC mode
  TCCR1B |= (1 << CS11) | (1 << CS10);  // Prescaler 64
  TIMSK1 |= (1 << OCIE1A);              // Enable Timer1 compare interrupt

  interrupts();  // Enable global interrupts

}  // setup


void loop() {
  if (sampleFlag) {
    sampleFlag = false;

    if (LoadCell.update()) {
      addToBuffer(LoadCell.getData());
    }
  }//if

  //   LoadCell.refreshDataSet();
  // LoadCell.update();
  //   float i = LoadCell.getData() / SCALING_FACTOR;

  static byte startByte = '<';
  static byte stopByte = '>';
  static byte commandChar;
  // static uint16_t int1;
  // static uint16_t int2;

  static bool receiving = false;
  static byte buffer[256];
  static int bufferIndex = 0;

  // Check if data is available
  while (CMD.available()) {
    byte incomingByte = CMD.read();

    if (incomingByte == startByte) {
      // Start receiving message
      receiving = true;
      bufferIndex = 0;
      continue;
    }

    // EVAL: Stop receiving message and process data
    if (incomingByte == stopByte) {
      receiving = false;
      commandChar = buffer[0];

      switch (commandChar) {
        case 'i':
          // identify as scale
          identifyMyself();
          break;

        case 'w':
          // read weight

          if (DEBUG_PRINT)
            logMessage("reading weight");

          // readWeight();
          CMD.println(String(getRollingAverage(2)));
          break;

        case 't':
          // tare scale
          tare_scale();
          break;

        case 'c':
          // calibrate scale (factor)
          calibrate();
          break;

        case 'f':
          // read calibration factor
          CMD.println(String(CALIBRATION_FACTOR));
          break;

        default:
          if (DEBUG_PRINT)
            logMessage("Invalid command");
          break;
      }
    }  // EVAL

    // RX
    if (receiving) {
      // Store received bytes in buffer
      if (bufferIndex < sizeof(buffer)) {
        buffer[bufferIndex++] = incomingByte;
      }
    }  // RX
  }    // while
}  // loop


// Timer interrupt handler for sampling
void sampleLoadCell() {
  if (LoadCell.update()) {
    float sample = LoadCell.getData();  // Read sample from HX711
    addToBuffer(sample);
  }
}

// Timer1 ISR every 100ms
ISR(TIMER1_COMPA_vect) {
  sampleFlag = true;
}

// Add the new sample to the buffer
void addToBuffer(float val) {
  buffer[bufIndex++] = val;
  if (bufIndex >= BUFFER_SIZE) {
    bufIndex = 0;
    bufFilled = true;
  }
}

float getRollingAverage(int precision) {
  uint8_t size = bufFilled ? BUFFER_SIZE : bufIndex;
  if (size == 0) return 0.0;

  float sum = 0;
  for (uint8_t i = 0; i < size; i++) sum += buffer[i];
  float avg = sum / size;

  // Round to specified precision
  float factor = pow(10, precision);
  return round(avg * factor) / factor;
}


void identifyMyself() {
  CMD.println(ID_STRING);
}

void logMessage(const String& msg) {
  CMD.print("LOG: ");
  CMD.println(msg);
}  // end:log


void sendFloatAsBytes(float value) {
  union {
    float f;
    byte b[4];
  } data;

  data.f = value;

  for (int i = 0; i < 4; i++) {
    CMD.write(data.b[i]);
  }
}  // end:float

void readWeight() {
  if (DEBUG_PRINT)
    logMessage("fct: readWeight");

  // LoadCell.refreshDataSet();
  LoadCell.update();
  float i = LoadCell.getData() / SCALING_FACTOR;
  // sendFloatAsBytes(i);
  CMD.println(String(i));
}  // end: read weight

int tare_scale() {
  // LoadCell.tareNoDelay();  // Start tare without delay
  LoadCell.tare();  // Start tare (blocking)
}  // end: tare


void calibrate() {
  LoadCell.setCalFactor(1.0);  // Reset calibration factor to default
  tare_scale();                // Tare the scale before calibration

  logMessage("Make sure to send 'c' calibrate command and known mass float each without line ending!");
  logMessage("Please enter the known mass (in grams) and press Enter:");
  while (!CMD.available()) {
    // Wait for the user to submit the known mass
    delay(100);
  }

  // Read the known mass input from serial
  float known_mass = CMD.parseFloat();
  logMessage("Known mass received: ");
  logMessage(String(known_mass));  // Confirm receipt of known mass

  logMessage("Now, please place the known weight on the scale and press 'a' to begin calibration.");

  boolean weight_added = false;
  while (!weight_added) {
    if (CMD.available()) {
      char cmdChar = CMD.read();  // Read input from user
      LoadCell.update();          // Update load cell reading

      // Wait for user to confirm the weight is placed and press 'a'
      if (cmdChar == 'a') {
        LoadCell.refreshDataSet();  // Refresh data from the load cell
        float new_calibration_factor = LoadCell.getNewCalibration(known_mass);

        logMessage("New calibration factor: ");
        logMessage(String(new_calibration_factor));

        weight_added = true;  // Calibration is complete
      }
    }
    delay(10);  // Short delay to avoid excessive CPU usage
  }             // while
}  // end: calibrate
