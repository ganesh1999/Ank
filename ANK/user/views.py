from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage
from django.core.files import File

from django.contrib import messages

from .models import *
from .utils import render_to_pdf
from io import BytesIO
from .forms import CreateUserForm

from .reSPPU import *
# Create your views here.

###############################################   HOMEPAGE   ###############################################


def home(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save('exp.pdf', myfile)
        uploaded_file_url = fs.url(filename)

        if uploaded_file_url:

            BASE_DIR = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))

            pdfname = ('.' + uploaded_file_url)

            home.StudentInformationfromfunction = studInfoX(pdfname)
            # returns string of all students result

            home.StudentRank = studRanking(pdfname)
            # returns dictionary as [('name',SGPA), ....]

            home.SubjectResult = passRatio(pdfname)
            # returns  dictonary as {'subcode':[failed, outof, percentage], ........}

            # home.FailedNamesfromfunction = infoFailed(pdfname)
            # returns  string of all failed students with respective subject code

            home.FailedNamesinSubject = infoFailed2(pdfname)
            # returns doctonary as {'subcode':[failed name list], ......}

            if request.user.is_authenticated:
                # save this for forever
                '''tempPost = Result(
                    owner=request.user,
                    StudentRanking=StudentRankingfromfunction,
                    # SubjectResult=SubjectPassingPercentagefromfunction,
                    FailedlistwithSubject=FailedNamesfromfunction,
                    FailedinParticularSubject=FailedNames2fromfunction
                )

                tempPost.save()'''

                fs.delete(filename)
                return redirect('results')

            else:
                # delete this in demo function
                '''tempPost = Result(
                    owner='testuser',
                    StudentRanking=StudentRankingfromfunction,
                    # SubjectResult=SubjectPassingPercentagefromfunction,
                    FailedlistwithSubject=FailedNamesfromfunction,
                    FailedinParticularSubject=FailedNames2fromfunction
                )

                tempPost.save()'''
                fs.delete(filename)
                return redirect('demo')

    return render(request, 'home.html')


#####################################################   DEMOPAGE   #########################################

def demo(request):
    '''lastuser = Result.objects.filter(owner="testuser").last()
    print(lastuser)
    notnecessoryusers = Result.objects.filter(owner="testuser")
    notnecessoryusers.delete()'''

    context = {
        'studentranking': home.StudentRank,
        'subjectresult': home.SubjectResult,
        'failednamesinsubject': home.FailedNamesinSubject,
        'studentresult': home.StudentInformationfromfunction
    }

    return render(request, 'demo.html', context)


#############################################  RESULTSPAGE  ###################################

@login_required(login_url='login')
def results(request):

    results.context = {
        'studentranking': home.StudentRank,
        'subjectresult': home.SubjectResult,
        'failednamesinsubject': home.FailedNamesinSubject,
        'studentresult': home.StudentInformationfromfunction
    }

    pdf = render_to_pdf('results.html', results.context)

    temppost = Userdata(
        owner=request.user
    )
    temppost.save()
    lastinstance = Userdata.objects.filter(owner=request.user).last()
    filename = 'results.pdf'
    lastinstance.orders.save(filename, File(BytesIO(pdf.content)))

    return render(request, 'results.html', results.context)


######################################      Download PDF   #################################

def Downloadpdf(request):

    pdf = render_to_pdf('results.html', results.context)

    response = HttpResponse(pdf, content_type='application/pdf')
    filename = 'result.pdf'
    content = "attachment; filename='%s'" % (filename)
    response['Content-Disposition'] = content
    return response


#############################################   REGISTERPAGE   ########################################
def registerpage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'account created for : ' + user)

            return redirect('login')

    context = {'form': form}

    return render(request, 'register.html', context)


################################################   LOGINPAGE  ################################################

def loginpage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username or Password is incorrect")

    return render(request, 'login.html')


##################################################   LOGOUTPAGE     ##########################################
def logoutpage(request):
    logout(request)
    return redirect('login')


#################################################  USERPROFILEPAGE   ############################################
@login_required(login_url='login')
def profilepage(request):

    context = {
        'Userdata': Userdata.objects.filter(owner=request.user)
    }
    return render(request, 'profile.html', context)
