#include <EEPROM.h>

char newline = '\n';

void setup(){
    Serial.setTimeout(1000000);
    Serial.begin(115200);
    while(!Serial){
        ;
    }
}

void loop(){
    int request = readline().toInt();
    bool success = handleRequest(request);
}

String readline() {
  char lastChar = 0;
  String line = "";
  while (lastChar != '\n') {
    if (Serial.available() > 0) {
      lastChar = Serial.read();
      line = line + String(lastChar);
    }
  }
  return line;
}

bool handleRequest(int request){

    if (checkGetIDRequest(request)){
        sendIDNumber();
    }
    else if (checkEncryptionRequest(request)){
        sendEncrpytedNonce();
    } else {
      return false;
    }
    return true;
}

void sendIDNumber(){
    Serial.println(2);
    Serial.println(EEPROM.read(8));
}

void sendEncrpytedNonce(){
    long privateKey = getPrivateKey();
    long sharedModulus = getSharedModulus();
    String nonceStr = readline();
    long nonce = nonceStr.toInt();
    long response = encrypt(nonce,privateKey,sharedModulus);
    Serial.println(4);
    Serial.println(nonce);
    Serial.println(response);
}

long encrypt(long message, long privateKey, long sharedModulus) {  
    return expmod(message, privateKey, sharedModulus);
}

bool checkGetIDRequest(int request){
    if (request == 1){
        return true;
    }
    else{
        return false;
    }

}

bool checkEncryptionRequest(int request){
    if (request == 3){
        return true;
    }
    else{
        return false;
    }
}

long getMessage(){
    long message = 0;
    for(int i = 0; i<4; i++){
        message += Serial.read();
        message *= 256;
    }
    return message;
}

void setPrivateKey(long privateKey) {
    for(int i = 3; i >= 0; i--){
        EEPROM.write(i, privateKey % 256);
        privateKey = privateKey / 256;
    }
}

void setSharedModulus(long sharedModulus){
    for(int i = 7; i >= 4; i--){
        EEPROM.write(i, sharedModulus % 256);
        sharedModulus = sharedModulus / 256;
    }
}

long getPrivateKey(){
    long num = EEPROM.read(0);
    for(int i = 1; i<4; i++){
        num *= 256;
        num += EEPROM.read(i);
    }
    return num;
}

long getSharedModulus(){
    long num = EEPROM.read(4);
    for(int i = 5; i<8; i++){
        num *= 256;
        num += EEPROM.read(i);
    }
    return num;
}

long expmod(long long a, long long b, long long c) {
    long long x = 1;
    while(b > 0) {
        if((b & 1) == 1) {
            x = (x*a) % c;
        }
        a = (a*a) % c;
        b >>= 1;
    }
    return x % c;
}



