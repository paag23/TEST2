##Prueba Cambio de Paradigma##
####Bibliotecas ####################

from datetime import datetime, date, timedelta
import calendar 
import  time
from time import sleep
import random
from Ctes import*
from Modulos import *

################## Librerias en RaspberryPi####################

'''from gpiozero import MCP3008
from gpiozero.tools import scaled

###################Entrada de Sensores ########################
CH0 = MCP3208(0)  # CH0 Acelerometro Eje X
CH1 = MCP3208(1)  # CH1 Acelerometro Eje Y
CH2 = MCP3208(2)  # CH2 Acelerometro Eje Z
CH3 = MCP3208(3)  # CH3 Corriente  
CH4 = MCP3208(5)  # CH4 Velocidad RPMs
#CH5 = MCP3208(5)  # LIBRE 
#CH6 = MCP3208(6)  # LIBRE
#CH7 = MCP3208(7)  # LIBRE

'''

antes = 0.0   #Muetra Anterior
i = 0


Acelerometro_X = Sensores("GY-61-X")
Acelerometro_Y = Sensores("GY-61-Y")
Acelerometro_Z = Sensores("GY-61-Z")
Corriente      = Sensores("ACS712")
BD = Archivo()


while  True:

#################Incio de Muestreo  ######################################################
    for vuelta in range( 1, 10 ):                   #Quitar este ciclo en RaspberryPi#####

        ahora = int (time.monotonic_ns())
        #print (ahora)
        cambio = ( ahora - antes )
        #print( "cambio = ", cambio )

        if ( cambio >= TM ):

           hora = str( datetime.now() )
            #Filtraje 
           S0 = Acelerometro_X.filtro(SIMU_CH0, alpha0, S0)
           S1 = Acelerometro_Y.filtro(SIMU_CH1, alpha1, S1)
           S2 = Acelerometro_Z.filtro(SIMU_CH2, alpha2, S2)
           S3 = Corriente.filtro(SIMU_CH3, alpha3, S3)

           #print ("X = ",S0,"Y = ", S1, "Z = ", S2, "I = ", S3)

           #Caraterizacion 
           T0 = Acelerometro_X.Caracterizacion_Acelerometro(S0)
           T1 = Acelerometro_Y.Caracterizacion_Acelerometro(S1)
           T2 = Acelerometro_Z.Caracterizacion_Acelerometro(S2)
           T3 = Corriente.Caracterizacion_Corriente(S3) 
           
           print("x =",T0,"Y =", T1,"Z =", T2, "I = ", T3)

           antes = ahora  #Actualizacion de Tiempo 

           BD.ArchivoTexto( hora, str( round ( T0, 4) ), str( round ( T1, 4 ) ), str( round( T2, 4) ), str( round( T3, 4 ) ), str(ahora) )

            #hora = str( datetime.now() )
            #print(hora)
        

    
    break      