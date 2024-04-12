from daq import *
from processaDados import * #TODO: resolver problema do scipy 

import csv

import serial.tools.list_ports

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

#Problema com o matplotlib: https://learn.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist?view=msvc-170#latest-microsoft-visual-c-redistributable-version

from datetime import datetime, timedelta
import numpy as np

import time

import tkinter as tk
from tkinter import *
from tkinter import messagebox


TEMPO_PERIODO_AQUISICAO = 0.00001

class arduinoDAQ():
    def __init__(self):
        self.canal = 0

        self.com_aberta = 0
        self.complemento_nome_arquivo = 0
        self.script = 0


        #Cria Janela
        self.root = Tk()
        self.root.title('DAQino')
        self.root.geometry("1200x670")

        self.top_frame = Frame(self.root, width=500, height=140)
        self.top_frame.pack(side='top', expand='True', fill = BOTH)

        self.graph_frame = Frame(self.root, width=500, height=530, bg = 'blue')
        self.graph_frame.pack(side='bottom', expand='True', fill = BOTH)

#############################
###########################################################
########### TEXTO (entrada de texto)
        #Texto do Periodo
        self.lbl_periodo = tk.Label(self.top_frame, width=11, height = 1, text="Aq Period:", justify=LEFT)
        self.lbl_periodo.place(y = 15, x = 10)

        self.input_periodo = tk.Text(self.top_frame, width = 10, height = 1)
        self.input_periodo.insert("1.0", str(150))
        self.input_periodo.place(y = 15, x = 100)

        #Texto do Numero de Amostras

        self.lbl_num_amostras = tk.Label(self.top_frame, width=11, height = 1, text="Samples:", justify=LEFT)
        self.lbl_num_amostras.place(y = 45, x = 10)

        self.input_num_amostras = tk.Text(self.top_frame, width = 10, height = 1)
        self.input_num_amostras.insert("1.0", 200)
        self.input_num_amostras.place(y = 45, x = 100)

        #Texto do Numero do Canal Analógico

        self.lbl_num_canal_an = tk.Label(self.top_frame, width=13, height = 1, text="AN Port:", justify=LEFT)
        self.lbl_num_canal_an.place(y = 15, x = 190)

        self.input_num_canal_an = tk.Text(self.top_frame, width = 10, height = 1)
        self.input_num_canal_an.insert("1.0", 0)
        self.input_num_canal_an.place(y = 15, x = 290)

        #Texto do Numero do Canal PWM

        self.lbl_num_canal_pwm = tk.Label(self.top_frame, width=13, height = 1, text="PWM Port:", justify=LEFT)
        self.lbl_num_canal_pwm.place(y = 45, x = 190)

        self.input_num_canal_pwm = tk.Text(self.top_frame, width = 10, height = 1)
        self.input_num_canal_pwm.insert("1.0", 6)
        self.input_num_canal_pwm.place(y = 45, x = 290)

        #Texto do Atraso do Degrau

        self.lbl_atraso_degrau = tk.Label(self.top_frame, width=13, height = 1, text="Step Delay(n):", justify=LEFT)
        self.lbl_atraso_degrau.place(y = 75, x = 190)

        self.input_atraso_degrau = tk.Text(self.top_frame, width = 10, height = 1)
        self.input_atraso_degrau.insert("1.0", 25)
        self.input_atraso_degrau.place(y = 75, x = 290)

        #Texto da Razão Ciclica Final

        self.lbl_razao_ciclica = tk.Label(self.top_frame, width=18, height = 1, text="Duty Cycle/Final Val.:", justify=LEFT)
        self.lbl_razao_ciclica.place(y = 15, x = 380)

        self.input_razao_ciclica = tk.Text(self.top_frame, width = 10, height = 1)
        self.input_razao_ciclica.insert("1.0", 120)
        self.input_razao_ciclica.place(y = 15, x = 520)

        #Texto da Razão Ciclica Inicial

        self.lbl_razao_ciclica_pre_degrau = tk.Label(self.top_frame, width=18, height = 1, text="Duty Cycle pre step:", justify=LEFT)
        self.lbl_razao_ciclica_pre_degrau.place(y = 45, x = 380)

        self.input_razao_ciclica_pre_degrau = tk.Text(self.top_frame, width = 10, height = 1)
        self.input_razao_ciclica_pre_degrau.insert("1.0", 0)
        self.input_razao_ciclica_pre_degrau.place(y = 45, x = 520)

        #Texto do Tempo pré degrau

        self.lbl_tempo_pre_degrau = tk.Label(self.top_frame, width=18, height = 1, text="Wait Time(s):", justify=LEFT)
        self.lbl_tempo_pre_degrau.place(y = 75, x = 380)

        self.input_tempo_pre_degrau = tk.Text(self.top_frame, width = 10, height = 1)
        self.input_tempo_pre_degrau.insert("1.0", 0)
        self.input_tempo_pre_degrau.place(y = 75, x = 520)

        #Texto Nome do Arquivo (sem extensão)

        self.lbl_nome_arquivo = tk.Label(self.top_frame, width=11, height = 1, text="File Name:", justify=LEFT)
        self.lbl_nome_arquivo.place(y = 75, x = 630)

        self.input_nome_arquivo = tk.Text(self.top_frame, width = 10, height = 1)
        self.input_nome_arquivo.insert("1.0", 'dados')
        self.input_nome_arquivo.place(y = 75, x = 720)

        #Texto Caminho da pasta de arquivos

        self.lbl_caminho_pasta = tk.Label(self.top_frame, width=12, height = 1, text="File Path:", justify=LEFT)
        self.lbl_caminho_pasta.place(y = 15, x = 630)

        self.input_caminho_pasta = tk.Text(self.top_frame, width = 28, height = 1)
        self.input_caminho_pasta.insert("1.0", 'C:/Users/Carlos/Downloads/DAQino/Dados')
        self.input_caminho_pasta.place(y = 15, x = 720)

        #Texto Caminho do script

        self.lbl_caminho_script = tk.Label(self.top_frame, width=12, height = 1, text="Script Path:", justify=LEFT)
        self.lbl_caminho_script.place(y = 45, x = 630)

        self.input_caminho_script = tk.Text(self.top_frame, width = 28, height = 1)
        self.input_caminho_script.insert("1.0", 'C:/Users/Carlos/Downloads/DAQino/Script/script.csv')
        self.input_caminho_script.place(y = 45, x = 720)

