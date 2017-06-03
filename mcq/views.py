from django.shortcuts import render,redirect,render_to_response
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.contrib.auth.models import User
from .models import Qrecord, Qattempt, Profile, SeniorQrecord, SeniorQattempt
from random import randint
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone




from django.shortcuts import get_object_or_404


# Set max_question to the number of question available in database
#set per_skip_score to the amount of skip you have to give it to user for a skip 
#set competition_time_minute 

global_id = 0
max_question = 99                                
correct_score = 4
wrong_score = 2
competition_time_minute = 20
per_skip_score = 1
# per_skip_minute = 2

# Returns time via HttpResponse
questionDatabase = SeniorQrecord
AttemptedQuestion = SeniorQattempt

@csrf_exempt
def get_time(request):
    profile_obj = get_object_or_404(Profile, user=request.user)
    end_time = profile_obj.end
    diff = end_time-timezone.now()
    diff_seconds = diff.seconds
    return HttpResponse(str(diff_seconds))


@csrf_exempt
def home(request):
    return render(request, "home.html")


@csrf_exempt
def signup(request):
    return render(request, 'signup.html')




@csrf_exempt
def new_user(request):
    global global_id, questionDatabase, AttemptedQuestion
    if request.POST.get('signup'):
        if request.method == 'POST':
            if User.objects.filter(username=str(request.POST.get('uname'))).exists():
                return render(request, 'signup.html', {'message': "User already exists."})
            else:
                uname = request.POST.get('uname')
                password = request.POST.get('passwd')
                email = request.POST.get('email')
                obj = User.objects.create_user(username=str(uname), password=str(password), email=str(email))
                obj1 = Profile.objects.create(score=0, name1=request.POST.get('name1'), name2=request.POST.get('name2'), contact=request.POST.get('contact'), college=request.POST.get('college'), reciept=request.POST.get('reciept'), start=timezone.now(), end=(timezone.now() + timedelta(minutes=competition_time_minute)), lasttimeupdated=timezone.now(), user=obj, level=request.POST.get('level'))
                user = authenticate(username=uname, password=password)
                if user is not None:
                    login(request, user)
                    prof_obj = Profile.objects.get(user=request.user)
                    if prof_obj.level == "Junior":
                        questionDatabase = Qrecord
                        AttemptedQuestion = Qattempt
                    else:
                        questionDatabase = SeniorQrecord
                        AttemptedQuestion = SeniorQattempt

                    prof_obj.endgame = True
                    prof_obj.save()
                    global_id = randint(1, max_question)
                    obj = questionDatabase.objects.filter(id=int(global_id))
                    return render(request, 'page2.html', {'obj': obj, 'obj1': [obj1]})
                else:
                    return render(request, 'signup.html')

    if request.POST.get('login'):
        if request.method == 'POST':
            username = request.POST.get('username')				# gets username from text field
            password = request.POST.get('password')				# gets password from password field
            user = authenticate(username=username, password=password)    # checks for correct username and password
            if user is not None:
                o = User.objects.get(username=username)
                prof_obj = Profile.objects.get(user=o)
                if prof_obj.level == "Junior":
                    questionDatabase = Qrecord
                    AttemptedQuestion = Qattempt
                else:
                    questionDatabase = SeniorQrecord
                    AttemptedQuestion = SeniorQattempt
                if prof_obj.endgame:
                    return render(request, 'signup.html', {'message1': "You have Attempted a Test"})

                prof_obj.endgame = True
                prof_obj.score -= prof_obj.skipscoreadded
                prof_obj.skipscoreadded = 0
                prof_obj.save()

                login(request, user)
                global_id = randint(1, max_question)
                while True:
                    try:
                        if AttemptedQuestion.objects.filter(user=request.user, attempt=global_id).exists():
                            global_id = randint(1, max_question)
                        else:
                            break
                    except:
                        break

                obj = questionDatabase.objects.filter(id=int(global_id))
                o = User.objects.get(username=request.user)

                # obj1=Profile.objects.filter(user=o)			<--error kyu aaya
                # obj1=User.objects.filter(user=request.user) 		<--pata hai its wrong bt try krne me kya jara
                # obj1=Profile.objects.filter(user="roshan")		<--dummy try krte
                # obj1=Profile.objects.filter(user=request.user)		<--ab work krega

                obj1 = Profile.objects.get(user=o)			# <--Yeaaaaa its working

                # objarray = Profile.objects.filter(user=o)		<--As well ye bhi :P
                # if len(objarray) == 1 :
                #     obj1 = objarray[0]
                # else :
                #     pass

                return render(request, 'page2.html', {'obj': obj, 'obj1': [obj1]})
            else:
                return render(request, 'signup.html',{'message1' : "Invalid UserName Or Password"})


