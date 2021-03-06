import math
import random
import requests
from datetime import datetime, date
from pymongo import MongoClient
from rest_framework.authtoken.models import Token
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Employee, Otp
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from channel.models import channel_model
from video.models import video_class
from video.loading import filter_unnessary

client = MongoClient('mongodb://127.0.0.1:27017')
db = client.test
db = db.geniobits


# Create your views here.

# Logger function

# logger_history_function


def video_logger(user_id, video_id, video_tags, activity):
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.geniobits
    mycollection = db['video_log']
    today = date.today()
    print(datetime.now())
    today = (str(datetime.now()).split(" ")[1]).split(".")[0]
    print(today)
    if mycollection.find({'user_id': user_id}).count() <= 0:
        mydict = {'user_id': user_id, 'activity': []}
        inserting = mycollection.insert(mydict)
    result = mycollection.update({
        'user_id': user_id
    }, {
        '$push': {
            'activity': {'video_id': video_id, 'video_tags': video_tags, 'activity': activity,
                         'time': str(datetime.now())}
        }
    })


def logger_function(username, activity):
    flag = 0
    print('call')
    if User.objects.filter(username=username):  # change here
        print('username found in database')
        flag = 1

    if Token.objects.filter(key=username):
        print('Token found in database')
        token = Token.objects.get(key=username)
        username = token.user.username  # change here
        flag = 1

    if flag == 1:
        client = MongoClient('mongodb://127.0.0.1:27017')
        print('database connection successfully')
        db = client.geniobits
        mycollection = db[username]
        today = date.today()
        today = str(today)
        today = '2019-12-31'
        print('today date : ' + today)
        print(username)
        if username in db.list_collection_names():
            print('usename found in document ')
            result = mycollection.update({
                'date': today
            }, {
                '$push': {
                    "activity": activity,
                }
            })
            print(str(result['updatedExisting']) + ' date not found create new database')
            if not result['updatedExisting']:
                mycollection.insert({
                    'user': username,
                    "activity": [activity],
                    "date": today
                })
                print('new document create successful')
        else:
            print('usename not found in document')
            mycollection.insert({
                'user': username,
                "activity": [activity],
                "date": today
            })
    else:
        print('username not found')
    return


def logger_function_no_work(username, activity):
    flag = 0
    if User.objects.filter(username=username).exists():  # change here
        flag = 1
    if Token.objects.filter(key=username).exists():
        token_obj = Token.objects.get(key=username)
        username = token_obj.user.username
        flag = 1
    if flag == 1:
        db.insert({"username": username, "activity": activity, "data": datetime.now()})
    return


def home(request):
    db.insert({"Rules": "My life my rules"})
    Result = db.find()
    print(Result)
    for c in Result:
        print(c)
    return render(request, 'main_app/home.html')


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)  # change here
        if user is not None:
            login(request, user)  # change here
            if Token.objects.filter(user=user).exists():  # change here
                token = Token.objects.get(user=user)  # change here
                token.delete()
            token = Token.objects.create(user=user)  # change here
            user = User.objects.get(username=token.user.username)  # change here
            print(user.username)
            emp_object = Employee.objects.get(user=user)  # change here
            if not emp_object.is_verify:
                data = {'message': 'mobile number not verify', 'error': 'False', 'token': token.key}
            data = {'message': 'user log in successfully', 'error': 'False', 'token': token.key}
            print(data)
            # Response(data)
            # print(data)
            # return Response(data)
            logger_function(username, 'mobile number not verify')
            return Response(data)
        else:
            data = {'message': 'user not log in', 'error': 'True', 'token': 'empty'}
            print(data)
            # Response(data)
            # print(data)
            logger_function(username, 'user not log in')
            return Response(data)


