#include <EEPROM.h>

char newline = ' ';

void setup(){
    Serial.setTimeout(1000000);
    EEPROM.write(8, 123);
    Serial.begin(115200);
    while(!Serial){
        ;
    }
}

void loop(){
  delay(1000);
  if(Serial.available() > 0){
    char request = Serial.read();
    bool success = handleRequest(request);
    //if (!success) {
    //    Serial.println("bad request: [" + request + "]");
    //}
  }

}

bool handleRequest(char request){

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
    long sharedModulus = getPrivateExp();
    String nonceStr = Serial.readStringUntil(newline);
    long nonce = nonceStr.toInt();
    long response = encrypt(nonce,privateKey,sharedModulus);
    Serial.println(4);
    Serial.println(nonceStr);
    Serial.println(response);
}

long encrypt(long message, long privateKey, long sharedModulus) {  
    return expmod(message, privateKey, sharedModulus);
}

bool checkGetIDRequest(char request){
    if (request == 1){
        return true;
    }
    else{
        return false;
    }

}

bool checkEncryptionRequest(char request){
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

long getPrivateKey(){
    long privateKey = 0;
    for(int i = 0; i<4; i++){
        privateKey += EEPROM.read(i);
        privateKey *= 256;
    }
    return privateKey;
}

long getPrivateExp(){
    long sharedModulus = 0;
    for(int i = 4; i<8; i++){
        sharedModulus += EEPROM.read(i);
        sharedModulus *= 256;
    }
    return sharedModulus;
}

long expmod(long a, long b, long c) {
    long x = 1;
    while(b > 0) {
        if((b & 1) == 1) {
            x = (x*a) % c;
        }
        a = (a*a) % c;
        b >>= 1;
    }
    return x % c;
}



