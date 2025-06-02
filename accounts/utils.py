import random
from datetime import timedelta
from django.core.mail import send_mail
from django.utils import timezone
from .models import EmailOTP


def generate_and_send_otp(email: str) -> str:
    """Generate a 6 digit OTP and send it via email."""
    code = f"{random.randint(0, 999999):06d}"
    EmailOTP.objects.create(email=email, code=code)
    send_mail(
        "Your verification code",
        f"Your OTP code is {code}",
        "noreply@example.com",
        [email],
        fail_silently=True,
    )
    return code


def verify_otp(email: str, code: str, expiry_minutes: int = 5) -> bool:
    """Return True if the provided OTP is valid and not expired."""
    try:
        otp = EmailOTP.objects.filter(email=email, code=code).latest("created_at")
    except EmailOTP.DoesNotExist:
        return False
    if otp.created_at + timedelta(minutes=expiry_minutes) < timezone.now():
        return False
    return True