########### CHECLBOX (entrada 1/0)
        #Checkbox do Tempo
        self.var_tempo = IntVar()

        self.cb_tempo = tk.Checkbutton(self.top_frame, text='Time', variable=self.var_tempo, onvalue=1, offvalue=0, command=self.atualizarGrafico)
        self.cb_tempo.place(y=90, x=15)

        #Checkbox do Tipo de Grafico
        self.var_grafico = IntVar()

        self.cb_grafico = tk.Checkbutton(self.top_frame, text='Interpolate', variable=self.var_grafico, onvalue=1, offvalue=0, command=self.atualizarGrafico)
        self.cb_grafico.place(y=115, x=15)

        #Checkbox do Volts
        self.var_volt = IntVar()

        self.cb_volt = tk.Checkbutton(self.top_frame, text='Volts', variable=self.var_volt, onvalue=1, offvalue=0, command=self.atualizarGrafico)
        self.cb_volt.place(y=90, x=110)

        #Checkbox da FFT / Sinal
        self.var_fft = IntVar()

        self.cb_fft = tk.Checkbutton(self.top_frame, text='FFT', variable=self.var_fft, onvalue=1, offvalue=0, command=self.atualizarGrafico)
        self.cb_fft.place(y=115, x=110)

        #Checkbox de Salvar
        self.var_salvar = IntVar()

        self.cb_salvar = tk.Checkbutton(self.top_frame, text='Save Data', variable=self.var_salvar, onvalue=1, offvalue=0)
        self.cb_salvar.place(y=75, x=815)

