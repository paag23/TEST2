####Bibliotecas ####################

from datetime import datetime, date, timedelta
import calendar 
import  time
from time import sleep
import random
import multiprocessing

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
###############Referencia de Voltaje ADC######################
Voltaje0 = 2.5
Voltaje1 = 3.5
Voltaje2 = 4.5
Ref = 5             
#################Variables Globales###########################

antes = 0.0   #Muetra Anterior
TM = 1000000     #Tiempo de Muestreo en "nanosegundos" 1 miliSegundo = 1 000 000 nanoSegundos; 10000 sp/s

i = 0

alpha0 = 0.05 #Coeficiente de Frecuencia Fitro de Corte X Paso ALto, Paso BAjo
alpha1 = 0.25 #Fitro de Corte Y
alpha2 = 0.15 #Fitro de Corte Z
alpha3 = 0.55 #Frecuencia Fitro de Corte  I

##################Variables de Filtrado de Ruido EMA #################
S0 = 0.0
S1 = 0.0
S2 = 0.0
S3 = 0.0

################## Rangos de Operacion Normal #################

RI_A = 4.500   #Ranglo ALTO
RI_B = 0.600   #Ranglo BAJO

RX_A =  127.53 #3G Ranglo ALTO
RX_B =  29.43  #13G Ranglo BAJO
RY_A =  127.53 #Rango ALTO
RY_B =  29.43  #Rango BAJO
RZ_A =  29.4   #Rango ALTO
RZ_B =  127.53 #Rango BAJO

RrpM_A = 2800  #Rango ALTO
RrpM_B = 100   #Rango BAJO




def Rango( R0, R1, R2, R3, R4 ):

    #Desviacion de Eje X
    if R0>RX_A:
        DI =  R0 - S0
        Variable = 'X'
        ArchivoDesviaciones(Variable, str(R0), str(DI), str(R4))
    elif  R0<RX_B:
        DI =  S0 - R0
        Variable = 'X'
        ArchivoDesviaciones(Variable, str(R0), str(DI), str(R4))
    #Desviacion de Eje Y
    if R1>RY_A:
        DI =  R1 - S1
        Variable = 'Y'
        ArchivoDesviaciones(Variable, str(R1), str(DI), str(R4))
    elif  R1<RY_B:
        DI =  S1 - R1
        Variable = 'Y'
        ArchivoDesviaciones(Variable, str(R1), str(DI), str(R4))
    #Desviacion de Eje Z
    if R2>RZ_A:
        DI =  R2 - S2
        Variable = 'Z'
        ArchivoDesviaciones(Variable, str(R2), str(DI), str(R4))
    elif  R2<RZ_B:
        DI =  S2 - R2
        Variable = 'Z'
        ArchivoDesviaciones(Variable, str(R2), str(DI), str(R4))
    #Desviacion de Corriente 
    if R3>RI_A:
        DI =  R3 - S3
        Variable = 'I'
        ArchivoDesviaciones(Variable, str(R3), str(DI), str(R4))
    elif  R3<RI_B:
        DI =  S3 - R3
        Variable = 'I'
        ArchivoDesviaciones(Variable, str(R3), str(DI), str(R4))
    
    '''PENDIENTE 
    #Desviacion de RPM
    if R4<=RrpM_A and R4<=RrpM_B:
        print ('Pormedio de desviacion')

    '''
############# CREACION DE ARCHIVO BASE DE DATOS para datos Fuera de Rango Normal ###################################
def ArchivoDesviaciones(  Variable, Valor, Desviacion, tiempo  ):

    archivo = open('Base_de_Datos_Desviaciones.txt','a' )
    archivo.write( Variable )
    archivo.write( ',' )
    archivo.write( Valor )
    archivo.write( ',' )
    archivo.write( Desviacion )
    archivo.write( ',' )
    archivo.write( tiempo )
    archivo.write( '\n' )
    archivo.close()


'''
def FiltarjeMedia():
    lista[]
    for low in range (0,100):
        Val_0 += CH0.voltage
        Val_1 += CH1.voltage
        Val_2 += CH2.voltage
        #Val_3 += CH3.voltage
        i++
    lista[0] = Val_0/100
    lista[1] = Val_1/100
    lista[2] = Val_2/100
    #lista[3] = Val_3/100
    
    return lista

'''
############# CREACION DE ARCHIVO BASE DE DATOS Discretizados de Sensores ###################################

def ArchivoTexto(In0, In1, In2, In3, In4, In5):
## Fecha, Hora, muestra, muestra n
    archivo = open('Base_de_Datos.txt','a' )
    archivo.write( In0 )
    archivo.write( ',' )
    archivo.write( In1 )
    archivo.write( ',' )
    archivo.write( In2 )
    archivo.write( ',' )
    archivo.write( In3 )
    archivo.write( ',' )
    archivo.write( In4 )
    archivo.write( ',' )
    archivo.write( In5 )
    archivo.write( '\n' )
    archivo.close()

    #print ( " Archivo de impresión \n", In0, In1, In2, In4 )

    
