from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Test email configuration by sending a test email'

    def handle(self, *args, **options):
        try:
            # Log current email settings
            self.stdout.write(f"Current email settings:")
            self.stdout.write(f"HOST: {settings.EMAIL_HOST}")
            self.stdout.write(f"PORT: {settings.EMAIL_PORT}")
            self.stdout.write(f"TLS: {settings.EMAIL_USE_TLS}")
            self.stdout.write(f"USER: {settings.EMAIL_HOST_USER}")
            self.stdout.write(f"ADMIN EMAIL: {settings.ADMIN_EMAIL}")
            
            if not all([settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD, settings.ADMIN_EMAIL]):
                self.stderr.write(self.style.ERROR('Email settings are not properly configured'))
                return
            
            # Create test email message
            test_reply_to = "test@example.com"  # Example reply-to address
            email_message = EmailMessage(
                subject='Test Email from Django Portfolio',
                body='This is a test email to verify the email configuration.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.ADMIN_EMAIL],
                reply_to=[test_reply_to]
            )
            
            # Send email
            email_message.send(fail_silently=False)
            
            self.stdout.write(self.style.SUCCESS('Test email sent successfully!'))
            self.stdout.write(f"Reply-To address set to: {test_reply_to}")
            
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Failed to send test email: {str(e)}'))
            logger.error("Test email failed", exc_info=True) 