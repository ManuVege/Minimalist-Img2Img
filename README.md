# Minimalist-Img2Img
Little neural network with Python Sklearn that learns how to create visual effects from examples

Presentation
This code can be configured in different ways to vary all its parameters and fulfill different functions.
Sklearn and Numpy libraries are required.


I think that with this code, the Neural Network could learn any effect.
The model that I have uploaded as an example can color black and white images, works with 256 neurons and weighs about 2mb.
It has been trained with a training set of 227 examples of black and white mandalas as Input in its original color version as Output.
The training set works with 20x20 pixel BMP.
Remember that by creating another training set, you could fulfill other functions and work with higher resolution images.
I have created the code on a Pentium Dual-Core with 2gb of Ram, the training has taken just under an hour.




Manual
The code has two parts: Train and Predict If you are only interested in testing this model, you will only use Predict.
But if you try to create your own model, you will use Train.

Predict
The script uses the file "./InputOutputFile/In.bmp" and creates "./InputOutputFile/Out.bmp"
This example model is trained with 20x20 pixel BMPs weighing exactly 1338 bytes. With another size, it could not work (the network would have to be trained to use other size).
I have adapted the different images with ImageMagick and they work perfectly. (convert FILE.BMP -resize 20x20\! FILEOUT.bmp)

Train
The script trains by learning from the files found in "./TrainingSet/Inputs" and compares them with those in "./TrainingSet/Outputs".
Remember that it is very important to know that the Inputs and the Outputs are integrated in alphabetical order, the first Input with the first Output, etc. If the examples do not correspond, it would not be possible to find the solution to the problem.
It is also important to remember that all files must weigh exactly the same, I have used "ImageMagick" to achieve this. (convert FILE.BMP -resize 20x20\! FILEOUT.bmp)
This code is only prepared to work with BMP files and no other format.

Finally the script creates, after training, a file called "network_state.mdl", you must manually copy this file to the Predict folder in order to use it.

You can modify script.py to change the number of neurons, layers, iterations, and more.
Enjoy!

****

Presentacion
Este codigo puede ser configurado de diferentes maneras para variar todos sus parametros y cumplir diferentes funciones.
Se necesitan las librerias Sklearn y Numpy.


Pienso que con este codigo, la Red Neuronal podria aprender cualquier efecto.
El modelo que he subido como ejemplo puede colorar imagenes en blanco y negro, funciona con 256 neuronas y pesa alrededor de 2mb.
Se ha entrenado con un training set de 227 ejemplos de mandalas en blanco y negro como Input en su version original en color como Output.
El training set trabaja con BMP de 20x20 pixeles.
Recuerda que creando otro training set, podria cumplir otras funciones y trabajar con imagenes de mas resolucion.
He creado el codigo en un Pentium Dual-Core con 2gb de Ram, el entrenamiento ha tomado poco menos de una hora.




Manual
El codigo cuenta con dos partes: Train and Predict Si solo estas interesado en probar este modelo, solo usaras Predict.
Pero si intentas crear tu propio modelo, usaras Train.

Predict
El script utiliza el archivo "./InputOutputFile/In.bmp" y crea "./InputOutputFile/Out.bmp"
Este modelo de ejemplo esta entrenado con BMPs de 20x20 pixeles que pesan exactamente 1338 bytes. Con otra peso, no podria funcionar (habria que entrenar la red para usar otro peso).
Las imagenes diferentes las he adaptado con ImageMagick y funcionan perfectamente. (convert FILE.BMP -resize 20x20\! FILEOUT.bmp)

Train
El script entrena aprendiendo de los archivos que se encuentra en "./TrainingSet/Inputs" y los compara con los de "./TrainingSet/Outputs".
Recuerda que es muy importante saber que los Inputs y los Outputs se integran por orden alfabetico, El primer Input con el primer Output, etc. Si los ejemplos no se corresponden, no seria posible encontrar la solucion al problema.
Tambien es importante recordar, que todos los archivos deben pesar exactamente lo mismo, yo me he valido de "ImageMagick" para lograr esto. (convert FILE.BMP -resize 20x20\! FILEOUT.bmp)
Este codigo solo esta preparado para trabajar con archivos BMP y ningun otro formato.

Finalmente el script crea, luego del entrenamiento, un archivo llamado "network_state.mdl", debes copiar manualmente este archivo a la carpeta Predict para poder utilizarlo.

Puedes modificar script.py para cambiar la cantidad de neuronas, capas, iteraciones y mas.
Disfruta!
