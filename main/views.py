from django.shortcuts import render, redirect
from django.contrib import messages
from django.templatetags.static import static
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
        
        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )
        
        messages.success(request, 'Thank you for your message! I will get back to you soon.')
        return redirect('index')
    
    context = {
        'social_links': SocialLink.objects.all(),
    }
    return render(request, 'main/contact.html', context)
