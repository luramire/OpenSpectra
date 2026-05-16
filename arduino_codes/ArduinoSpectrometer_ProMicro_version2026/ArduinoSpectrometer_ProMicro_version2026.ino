//Programmer: L. Feipe Ramirez 2026
//Works
/*
 * Arduino Pro micro pins
 * Select board: Arduino Leonardo (even if it is an Arduino Pro micro)
 */
#define SPEC_EOS         3
#define SPEC_TRG         4
#define SPEC_ST          5
#define SPEC_CLK         6
#define SPEC_VIDEO       A0
#define WHITE_LED        8
#define LASER_404        9

#define SPEC_CHANNELS    288 // New Spec Channel

int delayTime;// (microseconds). The f(CLK) (Hz) will be: 1000000/(2*delayTime). 500 kHz if delayTime=1.

uint16_t data[SPEC_CHANNELS];
unsigned long INT_TIME; //Integration time in microseconds
unsigned long N_THP=15; //Number of cycles for start pulse hifg period thp(ST) //Default = 15, 499952 for 1 second of integration time

boolean laser_state, led_state;

void setup(){

  //Set desired pins to OUTPUT
  pinMode(SPEC_CLK, OUTPUT);
  pinMode(SPEC_ST, OUTPUT);
  pinMode(LASER_404, OUTPUT);
  pinMode(WHITE_LED, OUTPUT);
  pinMode(SPEC_EOS, INPUT);
  pinMode(SPEC_TRG, INPUT);
  digitalWrite(SPEC_CLK, HIGH); // Set SPEC_CLK High
  digitalWrite(SPEC_ST, LOW); // Set SPEC_ST Low

  digitalWrite(LASER_404,0);
  digitalWrite(WHITE_LED,0);
  Serial.begin(115200); // Baud Rate set to 115200
  
}

/*
 * This functions reads spectrometer data from SPEC_VIDEO
 * Look at the Timing Chart in the Datasheet for more info
 */
void readSpectrometer(){

  delayTime = 1; // delay time

  // Start clock cycle and set start pulse to signal start
  digitalWrite(SPEC_CLK, LOW);
  delayMicroseconds(delayTime);
  digitalWrite(SPEC_CLK, HIGH);
  delayMicroseconds(delayTime);
  digitalWrite(SPEC_CLK, LOW);
  digitalWrite(SPEC_ST, HIGH);
  delayMicroseconds(delayTime);

  //Sample for a period of time
  for(unsigned long i = 0; i < N_THP; i++){

      digitalWrite(SPEC_CLK, HIGH);
      delayMicroseconds(delayTime);
      digitalWrite(SPEC_CLK, LOW);
      delayMicroseconds(delayTime); 
 
  }

  //Set SPEC_ST to low
  digitalWrite(SPEC_ST, LOW);

  //Sample for a period of time
  for(int i = 0; i < 85; i++){

      digitalWrite(SPEC_CLK, HIGH);
      delayMicroseconds(delayTime);
      digitalWrite(SPEC_CLK, LOW);
      delayMicroseconds(delayTime); 
      
  }

  //One more clock pulse before the actual read
  digitalWrite(SPEC_CLK, HIGH);
  delayMicroseconds(delayTime);
  digitalWrite(SPEC_CLK, LOW);
  delayMicroseconds(delayTime);

  //Read from SPEC_VIDEO
  for(int i = 0; i < SPEC_CHANNELS; i++){

      data[i] = analogRead(SPEC_VIDEO);
      
      digitalWrite(SPEC_CLK, HIGH);
      delayMicroseconds(delayTime);
      digitalWrite(SPEC_CLK, LOW);
      delayMicroseconds(delayTime); 
  }

  //Set SPEC_ST to high
  digitalWrite(SPEC_ST, HIGH);

  //Sample for a small amount of time
  for(int i = 0; i < 7; i++){
    
      digitalWrite(SPEC_CLK, HIGH);
      delayMicroseconds(delayTime);
      digitalWrite(SPEC_CLK, LOW);
      delayMicroseconds(delayTime);
    
  }

  digitalWrite(SPEC_CLK, HIGH);
  delayMicroseconds(delayTime);
  
}

/*
 * The function below prints out data to the terminal or 
 * processing plot
 */
void printData(){
  
  for (int i = 0; i < SPEC_CHANNELS; i++){
    
    Serial.print(data[i]);
    Serial.print(',');
    
  }
  
  Serial.print("\n");
}

void loop(){
  if(Serial.available()>0){
    char caracter=Serial.read();
    if(caracter=='U'){
      laser_state=not laser_state;
      digitalWrite(LASER_404,laser_state);
    }else if(caracter=='L'){
      led_state=not led_state;
      digitalWrite(WHITE_LED,led_state);
    }else if(caracter=='I'){
      while(Serial.available()==0);
      INT_TIME=Serial.parseInt();//INT_TIME in microseconds
      if(INT_TIME>107&&INT_TIME<1000001){
       N_THP=long(INT_TIME/(delayTime*2.0))-48;//This calculation is based on the C12880MA datasheet.
      }
    }
  }
  readSpectrometer();
  printData();
  delay(100);  
   
}
