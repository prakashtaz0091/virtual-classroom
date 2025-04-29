import hmac
import hashlib
import base64
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from main.models import Note
from . import models
from django.http import HttpResponse

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
        # if note.user == request.user:
        #     return HttpResponse("You cannot buy your own note", status=400)
        
        if note.is_premium == False:
            return HttpResponse("Note is not premium", status=400)
        
        # Check if transaction already exists
        old_transaction = models.EsewaTransaction.objects.filter(notes=note, initiater=request.user).first()
        if old_transaction:        
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
    
    return render(request, "esewa_payment/payment_form.html", {"form_url": settings.ESEWA_CONFIG["FORM_URL"], "payload": payload})


@csrf_exempt
def payment_success(request, transaction_uuid):
    encoded_data = request.GET.get("data")
    received_signature = request.GET.get("signature")

    if not encoded_data or not received_signature:
        return HttpResponse("Missing data or signature", status=400)

    # Decode payload
    decoded_data = base64.b64decode(encoded_data).decode()
    payload = json.loads(decoded_data)

    # Recalculate signature
    signed_fields = payload.get("signed_field_names").split(",")
    data_to_sign = ",".join([f"{field}={payload[field]}" for field in signed_fields])
    secret = settings.ESEWA_CONFIG["MERCHANT_SECRET"]
    hmac_obj = hmac.new(secret.encode(), data_to_sign.encode(), hashlib.sha256)
    expected_signature = base64.b64encode(hmac_obj.digest()).decode()

    # Compare
    if expected_signature == received_signature:
        # Valid payment
        try:
            # print(transaction_uuid)
            transaction = models.EsewaTransaction.objects.filter(transaction_id=transaction_uuid).first()
            transaction.status = "success"
            transaction.save()
        except Exception as e:
            print(e)
            
        return render(request, "esewa_payment/success.html", {"payload": payload})
    else:
        return HttpResponse("Invalid signature", status=403)


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