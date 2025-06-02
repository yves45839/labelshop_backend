from django.test import TestCase
from django.core import mail
from django.utils import timezone
from unittest.mock import patch

from accounts.models import EmailOTP, User
from accounts.utils import generate_and_send_otp, verify_otp
from django.urls import reverse


class OTPUtilsTests(TestCase):
    def test_generate_and_send_otp_creates_entry_and_sends_email(self):
        with patch('accounts.utils.send_mail') as mock_send_mail:
            code = generate_and_send_otp('foo@example.com')
            self.assertTrue(EmailOTP.objects.filter(email='foo@example.com', code=code).exists())
            mock_send_mail.assert_called_once()

    def test_verify_otp_valid_invalid_expired(self):
        code = generate_and_send_otp('bar@example.com')
        self.assertTrue(verify_otp('bar@example.com', code))
        self.assertFalse(verify_otp('bar@example.com', '000000'))
        otp = EmailOTP.objects.get(email='bar@example.com', code=code)
        otp.created_at = timezone.now() - timezone.timedelta(minutes=10)
        otp.save(update_fields=['created_at'])
        self.assertFalse(verify_otp('bar@example.com', code))


class OTPViewsTests(TestCase):
    def setUp(self):
        self.register_url = reverse('register_user')
        self.verify_url = reverse('verify_otp')

    def test_register_and_verify_flow(self):
        data = {'username': 'user1', 'password': 'pass', 'email': 'baz@example.com', 'role': User.INSTALLER}
        with patch('accounts.utils.send_mail') as mock_send_mail:
            response = self.client.post(self.register_url, data=data, content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(EmailOTP.objects.filter(email='baz@example.com').count(), 1)
            mock_send_mail.assert_called_once()
            code = EmailOTP.objects.get(email='baz@example.com').code

        response = self.client.post(self.verify_url, data={'email': 'baz@example.com', 'code': code}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('OTP verified', response.json().get('message', ''))
