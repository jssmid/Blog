from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Tag, Post
from django.db.models import Q
from django.http import JsonResponse


# -------------------- HOME ----------------------
def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    search_result = Q(title__icontains=q) | Q(tag__name__icontains=q)

    posts = Post.objects.filter(search_result)

    latest_posts = Post.objects.all().order_by('-id')[:5]

    tags = Tag.objects.all()

    context = {
        'posts':posts,
        'latest_posts': latest_posts,
        'tags':tags,

        }

    return render(request, 'index.html', context)



# ------------------ CONTACT ---------------------
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        html = render_to_string('email.html',{
            'name': name,
            'email': email,
            'subject': subject,
            'message' : message
        } )
        send_mail(subject, message, email, ['noreply@gmail.com'], html_message=html)
        return redirect('contact')

    return render(request, 'contact.html')


# --------------- ABOUT ME --------------------
def aboutMe(request):
    return render(request, 'about-me.html')


# ----------------POST DETAILS --------------------
def postDetails(request, slug):
    posts = Post.objects.filter(slug=slug)
    latest_posts = Post.objects.all().order_by('-id')[:5]
    tags = Tag.objects.all()
    context = {
        'posts': posts,
        'latest_posts': latest_posts,
        'tags': tags,
    }
    return render(request, 'single-post.html', context)