def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
    req_params = {
        'apikey': apiKey,
        'secret': secretKey,
        'usetype': useType,
        'phone': phoneNo,
        'message': textMessage,
        'senderid': senderId
    }
    return requests.post(reqUrl, req_params)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = {}
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        print(password)
        print(re_password)
        if password == re_password:
            if User.objects.filter(username=username).exists():  # change here
                data = {'message': 'username already exist', 'error': 'True', 'token': ''}
            else:
                if not Employee.objects.filter(phone_no=phone_no).exists():  # change here
                    user = User.objects.create_user(username, email, password)  # change here
                    user.save()
                    profile = Employee(user=user, phone_no=phone_no)
                    profile.save()
                    login(request, user)
                    token = Token.objects.create(user=user)
                    print(token.key)
                    digits = "0123456789"
                    OTP = ""
                    # duration = (datetime.now().time() - Otp.time_generate_otp);
                    for i in range(6):
                        OTP += digits[math.floor(random.random() * 10)]
                    if not Otp.objects.filter(user=user):
                        obj = Otp(user=user, attempts=5, OTP=OTP)  # change here
                        obj.save()
                    obj = Otp.objects.get(user=user)
                    if obj.get_time_diff() > 3600:
                        obj = Otp(user=user, attempts=5, OTP=OTP)
                        obj.save()
                    text_message = 'your OTP is : ' + OTP

                    data = {'message': 'user registration successful', 'error': 'False', 'token': token.key}
                    URL = 'https://www.sms4india.com/api/v1/sendCampaign'
                    response = sendPostRequest(URL, '600XK5ONNJVYPIO66ZHUTX4PXBCGA7NT', '9TFM3V54JHDYK127', 'stage',
                                               '+91' + phone_no, '012345', text_message)

                    print(response.text)
                else:
                    data = {'message': 'Phomne number already exist with another username', 'error': 'True',
                            'token': ''}
                    logger_function(username, 'Phomne number already exist with another username')

        else:
            data = {'message': 'password and re_enter password not match', 'error': 'True', 'token': ''}
            # Response(data)
            # print(data)
    return Response(data)


#
# @api_view(['POST'])
# @login_required
# def create_token(request,user):
#     # user = User.objects.get(username=request.data.get('username'))
#     return HttpResponse({'token': token.key})
#
#


def logout(request):
    auth_logout(request)

    return render(request, "main_app/home.html")