def Caracterizacion_Acelerometro( C0, C1, C2 ):
    # y = ax + b    C0 = X   C1 = Y   C2 = Z
    # 800mmV/G +-1G ; 850mmV - 2.45V

    #EJE X ACX
    ACX = ( ( 0.8 * C0 ) + 1.65 ) * 4096 / Ref 
    ACX = ACX * 9.81    # G -> m/s2
 
    #EJE Y ACY
    ACY = ( ( 0.8 * C1 ) + 1.65 ) * 4096 / Ref 
    ACY = ACY * 9.81    #G -> m/s2

    #EJE Z ACZ
    ACZ = ( ( 0.8 * C2 ) + 1.65 ) * 4096 / Ref 
    ACZ = ACZ * 9.81    #G -> m/s2

    return ( ACX, ACY, ACZ )


def Caracterizacion_Corriente( C3 ):
    # Sensor ACS712
    #y = ax + b    b = - 2.5 cero positivo
    #Sensibilidad Experiemtal 0.179
    ACI = 0.0
    
    ACI = ( C3 * 4096) / Ref #Cuentas 

    if ACI>=2047:

        ACI =  ACI * (5 / 4096)

        ACI = ( ACI - 2.5 ) / 0.185
        ACI = round ( ACI, 3 )
        #print ("ACI = ",ACI)

    else: ACI = 0
    
    #print ('--------------------------', ACI)
    return ACI
    

def pruebaGIT ():

    print ("Probando prueba GIT-HUB")


def FiltrajeEMA ( A, alpha, S ):
    #EMA Exponential Moving Average
    #A Voltaje de Sensor
    #alpha coeficiente frecuencia de corte de filtro 
    #S Lectura anterion (S-1)
    #print ( "A = ", A)
    
    S = ( alpha * A ) + ( ( 1 - alpha ) * S )

    #print( "--------------------Sub Programa FiltrajeEMA", S ) 
    
    return S


  
while  True:

    try:

        #################Incio de Muestreo  ######################################################
        for vuelta in range( 1, 100000 ):                   #Quitar este ciclo en RaspberryPi#####

            ahora = int (time.monotonic())
            #print (ahora)
            cambio = ( ahora - antes )
            #print( "cambio = ", cambio )            
        
            if ( cambio >= TM ):
                hora = str( datetime.now() )

                #print ( "CORRIENTE S3 = ", S3)

                ############## Funcion de Filtro EMA para señal de Sensor Acelerometro ##########################################
                S0 = FiltrajeEMA( A = random.uniform(0,5), alpha = alpha0, S = S0 ) #Cambiar en RaspberryPi random por A = CH0.voltage
                #print ( "S0 = ", S0 )
                S1 = FiltrajeEMA( A = random.uniform(0,5), alpha = alpha1, S = S1 ) #Cambiar en RaspberryPi random por A = CH1.voltage
                #print ( "S1 = ", S1 )
                S2 = FiltrajeEMA( A = random.uniform(0,5), alpha = alpha2, S = S2 ) #Cambiar en RaspberryPi random por A = CH2.voltage
                #print ( "S2 = ", S2 )
                ################ Funcion de Filtro EMA para señal de Sensor de Corriente electrica ################################
                S3 = FiltrajeEMA( A = 7, alpha = alpha3, S = S3 )                   #Cambiar en RaspberryPi random por A = CH3.voltage
                #print('----------------', S3)
                ################ Funcion de Filtro EMA para señal de Sensor  RPM´s   ##################################
                #PENDIENTE 

                ################ Funcion para Caracterizacion de Sensores #############################################
                T0, T1, T2 = Caracterizacion_Acelerometro( C0 = S0, C1 = S1, C2 = S2 )    #Unidades m/s2
                T3 = Caracterizacion_Corriente( S3 )                                      #Unidades mA
                #T4                                                                       #Unidades RPM/min
                     
                ############# ARCHIVO BASE DE DATOS Discretizados de Sensores ###################################
                ArchivoTexto( hora, str( round ( T0, 4) ), str( round ( T1, 4 ) ), str( round( T2, 4) ), str( round( T3, 4 ) ), str(ahora) )

                antes = ahora  #Actualizacion de Tiempo 

                ############# Funcion para evaluar los  datos fuera de  rango Normal####################################        
                Rango( T0, T1, T2, T3, ahora )


        #print("cambio =  ahora - antes    i ")
        #print( cambio, " = ", ahora, " - ", antes, i )
 
        #print( 'X= {0:.4f} m/s2  Y= {0:.4f} m/s2  Z= {0:.4f} m/s  I= {0:.0f}mA  t= {0:.0f} '. format(T0, T1, T2, T3, ahora ) )
        
    except KeyboardInterrupt:
        print( " \n =>>>>>Finalizado... " )
    break  