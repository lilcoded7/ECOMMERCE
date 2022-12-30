from django.conf import settings 
import requests 
import os 
 

class Paystack:
    PAYSTACK_SECERET_KEY = 'sk_live_d4039e928f5d4d81fe00acd97652fed8c60325b3'
    base_url             = 'https//api.paystack.co'

    def verify_payment(self, ref, *args, **kwargs):
        path  = f'/transaction/verify/{ref}'

        headers = {
            'Authorization' : f'Bearer {self.PAYSTACK_SECERET_KEY}',
            'Content-Type ' : 'application/json,'
        }
        url = self.base_url + path 
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            response_data['status'], response_data['data']
        response_data = response.json()
        return  response_data['status'], response_data['message']
            