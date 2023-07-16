from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate , login as loginUser , logout
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
# Create your views here.
from app.forms import TODOForm
from app.models import TODO
from django.contrib.auth.decorators import login_required


'''Our home page will show the todo list but to distinguish between users i used a decorator 
@login_required(login_url='login')
to ensure that the user is authorized to add or delete todo list or the items inside the todo
'''
@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user = user).order_by('priority')
        return render(request , 'index.html' , context={'form' : form , 'todos' : todos})
    
'''  checking the request type is GET or not
     If yes then show login page
     if the request type is not GET
     then fetch data  from the POST request
     and check whether the user is authorized or not
     if authorized show the todo list of that user
'''
def login(request): 
    if request.method == 'GET':      
        form1 = AuthenticationForm()
        context = {
            "form" : form1
        }
        return render(request , 'login.html' , context=context )
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username , password = password)
            if user is not None:
                loginUser(request , user)
                return redirect('home')
        else:
            context = {
                "form" : form
            }
            return render(request , 'login.html' , context=context )

'''  checking the request type is GET or not
     If yes then show signup page
     if the request type is not GET
     then fetch data from the POST request
     and check if the creadentials are valid or not
     if yes then redirect to login page  
'''
def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            "form" : form
        }
        return render(request , 'signup.html' , context=context)
    else:
        form = UserCreationForm(request.POST)  
        context = {
            "form" : form
        }
        if form.is_valid():
            user = form.save()
            if user is not None:
                return redirect('login')
        else:
            return render(request , 'signup.html' , context=context)


'''
    If the user is authorized then allow the user
    to add tasks into the todo list
    and if the form is valid then 
    add the task in the todo list
    and redicrect to the hoem page
'''
@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            return redirect("home")
        else: 
            return render(request , 'index.html' , context={'form' : form})

'''
    If the user is authorized then allow the user
    to delete tasks from the todo list 
    delete the task from the todo list
    and redicrect to the hoem page
'''
def delete_todo(request , id ):
    print(id)
    TODO.objects.get(pk = id).delete()
    return redirect('home')

'''
    If the user is authorized then allow the user
    to change task's status from the todo list
'''
def change_todo(request , id  , status):
    todo = TODO.objects.get(pk = id)
    todo.status = status
    todo.save()
    return redirect('home')

'''
    This function will be called when the user hits the logout.
'''
def signout(request):
    logout(request)
    return redirect('login')