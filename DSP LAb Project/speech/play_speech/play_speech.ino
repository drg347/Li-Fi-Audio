#include <stdint.h>
#include <avr/interrupt.h>
#include <avr/io.h>
#include <avr/pgmspace.h>

#define SAMPLE_RATE 8000
#define BUFFER_SIZE 1024

unsigned char sounddata_data[BUFFER_SIZE];
int BufferHead=0;
int BufferTail=0;
unsigned long sample=0;
unsigned long BytesReceived=0;

int ledPin = 13;
int speakerPin = 11;
int Playing = 0;

//Interrupt Service Routine (ISR)
// This is called at 8000 Hz to load the next sample.
ISR(TIMER1_COMPA_vect) 
{
  //Set the PWM Freq.
  OCR2A = sounddata_data[BufferTail];
  
  //If circular buffer is not empty
  if (BufferTail != BufferHead)  
  {
    //Increment Buffer's tail index.
    BufferTail = ((BufferTail+1) % BUFFER_SIZE);
    //Increment sample number.
    sample++;
  }
}

void startPlayback()
{
  //Set pin for OUTPUT mode.
  pinMode(speakerPin, OUTPUT);

  //---------------TIMER 2-------------------------------------
  // Set up Timer 2 to do pulse width modulation on the speaker
  // pin.  
  //This plays the music at the frequency of the audio sample.

  ASSR &= ~(_BV(EXCLK) | _BV(AS2));

  TCCR2A |= _BV(WGM21) | _BV(WGM20);
  TCCR2B &= ~_BV(WGM22);

  // Do non-inverting PWM on pin OC2A (p.155)
  // On the Arduino this is pin 11.
  TCCR2A = (TCCR2A | _BV(COM2A1)) & ~_BV(COM2A0);
  TCCR2A &= ~(_BV(COM2B1) | _BV(COM2B0));

  // No prescaler (p.158)
  TCCR2B = (TCCR2B & ~(_BV(CS12) | _BV(CS11))) | _BV(CS10);

  // Set PWM Freq to the sample at the end of the buffer.
  OCR2A = sounddata_data[BufferTail];
   
  cli();

  // Set CTC mode (Clear Timer on Compare Match) (p.133)
  // Have to set OCR1A *after*, otherwise it gets reset to 0!
  TCCR1B = (TCCR1B & ~_BV(WGM13)) | _BV(WGM12);
  TCCR1A = TCCR1A & ~(_BV(WGM11) | _BV(WGM10));

  // No prescaler (p.134)
  TCCR1B = (TCCR1B & ~(_BV(CS12) | _BV(CS11))) | _BV(CS10);

  // Set the compare register (OCR1A).
  // OCR1A is a 16-bit register, so we have to do this with
  // interrupts disabled to be safe.
  OCR1A = F_CPU / SAMPLE_RATE;    // 16e6 / 8000 = 2000

  //Timer/Counter Interrupt Mask Register
  // Enable interrupt when TCNT1 == OCR1A (p.136)
  TIMSK1 |= _BV(OCIE1A);

  sample = 0;
   
  sei();  
}

void setup()
{
  //Set LED for OUTPUT mode
  pinMode(ledPin, OUTPUT);
   
  Serial.begin(115200);
   
  Playing =0;
}

void loop()
{
  //If audio not started yet
  if (Playing == 0) {
    //Check to see if the first 1000 bytes are buffered.
    if (BufferHead = 1023) {
      Playing=1;
      startPlayback();
    }
  }
  
  //While the serial port buffer has data
  while (Serial.available()>0) {
    if (((BufferHead+1) % BUFFER_SIZE) != BufferTail) {
      BufferHead = (BufferHead+1) % BUFFER_SIZE;
      sounddata_data[BufferHead] = Serial.read();
      BytesReceived++;
    }
  }
}
