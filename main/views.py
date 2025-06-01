from django.shortcuts import render, redirect
from django.contrib import messages
from django.templatetags.static import static
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
import logging
from .models import Project, Skill, Contact, SocialLink
# Create your views here.

# Set up logger
logger = logging.getLogger(__name__)

def index(request):
    context = {
        'hero_image': static('main/images/hero.png'),
        'projects': Project.objects.all()[:3],  # Show only 3 latest projects
        'skills': Skill.objects.all()[:6],  # Show only 6 top skills
        'social_links': SocialLink.objects.all(),
    }
    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'social_links': SocialLink.objects.all(),
    }
    return render(request, 'main/about.html', context)

def projects(request):
    context = {
        'projects': Project.objects.all(),
        'social_links': SocialLink.objects.all(),
    }
    return render(request, 'main/projects.html', context)

def skills(request):
    context = {
        'skills': Skill.objects.all(),
        'social_links': SocialLink.objects.all(),
    }
    return render(request, 'main/skills.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        if not all([name, email, message]):
            messages.error(request, 'Please fill in all fields.')
            return redirect('contact')
        
        # Create contact record
        contact = Contact.objects.create(
            name=name,
            email=email,
            message=message
        )
        
        # Debug log the email settings
        logger.debug(f"Email Settings: HOST={settings.EMAIL_HOST}, PORT={settings.EMAIL_PORT}, "
                    f"USER={settings.EMAIL_HOST_USER}, ADMIN={settings.ADMIN_EMAIL}, "
                    f"TLS={settings.EMAIL_USE_TLS}")
        
        # Prepare and send email notification
        try:
            # Prepare email context
            context = {
                'name': name,
                'email': email,
                'message': message,
                'date': timezone.now().strftime('%B %d, %Y %H:%M:%S')
            }
            
            logger.debug(f"Email Context: {context}")
            
            # Render email templates
            html_message = render_to_string('main/emails/contact_notification.html', context)
            plain_message = strip_tags(html_message)
            
            logger.debug("Email templates rendered successfully")
            
            if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
                raise ValueError("Email credentials are not configured")
            
            if not settings.ADMIN_EMAIL:
                raise ValueError("Admin email is not configured")
            
            # Create email message with Reply-To header
            email_message = EmailMessage(
                subject=f'New Contact Form Submission from {name}',
                body=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.ADMIN_EMAIL],
                reply_to=[email]  # Set reply-to to the contact form sender's email
            )
            email_message.content_subtype = "html"  # Set the content type to HTML
            
            # Send email
            email_message.send(fail_silently=False)
            
            logger.debug("Email sent successfully")
            messages.success(request, 'Thank you for your message! I will get back to you soon.')
        except ValueError as ve:
            logger.error(f"Configuration error: {str(ve)}")
            messages.error(request, 'The contact form is not properly configured. Please contact the administrator.')
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}", exc_info=True)
            messages.warning(request, 'Your message was saved but there was an issue sending the notification email. I will still receive your message.')
        
        return redirect('index')
        
    context = {
        'social_links': SocialLink.objects.all(),
    }
    return render(request, 'main/contact.html', context)