@csrf_exempt
def index(request):
    global global_id, questionDatabase, AttemptedQuestion
    Profile.objects.filter(user=request.user).update(lasttimeupdated=timezone.now())
    if request.POST.get('sub_ans'):
        if request.POST:
            if request.user.is_authenticated():
                print global_id
                ans = request.POST.get('choice')
                p = Profile.objects.get(user=request.user)
                # print (ans)
                obj = questionDatabase.objects.get(id=int(global_id))
                ob = questionDatabase.objects.get(id=int(global_id))
                if str(obj.correct) == str(ans):
                    obj_score = Profile.objects.get(user=request.user)
                    t_score = int(obj_score.score)+correct_score
                    Profile.objects.filter(user=request.user).update(score=t_score)
                    if int(p.count) == 0:
                        Profile.objects.filter(user=request.user).update(count=1)
                    elif int(p.count) == 1:
                        Profile.objects.filter(user=request.user).update(count=2)
                    elif int(p.count) == 2:
                        Profile.objects.filter(user=request.user).update(count=0)
                        Profile.objects.filter(user=request.user).update(skip=int(p.skip)+1)

                    Profile.objects.filter(user=request.user).update(wrong_count=0)
                    if int(p.correct_count) == 0:
                        Profile.objects.filter(user=request.user).update(correct_count=1)
                    elif int(p.correct_count) == 1:
                        Profile.objects.filter(user=request.user).update(correct_count=2)
                    elif int(p.correct_count) == 2:
                        Profile.objects.filter(user=request.user).update(correct_count=3)
                    elif int(p.correct_count) == 3:
                        Profile.objects.filter(user=request.user).update(correct_count=0)
                        Profile.objects.filter(user=request.user).update(score=t_score+4)


                    q = AttemptedQuestion(user=p, attempt=ob, correct_count=1)
                    q.save()

                elif str(ans)=='None':
                    print("WTF")
                    obj = questionDatabase.objects.filter(id=int(global_id))
                    o = User.objects.get(username=request.user)
                    obj1 = Profile.objects.filter(user=o)
                    return render(request, 'page2.html', {'obj': obj, 'obj1': obj1, 'message': "Select an answer."})
                
                else:
                    o = User.objects.get(username=request.user)
                    obj_score = Profile.objects.get(user=o)
                    t_score = int(obj_score.score)-wrong_score
                    Profile.objects.filter(user=o).update(score=t_score)
                    Profile.objects.filter(user=o).update(count=0)

                    Profile.objects.filter(user=request.user).update(correct_count=0)
                    if int(p.wrong_count) == 0:
                        Profile.objects.filter(user=request.user).update(wrong_count=1)
                    elif int(p.wrong_count) == 1:
                        Profile.objects.filter(user=request.user).update(wrong_count=2)
                    elif int(p.wrong_count) == 2:
                        Profile.objects.filter(user=request.user).update(wrong_count=0)
                        Profile.objects.filter(user=request.user).update(score=t_score-3)


                    q = AttemptedQuestion(user=p, attempt=ob, correct_count=0)
                    q.save()
                # Q = Qattempt.objects.get(user=request.user, attempt=Qrecord.objects.get(pk=int(global_id)))

                while True:
                    global_id = randint(1, max_question)
                    if AttemptedQuestion.objects.filter(user=p, attempt=global_id, correct_count=1).exists():
                        print("")
                    elif AttemptedQuestion.objects.filter(user=p, attempt=global_id, correct_count=0).exists():
                        print("")
                    else:
                        obj = questionDatabase.objects.filter(id=int(global_id))
                        o = User.objects.get(username=request.user)
                        obj1 = Profile.objects.filter(user=o)
                        return render(request, 'page2.html', {'obj': obj, 'obj1': obj1})    # INFINITE LOOOOOO:O:P###
            else:
                return render(request, 'invalid.html')
    if request.POST.get('skip'):
        global global_id
        p = Profile.objects.get(user=request.user)
        if int(p.skip) > 0:
            Profile.objects.filter(user=request.user).update(skip=int(p.skip)-1)
            oo2 = questionDatabase.objects.get(id=int(global_id))
            oo3 = AttemptedQuestion(user=p, attempt=oo2)
            oo3.save()
            while True:
                global_id = randint(1, max_question)
                if AttemptedQuestion.objects.filter(user=p, attempt=global_id).exists():
                    print("")
                else:
                    obj = questionDatabase.objects.filter(id=int(global_id))
                    obj1 = Profile.objects.filter(user=request.user)
                    return render(request, 'page2.html', {'obj': obj, 'obj1': obj1})
        else:
            print("WTF")
            obj = questionDatabase.objects.filter(id=int(global_id))
            obj1 = Profile.objects.filter(user=request.user)
            return render(request, 'page2.html', {'obj': obj, 'obj1': obj1, 'message2': "No skips left!"})

    return render(request, 'signup.html')


