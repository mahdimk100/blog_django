from typing import Any, Dict, Optional
from django.shortcuts import render, redirect
from django.views import View, generic
from .forms import UserRegisterForm
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

class Index(generic.ListView):
    model = Article
    queryset = Article.objects.all().order_by('-date')
    template_name = 'posts/index.html'
    paginate_by = 1

class Featured(generic.ListView):
    model = Article
    queryset = Article.objects.filter(featured=True).order_by('-date')
    template_name = 'posts/featured.html'
    paginate_by = 1

class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})
    
    def post(self, request):
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('index')

class DetailArticleView(generic.DetailView):
    model = Article
    template_name = 'posts/blog_post.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(DetailArticleView, self).get_context_data(*args, **kwargs)
        context['liked_by_user'] = False
        article = Article.objects.get(id=self.kwargs.get('pk'))
        if article.likes.filter(pk=self.request.user.id).exists():
            context['liked_by_user'] = True
        return context
            
    
class LikeArticle(View):
    def post(self, request, pk):
        article = Article.objects.get(id=pk)
        if article.likes.filter(pk=self.request.user.id).exists():
            article.likes.remove(request.user.id)
        else:
            article.likes.add(request.user.id)
        article.save()
        return redirect('detail_article', pk)

class DeleteArticleView(LoginRequiredMixin,UserPassesTestMixin, generic.DeleteView):
    model = Article
    template_name = 'posts/blog_delete.html'
    success_url = reverse_lazy('index')
    
    def test_func(self):
        article = Article.objects.get(id=self.kwargs.get('pk'))
        return self.request.user.id == article.author.id