############## BOTÂO (ativar função)     
        #Botão Medir
        self.btn_medir = Button(self.top_frame, text="Measure", command=self.medir_dados, height = 1, width = 15)
        self.btn_medir.place(y = 105, x = 200)
        self.btn_medir.config(state=DISABLED)

        #Botão Resposta ao degrau
        self.btn_resp_degrau = Button(self.top_frame, text="Step Response", command=self.medir_resp_degrau, height = 1, width = 15)
        self.btn_resp_degrau.place(y = 105, x = 320)
        self.btn_resp_degrau.config(state=DISABLED)

        #Botão Acionar PWM
        self.btn_acionar_pwm = Button(self.top_frame, text="Set PWM", command=self.acionar_pwm, height = 1, width = 15)
        self.btn_acionar_pwm.place(y = 105, x = 440)
        self.btn_acionar_pwm.config(state=DISABLED)


        #Botão Acionar Script
        self.btn_acionar_script = Button(self.top_frame, text="Start Script", command=self.acionar_script, height = 1, width = 15)
        self.btn_acionar_script.place(y = 105, x = 560)
        self.btn_acionar_script.config(state=DISABLED)

        #Botão Sobre
        self.btn_sobre = Button(self.top_frame, text="About", command=self.acionar_sobre, height = 1, width = 15)
        self.btn_sobre.place(y = 105, x = 680)

        #Botão Abrir porta
        self.btn_abrir_porta = Button(self.top_frame, text="Open COM", command=self.abrir_com_porta, height = 1, width = 15)
        self.btn_abrir_porta.place(y = 85, x = 980)

############## Drop Down
        comport_list_hw = serial.tools.list_ports.comports()
        comport_list = []
        comport_descricao_list = []
        for port, desc, hwid  in sorted(comport_list_hw):
            comport_list.append(port)
            comport_descricao_list.append(desc)

        self.comport =  StringVar(self.top_frame)
        self.comport.set(comport_list[0])

        self.lbl_comport = tk.Label(self.top_frame, width=10, height = 1, text="Port:", justify=LEFT)
        self.lbl_comport.place(y = 50, x = 950)

        self.dropDown_comport = OptionMenu(self.top_frame, self.comport, *comport_list)
        self.dropDown_comport.place(y = 50, x = 1010)


############## Label com informação que atualiza
        #Label frequencia
        self.lbl_freq = tk.Label(self.top_frame, width=20, height = 1, text="Frequency: N/C Hz")
        self.lbl_freq.place(y = 20, x = 950)

        #Label Script
        self.lbl_script = tk.Label(self.top_frame, width=20, height = 1, text="", justify=LEFT)
        self.lbl_script.place(y = 105, x = 800)

############## Label fixa
        #Label Grafico
        self.lbl_grafico = tk.Label(self.top_frame, width=20, height = 1, text="Graphic")
        self.lbl_grafico.place(y = 75, x = 35)

        #Figura do IFC
        imagem = tk.PhotoImage(file="ifc.png")
        self.lbl_figura = tk.Label(self.top_frame, image=imagem)
        self.lbl_figura.place(y = 15, x = 1100)

