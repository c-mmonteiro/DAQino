#from scipy.fft import fft, fftfreq, fftshift
#from scipy.signal.windows import blackman
import numpy as np


class processaDados:
    def __init__(self, dados, periodo_amostragem) -> None:
        self.dados = dados
        self.periodo_amostragem = periodo_amostragem




    def freqCruzamentoZero (self):
        zero_cross = []
        valor_medio = sum(self.dados)/len(self.dados)
        
        for idx, d in enumerate(self.dados):
            if idx > 0:
                if ((d <= valor_medio) and (self.dados[idx-1] > valor_medio)):
                    zero_cross.append(idx)
        
        if len(zero_cross) >= 2:
            return 1/(((zero_cross[1]) - zero_cross[0])*self.periodo_amostragem)
        else:
            return -1
        
    def amostrasCruzamentoZero (self):
        zero_cross = []
        valor_medio = sum(self.dados)/len(self.dados)
        
        for idx, d in enumerate(self.dados):
            if idx > 0:
                if ((d <= valor_medio) and (self.dados[idx-1] > valor_medio)):
                    zero_cross.append(idx)
        
        if len(zero_cross) >= 2:
            return ((zero_cross[1]) - zero_cross[0])
        else:
            return -1
        
    def fourier(self):
        # Number of sample points
        N = len(self.dados)

        x = np.linspace(0.0, N*self.periodo_amostragem, N, endpoint=False)

        yf = fft(self.dados)
        xf = fftfreq(N, self.periodo_amostragem)
        xf = fftshift(xf)
        yplot = fftshift(yf)

        return xf, yplot
