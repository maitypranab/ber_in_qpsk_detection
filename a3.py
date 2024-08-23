import numpy as np
import matplotlib.pyplot as plt
import numpy.random as nr
from scipy.stats import norm
def Q(x):
    return 1-norm.cdf(x);

blockLength = 1000; # Number of symbols in block
nBlocks=10000; # Number of blocks
EbdB = np.arange(1.0,10.1); # Energy per bit Eb in dB
Eb = 10**(EbdB/10); # Energy per bit Eb
No = 1; # Total noise power No
SNR = 2*Eb/No; # Signal-to-noise power ratio
SNRdB = 10*np.log10(SNR); # SNR in dB
SER = np.zeros(len(EbdB)); # Bit-error rate
BER = np.zeros(len(EbdB));  # Bit-error rate from formula

for blk in range(nBlocks):
    BitsI=nr.randint(2,size=blockLength); # I channel bits
    BitsQ=nr.randint(2,size=blockLength); # Q channel bits
    Sym=(2*BitsI-1)+1j*(2*BitsQ-1); # Complex symbols each power 2Eb
    # Complex Gaussian noise, I/Q power No/2
    noise=nr.normal(0.0,np.sqrt(No/2),blockLength)+1j*nr.normal(0,np.sqrt(No/2),blockLength);                   
    for K in range(len(EbdB)):
        TxSym=np.sqrt(Eb[K])*Sym; #Calculating transmitting symbol
        RxSym=TxSym+noise; #Calculating receiving symbol(y=x+n)
        DecBitsI=(np.real(RxSym)>0); #Detecting I bits
        DecBitsQ=(np.imag(RxSym)>0); #Detecting Q bits
        SER[K]=SER[K]+np.sum(np.logical_or(DecBitsI !=BitsI,DecBitsQ !=BitsQ)); #Total SER
        BER[K]=BER[K]+np.sum(DecBitsI !=BitsI)+np.sum(DecBitsQ !=BitsQ); #Total BER
        
    
SER = SER/blockLength/nBlocks; # Evaluating SYMBOL error rate
BER = BER/blockLength/nBlocks/2; # Evaluating bit error rate
# Plotting bit-error rate and symbol error rate from simulation and formula
plt.yscale('log')
plt.plot(SNRdB, SER,'g-');
plt.plot(SNRdB, 2*Q(np.sqrt(SNR)),'ro');
plt.plot(SNRdB, BER,'b-.');
plt.plot(SNRdB, Q(np.sqrt(SNR)),'ms');
plt.grid(1,which='both')
plt.suptitle('BER and SER for AWGN Channel QPSK')
plt.legend(["SER","SER Theory","BER","BER Theory"], loc ="lower left");
plt.xlabel('SNR (dB)')
plt.ylabel('SER') 
