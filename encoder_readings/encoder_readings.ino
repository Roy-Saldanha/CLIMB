// --- PIN CONFIGURATION ---
const int M1_DIR = 19;     // URC10 DIR1 -> ESP32 P19
const int M1_PWM = 18;     // URC10 PWM1 -> ESP32 P18
const int ENCODER_A = 23;  // Encoder OUT A -> ESP32 P23
const int ENCODER_B = 22;  // Encoder OUT B -> ESP32 P22

// --- PWM SETTINGS ---
const int PWM_FREQ = 5000;  // 5 kHz PWM signal
const int PWM_RES = 8;      // 8-bit resolution (0 to 255)

// --- MOTOR CONSTANTS ---
const float PULSES_PER_REV = 88;

// --- GLOBAL VARIABLES ---
volatile long pulseCount = 0;
unsigned long lastTime = 0;

// High-speed Interrupt Service Routine stored in RAM
void IRAM_ATTR handleEncoder() {
  if (digitalRead(ENCODER_B) == HIGH) {
    pulseCount++;
  } else {
    pulseCount--;
  }
}

void setup() {
  Serial.begin(115200);

  // Setup Direction Pin
  pinMode(M1_DIR, OUTPUT);
  digitalWrite(M1_DIR, LOW); // LOW = Forward, HIGH = Reverse

  // Setup ESP32 Hardware PWM Output
  ledcAttach(M1_PWM, PWM_FREQ, PWM_RES);

  // Setup Encoder Interrupts
  pinMode(ENCODER_A, INPUT_PULLUP);
  pinMode(ENCODER_B, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(ENCODER_A), handleEncoder, RISING);

  // Set initial motor speed (0 = Stop, 255 = Full Speed)
  ledcWrite(M1_PWM, 200);
}

void loop() {
  unsigned long currentTime = millis();

  // Print live RPM every 500 ms
  if (currentTime - lastTime >= 500) {
    noInterrupts();
    long currentPulses = pulseCount;
    pulseCount = 0;
    interrupts();

    float timeElapsedMin = (currentTime - lastTime) / 60000.0;
    float rpm = (currentPulses / PULSES_PER_REV) / timeElapsedMin;

    Serial.print("PWM Output: 200 | Live Motor RPM: ");
    Serial.println(rpm, 2);

    lastTime = currentTime;
  }
}