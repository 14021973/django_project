from django.shortcuts import render,get_object_or_404,redirect
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import  LoginRequiredMixin,UserPassesTestMixin,PermissionRequiredMixin
from django.contrib.auth.models import User


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class UserAccessMixin(PermissionRequiredMixin):

    #nadpisanie metody pozwalajacej sterowac uprawnieniami do classbasedviews
    #parametry dla klasy w poszczegolnych widokach

    def dispatch(self,request,*args,**kwargs):
        if (not self.request.user.is_authenticated):
            return redirect_to_login(self.request.get_full_path(),self.get_login_url(),self.get_redirect_field_name())
        if not self.has_permission():
            return redirect('blog-home')
        return super(UserAccessMixin,self).dispatch(request,*args,**kwargs)





#class PostListView(PermissionRequiredMixin,ListView):
class PostListView(ListView):

    # permission_required = 'blog.view_post'
    # login_url = '/about'
    # raise_exception = False

    model = Post
    template_name = 'blog/home.html'    #<app>/<model>_<viewtype>.html
    context_object_name='posts'
    ordering=['-date_posted']     #['-date_posted'] z minusem odwrotne sortowanie
    paginate_by=5


class UserPostListView(UserAccessMixin,ListView):
#class UserPostListView(ListView):

    raise_exception = False
    permission_required = 'blog.view_post'
    permission_denied_message = "XXX"
    login_url = ''
    redirect_field_name = 'next'


    model = Post
    template_name = 'blog/user_posts.html'    #<app>/<model>_<viewtype>.html
    context_object_name='posts'
    paginate_by=5

    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

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

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})