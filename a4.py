import numpy as np
import matplotlib.pyplot as plt
import numpy.random as nr

blockLength = 1000; # Number of symbols in block
nBlocks = 50000; # Number of blocks
EbdB = np.arange(1.0,45.1,4.0); # Energy per bit Eb in dB
Eb = 10**(EbdB/10); # Energy per bit Eb
No = 1; # Total noise power No
SNR = 2*Eb/No; # Signal-to-noise power ratio
SNRdB = 10*np.log10(SNR); # SNR in dB
BER = np.zeros(len(EbdB)); # Bit-error rate
BERt = np.zeros(len(EbdB)); # Bit-error rate from formula

for blk in range(nBlocks):
    # Rayleigh fading channel coefficient with average power unity
    h = (nr.normal(0.0, 1.0, 1)+1j*nr.normal(0.0, 1.0, 1))/np.sqrt(2);
    # Complex Gaussian noise, I/Q power No/2
    noise = nr.normal(0.0, np.sqrt(No/2), blockLength)+1j*nr.normal(0.0, np.sqrt(No/2), blockLength);
    BitsI = nr.randint(2,size=blockLength); # I channel bits
    BitsQ = nr.randint(2,size=blockLength); # Q channel bits
    Sym = (2*BitsI-1)+1j*(2*BitsQ-1); # Complex symbols each power 2Eb
    
    for K in range(len(SNRdB)):
        TxSym=np.sqrt(Eb[K])*Sym; #Calculating transmitting symbol
        RxSym=h*TxSym+noise; #Calculating transmitting symbol(y=h*x+n)
        EqSym=RxSym/h;
        DecBitsI=(np.real(EqSym)>0); #Detecting I bits
        DecBitsQ=(np.imag(EqSym)>0); #Detecting Q bits
        BER[K]=BER[K]+np.sum(DecBitsI !=BitsI)+np.sum(DecBitsQ !=BitsQ); #Total BER

BER = BER/blockLength/nBlocks/2; # Evaluating average bit error rate    
BERt = 1/2/SNR; # Evaluating bit error rate from formula 
# Plotting bit-error rate from simulation and formula
plt.yscale('log')
plt.plot(SNRdB, BER,'g-');
plt.plot(SNRdB, BERt,'ro');
plt.grid(1,which='both')
plt.suptitle('BER for Rayleigh Fading Channel QPSK')
plt.legend(["BER","BER Theory"], loc ="lower left");
plt.xlabel('SNR (dB)')
plt.ylabel('BER') 



