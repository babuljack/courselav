from django.shortcuts import render
from django.shortcuts import HttpResponse,HttpResponseRedirect,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import *
from moviepy.editor import VideoFileClip
import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from time import time
import razorpay
client =razorpay.Client(auth=('rzp_test_26WYBJdjNWA64A', '0AORmLYrdmWn4Pxvs0ai3EuH'))
# Create your views here.
def Home(request):
    course=Course.objects.all()
      

    '''selectedcourse=Course.objects.get(id=6)
    allvideo=selectedcourse.video_set.all()
    links=allvideo.values('video')
    urls={}
    for link in singlevideo:
        v=link['video']
        print(v)
        

    print(urls)'''
    #code=encrypt()
    context={
        'courses':course,
        'code':'https://www.youtube.com/embed/kTa_CR8rROI',
        
    }
    return render(request, 'course/index.html',context)


def SignUp(request):
  if not request.user.is_authenticated:
    if request.method=='POST':
        fm=UserForm(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, "User register successfully")
    else:
        fm=UserForm()
    return render(request,'course/signup.html',{'fm':fm})
  else:
      return HttpResponseRedirect('/profile')           


def loginUser(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            fm=AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                upass=fm.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    try:
                        nextpage=request.GET['next']
                        if nextpage:

                            """Protacting From ssrf attacks"""                   
                            url_is_safe=url_has_allowed_host_and_scheme(url=nextpage,allowed_hosts=set(),
                            require_https=request.is_secure())           
                            if url_is_safe:
                                return HttpResponseRedirect(nextpage)
                            else:
                                return HttpResponseRedirect('/profile')

                            """default , Never use like this it's vulnerable."""
                            #return HttpResponseRedirect(nextpage)         

                    except:
                        return HttpResponseRedirect('/profile')               
        else:
            fm=AuthenticationForm()
        return render(request,'course/login.html',{'fm':fm})
    else:
        return HttpResponseRedirect('/profile')                  

def LogoutUser(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/login')
    else:
        return HttpResponseRedirect('/login')  

def Profile(request):
    if request.user.is_authenticated:
        return render(request,'course/profile.html')
    else:
        return HttpResponseRedirect('/login') 






def CourseView(request , slug):
    serial_number  = request.GET.get('lecture')
    lecture=serial_number
    course = Course.objects.get(slug  = slug)
    #Best usecase with secure#
    #allvideo=course.video_set.all().order_by('serial')
    #allmodule=course.module_set.all()
    #modules={}
    #for module in allmodule:
        #video=allvideo.filter(module__title=module)
        #modules[module]=video
     
    #slow and worest case.
    videos = course.video_set.all().order_by("serial")
    allmodule=videos.values('module__title').distinct().order_by('module__title')
    modules={}
    for module in allmodule:
        spmodule=module['module__title']
        undermodule=videos.filter(module__title=spmodule)
        modules[spmodule]=undermodule   
    

    serve_video=None
    access=None
    if serial_number is None:
        serial_number = 1

    video = Video.objects.get(serial=serial_number , course = course)
    #previews
    try:
        exists=UserCourse.objects.get(user=request.user,course=course)
        if exists:
            serve_video=Video.objects.get(serial=serial_number , course = course)
            access=True
    except:
        if not video.is_preview:
            if not request.user.is_authenticated:
                if serial_number==1:
                    redirects= f'/login?next=/courseview/{slug}'
                else:
                    redirects= f'/login?next=/courseview/{slug}?lecture={serial_number}'   
                return HttpResponseRedirect(redirects)
        else:
            serve_video=Video.objects.get(serial=serial_number , course = course,is_preview=True)
        

       
        
        
    context = {
        "course" : course , 
        "modules" : modules, 
        'video':serve_video,
        'access':access,
        'slug':slug,
        'lecture':lecture
      
    }
    return  render(request , template_name="course/courseview.html" , context=context )


@login_required(login_url='/login')
def UploadCourse(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            courseform=CourseForm(request.POST,request.FILES)
            tagform=TagForm(request.POST)
            preform=PrerequisiteForm(request.POST)
            learningform=LearningForm(request.POST)
            videoform=VideoForm(request.POST,request.FILES)
            if courseform.is_valid() and tagform.is_valid() and preform.is_valid() and learningform.is_valid() and videoform.is_valid():
                course=courseform.save()
                #Tag
                tag=tagform.cleaned_data['title']
                Tag(title=tag,course=course).save()
                #Pre
                pre=preform.cleaned_data['title']
                Prerequisite(title=pre,course=course).save()
                #learning
                learning=preform.cleaned_data['title']
                Learning(title=learning,course=course).save()
                #video
                vserial=videoform.cleaned_data['serial']
                vtitle=videoform.cleaned_data['title']
                vmodule=videoform.cleaned_data['module']
                vdesc=videoform.cleaned_data['desc']
                vvideo=videoform.cleaned_data['video']
                vnote=videoform.cleaned_data['notes']
                vpreview=videoform.cleaned_data['is_preview']
                Video(serial=vserial,title=vtitle,module=vmodule,desc=vdesc,video=vvideo,notes=vnote,is_preview=vpreview,course=course).save()
                messages.success(request,'Course created')
            else:
                print('something wrong')    
        else:
            courseform=CourseForm()
            tagform=TagForm()
            preform=PrerequisiteForm()
            learningform=LearningForm()
            videoform=VideoForm()

        context={
          'courseform':courseform,
          'tagform':tagform,
          'preform':preform,
          'learningform':learningform,
          'videoform':videoform
        }    
        return render(request,'course/upload.html',context) 




def CheckOut(request,slug):
    course=Course.objects.get(slug=slug)
    user = request.user
    try:
        encounrse=Payment.objects.get(status=True,course=course,user=user)
        enroll=True
    except:
        enroll=None    
    action=None
    buy=None
    action=request.GET.get('action')
    copun=request.GET.get('copun')
    copundiscount=None
    cpdiscount=None
    error_copun=None
    order=None
    payment=None

    if copundiscount:
        amount=copundiscount*100
    else:
        price=course.price
        discount=course.discount
        discountprices=int(price-(price*discount*0.01))
        amount=discountprices*100

    videos = course.video_set.all().order_by("serial")
    allmodule=videos.values('module__title').distinct().order_by('module__title')
    modules={}
    for module in allmodule:
        spmodule=module['module__title']
        undermodule=videos.filter(module__title=spmodule)
        modules[spmodule]=undermodule   
    
    if copun:
        try:
            copun=Copun.objects.get(code=copun,course=course)
            price=int(course.price)
            cpdiscount=int(copun.discount)
            copundiscount=int(price-(price*cpdiscount*0.01))
            amount=copundiscount*100
        except:
            error_copun='Invalid Copun'
    if action=='payment':
        if request.user.is_authenticated:
            currency = "INR"
            notes = {
                "email" : user.email, 
                "name" : f'{user.username}'
            }
            reciept = f"learning-{int(time())}"
            order = client.order.create(
                {'receipt' :reciept , 
                'notes' : notes , 
                'amount' : amount ,
                'currency' : currency
                }
            )

            payment =Payment()
            payment.user  = user
            payment.course = course
            payment.order_id = order.get('id')
            payment.save()
   
        else:
            url= f'/login?next=/check-out/{slug}?action=payment'
            return HttpResponseRedirect(url)

    context={
       'course':course,
       'buy':buy,
       'copun':copun,
       'copundiscount':copundiscount,
       'cpdiscount':cpdiscount,
       'error_copun':error_copun,
        "modules" : modules, 
        "order" : order, 
        "payment" : payment, 
        'enroll':enroll,

       

    }       
    return render(request,'course/checkout.html',context)


@login_required(login_url='/login')
@csrf_exempt
def verifyPayment(request):
    if request.method == "POST":
        data = request.POST
        context = {}
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']
            payment = Payment.objects.get(order_id = razorpay_order_id)
            payment.payment_id  = razorpay_payment_id
            payment.status =  True        
            userCourse = UserCourse(user = payment.user , course = payment.course)
            userCourse.save()
            payment.user_course = userCourse
            payment.save()
            return HttpResponseRedirect('/mycourse')   

        except:
            messages.error(request, 'Something went wrong try again!')
            return HttpResponseRedirect('/profile')



@login_required(login_url='/login')
def Mycourse(request):
    courses=UserCourse.objects.filter(user=request.user)
    return render(request, 'course/mycourse.html',{'courses':courses})