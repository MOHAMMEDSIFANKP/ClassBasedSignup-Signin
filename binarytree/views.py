from django.shortcuts import render,redirect
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Binary
from .forms import *

class Signup(CreateView):
    queryset = User.objects.all()
    form_class = SignUpForm
    template_name = 'registraion.html'
    success_url =  reverse_lazy('Signin')
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('UsersList')
        return render(request,self.template_name)

class Signin(FormView):
    template_name = 'loginpage.html'
    form_class = LoginForm
    success_url = '/'
    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
        
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('UsersList')
        return render(request,self.template_name)

class signout(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        return redirect('Signin')
    

class UsersList(LoginRequiredMixin, ListView):
    login_url = 'signin/'
    paginate_by = 3
    template_name = 'index.html'
    queryset = User.objects.all().order_by('id')
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.queryset, self.paginate_by)
        page = self.request.GET.get('page')
        users = paginator.get_page(page)
        context['users'] = users
        return context

class SearchUserList(View):
    paginate_by = 3
    def get(self,request, *args, **kwargs):
        query = request.GET.get("query")
        results = User.objects.filter(Q(username__icontains=query) | Q(email__icontains = query) | Q(first_name__icontains = query) | Q(last_name__icontains = query)).order_by('id')
        paginator = Paginator(results, self.paginate_by)
        page = self.request.GET.get('page')
        users = paginator.get_page(page)
        context = {"users": users}
        return render(request, "ajax/search_results.html", context)
    
class Home(LoginRequiredMixin,ListView):
    login_url = 'signin/'
    template_name = 'index.html'
    queryset = Binary.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["binary"] = self.get_queryset()
        return context
    def post(self,request):
        data = request.POST.get('data')
        data_childs = Binary.objects.filter(data=data)
        return redirect('Home')
    
class SubmitForm(LoginRequiredMixin,View):
    login_url = 'signin/'
    template_name = 'form.html'
    def get(self,request):
        return render(request,self.template_name)
    def post(self,request):
        data = request.POST.get('data')
        left = request.POST.get('left')
        right = request.POST.get('right')
        
        parent = Binary.objects.create(data=data)
        left_child = Binary.objects.create(data=left)
        right_child = Binary.objects.create(data=right)

        parent.left = left_child
        parent.right = right_child
        parent.save()

        return render(request,self.template_name)
    
