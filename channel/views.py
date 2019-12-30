from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from main_app.views import logger_function
from main_app.models import Employee
from .models import channel_model
from video.models import video_class
from django.contrib.auth.models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def create_channel(request):
    data = {}
    if request.method == "POST":
        token = request.POST.get('token')
        logo = request.FILES.get('logo')
        title = request.POST.get('title')
        description = request.POST.get('description')
        if Token.objects.filter(key=token):
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            employee = Employee.objects.get(user=user)
            if employee.channel_id == 0:
                channel_obj = channel_model(logo=logo, title=title, description=description)
                channel_obj.save()
                # channel_obj = channel_model.objects.get(title=title)
                employee.channel_id = channel_obj.id
                print(channel_obj.id)
                employee.save()
                message = 'channel create successfully'
                error = 'False'
                data = {'message ': message, 'error': error}
            else:
                message = 'channel already exist'
                error = 'True'
                data = {'message ': message, 'error': error}

        else:  # if  Token not found in database means user not exit
            message = 'token not found'
            error = 'True'
            data = {'message ': message, 'error': error}
    return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def delete_channel(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        channel_id = request.POST.get('channel_id')
        if Token.objects.filter(key=token).exists():
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            if Employee.objects.filter(user=user).exists():
                emp_obj = Employee.objects.get(user=user)
                channel_id_by_token = emp_obj.channel_id
                print(" found:" + str(channel_id))
                if str(channel_id) == str(channel_id_by_token):
                    if channel_model.objects.filter(id=channel_id).exists():
                        channel_obj = channel_model.objects.get(id=channel_id)
                        video_ids = channel_obj.video_id
                        video_ids = video_ids.split(",")
                        video_ids.remove("")
                        for v in video_ids:
                            if video_class.objects.filter(id=v).exists():
                                temp = video_class.objects.get(id=v)
                                temp.delete()
                        channel_obj.delete()
                        emp_obj.channel_id = 0
                        emp_obj.save()
                        error = "False"
                        message = "your channel deleted successfully and your videos too"
                        token = "empty"
                        data = {'error': error, 'message': message, 'token': token}
                        logger_function(token, message)
                        return Response(data)
                    error = "True"
                    message = "channel doesn't present"
                    token = "empty"
                    data = {'error': error, 'message': message, 'token': token}
                    logger_function(token, message)
                    return Response(data)
                error = "True"
                message = "invalid channel id"
                token = "empty"
                data = {'error': error, 'message': message, 'token': token}
                logger_function(token, message)
                return Response(data)
            error = "True"
            message = "invalid user id"
            token = "empty"
            data = {'error': error, 'message': message, 'token': token}
            logger_function(token, message)
            return Response(data)
        error = "True"
        message = "token is invalid"
        token = "empty"
        data = {'error': error, 'message': message, 'token': token}
        return Response(data)
    error = "True"
    message = "invalid request type"
    token = "empty"
    data = {'error': error, 'message': message, 'token': token}
    return Response(data)
