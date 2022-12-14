import os
import time
import struct
import numpy as np
import sklearn.neural_network
import pickle

#====================================================
#NEURAL NETWORK
#====================================================

#Example Full
#https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html
#sklearn.neural_network.MLPRegressor(hidden_layer_sizes=(100,), activation='relu', *, solver='adam', alpha=0.0001, batch_size='auto', learning_rate='constant', learning_rate_init=0.001, power_t=0.5, max_iter=200, shuffle=True, random_state=None, tol=0.0001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True, early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08, n_iter_no_change=10, max_fun=15000)

#activation{‘identity’, ‘logistic’, ‘tanh’, ‘relu’}, default=’relu’
#solver{‘lbfgs’, ‘sgd’, ‘adam’}, default=’adam’

#sklearn.neural_network.MLPClassifier(hidden_layer_sizes=(100,), activation='relu', *, solver='adam', alpha=0.0001, batch_size='auto', learning_rate='constant', learning_rate_init=0.001, power_t=0.5, max_iter=200, shuffle=True, random_state=None, tol=0.0001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True, early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08, n_iter_no_change=10, max_fun=15000)







MaxEpoc = 200
#Crear el Modelo
model = sklearn.neural_network.MLPRegressor(
    #activation='relu',
    #activation='logistic',
    activation='tanh',
    #solver='sgd',
    solver='adam',
    max_iter=20000,
    learning_rate_init=0.0001,
    #learning_rate_init=0.2,
    #alpha=0.0001,
    #power_t=0.5,
    verbose=True,
    #verbosity=100,
    n_iter_no_change=100000,
    hidden_layer_sizes=(256))







print("Start Training")

#====================================================
#
#====================================================







InputAdaptedArray = []
OutputAdaptedArray = []

def DirInToArray(DirPath):
    dir_list = os.listdir(DirPath)
    print(DirPath)
    
    #console.log(dir_list)
    return dir_list


#============================================================
#Adaptar el numero entre 0 y 1. Ej, 0=0 255=1 127=0.5
def AdaptNumber(NumberIn, MaxNumber):
    AdaptedNumber = (1 / MaxNumber) * NumberIn
    rounded = round((AdaptedNumber * 100) / 100, 2)
    return rounded

#============================================================
def AdatpArray(HeaderLength, bufferData):
    AdaptedArray = []
    for j in range(HeaderLength, len(bufferData)):
        AdaptedArray.append(AdaptNumber(bufferData[j], 255))
        #AdaptedArray[j] = AdaptNumber(bufferData[j], 255)
    
    return AdaptedArray
#============================================================
   



InputPath = './TrainingSet/Inputs/'
OutputPath = './TrainingSet/Outputs/'
InputFileNameArray = []
OutputFileNameArray = []

InputFileNameArray = DirInToArray(InputPath)
OutputFileNameArray = DirInToArray(OutputPath)



#====================================================
#FILE HEADER
#====================================================
print("-------------------------------")
#Get Full Length
fileIN = "./TrainingSet/Inputs/" + InputFileNameArray[0]

#====================================================
if fileIN.lower().find('wav') > -1: FileType = 'wav'
if fileIN.lower().find('bmp') > -1: FileType = 'bmp'
print('FileType = ' + FileType)
#====================================================

file_stats = os.stat(fileIN)

#====================================================
# WAV
#====================================================
if FileType == 'wav':
    FullFileLength = file_stats.st_size 
    #InputFileHeaderLength = 46
    InputFileHeaderLength = 78
    WAVWidth = FullFileLength - InputFileHeaderLength 
#Debug  
    print("FullFileLength " + str(FullFileLength))
    print("InputFileHeaderLength " + str(InputFileHeaderLength))
    print("WAVWidth " + str(WAVWidth))
    print("-------------------------------")
#====================================================
# BMP
#====================================================
if FileType == 'bmp':
    print("-------------------------------")
    flnm = InputPath + InputFileNameArray[0] 
    print(flnm)
    #Open File
    with open(flnm, "rb") as f:
        data = bytearray(f.read())
    #Get Width and Height
    BMWidth = struct.unpack_from('<i', data, 18)
    BMHeight = struct.unpack_from('<i', data, 22)
    BMPWidth = int(BMWidth[0])
    BMPHeight = int(BMHeight[0])
    
    #Get Full Length
    file = open("./TrainingSet/Inputs/" + InputFileNameArray[0], "rb")
    Lbuffer = file.read()
    file.close()
    FullFileLength = len(Lbuffer) 

    #Where Pixel Data begin
    BMOffset = FullFileLength - ((BMPWidth * 3) * BMPHeight)
    InputFileHeaderLength = BMOffset

    ModelWidth = BMPWidth * 3
    ModelHeight = BMPHeight

    
    #Debug  
    print("Width " + str(BMPWidth))
    print("Height " + str(BMPHeight))
    print("Offset " + str(InputFileHeaderLength))
    print("FULL Length " + str(FullFileLength))
    print("RAW Length " + str(FullFileLength - InputFileHeaderLength))
    print("-------------------------------")
#====================================================










BuffersArray = []
#por cada archivo

print(len(InputFileNameArray))



#************************************************************
#Por Cada Archivo de Entrada
StTimeCount = 0
for i in range(len(InputFileNameArray)):
    print("IN")
    print(InputFileNameArray[i])

    StTimePass = time.time() - StTimeCount
    StTimeSec = (len(InputFileNameArray) - i)  * StTimePass
    StTimeMin = StTimeSec / 60
    print("Stimated Time: " + str(StTimeMin) + " min")
    StTimeCount = time.time()
#************************************************************
    #GET INPUT FILE BUFFER
    file = open("./TrainingSet/Inputs/" + InputFileNameArray[i], "rb")
    buffer = file.read()
    #print(len(buffer) - InputFileHeaderLength)
    
    InputAdaptedArray = AdatpArray(InputFileHeaderLength, buffer)



    print("OUT")
    print(OutputFileNameArray[i])
#************************************************************
    #GET OUTPUT FILE BUFFER
    file = open("./TrainingSet/Outputs/" + OutputFileNameArray[i], "rb")
    buffer = file.read()
    
    OutputAdaptedArray = AdatpArray(InputFileHeaderLength, buffer)
#************************************************************

#====================================================
# BMP
#====================================================
    if FileType == 'bmp':
        xs = np.array(InputAdaptedArray).reshape(ModelHeight, ModelWidth)
        ys = np.array(OutputAdaptedArray).reshape(ModelHeight, ModelWidth)
#====================================================
# WAV
#====================================================
    if FileType == 'wav':
        xs = np.array(InputAdaptedArray).reshape(-1, 1)
        ys = np.array(OutputAdaptedArray).reshape(-1, 1).ravel()
    print('In Length: ' + str(len(xs)))
    print('Out Length: ' + str(len(ys)))
    #print(OutputAdaptedArray)
    #Por cada epoca
#====================================================
#ENTRENAR
#====================================================
    for k in range(MaxEpoc):
        model.partial_fit(xs, ys)
        print('File: ' + str(i) + '/' + str(len(InputFileNameArray)))
        print('Epoc: ' + str(k))
#====================================================


print("Save Model")
filename = 'network_state.mdl'
pickle.dump(model, open(filename, 'wb'))

print("END")
