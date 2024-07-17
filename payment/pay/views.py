from django.http import JsonResponse, HttpResponse
from .forms import CustomerForm, TransactionForm
from django_daraja.mpesa.core import MpesaClient
from .models import Transaction, Customer
from django.shortcuts import render
from django.conf import settings
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import requests
import base64
import json



def home(request):
    customer = CustomerForm()
    transaction = TransactionForm()
    context = {
        'customer': customer,
        'transaction': transaction
    }
    return render(request, 'paymentform.html', context)

def stkPush(request):
    cl = MpesaClient()
    if request.method == 'POST':
        customer = CustomerForm(request.POST)
        transaction = TransactionForm(request.POST)
        if customer.is_valid() and transaction.is_valid():
            cd = customer.cleaned_data
            cd1 = transaction.cleaned_data
            name = cd['name']
            email = cd['email']
            number = cd['number']
            customer = Customer.objects.update_or_create(number=number, defaults={'name': name, 'email': email})
            
            amount = int(cd1['amount'])
            acc_ref  = 'reference'
            trans_des = 'Description'
            callback_url = 'https://1106-102-219-208-126.ngrok-free.app/pay/callback/'

            response = cl.stk_push(number, amount, acc_ref, trans_des, callback_url)
            response = json.loads(response.text)
            try:
                checkout_id = response['CheckoutRequestID']
                response_code = response['ResponseCode']
                if response_code == '0':
                    return JsonResponse({'success': True, 'checkout_id': checkout_id})
                else:
                    return JsonResponse({'failed': 'Stk push failed'})
            except:
                return JsonResponse({'failed': 'No response yet'})
        else:
            return JsonResponse({'failed': 'Invalid data'})
    else:
        return JsonResponse({'failed': 'Invalid request method'})


def checkStatus(request):
    cl = MpesaClient()
    checkout_id = request.GET.get('checkout_id')
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    passkey = settings.MPESA_PASSKEY
    shortcode = settings.MPESA_EXPRESS_SHORTCODE
    password = base64.b64encode((shortcode + passkey + timestamp).encode('ascii')).decode('utf-8')
    url = 'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query'

    data = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp":timestamp,    
        "CheckoutRequestID": checkout_id, 
    }

    headers = {
        'Authorization': 'Bearer ' + cl.access_token(),
        'Content-Type': 'application/json'
    }
    

    response = requests.post(url, json=data, headers=headers)
    response = json.loads(response.text)
    try:
        if response['ResultCode']:
            if response['ResultCode'] == '0':
                return JsonResponse({'success': True})
            else: 
                return JsonResponse({'failed': 'Transaction failed'})
    except: 
        return JsonResponse({'Again': 'Send request again!'})
    
@csrf_exempt
def callback(request):
    
    if request.method == 'POST':
        cl = MpesaClient()
        data = cl.parse_stk_result(request.body)
        try:
            checkout_id = data['CheckoutRequestID']
            amount = data['Amount']
            ref_code = data['MpesaReceiptNumber']
            number = data['PhoneNumber']
            number = '0' + str(number)[-9:]
            customer = Customer.objects.filter(number=number).first()
            transaction = Transaction.objects.create(checkout_id=checkout_id, amount=amount, ref_code=ref_code, customer_id=customer.id)
            transaction.save()
            return JsonResponse({'success': 'Callback received!'})
        
        except:
            return JsonResponse({'success': 'Callback received!'})
        
    else:
        JsonResponse({'failed': 'Invalid request method!'})
            
    


# Create your views here.
