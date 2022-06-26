
from django.http import response
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.paginator import Paginator

from django.shortcuts import (get_object_or_404,render,HttpResponseRedirect)
from .models import * 
from .forms import DocumentForm
from django.core.files.storage import FileSystemStorage
#from .functions import handle_uploaded_file
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import views as auth_views
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.http import HttpResponse
from django.contrib.auth.models import User, Group


# Create your views here.
def index(request):
    return render(request ,'index.html')

def user_signup(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input
        if len(username) < 3:
            messages.error(request, " Your user name must be under 3 characters")
            #return redirect('user_login')
            print('user_signup')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('user_signup')
        if (pass1 != pass2):
            messages.error(request, " Passwords do not match")
            return redirect('user_signup')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        my_group = Group.objects.get(name='Custum_user')
        my_group.user_set.add(myuser)
        myuser.save()
        messages.success(request, " Your iCoder has been successfully created")
        return redirect('user_login')

    else:
        return render(request, 'signup.html')



def user_login(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("upload")#upload
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("user_login")

    return  render(request , 'login.html')
@login_required
def details(request):
    snipps = Document.objects.filter(user__id=request.user.id)
    page = request.GET.get('page', 1)
    paginator = Paginator(snipps, 10)
    

    try:
        docs = paginator.page(page)
    except PageNotAnInteger:
        docs = paginator.page(1)
    except EmptyPage:
        docs = paginator.page(paginator.num_pages)
    
    return render(request, 'details.html', {'docs' : docs})
@login_required
def upload(request):
    form = DocumentForm(request.POST or None, request.FILES or None)
    if request.method =='POST':
          
        if form.is_valid():
              
            obj = form.save(commit = False)
            obj.user = request.user;
            obj.save()
            form = DocumentForm()
            messages.success(request, "Successfully created")
          
  
    return render(request, 'upload_form.html', {'form':form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('user_login')
@login_required
def destroy(request, id):  
    doc = Document.objects.get(id=id)  
    doc.delete()  
    return redirect("details")


def new(request):
    return render(request,'newform.html')   



def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "myapp/templates/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})