@api_view(['POST'])
@permission_classes([AllowAny])
def profileinfo(request):
    if request.method == "POST":
        token = request.POST.get('token')
        if Token.objects.filter(key=token).exists():
            token = Token.objects.get(key=token)
            message = 'token present'
            username = token.user.username
            email = token.user.email
            phone_no = token.user.employee.phone_no
            error = 'False'
            token = 'empty'
            data = {'message': message, 'username': username, 'email': email, 'phone_no': phone_no, 'error': error,
                    'token': token}
            logger_function(username, message)
            return Response(data)
        else:
            message = 'token not present'
            username = 'empty'
            email = 'empty'
            phone_no = 'empty'
            token = 'empty'
            error = 'True'
            data = {'message': message, 'username': username, 'email': email, 'phone_no': phone_no, 'error': error,
                    'token': token}
            logger_function(username, message)
            return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_opt(request):
    if request.method == "POST":
        token = request.POST.get('token')
        otp = request.POST.get('otp')
        if Token.objects.filter(key=token):
            token_obj = Token.objects.get(key=token)
            print(token_obj.key)
            user = token_obj.user
            print(user.username)
            otp_object = Otp.objects.get(user=user)
            print(otp_object.OTP)
            print(otp_object.attempts)
            print(otp)
            if otp_object.get_time_diff() > 1800:
                message = 'Otp expired try later'
                username = 'empty'
                phone_no = 'empty'
                error = 'True'
                data = {'message': message, 'username': username, 'phone_no': phone_no, 'error': error, }
                logger_function(username, message)
                return Response(data)
            elif otp_object.attempts < 0:
                message = 'you try more than 5 time'
                username = 'empty'
                phone_no = 'empty'
                error = 'True'
                data = {'message': message, 'username': username, 'phone_no': phone_no, 'error': error, }
                logger_function(username, message)
                return Response(data)
            elif int(otp_object.OTP) == int(otp):
                otp_object.is_verify = "True"
                username = user.username
                message = "Otp successfull verify " + username
                phone_no = user.employee.phone_no
                error = 'False'
                otp_object.is_verify = "True"
                data = {'message': message, 'username': username, 'phone_no': phone_no, 'error': error}
                logger_function(username, message)
                return Response(data)
            else:
                otp_object.attempts = otp_object.attempts - 1
                otp_object.save()
                username = user.username
                message = "Otp not match try later"
                phone_no = user.employee.phone_no
                error = 'True'
                data = {'message': message, 'username': username, 'phone_no': phone_no, 'error': error}
                logger_function(username, message)
                return Response(data)
        else:
            message = 'Token Not verify'
            username = 'empty'
            phone_no = 'empty'
            error = 'True'
            data = {'message': message, 'username': username, 'phone_no': phone_no, 'error': error}
            return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def mobile_check(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        phone_no = request.POST.get('phone_no')
        if Token.objects.filter(key=token).exists:
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            if Employee.objects.filter(user=user).exists():
                obj = Employee.objects.get(user=user)
                phone_no_old = obj.phone_no
                if phone_no != phone_no_old:
                    emp_obj = Employee.objects.get(user=user)
                    emp_obj.phone_no = phone_no
                    emp_obj.save()
                    error = "False"
                    message = "User phone number is updated."
                    token = "empty"
                    data = {"error": error, "message": message, "token": token}
                    logger_function(token, message)
                    return Response(data)
                else:
                    error = "False"
                    message = "User phone number is already correct."
                    token = "empty"
                    data = {"error": error, "message": message, "token": token}
                    logger_function(token, message)
                    return Response(data)
        error = "True"
        message = "Token is not present or phone_no is not present."
        token = "empty"
        data = {"error": error, "message": message, "token": token}
        return Response(data)
    return Response()


@api_view(['POST'])
@permission_classes([AllowAny])
def delete_user(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        if Token.objects.filter(key=token).exists():
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            # token_obj.delete()
            if Employee.objects.filter(user=user).exists():
                emp_obj = Employee.objects.get(user=user)
                channel_id_by_token = emp_obj.channel_id
                user.delete()
                if channel_model.objects.filter(id=channel_id_by_token).exists():
                    channel_obj = channel_model.objects.get(id=channel_id_by_token)
                    video_ids = channel_obj.video_id
                    video_ids = video_ids.split(",")
                    video_ids.remove("")
                    for v in video_ids:
                        if video_class.objects.filter(id=v).exists():
                            temp = video_class.objects.get(id=v)
                            temp.delete()
                    channel_obj.delete()
                    error = "False"
                    message = "your channel deleted successfully and your videos too"
                    token = "empty"
                    data = {'error': error, 'message': message, 'token': token}
                    logger_function(token, message)
                    return Response(data)
                error = "False"
                message = "channel was not created"
                token = "empty"
                data = {'error': error, 'message': message, 'token': token}
                logger_function(token, message)
                return Response(data)
            user.delete()
            error = "False"
            message = "user deleted or may user is admin with doesn't have employee table entry"
            token = "empty"
            data = {'error': error, 'message': message, 'token': token}
            logger_function(token, message)
            return Response(data)
        error = "True"
        message = "invalid token"
        token = "empty"
        data = {'error': error, 'message': message, 'token': token}
        return Response(data)
    error = "True"
    message = "invalid request type"
    token = "empty"
    data = {'error': error, 'message': message, 'token': token}
    return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if Employee.objects.filter(user=user).exists():
                emp_obj = Employee.objects.get(user=user)
                phone_no = emp_obj.phone_no
                digits = "0123456789"
                digit = "123456789"
                OTP = ""
                # duration = (datetime.now().time() - Otp.time_generate_otp);
                for i in range(6):
                    if i == 0:
                        OTP += digit[math.floor(random.random() * 10)]
                    else:
                        OTP += digits[math.floor(random.random() * 10)]
                if Otp.objects.filter(user=user).exists():
                    otp_obj = Otp.objects.get(user=user)
                    otp_obj.delete()
                obj = Otp(user=user, attempts=5, OTP=OTP)
                obj.save()
                error = 'False'
                message = 'otp sent successfully'
                token = 'empty'
                data = {'error': error, 'message': message, 'token': token}
                logger_function(username, message)
                return Response(data)
            error = 'True'
            message = 'username my be admin'
            token = 'empty'
            data = {'error': error, 'message': message, 'token': token}
            logger_function(username, message)
            return Response(data)
        error = 'True'
        message = 'user not exists'
        token = 'empty'
        data = {'error': error, 'message': message, 'token': token}
        return Response(data)
    error = 'True'
    message = 'request type is invalid'
    token = 'empty'
    data = {'error': error, 'message': message, 'token': token}
    return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        otp = request.POST.get('otp')
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if Otp.objects.filter(user=user).exists():
                otp_obj = Otp.objects.get(user=user)
                otp_in_table = otp_obj.OTP
                print("-----------------------------------")
                print(otp_in_table)
                print(otp)
                print("-----------------------------------")
                if otp_in_table == int(otp) and otp_obj.attempts > 0:
                    otp_obj.delete()
                    if Token.objects.filter(user=user).exists():
                        token_obj = Token.objects.get(user=user)
                    else:
                        token_obj = Token.objects.create(user=user)
                    error = 'False'
                    message = 'otp varified successfully'
                    token = token_obj.key
                    data = {'error': error, 'message': message, 'token': token}
                    logger_function(username, message)
                    return Response(data)
                otp_obj.attempts -= 1
                otp_obj.save()
                if otp_obj.attempts <= 0:
                    digits = "0123456789"
                    digit = "123456789"
                    OTP = ""
                    # duration = (datetime.now().time() - Otp.time_generate_otp);
                    for i in range(6):
                        if i == 0:
                            OTP += digit[math.floor(random.random() * 10)]
                        else:
                            OTP += digits[math.floor(random.random() * 10)]
                    if Otp.objects.filter(user=user).exists():
                        otp_obj = Otp.objects.get(user=user)
                        otp_obj.delete()
                    obj = Otp(user=user, attempts=5, OTP=OTP)
                    obj.save()
                    error = 'True'
                    message = 'new otp generated due to max wrong attempts'
                    token = 'empty'
                    data = {'error': error, 'message': message, 'token': token}
                    logger_function(username, message)
                    return Response(data)
                error = 'True'
                message = 'wrong attempts'
                token = 'empty'
                data = {'error': error, 'message': message, 'token': token}
                logger_function(username, message)
                return Response(data)
            error = 'True'
            message = 'first tap on send otp.'
            token = 'empty'
            data = {'error': error, 'message': message, 'token': token}
            logger_function(username, message)
            return Response(data)
        error = 'True'
        message = 'invalid username'
        token = 'empty'
        data = {'error': error, 'message': message, 'token': token}
        return Response(data)
    error = 'True'
    message = 'wrong request type'
    token = 'empty'
    data = {'error': error, 'message': message, 'token': token}
    return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def resend_reset_otp(request):
    return reset(request)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_change(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        token = request.POST.get('token')
        if password == re_password:
            if Token.objects.filter(key=token).exists():
                token_obj = Token.objects.get(key=token)
                user = token_obj.user
                if user.password == password:
                    error = 'True'
                    message = 'password can\'t be old one'
                    token = 'empty'
                    data = {'error': error, 'message': message, 'token': token}
                    logger_function(token, message)
                    return Response(data)
                user.password = password
                user.save()
                error = 'False'
                message = 'password reset successfully'
                token = 'empty'
                data = {'error': error, 'message': message, 'token': token}
                logger_function(token, message)
                return Response(data)
            error = 'True'
            message = 'user is invalid'
            token = 'empty'
            data = {'error': error, 'message': message, 'token': token}
            return Response(data)
        error = 'True'
        message = 'password not match'
        token = 'empty'
        data = {'error': error, 'message': message, 'token': token}
        return Response(data)
    error = 'True'
    message = 'wrong request type'
    token = 'empty'
    data = {'error': error, 'message': message, 'token': token}
    return Response(data)


# trending data for the user with any search when he visit for the first time.


@api_view(['POST'])
@permission_classes([AllowAny])
def trending(request):
    token = request.POST.get('token')
    if Token.objects.filter(key=token).exists():
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
        if Employee.objects.filter(user=user).exists():
            emp_obj = Employee.objects.get(user=user)
            if emp_obj.tags != "":
                obj = emp_obj.tags
                if obj is not None:
                    lists = emp_obj.tags.split(",")
                    user_dataset(lists)
    return Response()


def user_dataset(tags):
    dataset = []
    for tag in tags:
        dataset_tags = video_class.objects.filter(tags__contains=tag)
        for d in dataset_tags:
            dataset.append(d)
    dataset = list(dict.fromkeys(dataset))
    list1 = []
    list2 = []
    for i in dataset:
        video_score = 0
        for tag in tags:
            if tag in i.tags:
                video_score += 100  # tags = 100 || like = 10 / total days || dislike = -10 / total days || views = 1/td
        video_score += (i.views + 20 * (i.like - i.dislike)) / (i.get_time_diff())
        list1.append(video_score)
        list2.append(i.id)
    list1, list2 = zip(*sorted(zip(list1, list2)))
    all_videos = []
    video_ids = list2
    for i in video_ids:
        video = video_class.objects.filter(id=i)
        for v in video:
            all_videos.append(v)
    all_videos = all_videos[::-1]
    print(all_videos)
    return Response()


@api_view(['POST'])
@permission_classes([AllowAny])
def search(request):
    result_videos = []  # separate list for the end result
    search_keyword = request.POST.get('search')
    if search_keyword is not None:
        search_useful_tags = filter_unnessary(search_keyword)  # returns list of useful data only
        for tags in search_useful_tags:
            video_having_tags = video_class.objects.filter(tags__contains=tags)
            for vid in video_having_tags:
                result_videos.append(vid)
            result_videos = list(dict.fromkeys(result_videos))  # Filter repeated objects
            list1 = []
            list2 = []
            for v in result_videos:
                video_score = 0
                for tag in search_useful_tags:
                    if tag in v.tags:
                        video_score += 100
                video_score += v.views + 20 * (v.like - v.dislike)  # ) / (v.get_time_diff())
                list1.append(video_score)
                list2.append(v)
            list2 = list2[::-1]
            print(list2)
            dictn = {}
            for l in list2:
                dictn[l.id] = l.title
            return Response(dictn)
