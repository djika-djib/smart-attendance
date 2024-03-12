from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
# Create your views here.
def home(request):
    #Grab all Record in our table
    records = Record.objects.all()
    
    #check to see if logging in
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        #Authenticate
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "There Was An Error Logging In, Please Try Again...")
            return render(request, 'attendance/home.html')  # Return the template with error messages
    else:
        return render(request, 'attendance/home.html', {'records': records})



def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'attendance/register.html', {'form':form})

	return render(request, 'attendance/register.html', {'form':form})


def workers_record(request, pk):
    if request.user.is_authenticated:
        #Lookup the Records
        workers_record = Record.objects.get(id=pk)
        return render(request, 'attendance/record.html', {'workers_record':workers_record})
    
    else:
        messages.success(request, "You Must to be Logged in to View Record")
        return redirect('home')


def delete_worker(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, 'Worker Record deleted successfully')
        return redirect('home')
    else:
        messages.success(request, 'You must be logged in to continue')
        return redirect('home')
    
def add_record(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddRecordForm(request.POST or None)
            if form.is_valid():
                record = form.save(commit=False)
                record.user = request.user  # Assuming user is required
                record.save()
                messages.success(request, "Record Added...")
                return redirect('home')
        else:
            form = AddRecordForm()  # Create an empty form for GET requests
        return render(request, 'attendance/add_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')

def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'attendance/update_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')

