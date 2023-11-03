from django.shortcuts import render, get_object_or_404
from .models import About, Post, AboutPage, ContactInfo
from .forms import CommentForm, ContactForm
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger


def home(request):
    about = About.objects.last()
    posts = Post.objects.all()[:6]
    posts_slider = Post.objects.all().order_by('-comment_count')[:3]
    return render(request, 'blog/home.html', {'about': about, 'posts': posts, 'posts_slider': posts_slider})


def post_list_by_tag(request, tag):
    about = About.objects.last()
    
    object_list = Post.objects.filter(tag__title=tag)
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'about': about, 'posts': posts, 'num_pages': paginator.num_pages})


def post_list(request):
    about = About.objects.last()
    object_list = Post.objects.all()
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'about': about, 'posts': posts, 'num_pages': paginator.num_pages})


def about(request):
    about = About.objects.last()
    about_page = AboutPage.objects.last()
    return render(request, 'blog/about.html', {'about': about, 'about_page': about_page})


def contact(request):
    about = About.objects.last()
    contact_info = ContactInfo.objects.last()
    success = False
    if request.method == 'POST':
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            contact_form.save()
            success = True
    else:
        contact_form = ContactForm()

    return render(request, 'blog/contact.html', {'about': about, 'contact_info': contact_info, 'contact_form': contact_form, 'success': success})


def post_detail(request, slug):
    about = About.objects.last()
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(parent=None)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.comment_count += 1
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html', {'about': about,
                                                     'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form})
