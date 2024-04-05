import time
import serial

class DAQ:
    def __init__(self, porta) -> None:
        # Iniciando conexao serial
        self.porta = porta
        self.amostras_lista = []
        self.comport = serial.Serial(porta, 115200, timeout=5)# Setando timeout 1s para a conexao
        # Time entre a conexao serial e o tempo para escrever (enviar algo)
        time.sleep(1.8) # Entre 1.5s a 2s

        self.comport.read()

    def fecharDAQ(self):
        # Fechando conexao serial
        self.comport.close()

    def lerResposta(self):
        serial_bruto = self.comport.readline()
        print(f'Bruto: {serial_bruto}')
        resposta_lista = list(serial_bruto)
        tamanho_lista = len(resposta_lista)
        #valor_amostra = "".join(map(chr, resposta_lista[1:tamanho_lista-1]))
        valor_amostra = int(bytearray(resposta_lista[1:tamanho_lista-1]))
        print(f'Lista: {resposta_lista} \nAmostra: {valor_amostra}\n')
        return valor_amostra
        
    def fazerConversaoAD(self, numero_de_amostras):        
        self.comport.flush()
        if ((numero_de_amostras >= 0) and (numero_de_amostras <= 255)):
            self.comport.write(bytearray([5,0]))
            self.lerResposta()
            self.comport.write(bytearray([1,numero_de_amostras]))
        elif ((numero_de_amostras >= 256) and (numero_de_amostras <= 511)):
            self.comport.write(bytearray([5,1]))
            self.lerResposta()
            self.comport.write(bytearray([1,numero_de_amostras - 256]))
        elif ((numero_de_amostras >= 512) and (numero_de_amostras <= 767)):
            self.comport.write(bytearray([5,2]))
            self.lerResposta()
            self.comport.write(bytearray([1,numero_de_amostras - 512]))
        self.lerResposta()        
        self.amostras_lista = self.lerListaAmostras(numero_de_amostras)
        return self.amostras_lista
    
    def configurarPeriodo(self, periodo):
        aux = bytearray([2,periodo])
        self.comport.write(aux)
        if periodo == self.lerResposta():
            return 0
        else:
            return -1
        
    def configurarCanalAD(self, canal):
        self.comport.write(bytearray([3,canal]))
        if canal == self.lerResposta():
            return 0
        else:
            return -1

    def lerListaAmostras(self, quantidade):
        amostras_lista = []
        if quantidade > 0:
            for idx in range(quantidade):
                if (idx == 0):
                    self.comport.write(bytearray([5,0]))
                    self.lerResposta()
                elif (idx == 256):
                    self.comport.write(bytearray([5,1]))
                    self.lerResposta()
                elif (idx == 512):
                    self.comport.write(bytearray([5,2]))
                    self.lerResposta()

                if ((idx >= 0) and (idx <= 255)):
                    self.comport.write(bytearray([4,idx]))
                elif ((idx >= 256) and (idx <= 511)):
                    self.comport.write(bytearray([4,idx - 256]))
                elif ((idx >= 512) and (idx <= 767)):
                    self.comport.write(bytearray([4,idx - 512]))

                amostra = self.lerResposta()
                amostras_lista.append(amostra) 

        return amostras_lista
    
    def configCanalPWM(self, canal):
        self.comport.write(bytearray([6,canal]))
        if canal == self.lerResposta():
            return 1
        else:
            return 0
    
    def configRazaoCiclicaPWM(self, razao_ciclica):
        self.comport.write(bytearray([7,razao_ciclica]))
        if razao_ciclica == self.lerResposta():
            return 1
        else:
            return 0
        
    def configRazaoCiclicaDegrau(self, razao_ciclica):
        self.comport.write(bytearray([8,razao_ciclica]))
        if razao_ciclica == self.lerResposta():
            return 1
        else:
            return 0
        
    def respostaDegrau(self, numero_de_amostras):
        self.comport.flush()
        if ((numero_de_amostras >= 0) and (numero_de_amostras <= 255)):
            self.comport.write(bytearray([5,0]))
            self.lerResposta()
            self.comport.write(bytearray([9,numero_de_amostras]))
        elif ((numero_de_amostras >= 256) and (numero_de_amostras <= 511)):
            self.comport.write(bytearray([5,1]))
            self.lerResposta()
            self.comport.write(bytearray([9,numero_de_amostras - 256]))
        elif ((numero_de_amostras >= 512) and (numero_de_amostras <= 767)):
            self.comport.write(bytearray([5,2]))
            self.lerResposta()
            self.comport.write(bytearray([9,numero_de_amostras - 512]))
        self.lerResposta()
        self.amostras_lista = self.lerListaAmostras(numero_de_amostras)
        return self.amostras_lista
    
    def configAtrasoDegrau(self, atraso):
        self.comport.write(bytearray([10,atraso]))
        if atraso == self.lerResposta():
            return 1
        else:
            return 0
    
    def amostrasVolt(self):
        amostras_volt_lista = [] 

        for amostra in self.amostras_lista:
            volt = 5*amostra/1023.0
            amostras_volt_lista.append(volt)

        return amostras_volt_lista


