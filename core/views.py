from datetime import datetime
import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import CompraForm
from django.views.generic import *
from requests.structures import CaseInsensitiveDict

def index(request):
    btc_products = [
        { "price": 3000 },
        { "price": 2000 },
        { "price": 1000 },
        { "price": 500 },
        { "price": 300 },
        { "price": 200 },
        { "price": 100 }
    ]
    form = CompraForm()
    success = request.GET.get('s') == '1'
    context = {
        'form': form,
        'success': success,
        'btc_products': btc_products
    }
    return render(request, 'core/index.html', context)

def pago(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            # TODOPAGO
            tarjetaExpiration = (form.cleaned_data['tarjeta_expiration_field']).split('/')
            tarjetaExpirationMonth = tarjetaExpiration[0]
            tarjetaExpirationYear = tarjetaExpiration[1]
            responseTodoPago = postTodoPago(
                form.cleaned_data['lempiras_field'], 
                form.cleaned_data['tarjeta_numero_field'], 
                form.cleaned_data['tarjeta_nombre_field'], 
                form.cleaned_data['tarjeta_cvc_field'], 
                tarjetaExpirationMonth, 
                tarjetaExpirationYear
            )

            if responseTodoPago['status'] == 200:
                # ELECTRUM
                # response = postElectrum(form.cleaned_data['address_field'], form.cleaned_data['amount_field'])
            else:
                return responseTodoPago

            return HttpResponseRedirect('/?s=1')
    else:
        form = CompraForm()
    
    context = {
        'form': form
    }
    return render(request, 'core/index.html', context)

def postTodoPago(lempiras, tarjetaNumero, tarjetaNombre, tarjetaCVC, tarjetaExpirationMonth, tarjetaExpirationYear):
    responseLogin = postTodoPagoLogin()
    responseLoginJSON = responseLogin.json()
    
    if responseLoginJSON['status'] == 200:
        token = responseLoginJSON['data']['token']
        responsePayDirect = postTodoPagoPayDirect(token, lempiras, tarjetaNumero, tarjetaNombre, tarjetaCVC, tarjetaExpirationMonth, tarjetaExpirationYear)
        responsePayDirectJSON = responsePayDirect.json()
        return responsePayDirectJSON
    
    return responseLoginJSON

def postTodoPagoLogin():
    urlLogin = 'https://preprod-api.todopago.hn/pay/v1/login'
    user = '0801-9019-1693431'
    password = 'todopago'

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "*/*"
    headers["X-Tenant"] = "HNTP"

    body = '{"user":"' + user + '", "password":"' + password + '"}'

    return requests.post(urlLogin, headers=headers, data=body)

def postTodoPagoPayDirect(token, lempiras, tarjetaNumero, tarjetaNombre, tarjetaCVC, tarjetaExpirationMonth, tarjetaExpirationYear):
    urlPayDirect = 'https://preprod-api.todopago.hn/pay/v1/direct-payment-without-register'
    
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "*/*"
    headers["X-Token"] = token
    headers["X-Tenant"] = "HNTP"
    headers["X-Content"] = "json"

    now = datetime.now()
    externalReference = "".join(tarjetaNombre.split()) + "-" + now.strftime('%d-%m-%Y-%H:%M')

    body = '{"accountNumber": "' + tarjetaNumero + '", "amount": ' + str(lempiras) 
    body += ', "taxes": "15", "cardHolderName": "' 
    body += tarjetaNombre + '", "comment": "Pago Directo ' + tarjetaNombre 
    body += '", "commerceID": 429, "customerName": "' + tarjetaNombre 
    body += '", "cvc": "' + str(tarjetaCVC) 
    body += '", "expirationMonth": "' + tarjetaExpirationMonth 
    body += '", "expirationYear": "' + tarjetaExpirationYear 
    body += '", "externalReference": "'+ externalReference + '", "customerEmail": "dtejada@isonet-globalsys.com", "terminalNbr": "1"}'
    
    return requests.post(urlPayDirect, headers=headers, data=body)

def postElectrum(destination, amount):
    user = 'user'
    password = 'k1RIVG6tRhy9TQVANfBOng=='
    host = '127.0.0.1'
    port = '7777'
    bodyPassword = 'daniel'
    
    url = 'http://' + user + ':' + password + '@' + host + ':' + port + '/'

    headers = CaseInsensitiveDict()
    headers["Authorization"] = "Basic dXNlcjpGbEJjYXFZNVo1c1liVzdYVDNMQU53PT0="
    headers["Content-Type"] = "application/json"

    data = '{"jsonrpc":"2.0","id":"curltext","method":"payto","params":{"destination":"' + destination + '", "amount":"' + str(amount) + '", "password":"' + bodyPassword + '"}}'
    
    return requests.post(url, headers=headers, data=data)