def handler404(request):
    response = render_to_response('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response


# def select(request):
#     return render(request,"select.html")

# user selects skip after 20 mins


# @csrf_exempt
# def skips(request):
#     profile_obj=Profile.objects.get(user=request.user)
#     skips=profile_obj.skip
#     profile_obj.score=profile_obj.score+(skips*1) #Skip multiplier here
#     profile_obj.save()
#     newscore=profile_obj.score
#     logout(request)
#     return render(request,"endgame.html",{'score':newscore })
#

# @csrf_exempt
# def playmore(request):
#     profile_obj=Profile.objects.get(user=request.user)
#     profile_obj.start=datetime.now()
#     profile_obj.end=datetime.now()+timedelta(minutes=int(profile_obj.skip)*per_skip_minute	)
#     profile_obj.access=False
#     profile_obj.save()
#     while(True):
#         random=randint(1,max_question)
#         qobj=Qrecord.objects.get(id=random)
#         if not Qattempt.objects.filter(user=profile_obj,attempt=qobj).exists():
#             break
#     return render(request, 'playmore.html', {'obj':[qobj],'obj1':[profile_obj]})


@csrf_exempt
def endgame(request):
    profile_obj = Profile.objects.get(user=request.user)
    skips = profile_obj.skip
    profile_obj.score += (skips*per_skip_score)    # Skip multiplier here
    profile_obj.skipscoreadded = skips*per_skip_score
    profile_obj.save()
    new_score = profile_obj.score
    user = profile_obj.user
    logout(request)
    return render(request, "endgame.html", {'score': new_score, 'user': user})


@csrf_exempt
def powerbackup(request):
    if request.POST.get('password')=="yolo":
        if request.POST.get('username')=="all":
            p = Profile.objects.all()
            for asd in p:
                timedeltavalue = asd.end + (timezone.now() - asd.lasttimeupdated)
                asd.end = timedeltavalue
                asd.lasttimeupdated = timezone.now()
                asd.endgame = False
                asd.save()
        elif request.POST.get('username'):
            u = User.objects.get(username=request.POST.get('username'))
            p = Profile.objects.get(user=u)
            timedeltavalue = p.end + (timezone.now() - p.lasttimeupdated)
            p.end = timedeltavalue
            p.lasttimeupdated = timezone.now()
            p.endgame = False
            p.save()
        else:
            print("***********No username******************")

        return render(request, "powerbackup.html", {'message': "Successfully Executed"})

    return render(request, "powerbackup.html", {'message': "Invalid Password"})
