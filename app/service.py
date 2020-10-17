from flask import Blueprint, current_app, redirect
from flask import Flask, jsonify, request, render_template
import os
from datetime import datetime
import requests

from .model import EntregaProdutos, db
from .deliveryService import deliveryHeader, deliveryOffHeader
from .databaseService import insertProductDelivery, getLastData, consultStorage, updateStorage

import time
#TODO
date = datetime.today()
bp_app = Blueprint('app', __name__)


@bp_app.route('/', methods=['GET'])
def home():
    dataFrame, totalValueStorage, totalQuantityStorage = consultStorage()
    return render_template('index.html', df=dataFrame,tamanho=len(dataFrame), totalEstoque=totalValueStorage, somaEstoque=totalQuantityStorage)   

    

@bp_app.route('/delivery', methods=['GET'])
def teste():
    return render_template('delivery.html')

@bp_app.route('/set_delivery', methods=['POST'])
def entregaProdutos():
    planilhaWishLocal = request.form['estoque']
    if planilhaWishLocal[0:5] == 'Order':
        dataFrame = deliveryHeader(planilhaWishLocal)
    else:
        dataFrame = deliveryOffHeader(planilhaWishLocal)

    updateStorage(dataFrame)
    dataFrameJson = dataFrame.to_dict('records')
    insertProductDelivery(str(date.strftime('%d/%m/%Y %H:%M:%S')), str(dataFrameJson))

    return redirect('/')

@bp_app.route('/romaneio')
def imprimeRomaneio(): 
    dataFrame = getLastData()
    time.sleep(10)
    return render_template('romaneio.html',df=dataFrame,tamanho=len(dataFrame),date=date.strftime('%d/%m/%Y'))

@bp_app.route('/etiquetas')
def imprimeEtiqueta():
    dataFrame = getLastData()    
    return render_template('etiquetas.html',data=dataFrame,sizeData=len(dataFrame))

@bp_app.route("/estoque")
def consultarEstoque():
    dataFrame, totalValueStorage, totalQuantityStorage = consultStorage()
    return render_template('Nestoque.html', df=dataFrame,tamanho=len(dataFrame), totalEstoque=totalValueStorage, somaEstoque=totalQuantityStorage)   

