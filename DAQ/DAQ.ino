#include <TimerOne.h>


//Defines
#define SIZE_DATA_IN_SERIAL 2
#define MAX_NUM_AMOSTRA 767 
//Variaveis Globais
unsigned char data_in_serial[SIZE_DATA_IN_SERIAL];
unsigned char dado_novo = 0;
unsigned char medindo = 0;

int amostras[MAX_NUM_AMOSTRA];


//Variaveis de configuração
int num_amostras = 100;    //Numero de amostras para leitura contínua
unsigned char periodo_amostragem = 60;  //periodo entre amostras (em ms)
unsigned char canal_an = 0;     //Canal analógico de leitura 
unsigned char canal_pwm = 2;         //Canal de escrita PWM
unsigned char pwm_degrau = 0;     //razao ciclica aplicada no degrau
unsigned char offset_leitura = 0; //offset da posição de leitura da amostra
unsigned char atraso_degrau = 0;
unsigned char degrau = 0;


void medir(void);
void responder(void);
void processarMensagem(void);
void iniciaAD(void);

enum ESTADOS_TYPE {AGUARDANDO_MSG_ST, PROCESSANDO_MSG_ST, AGUARDANDO_MEDICAO_ST, RESPONDER_ST};

ESTADOS_TYPE estados_st;


void setup() {
  Serial.begin(115200);
  pinMode(13, OUTPUT);
  estados_st = AGUARDANDO_MSG_ST;
}

void loop() {
  switch (estados_st){
    case AGUARDANDO_MSG_ST:
      if (dado_novo == 1){
        estados_st = PROCESSANDO_MSG_ST;
      }
      break;

    case PROCESSANDO_MSG_ST:
      processarMensagem();
      if ((data_in_serial[0] == 1) || (data_in_serial[0] == 9)){
        estados_st = AGUARDANDO_MEDICAO_ST;
      }
      else{
        estados_st = RESPONDER_ST;
      }   
      break;
    
    case AGUARDANDO_MEDICAO_ST:
        if (medindo == 0){
          digitalWrite(13, LOW);
          estados_st = RESPONDER_ST;
        }
      break;

    case RESPONDER_ST:
      responder();  
      dado_novo = 0;
      estados_st = AGUARDANDO_MSG_ST;
      break;

    default:
      break;
  }
}

void medir(){
  digitalWrite(13, HIGH);

  // Configura o ADC
  ADMUX = 0x40 | (canal_an & 0x0F); //Referencia no AVcc com capacitor externo (normal do arduino)
                                        //Justificado a direita (ADLAR = 0;)
                                        //determina o canal


  if (canal_an <= 5){
    DIDR0 = (1 << canal_an); //torna o canal digital desabilitado
  }

  ADCSRA = 0xC7;
              //ADPS0 = 1;  //Seleciona o Pré-scale para 128 (D0)
              //ADPS1 = 1;
              //ADPS2 = 1;
              //ADIE = 0; //Habilita Interrupção
              //ADIF = 0; //Limpa o flag
              //ADATE = 0; //Habilita Auto triger
              //ADSC = 1; //Inicia conversão AD              
              //ADEN = 1; // Habilita o AD     (D7)    
  ADCSRB = 0x00;     
  while(ADCSRA & (1 << ADSC));

  medindo = 1;  

  Timer1.initialize(periodo_amostragem*10);
  Timer1.attachInterrupt(iniciaAD);
   
  
}

void iniciaAD(void){
  static int idx = 0;
  //amostras[idx] = analogRead(canal_an);

  if ((degrau == 1) and (idx == atraso_degrau)){
    analogWrite(canal_pwm, pwm_degrau);
  }

  ADCSRA |= 0x40;

  //ADCSRA = ADCSRA | (1 << ADSC);
  while(ADCSRA & (1 << ADSC));
  int ad_low = ADCL;
  int ad_high = ADCH;
  amostras[idx] = (ad_high<<8) | ad_low;

  if (idx < num_amostras){
    idx = idx + 1;
  }
  else{
    idx = 0;
    Timer1.detachInterrupt();
    medindo = 0;
  } 
}

void responder(){
  Serial.print(data_in_serial[0]);
  switch (data_in_serial[0]) {
    case 1:
      Serial.print(amostras[0]);
      break;
    case 2:
      Serial.print(periodo_amostragem);
      break;
    case 3:
      Serial.print(canal_an);
      break;
    case 4:
      Serial.print(amostras[(int)offset_leitura*256 + (int)data_in_serial[1]]);
      break;
    case 5:
      Serial.print(data_in_serial[1]);
      break;
    case 6:
      Serial.print(canal_pwm);
      break;
    case 7:
      Serial.print(data_in_serial[1]);
      break;
    case 8:
      Serial.print(pwm_degrau);
      break;
    case 9:
      degrau = 0;
      Serial.print(amostras[0]);
      break; 
    case 10:
      Serial.print(atraso_degrau);
      break;
    default:
      break; 
  }  
  Serial.print('\n');
}

void processarMensagem(){
  switch (data_in_serial[0]) {
    case 1:
      num_amostras = (int)offset_leitura*256 + data_in_serial[1];
      if (num_amostras > MAX_NUM_AMOSTRA){
        num_amostras = MAX_NUM_AMOSTRA;
      }
      medir();
      break;
    case 2:
      periodo_amostragem = data_in_serial[1];
      break;
    case 3:
      canal_an = data_in_serial[1];
      break;
    case 4:
      break;
    case 5:
      offset_leitura = data_in_serial[1];
      break;
    case 6:
      canal_pwm = data_in_serial[1];
      pinMode(canal_pwm, OUTPUT);
      break;
    case 7:
      analogWrite(canal_pwm, data_in_serial[1]);
      break;
    case 8:
      pwm_degrau = data_in_serial[1];
      break;
    case 9:
      num_amostras = (int)offset_leitura*256 + data_in_serial[1];
      if (num_amostras > MAX_NUM_AMOSTRA){
        num_amostras = MAX_NUM_AMOSTRA;
      }
      degrau = 1;
      medir();
      break;  
    case 10:
      atraso_degrau = data_in_serial[1];
      break;  
    default:
      break;
  }
}

void serialEvent() {  
  static char countSerial = 0;
  while (Serial.available()){
    if (dado_novo == 0){
      data_in_serial[countSerial] = (unsigned char)Serial.read();
      if (countSerial == SIZE_DATA_IN_SERIAL - 1){
        countSerial = 0;
        dado_novo = 1; 
      }
      else{
        countSerial = countSerial + 1;
      }
    }
  }
}
