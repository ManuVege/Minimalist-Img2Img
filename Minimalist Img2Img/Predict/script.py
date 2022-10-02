import math
import pickle
import struct
import numpy as np
import sklearn.neural_network
from os.path import exists


#Is BMP or WAV?
if exists("./InputOutputFile/In.wav") == True: FileType = 'wav'
if exists("./InputOutputFile/In.bmp") == True: FileType = 'bmp'
print('FileType = ' + FileType)


#Get the buffer of the In File, will be used for the Header
if FileType == 'wav':
    INfile = open("./InputOutputFile/In.wav", "rb")
if FileType == 'bmp':
    INfile = open("./InputOutputFile/In.bmp", "rb")
INbuffer = INfile.read()
INbufferAr = bytearray(INbuffer)


# Create a Neural Network
# load the model from disk
model = pickle.load(open("network_state.mdl", 'rb'))







#============================================================
#Adaptar el numero entre 0 y 1. Ej, 0=0 255=1 127=0.5
def AdaptNumber(NumberIn, MaxNumber):
    AdaptedNumber = (1 / MaxNumber) * NumberIn
    rounded = round((AdaptedNumber * 100) / 100, 2)
    return rounded

#============================================================
def AdaptArray(HeaderLength, bufferData):
    AdaptedArray = []
    for j in range(HeaderLength, len(bufferData)):
        AdaptedArray.append(AdaptNumber(bufferData[j], 255))
        #AdaptedArray[j] = AdaptNumber(bufferData[j], 255)
    
    return AdaptedArray
#============================================================
#============================================================


#preparar la salida binaria
iBinary = ''


#====================================================
# WAV
#====================================================
if FileType == 'wav':
    FullFileLength = len(INbufferAr)
    InputFileHeaderLength = 78
    WAVWidth = FullFileLength - InputFileHeaderLength 
    print(WAVWidth)
#====================================================
# BMP
#====================================================
if FileType == 'bmp':
    print("-------------------------------")
    #Open File
    InFile = './InputOutputFile/In.bmp'
    print(InFile)
    with open(InFile, "rb") as f:
        data = bytearray(f.read())
    #Get Width and Height
    BMWidth = struct.unpack_from('<i', data, 18)
    BMHeight = struct.unpack_from('<i', data, 22)
    BMPWidth = int(BMWidth[0])
    BMPHeight = int(BMHeight[0])

    ModelWidth = BMPWidth * 3
    ModelHeight = BMPHeight
    
    #Get Full Length
    file = open(InFile, "rb")
    Lbuffer = file.read()
    file.close()
    FullFileLength = len(Lbuffer) 

    #Where Pixel Data begin
    BMOffset = FullFileLength - ((BMPWidth * 3) * BMPHeight)
    InputFileHeaderLength = BMOffset

    #Debug  
    print("Width " + str(BMPWidth))
    print("Height " + str(BMPHeight))
    print("Offset " + str(InputFileHeaderLength))
    print("FULL Length " + str(FullFileLength))
    print("RAW Length " + str(FullFileLength - InputFileHeaderLength))
    print("-------------------------------")
#=================================================
    



AdaptedDataBuffer = bytearray()
AdaptedDataBuffer = AdaptArray(InputFileHeaderLength, INbufferAr)


def predecir(inputP):

#====================================================
# BMP
#====================================================
    if FileType == 'bmp':
        xs = np.array(inputP).reshape(ModelHeight, ModelWidth)
        print(FileType)
#====================================================
# WAV
#====================================================
    if FileType == 'wav':
        xs = np.array(inputP).reshape(-1, 1)
        print(FileType)
    
    #Predict
    result = model.predict(xs)
    
#====================================================
# BMP
#====================================================
    if FileType == 'wav':
        ArrayToFile1D(result, "./InputOutputFile/Out.wav")
#====================================================
# WAV
#====================================================
    if FileType == 'bmp':
        ArrayToFile2D(result, "./InputOutputFile/Out.bmp")
	


newFileByteArray = bytearray()







#============================================================
#WAV 1D
#============================================================
def ArrayToFile1D(iArray, iFileName):
    global iBinary
    global newFileByteArray
    # DEBES HACER QUE EL ARRAY SEA BINARIO
    #Por cada Byte, Transformar a 255
    for i in range(len(iArray)):
        #Adaptar el numero entre 0 y 255. Ej, 0=0 1=255 0.5=127
        XiArray = int(255 * iArray[i])
        if XiArray<0: XiArray=0
        if XiArray>255: XiArray=255
        newFileByteArray.append(XiArray)
    #Por cada byte del Resultado, empezando despues de InputFileHeaderLength
    for k in range(len(newFileByteArray)):
        #Reemplazo el Pixel Data con los Resultados
        INbufferAr[InputFileHeaderLength + k] = newFileByteArray[k]
    
    #print('INbufferAr')
    #print(len(INbufferAr))
    
    file = open(iFileName, "wb")
    #Save the file
    file.write(INbufferAr)
    file.close()

#============================================================
#BMP 2D
#============================================================
def ArrayToFile2D(iArray, iFileName):
    global iBinary
    global newFileByteArray
    # DEBES HACER QUE EL ARRAY SEA BINARIO
    #Por cada Renglong
    for i in range(len(iArray)):
        #Por cada Byte
        for j in range(len(iArray[i])):
            XiArray = int(255 * iArray[i][j])
            if XiArray<0: XiArray=0
            if XiArray>255: XiArray=255
            #print(XiArray)
            newFileByteArray.append(XiArray)
    #Por cada byte del Resultado, empezando despues de InputFileHeaderLength
    for k in range(len(newFileByteArray)):
        #Reemplazo el Pixel Data con los Resultados
        INbufferAr[InputFileHeaderLength + k] = newFileByteArray[k]
    
    
    file = open(iFileName, "wb")
    #Save the file
    file.write(INbufferAr)
    file.close()





print(len(AdaptedDataBuffer))
#print(AdaptedDataBuffer)
predecir(AdaptedDataBuffer)

print('> Largo Input')
print(len(INbufferAr))
print('> Largo Output')
print(len(INbufferAr))
