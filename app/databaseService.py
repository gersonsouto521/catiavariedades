import sqlite3
import os
from flask import Blueprint, current_app, request
bp_entregas = Blueprint('bp_entregas', __name__)
filepath = os.path.dirname(os.path.abspath(__file__))
import ast
import pandas as pd

from .Util import convertMoney, tomorrowDay

import numpy as np
import matplotlib.pyplot as plt


def insertProductDelivery(value1, value2):
    conn = sqlite3.connect(f'{filepath[:-3]}\\tmp\\Novodatabase.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO entrega_produtos (date, delivery_content) VALUES (?,?)",(value1, value2))
    conn.commit()
    conn.close()
    print("Dados inseridos com sucesso!")


def getLastData(table='entrega_produtos'):
    conn = sqlite3.connect(f'{filepath[:-3]}\\tmp\\Novodatabase.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table};")
    data = cursor.fetchall()[-1][2]
    dataFrameJson = ast.literal_eval(data)
    dataFrame = pd.json_normalize(dataFrameJson)
    return dataFrame


def getAll():
    conn = sqlite3.connect(f'{filepath[:-3]}\\tmp\\Novodatabase.db')
    cursor = conn.cursor()
    allProducts = []
    cursor.execute(""" SELECT * FROM estoque_produto; """)
    for item in cursor.fetchall():
        itemBuy = str(item[5]).replace(',', '.')
        itemSell = str(item[6]).replace(',', '.')
        product = {
            'SKU':item[2],
            'NOME':item[3],
            'QT_ATUAL':item[4],
            'VLR_COM':convertMoney(float(itemBuy)),
            'VLR_VEN':convertMoney(float(itemSell)),
            'FORNECEDOR':item[7],
            'IMAGEM':item[1],
            'QT_CATIA':item[9],
            'QT_GERSON':item[10],
        }
        allProducts.append(product)

    return allProducts


def getAllColumn(column, table, multiple=None):
    conn = sqlite3.connect(f'{filepath[:-3]}\\tmp\\Novodatabase.db')
    cursor = conn.cursor()
    groupColumnLists = []
    cursor.execute(f""" SELECT {str(column)} FROM {str(table)}; """)

    for item in cursor.fetchall():
        if multiple != None:
            groupColumnLists.append(item)
        else:
            groupColumnLists.append(item[0])

    return groupColumnLists


def consultStorage():
    dataFrame = getAll()
    totalValueStorage = getProductValue()
    totalQuantityStorage = getProductQuantity()
    generateGraph()

    return dataFrame, totalValueStorage, totalQuantityStorage


def getProductValue():
    ProductValue = getAllColumn('amount_current,price_sell,amount_catia,amount_gerson', 'estoque_produto', multiple=True)
    value = []

    for item in ProductValue:
        itemSell = str(item[1]).replace(',', '.')
        storageValue = int(item[0]) * float(itemSell)
        value.append(storageValue)

    return convertMoney(sum(value))


def getProductQuantity():
    totalProduct = getAllColumn('amount_current', 'estoque_produto')
    return sum(totalProduct)


def formatGraph(pct, allvals):
    absolute = int(pct/100*np.sum(allvals))
    return f"{pct:.0f}% \n[{absolute}]"


def generateGraph():
    product_type = getAllColumn('product_type', 'estoque_produto')
    recipe = sorted(set(product_type))
    fig, ax = plt.subplots(figsize=(4,3), subplot_kw=dict(aspect="equal", anchor='SW'))

    data = []
    for x in range(0, len(recipe)):
        itemQuantity = product_type.count(recipe[x])
        data.append(itemQuantity)

    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct:formatGraph(pct, data), textprops=dict(color="w"))
    ax.legend(wedges, recipe, title="Produtos", loc='right', bbox_to_anchor=(1,0,0.55,1))
    plt.setp(autotexts, size=7, weight="bold")
    plt.savefig(f'{filepath[0:63]}\\static\\grafico_tipo_produtos.png', format='png')

def updateStorage(dataFrame):
    conn = sqlite3.connect(f'{filepath[:-3]}\\tmp\\Novodatabase.db')
    cursor = conn.cursor()
    for x in range(len(dataFrame)):
        Quantity = dataFrame.loc[x]['Quantity']
        Product_Name = dataFrame.loc[x]['Product Name']
        cursor.execute(f"""UPDATE estoque_produto SET amount_current = amount_current - {Quantity} WHERE product_name = '{Product_Name}' """)
        conn.commit()

    conn.close()