########################################################################################
        
        #Criar figura do Gráfico
        self.fig_graph = Figure(figsize=(5,5), dpi=100)
        self.ax_fig_graph = self.fig_graph.add_subplot()

        self.canvas_graph = FigureCanvasTkAgg(self.fig_graph, self.graph_frame)
        self.canvas_graph.draw()
        self.canvas_graph.get_tk_widget().pack(side = TOP, fill=NONE, expand = True)

        self.tool_bar_graph = NavigationToolbar2Tk(self.canvas_graph, self.graph_frame)
        self.canvas_graph._tkcanvas.pack(side=BOTTOM, fill='both', expand=True)

        self.root.mainloop()

    
    def salvar_dados(self, tipo, razao_ciclica_inicial, razao_ciclica_final, complemento):
        ##Salva os dados
        if (self.var_salvar.get() == 1):
            nome_arquivo = self.input_caminho_pasta.get("1.0",'end-1c') + "/" + self.input_nome_arquivo.get("1.0",'end-1c') + "_" + str(complemento) + ".txt"
            arquivo = open(nome_arquivo, "w")
            arquivo.write(self.input_periodo.get("1.0",END))
            arquivo.write(self.input_num_amostras.get("1.0",END))
            if (tipo == 'M'):
                arquivo.write("M\n")
            elif(tipo == 'D'):
                arquivo.write("D\n")
            arquivo.write(str(razao_ciclica_inicial) + '\n' + str(razao_ciclica_final))
            for amostra in self.amostras_lista:
                arquivo.write('\n' + str(amostra))
            arquivo.close()

    
    def medir_dados(self):

        if (self.com_aberta == 1):

            self.num_amostras = int(self.input_num_amostras.get("1.0",END))
            self.periodo = int(int(self.input_periodo.get("1.0",END))/10.0)

            self.daq.configurarCanalAD(self.canal)
            self.daq.configurarPeriodo(self.periodo)

            self.amostras_lista = self.daq.fazerConversaoAD(self.num_amostras)
            self.amostras_volt_lista = self.daq.amostrasVolt()

            self.salvar_dados('M', 0, 0, self.complemento_nome_arquivo)
            
            ## Calcula a frequencia pelo cruzamento de zero para a label
            freq = processaDados(self.amostras_lista, (self.periodo)*TEMPO_PERIODO_AQUISICAO).freqCruzamentoZero()
            amostras = processaDados(self.amostras_lista, (self.periodo)*TEMPO_PERIODO_AQUISICAO).amostrasCruzamentoZero()
            self.lbl_freq['text'] = f'Frequency: {freq:.2f} Hz {amostras}'


            self.atualizarGrafico()

    
    def medir_resp_degrau(self):

        if (self.com_aberta == 1):

            self.num_amostras = int(self.input_num_amostras.get("1.0",END))
            self.periodo = int(int(self.input_periodo.get("1.0",END))/10.0)

            self.daq.configurarCanalAD(int(self.input_num_canal_an.get("1.0",END)))
            self.daq.configurarPeriodo(self.periodo)

            self.daq.configCanalPWM(int(self.input_num_canal_pwm.get("1.0",END)))
            self.daq.configRazaoCiclicaDegrau(int(self.input_razao_ciclica.get("1.0",END)))
            self.daq.configAtrasoDegrau(int(self.input_atraso_degrau.get("1.0",END)))

            self.daq.configRazaoCiclicaPWM(int(self.input_razao_ciclica_pre_degrau.get("1.0",END)))
            time.sleep(int(self.input_tempo_pre_degrau.get("1.0",END)))
    
            self.amostras_lista = self.daq.respostaDegrau(self.num_amostras)         
            self.amostras_volt_lista = self.daq.amostrasVolt()
                
            self.salvar_dados('D', self.input_razao_ciclica_pre_degrau.get("1.0",'end-1c'), self.input_razao_ciclica.get("1.0",'end-1c'), self.complemento_nome_arquivo)

            ## Calcula a frequencia pelo cruzamento de zero para a label
            freq = processaDados(self.amostras_lista, (self.periodo)*TEMPO_PERIODO_AQUISICAO).freqCruzamentoZero()
            amostras = processaDados(self.amostras_lista, (self.periodo)*TEMPO_PERIODO_AQUISICAO).amostrasCruzamentoZero()
            self.lbl_freq['text'] = f'Frequency: {freq:.2f} Hz {amostras}'


            self.atualizarGrafico()


    def acionar_pwm(self):
        if (self.com_aberta == 1):
            self.daq.configCanalPWM(int(self.input_num_canal_pwm.get("1.0",END)))
            self.daq.configRazaoCiclicaPWM(int(self.input_razao_ciclica.get("1.0",END)))


    def acionar_script(self):

        if (self.com_aberta == 1):
            arquivo = open(self.input_caminho_script.get("1.0",'end-1c'), 'r')
            script = csv.reader(arquivo, delimiter=';')
            for idx, linha in enumerate(script):
                if idx > 0:
                    print(linha)
                    self.lbl_script['text'] = f'Script: {idx}'

                    self.input_num_canal_an.delete("1.0", END)
                    self.input_num_canal_an.insert("1.0", linha[2])
                    self.input_periodo.delete("1.0", END)
                    self.input_periodo.insert("1.0", linha[3])
                    self.input_num_amostras.delete("1.0", END)
                    self.input_num_amostras.insert("1.0", linha[4])
                    self.input_num_canal_pwm.delete("1.0", END)
                    self.input_num_canal_pwm.insert("1.0", linha[5])
                    self.input_razao_ciclica_pre_degrau.delete("1.0", END)
                    self.input_razao_ciclica_pre_degrau.insert("1.0", linha[6])
                    self.input_tempo_pre_degrau.delete("1.0", END)
                    self.input_tempo_pre_degrau.insert("1.0", linha[7])
                    self.input_razao_ciclica.delete("1.0", END)
                    self.input_razao_ciclica.insert("1.0", linha[8])
                    self.input_atraso_degrau.delete("1.0", END)
                    self.input_atraso_degrau.insert("1.0", linha[9])
                    self.var_salvar.set(linha[10])

                    self.complemento_nome_arquivo = linha[0]

                    if (linha[1] == 'm'):
                        self.medir_dados()

                    elif (linha[1] == 'd'):
                        self.medir_resp_degrau()

                    elif (linha[1] == 'p'):
                        self.acionar_pwm()

                    elif (linha[1] == 'e'):
                        time.sleep(int(self.input_tempo_pre_degrau.get("1.0",END)))

                    else:
                        messagebox.showerror(title='Type', message=f'ERRO: Action type unknow on line {idx}!')

            
            self.lbl_script['text'] = ''

    def acionar_sobre(self):
        messagebox.showinfo(title='About', message='Version: 0.01 \nAutor: Carlos A M Monteiro\nDate: 04/2024')

    def abrir_com_porta(self):

        if (self.com_aberta == 0):
            self.daq = DAQ(self.comport.get())
            self.btn_medir.config(state=NORMAL)
            self.btn_resp_degrau.config(state=NORMAL)
            self.btn_acionar_pwm.config(state=NORMAL)
            self.btn_acionar_script.config(state=NORMAL)

            self.btn_abrir_porta.config(text="Close Port")
            self.com_aberta = 1

        else:
            self.daq.fecharDAQ()
            self.btn_abrir_porta.config(text="Open Port")
            self.btn_medir.config(state=DISABLED)
            self.btn_resp_degrau.config(state=DISABLED)
            self.btn_acionar_pwm.config(state=DISABLED)
            self.btn_acionar_script.config(state=DISABLED)
            self.com_aberta = 0


    def atualizarGrafico(self):
        if len(self.amostras_lista) > 0:

            self.ax_fig_graph.clear()

            if (self.var_fft.get() == 1):
                self.ax_fig_graph.set_title("FFT")
                self.ax_fig_graph.set_ylabel("Amplitude / 2 (Volts)")
                self.ax_fig_graph.set_xlabel("Frequency (Hz)")
                x, y = processaDados(self.amostras_volt_lista, (self.periodo + 1)*TEMPO_PERIODO_AQUISICAO).fourier()
                self.ax_fig_graph.scatter(x, y)

            else:
                self.ax_fig_graph.set_title("Analog Measurement")

                #Tensão / Digital
                if(self.var_volt.get() == 1):
                    y = self.amostras_volt_lista
                    self.ax_fig_graph.set_ylabel("Volts")
                else:
                    y = self.amostras_lista
                    self.ax_fig_graph.set_ylabel("Digital Value (0-1023)")

                #Tempo / Amostra
                if(self.var_tempo.get() == 1):
                    x = np.arange(0,0.1*self.num_amostras*self.periodo,0.1*self.periodo)
                    self.ax_fig_graph.set_xlabel("Time (ms)")
                else:
                    x = np.arange(0,self.num_amostras,1)
                    self.ax_fig_graph.set_xlabel("Samples [n]")

                #interpolação / amostra
                if (self.var_grafico.get() == 1):
                    self.ax_fig_graph.plot(x, y)
                else:
                    self.ax_fig_graph.scatter(x, y)
            
            self.ax_fig_graph.grid()

            self.canvas_graph.draw()

arduinoDAQ()