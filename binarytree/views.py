from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,AccessMixin
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout

from .models import Binary
from .forms import *

class Signup(CreateView):
    queryset = User.objects.all()
    form_class = SignUpForm
    template_name = 'registraion.html'
    success_url =  reverse_lazy('Signin')
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('Home')
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
            return redirect('Home')
        return render(request,self.template_name)

class signout(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        return redirect('Signin')
    
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
    
