from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Project, Skill, Contact, SocialLink

# Create your views here.

def index(request):
    context = {
        'hero_image': 'https://lh3.googleusercontent.com/aida-public/AB6AXuD8GAa_ywqSjQYKe-iihDxaNrU5Ot-FvPB0whvY3uPx8V25D9G2XHjHhdIcbt3u6SmDhfoqpAq92847b5zRupdgynE6m7UGCrK_PGNX0HsQUKX6i7oW2petjaoe3iKajua53mAsSjGwb6DB22tG6Z4QbuCBgKEFUomNKM1fAgEvkM-VC8EDZYgPhq_3m8ieDP3zW6fqGaG9RbKqigeFILhAWZNtAfUi1YpTROCKswDASR0S6k81Ianwr1u7gWKQ1cBT4dQZ9NkR5wk',
        'projects': Project.objects.all(),
        'skills': Skill.objects.all(),
        'social_links': SocialLink.objects.all(),
    }
    return render(request, 'main/index.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )
        
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('index')
    
    return redirect('index')
