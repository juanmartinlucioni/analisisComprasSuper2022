#%%
# Importaciones
from selenium import webdriver
from bs4 import BeautifulSoup
from functools import reduce
import pandas as pd
import os

# folder path
dir_path = r'/Users/juanmartin/Documents/AD-python/supermercado-list/Data/RawData'
count = 0
# Iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        count += 1
print('File count:', count)
lendirectorio = count
print(lendirectorio)
#%%
# 1
# Proceso de prettify de archivos en batch
for i in range(lendirectorio):
    # Abrir archivo HTML Raw de Coto
    number = i+1
    stringArray = ["../supermercado-list/Data/RawData/html-coto-",number,".html"]
    location = reduce(lambda a, b: a + str(b), stringArray)
    HTMLFileToBeOpened = open(location, "r")
    rawContents = HTMLFileToBeOpened.read()
    # Usamos beautifulsoup
    beautifulSoupText = BeautifulSoup(rawContents, 'lxml')
    # Usamos prettify para que beautifulsoup funcione mejor.
    text = beautifulSoupText.body.prettify()
    # Creamos el archivo nuevo donde se va a guardar.
    stringArray2 = ['../supermercado-list/Data/PDAta/Compra', number, '.html']
    newname = reduce(lambda a, b: a + str(b), stringArray2)
    f = open(newname,'w')
    f.write(text)

#%%
# 2
# Nombramos los array
date = []
nombres = []
kglt = []
cantidades = []
precios = []
for i in range(lendirectorio):
    # Iniciamos el proceso de extraccion de informacion de cada archivo.
    number = i+1
    stringArray3 = ['../supermercado-list/Data/PDAta/Compra', number, '.html']
    nlocation = reduce(lambda a, b: a + str(b), stringArray3)
    HTMLFileToBeOpened = open(nlocation, 'r')
    content = HTMLFileToBeOpened.read()
    beautifulSoupText = BeautifulSoup(content, 'lxml')

    # Nombre Producto
    for tag in beautifulSoupText.findAll('div', attrs={'class': 'descrip_full'}):
        newname = tag.text.split()
        desc = " ".join(newname)
        #buscar dentro del nombre la cantidad
        #append en kglt
        nombres.append(desc)
    # Cantidades
    for tag in beautifulSoupText.findAll('div', attrs={'class': 'quantityBuy'}):
        numbers = tag.text.split()[1]
        cantidades.append(numbers)
        # Fecha del pedido
        fecha = beautifulSoupText.find('p', attrs={'class': 'pasofecha'}).text
        dia = fecha.split()
        date.append(dia[0])
    # Precio
    cantidadLoop = []
    listaProvisoria = []
    for tag in beautifulSoupText.findAll('span', attrs={'class': 'unit'}):
        cantidadLoop.append(1)
        precio = tag.text.split()
        if len(precio)>1:
            listaProvisoria.append(precio[5])
            if  precio[5] != listaProvisoria[len(listaProvisoria)-1]:
                precios.append(precio[5])
#%%
for i in range(len(precios)):
    print(i)
    if i > 1:
        if precios[i] == precios[i-1]:
            precios.pop(i)
            print("borrado")

#%%
# 3
# Proceso de guardado de informacion en un archivo CSV general
df = pd.DataFrame({'Fecha':date, 'Nombre Productos': nombres, 'Cantidad': cantidades, 'Precios': precios })
df.to_csv('Compras.csv', index=False, encoding='utf-8')
