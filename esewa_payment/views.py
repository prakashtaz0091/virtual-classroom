import hmac
import hashlib
import base64
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from main.models import Note, BoughtFile
from . import models
from django.http import HttpResponse
from django.contrib import messages

def generate_signature(payload, secret_key):
    signed_fields = payload.get("signed_field_names").split(",")
    data = ",".join([f"{field}={payload[field]}" for field in signed_fields])
    hmac_obj = hmac.new(secret_key.encode(), data.encode(), hashlib.sha256)
    return base64.b64encode(hmac_obj.digest()).decode()

def initiate_payment(request, note_id):
    
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        return HttpResponse("Note not found", status=404)
    
    try:
        if note.user == request.user:
            return HttpResponse("You cannot buy your own note", status=400)
        
        if not note.is_premium:
            return HttpResponse("Note is not premium", status=400)
        
        # Check if transaction already exists
        old_transaction = models.EsewaTransaction.objects.filter(notes=note, initiater=request.user).first()
        if old_transaction:
            if old_transaction.status == "success":
                messages.success(request, "You have already bought this note")
                return redirect("premium_notes")
            
            return HttpResponse("Transaction already exists", status=400)
        
        new_transaction = models.EsewaTransaction.objects.create(
            notes=note,
            initiater=request.user,
            receiver=note.user,
        )
    except Exception as e:
        return HttpResponse(str(e), status=500)
                
    
    transaction_uuid = new_transaction.transaction_id  # should be dynamically generated
    payload = {
        "amount": f"{note.amount}",
        "tax_amount": "0",
        "total_amount": "100",
        "transaction_uuid": transaction_uuid,
        "product_code": settings.ESEWA_CONFIG["PRODUCT_CODE"],
        "product_service_charge": "0",
        "product_delivery_charge": "0",
        "success_url": f"{settings.ESEWA_CONFIG["SUCCESS_URL"]}{transaction_uuid}/",
        "failure_url": f"{settings.ESEWA_CONFIG["FAILURE_URL"]}{transaction_uuid}/",
        "signed_field_names": "total_amount,transaction_uuid,product_code",
    }
    payload["signature"] = generate_signature(payload, settings.ESEWA_CONFIG["MERCHANT_SECRET"])
    print("our signature", payload["signature"])
    
    return render(request, "esewa_payment/payment_form.html", {"form_url": settings.ESEWA_CONFIG["FORM_URL"], "payload": payload})


@csrf_exempt
def payment_success(request, transaction_uuid):
    encoded_data = request.GET.get("data")

    if not encoded_data:
        return HttpResponse("Missing data", status=400)

    # Decode payload
    decoded_data = base64.b64decode(encoded_data).decode()
    payload = json.loads(decoded_data)
    
    # payload {'transaction_code': '000AI77', 'status': 'COMPLETE', 'total_amount': '100.0', 'transaction_uuid': 'af47675c-ead7-4caa-8d9a-12e333a9bcd2', 'product_code': 'EPAYTEST', 'signed_field_names': 'transaction_code,status,total_amount,transaction_uuid,product_code,signed_field_names', 'signature': 'SNGYeo1a/tX7yNSx95zcW3vyWTnlHHl3+otbwCyWwn4='}

    # print("payload", payload)
    payload_transaction_uuid = payload["transaction_uuid"]
    payload_total_amount = payload["total_amount"]
    # Recalculate signature
    # signed_fields = payload.get("signed_field_names").split(",")
    # data_to_sign = ",".join([f"{field}={payload[field]}" for field in signed_fields])
    # secret = settings.ESEWA_CONFIG["MERCHANT_SECRET"]
    # hmac_obj = hmac.new(secret.encode(), data_to_sign.encode(), hashlib.sha256)
    # expected_signature = base64.b64encode(hmac_obj.digest()).decode()
    print("payload_transaction_uuid", payload_transaction_uuid)

    try: 
        transaction = models.EsewaTransaction.objects.get(transaction_id=payload_transaction_uuid)
        if transaction.notes.amount == float(payload_total_amount):
        # Compare
        # if expected_signature == received_signature:
        # Valid payment
            # print(transaction_uuid)
            # transaction = models.EsewaTransaction.objects.filter(transaction_id=transaction_uuid).first()
            transaction.status = "success"
            transaction.save()

            file_bought = transaction.notes.files.first()
            print(file_bought)
            BoughtFile.objects.create(
                user = transaction.initiater,
                file = file_bought
            )
            
            messages.success(request, "Payment successful, you can download the file now!")

            # return render(request, "esewa_payment/success.html", {"payload": payload})
            return redirect("premium_notes")
        else:
            return HttpResponse("Transaction not found, something wrong in payment data", status=404)
    except models.EsewaTransaction.DoesNotExist:
        return HttpResponse("Transaction not found", status=404)

    


@csrf_exempt
def payment_failure(request, transaction_uuid):
    # print(request.GET)
    try:
        # print(transaction_uuid)
        transaction = models.EsewaTransaction.objects.filter(transaction_id=transaction_uuid).first()
        transaction.status = "failed"
        transaction.save()
    except Exception as e:
        print(e)
    return render(request, "esewa_payment/failure.html")



# http://localhost:8000/esewa-payment/success/d111d9cd-d71b-440c-be53-eca3352cf5ab/?data=eyJ0cmFuc2FjdGlvbl9jb2RlIjoiMDAwQUk3NiIsInN0YXR1cyI6IkNPTVBMRVRFIiwidG90YWxfYW1vdW50IjoiMTAwLjAiLCJ0cmFuc2FjdGlvbl91dWlkIjoiZDExMWQ5Y2QtZDcxYi00NDBjLWJlNTMtZWNhMzM1MmNmNWFiIiwicHJvZHVjdF9jb2RlIjoiRVBBWVRFU1QiLCJzaWduZWRfZmllbGRfbmFtZXMiOiJ0cmFuc2FjdGlvbl9jb2RlLHN0YXR1cyx0b3RhbF9hbW91bnQsdHJhbnNhY3Rpb25fdXVpZCxwcm9kdWN0X2NvZGUsc2lnbmVkX2ZpZWxkX25hbWVzIiwic2lnbmF0dXJlIjoicUZzWTFWRHBqUnRHOGMyVmQvOHY0Q3d0eHRrdGJiM2ExaVFNYXVjMkZzST0ifQ==

{"transaction_code":"000AI76",
 "status":"COMPLETE",
 "total_amount":"100.0",
 "transaction_uuid":"d111d9cd-d71b-440c-be53-eca3352cf5ab",
 "product_code":"EPAYTEST",
 "signed_field_names":"transaction_code,status,total_amount,transaction_uuid,product_code,signed_field_names","signature":"qFsY1VDpjRtG8c2Vd/8v4Cwtxtktbb3a1iQMauc2FsI="
 }