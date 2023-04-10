from wsgiref.simple_server import WSGIRequestHandler
from zipfile import ZipFile
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Task, Client, Slave, Image
from .forms import ImageForm , TaskForm
from django.shortcuts import get_object_or_404
# Create your views here.
def home(request):
    return render(request,"mainpage/welcome.html" )
def signup(request):
    if request.method =="POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        status = request.POST.get('status')
        #return HttpResponse(request, username)
        myuser= User.objects.create_user(username,email,pass1)
        myuser.first_name=status
        myuser.save()
        if status == "Client" or status == "client":
            new_client = Client(name = myuser)
            new_client.save()
        elif status =="User" or status == "user":
            new_slave = Slave(name = myuser,score = 0)
            new_slave.save()
        messages.success(request, "Your account has been successfully created")
        return redirect("signin")
    return render(request,"mainpage/signup.html" )
def signin(request):
    if request.method =="POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        passw = request.POST.get('passw')
        user = authenticate(username=username,password=passw)
        if user is not None:
            login(request,user)
            username= user.username
            type = user.first_name.lower()
            return render(request,"mainpage/mainpage.html", {'username':username ,'user':user, 'tasks':Task.objects.all(), "type": type, 'people':Slave.objects.all()})
        else:
            messages.error(request,"Try Again")
            return redirect('')
    if request.user.is_authenticated :
        return render(request,"mainpage/mainpage.html", {'username':request.user.username ,'user':request.user, 'tasks':Task.objects.all(), "type": request.user.first_name, 'people':Slave.objects.all()})
    else:
        return render(request,"mainpage/signin.html" )
def signout(request):
    logout(request)
    messages.success(request,"logged out successfully")
    return redirect("signin")

def task(request, id):
    the_task = Task.objects.get(pk=id)
    if request.method == 'POST':
        files=request.FILES.getlist("image")
        user = request.user
        slave = Slave.objects.get(name = user)
        for i in files:
            Image.objects.create(task = the_task, image = i, origin = slave, reviewed = False, mark = 0)
            the_task.quantity_left = the_task.quantity_left - 1
            the_task.quantity_done = the_task.quantity_done + 1
            slave.score = slave.score + 10
        if the_task.quantity_left == 0:
            the_task.is_completed = True
        slave.save()
        the_task.save()
        messages.success(request,"task completed, you won 10 points!")
        return render(request,"mainpage/mainpage.html", {'username':request.user.username ,'user':request.user, 'tasks':Task.objects.all(), "type": request.user.first_name, 'people':Slave.objects.all()})
    else:
        imageform = ImageForm()
        return render(request, "mainpage/task.html" , {'task':the_task, "imageform":imageform})

def review_task(request, id):
    the_task = Task.objects.get(pk=id)
    slave = Slave.objects.get(name = request.user)
    return render(request, "mainpage/reviewtasks.html" , {'task':the_task, "images": Image.objects.all(),'user':slave})

def review_image(request, id, taskid):
    the_task = Task.objects.get(pk=taskid)
    image = Image.objects.get(pk=id)
    slave = Slave.objects.get(name = request.user)
    if request.method =="POST":
        mark = request.POST.get('mark')
        if mark:
            image.mark = int(mark)
            image.reviewed = True
            image.origin.score = image.origin.score + int(mark)
            the_task.quantity_done = the_task.quantity_done - 1 
            slave.score = slave.score + 5
            image.save()
            image.origin.save()
            the_task.save()
            slave.save()
            messages.success(request,"task reviewed, you won 5 coins!")
    if the_task.quantity_done != 0:
        return render(request, "mainpage/reviewtasks.html" , {'task':the_task, "images": Image.objects.all(),'user':slave})
    if the_task.quantity_done == 0:
        return render(request,"mainpage/mainpage.html", {'username':request.user.username ,'user':request.user, 'tasks':Task.objects.all(), "type": request.user.first_name, 'people':Slave.objects.all()})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit = False)
            task.client = Client.objects.get(name = request.user)
            task.save()
            messages.success(request,"Task added")
            return render(request,"mainpage/mainpage.html", {'username':request.user.username ,'user':request.user, 'tasks':Task.objects.all(), "type": request.user.first_name, 'people':Slave.objects.all()})
    else:
        form = TaskForm()
        return render(request, 'mainpage/addtask.html', {'form': form})
def download_task(request, id):
    images = Image.objects.filter(task=id)
    if not images:
        return HttpResponse("No images found for this task.")
    # Set the content type as application/zip
    response = HttpResponse(content_type='application/zip')
    # Set the content-disposition header to force file download
    response['Content-Disposition'] = f'attachment; filename="task_{id}_images.zip"'
    # Create a zip file with the images and write it to the response
    with ZipFile(response, 'w') as zipfile:
        for image in images:
            file_path = image.image.path
            # Add the image file to the zip file with a custom name
            zipfile.write(file_path, f'{image.mark}.jpg')
    return response
