from multiprocessing import context
from queue import Empty
from urllib import request
from django import forms
from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from hitcount.views import HitCountDetailView
from django.views.generic import(
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
) 
from .models import Category, IpModel, Post, PostFeature
from .forms import PostCreateForm, PostFeatureCreateForm
from .models import CustomUser
from django.http import HttpResponseRedirect
from django.urls import reverse


def home(request):
    if request.method == 'POST':
        day = request.POST['day']
        my_town = request.POST['town']
        posts = Post.objects.filter(event_day=day, town=my_town)
        features = PostFeature.objects.all()   
        cats_title = Category.objects.all()     
        p = Paginator(posts, 6)
        page_num = request.GET.get('page', 1)

        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)

        context = {
            'cats_title': cats_title,
            'posts': page,
            'features': features
        }
    else:
        posts = Post.objects.all()
        features = PostFeature.objects.all() 
        cats_title = Category.objects.all()       
        p = Paginator(posts, 6)
        page_num = request.GET.get('page', 1)

        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)

        
        context = {
            'cats_title': cats_title,
            'posts': page,
            'features': features,
        }        

    return render(request, 'whatsonzambia/home.html', context)



class PostListView(ListView):
    model = Post
    template_name = 'whatsonzambia/home.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['features'] = PostFeature.objects.all() 
        
        return context


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class UserPostListView(ListView):
    model = Post
    template_name = 'whatsonzambia/user_posts.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 6  

    def get_queryset(self):
        user = get_object_or_404(CustomUser, email=self.kwargs.get('email'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(HitCountDetailView):
    model = Post

    context_object_name = 'post'
    template_name = 'whatsonzambia/post_detail.html'

    # set to True to count the hit
    count_hit = True

    def get(self, request, pk, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context.update({'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],})
   
        return self.render_to_response(context)


def postLike(request, pk):
    post_id = request.POST.get('post-id')
    post = Post.objects.get(pk=post_id)
    ip = get_client_ip(request)
    if not IpModel.objects.filter(ip=ip).exists():
        IpModel.objects.create(ip=ip)
    if post.likes.filter(id=IpModel.objects.get(ip=ip).id).exists():
        post.likes.remove(IpModel.objects.get(ip=ip))
    else:
        post.likes.add(IpModel.objects.get(ip=ip))

    return HttpResponseRedirect(reverse('post-detail', args=[post_id]))


class PostDetailFeatureView(HitCountDetailView):
    model = PostFeature

    context_object_name = 'feature'
    template_name = 'whatsonzambia/postfeature_detail.html'

    # set to True to count the hit
    count_hit = True    

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context.update({'popular_features': PostFeature.objects.order_by('-hit_count_generic__hits')[:3],})

        return self.render_to_response(context)


def featureLike(request, pk):
    feature_id = request.POST.get('feature-id')
    feature = PostFeature.objects.get(pk=feature_id)
    ip = get_client_ip(request)
    if not IpModel.objects.filter(ip=ip).exists():
        IpModel.objects.create(ip=ip)
    if feature.ft_likes.filter(id=IpModel.objects.get(ip=ip).id).exists():
        feature.ft_likes.remove(IpModel.objects.get(ip=ip))
    else:
        feature.ft_likes.add(IpModel.objects.get(ip=ip))

    return HttpResponseRedirect(reverse('feature-detail', args=[feature_id]))


class PostCreateView(LoginRequiredMixin, CreateView):
    post_image = forms.ImageField()
    model = Post
    template_name = 'whatsonzambia/post_form.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def CategoryView(request, cats):
    cats_title = Category.objects.all()
    category_posts = Post.objects.filter(category=cats)
    context = {
        'cats_title': cats_title,
        'category_posts': category_posts,
        'cats': cats,
    }    
    return render(request, 'whatsonzambia/category.html', context)



class PostCreateFeatureView(LoginRequiredMixin, CreateView):
    ft_post_image = forms.ImageField()
    model = PostFeature
    template_name = 'whatsonzambia/postfeature_form.html'
    form_class = PostFeatureCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    post_image = forms.ImageField()
    model = Post
    template_name = 'whatsonzambia/post_form.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostUpdateFeatureView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    post_image = forms.ImageField()
    model = Post
    template_name = 'whatsonzambia/postfeature_form.html'
    form_class = PostFeatureCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteFeatureView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PostFeature
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'whatsonzambia/about.html')
