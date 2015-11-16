def decrypt(message, publicKey, sharedModulus):
    return expmod(long(message), long(publicKey), long(sharedModulus))

def expmod(a,b,c):
    x = 1
    while(b>0):
    	if(b&1==1): x = (x*a)%c
    	a=(a*a)%c
    	b >>= 1
    return x%c
