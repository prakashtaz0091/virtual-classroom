from django.core.exceptions import ValidationError
import re
import hashlib
import time
import datetime
from django.utils import timezone


def email_validation(value):
    # Regular expression for validating an Email
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not re.match(email_regex, value):
        raise ValidationError(f"Invalid email address: {value}")


def generate_otp():
    # Use the current time as a unique input
    current_time = str(time.time()).encode("utf-8")

    # Create a SHA256 hash of the current time
    hash_object = hashlib.sha256(current_time)

    # Get the hexadecimal representation of the hash
    hex_dig = hash_object.hexdigest()

    # Extract the first 8 characters for the OTP
    otp = hex_dig[:8]

    return otp


def is_otp_expired(otp_obj, expiry_time=5):
    # Get the OTP creation time as a timezone-aware datetime
    otp_created_time = otp_obj.created_at  # Assuming created_at is timezone-aware

    # Get the current time as a timezone-aware datetime
    current_time = timezone.now()

    # Check if the current time exceeds the expiry time
    if current_time - otp_created_time > datetime.timedelta(minutes=expiry_time):
        return True
    return False
