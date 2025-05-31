from django.shortcuts import render, redirect
from django.contrib import messages
from django.templatetags.static import static
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from .models import Project, Skill, Contact, SocialLink
# Create your views here.

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
        
        # Prepare and send email notification
        try:
            # Prepare email context
            context = {
                'name': name,
                'email': email,
                'message': message,
                'date': timezone.now().strftime('%B %d, %Y %H:%M:%S')
            }
            
            # Render email templates
            html_message = render_to_string('main/emails/contact_notification.html', context)
            plain_message = strip_tags(html_message)
            
            # Send email
            send_mail(
                subject=f'New Contact Form Submission from {name}',
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                html_message=html_message,
                fail_silently=False,
            )
            messages.success(request, 'Thank you for your message! I will get back to you soon.')
        except Exception as e:
            messages.warning(request, 'Your message was saved but there was an issue sending the notification email. I will still receive your message.')
        
        return redirect('index')
        
    context = {
        'social_links': SocialLink.objects.all(),
    }
    return render(request, 'main/contact.html', context)
