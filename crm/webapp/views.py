from django.shortcuts import render,redirect
from .forms import CreateUserForm,LoginForm,AddRecordForm,UpdateRecordForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Record
from django.views.decorators.cache import never_cache
from django.contrib import messages

# Create your views here.


# home page


def home(request):
    return render(request,'webapp/index.html')
    # return HttpResponse('hey there')
    

# register

def register(request):
    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
             
            form.save()
            
            messages.success(request,"Account created successfully!")
    
            return redirect("user-login")
    
    context = {'form':form}
    
    return render(request,'webapp/register.html', context=context)

#-- login a user


def login(request):
    form = LoginForm()
    
    if request.method == 'POST':
        form = LoginForm(request,data=request.POST)
        
    if form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request,username = username ,password = password)
        
        if user is not None:
            auth.login(request,user)
            
            return redirect("dashboard")
    context = {'form':form}
    
    return render(request,'webapp/my-login.html',context=context)


# --  Dashboard
@login_required(login_url='user-login')
def Dashboard(request):
    
    my_records = Record.objects.all()
    
    context = {'records':my_records}
    return render(request,"webapp/dashboard.html",context=context)








# -- create a record or add record

@login_required(login_url='user-login')

def create_record(request):
    form = AddRecordForm
    
    if request.method =='POST':
        
        form = AddRecordForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            messages.success(request,"record created!")
            
            return redirect('dashboard')
        
    context = {'form':form}
    
    return render(request,'webapp/create-record.html',context)


#--update record


@login_required(login_url='user-login')
def update_record(request,pk):
    record = Record.objects.get(id = pk)
    
    form = UpdateRecordForm(instance= record)
    # form = UpdateRecordForm
    
    if request.method=='POST':
        form = UpdateRecordForm(request.POST,instance=record)
        
        if form.is_valid():
            form.save()
            messages.success(request,"record updated!")
            
            return redirect('dashboard')
    
    context = {'form':form}
    return render(request,'webapp/update-record.html',context)



# -- user logout


def user_logout(request):
    auth.logout(request)
    messages.success(request,"logged out successfully!")
    return redirect("user-login")


# --read a single record
@login_required(login_url='user-login')
@never_cache
def view_record(request,pk):
    all_records = Record.objects.get(id=pk)
    context = {'record':all_records}
    return render(request,'webapp/view-record.html',context)


# --delete a record
@never_cache
@login_required(login_url='user-login')

def delete_record(request,pk):
    all_records = Record.objects.get(id=pk)
    all_records.delete()
    messages.success(request,"record deleted")
    return redirect('dashboard')
    