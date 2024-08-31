from django.shortcuts import HttpResponse, render
from random import shuffle
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import serial
from .models import User, RoomObjectIdentifiers
from .forms import OperatorAccountForm, RoomObjectForm
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import time
import socket
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_protect
import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskCreateForm, TaskCompleteForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


esp_ip = '192.168.173.181'  # Replace with your ESP32 IP address
esp_port = 10000  # Replace with the port you used

# Create your views here.
@csrf_protect
@login_required
def home(request):
    nodes=RoomObjectIdentifiers.objects.all()
    user = request.user.username

    if request.user.is_staff:
        return render(request, 'home_page.html',{'nodes':nodes, 'user':user})
    else:
        return render(request, 'homey.html',{'nodes':nodes, 'user':user})


def dashboard_view(request):
    return render(request, 'transactions.html')


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login_page.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Logged In Successfully")
            return redirect(reverse('home'))
        
        else:
            context = {"error": "Wrong username or password, try again."}            
            return render(request, "login_page.html", context)
    else:
        messages.error(request, "Invalid credentials")


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")  # Use the URL name instead of "/login"
    
    return render(request, "logout.html", {})


def signup(request):
    if request.method == "POST":
        form = OperatorAccountForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            auth_login(request, user)
            return redirect('home')  # Replace 'home' with the URL name of your home page
    else:
        form = OperatorAccountForm()

    return render(request, 'signup.html', {"form": form})


@login_required
def profile_view(request):
    user_profile = get_object_or_404(User, user=request.user)
    return render(request, 'profile.html', {"user_profile": user_profile})
    

@login_required
def connect(request):
    # ESP32 IP and port
    esp_ip = '192.168.173.181'  # Replace with your ESP32 IP address
    esp_port = 10000  # Replace with the port you used

    # Create a socket connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((esp_ip, esp_port))


    
def send_command(command):
        try:
            # Create a socket connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((esp_ip, esp_port))

            # Send the command
            sock.sendall(command.encode('utf-8'))

            # Receive response from ESP32
            response = sock.recv(1024).decode('utf-8')
            print(f"Response from ESP32: {response}")

            # Close the connection
            sock.close()
        except Exception as e:
            print(f"Error sending command: {e}")



@login_required
def send_signal(request, pk):
    nodes=RoomObjectIdentifiers.objects.all()
    button = RoomObjectIdentifiers.objects.get(pk=pk)  
    Schar = button.interaction_key
    button.interaction_count += 1
    button.save()

    bitString = ""
       
    context={
        'button':button,
        
    }
    if button.config_id is not None:
        try:
         
            bitString = str(Schar)
            time.sleep(2)

            print(bitString)     


            if bitString in ['A', 'B', 'X']:

                def update_json(bit_string):
                    # Load the JSON file
                    with open('/home/pnlarbi/Documents/2024-a/ETHACCRA/SmartHome/smart_home/client/detect.json', 'r') as file:
                        data = json.load(file)

                    # Update the fields based on the bit string
                    if 'A' == bit_string:
                        data['lighting']['living_room']['status'] = 'A'
                    elif 'B' == bit_string:
                        data['lighting']['living_room']['status'] = 'B'
                    if 'X' == bit_string:
                        data['lighting']['living_room']['status'] = 'X'


                    # Save the updated JSON file
                    with open('/home/pnlarbi/Documents/2024-a/ETHACCRA/SmartHome/smart_home/client/detect.json', 'w') as file:
                        json.dump(data, file)

                update_json(bitString)
            else:
                print("Invalid command. Please enter A, B, or X.")


       
        except Exception as e:
            # return HttpResponse(f"Error: {e}")
            context = {"error": f"The wifi communication for ip: {esp_ip} is either broken or not yet established\n\nError: {e}", "nodes":nodes}            
            if request.user.is_staff:
                return render(request, 'home_page.html',context)
    
            else:
                return render(request, 'homey.html',context)
                
    else: print(None)
        
    if request.user.is_staff:
                return render(request, 'home_page.html',context)
    
    else:
                return render(request, 'homey.html',context)
    
   
@login_required
def append_control(request):
    if request.method == 'POST':
        form = RoomObjectForm(request.POST, request.FILES)
        if form.is_valid():
            control_object = form.save(commit=False)  
            control_object.room_operator=request.user        
            control_object.save()
            form.save_m2m()
            return redirect('home')
        else:
            # Handle the case where the form is not valid
            return render(request, 'home_page.html', {'form': form})
    else:
        # Handle the case where the request method is not POST
        form = RoomObjectForm()
        return render(request, 'add_control.html', {'form': form})
      
@login_required
def edit_control(request, pk):
    # operator = get_object_or_404(User, user=request.id)
    node = get_object_or_404(RoomObjectIdentifiers, pk=pk)
    if request.method == 'POST':
        form = RoomObjectForm(request.POST, request.FILES, instance=node)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RoomObjectForm(instance=node)
    return render(request, 'edit_control.html', {'form': form, 'node': node})


@login_required
def delete_control(request, pk):
    node = get_object_or_404(RoomObjectIdentifiers, pk=pk)
    node.delete()
    return redirect('home')


@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.is_completed:
        return render(request, 'task_detail_readonly.html', {'task': task})
    elif task.created_by == request.user:
        return HttpResponseForbidden()
    # elif task.completed_by(request.user):
    else:
        return render(request, 'task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskCreateForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskCreateForm()
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    # if not task(request.user):
    #     return HttpResponseForbidden()

    if request.method == "POST":
        form = TaskCompleteForm(request.POST, instance=task)
        if form.is_valid():
            task.is_completed = True
            task.completed_by = request.user
            form.save()
            return redirect('task_list')
    else:
        form = TaskCompleteForm(instance=task)
    return render(request, 'task_complete.html', {'form': form, 'task': task})