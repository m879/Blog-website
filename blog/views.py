from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm,LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
#For POST IMPORT
from .models import Post
#for group in django
from django.contrib.auth.models import Group


#HOME
def home(request):
    posts=Post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})

#ABOUT
def about(request):
    return render(request,'blog/about.html')

#CONTACT
def contact(request):
    return render(request,'blog/contact.html')

#DASHBOARD
def dashboard(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        user=request.user
        full_name=user.get_full_name()
        # gps=user.group.all()
        # print(gps)
        # return render(request,'blog/dashboard.html',{'posts':posts,'full_name':full_name,'groups':gps})
        return render(request,'blog/dashboard.html',{'posts':posts,'full_name':full_name})
    else:
        return HttpResponseRedirect('/login/')
#Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#SIGNUP
# form=SignUpForm()
# return render(request,'blog/signup.html',{'form',form})
def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,"Hi !! You are author now")
            user=form.save()
            group=Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request,'blog/signup.html', {'form': form})


#LOGIN
def user_login(request):
    # form = LoginForm()
    # return render(request, 'blog/login.html', {'form': form})
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form =  LoginForm(request=request,data=request.POST)
            if form.is_valid():
                # form.save()
                username = form.cleaned_data.get('username')
                upassword = form.cleaned_data.get('password')
                user = authenticate(username=username, password=upassword)
                if user is not None:
                    login(request, user)
                    messages.success(request,"Logged in Successfully")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form =  LoginForm()
            return render(request, 'blog/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/dashboard/')


#ADD NEW POST
def add_post(request):
    if  request.user.is_authenticated:
        if request.method=='POST':
            form=PostForm(request.POST)
            if form.is_valid():
                title=form.cleaned_data['title']
                desc=form.cleaned_data['desc']
                pst=Post(title=title,desc=desc)
                pst.save()
                form=PostForm()
        else:
            form=PostForm()    
        return  render(request, 'blog/addpost.html',{'form': form})
    else:
        return HttpResponseRedirect('/login/')


#Update POST
def update_post(request,id):
    if  request.user.is_authenticated:
        if request.method=='POST':
            pi=Post.objects.get(pk=id)
            form=PostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                # form().save()

        else:
            pi=Post.objects.get(pk=id)
            form=PostForm(instance=pi)    
        return  render(request, 'blog/updatepost.html',{'form': form})
    else:
        return HttpResponseRedirect('/login/')


#Update POST
def delete_post(request,id):
    if  request.user.is_authenticated:
        if request.method=='POST':
            pi=Post.objects.get(pk=id)
            pi.delete()
        return  HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')   