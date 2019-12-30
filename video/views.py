from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from main_app.models import Employee
from channel.models import channel_model
from main_app.views import logger_function
from .models import video_class
from django.core.files.storage import FileSystemStorage


# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny])
def upload_video1(request):
    return Response({'error': 'False'})


@api_view(['POST'])
@permission_classes([AllowAny])
def upload_video(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        video = request.FILES.get('video')
        thumb_image = request.FILES.get('thumb_image')
        # url = fs.url(filename)
        title = request.POST.get('title')
        description = request.POST.get('description')
        if Token.objects.filter(key=token).exists():
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            if Employee.objects.filter(user=user).exists():
                emp_obj = Employee.objects.get(user=user)
                if emp_obj.channel_id != 0:
                    channel_id = emp_obj.channel_id
                    if channel_model.objects.filter(id=channel_id).exists():
                        new_video = video_class(channel_id=channel_id, video=video, thumb_image=thumb_image
                                                , title=title, description=description)
                        new_video.save()
                        cha_obj = channel_model.objects.get(id=channel_id)
                        vid = cha_obj.video_id
                        vid = vid.split(",")
                        vid.append(str(new_video.id))
                        vid = ",".join(vid)
                        cha_obj.video_id = vid
                        cha_obj.save()
                        error = "false"
                        message = "Video uploaded successfully"
                        token = "empty"
                        data = {'error': error, 'message': message, 'token': token}
                        logger_function(token, message)
                        return Response(data)
                    error = "true"
                    message = "Channel not present"
                    token = "empty"
                    data = {'error': error, 'message': message, 'token': token}
                    logger_function(token, message)
                    return Response(data)
                error = "true"
                message = "Channel not present"
                token = "empty"
                data = {'error': error, 'message': message, 'token': token}
                logger_function(token, message)
                return Response(data)
            error = "true"
            message = "User not present"
            token = "empty"
            data = {'error': error, 'message': message, 'token': token}
            return Response(data)
        error = "true"
        message = "token is invalid"
        token = "empty"
        data = {'error': error, 'message': message, 'token': token}
        return Response(data)
    else:
        error = "true"
        message = "Invalid request type"
        token = "empty"
        data = {'error': error, 'message': message, 'token': token}
        return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def delete_video(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        video_id = request.POST.get('video_id')
        if Token.objects.filter(key=token).exists():
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            if Employee.objects.filter(user=user).exists():
                emp_obj = Employee.objects.get(user=user)
                if emp_obj.channel_id != 0:
                    channel_id_by_token = emp_obj.channel_id
                    if video_class.objects.filter(id=video_id).exists():
                        video_obj = video_class.objects.get(id=video_id)
                        channel_id_by_video = video_obj.channel_id
                        if channel_id_by_token == channel_id_by_video:
                            if channel_model.objects.filter(id=channel_id_by_token):
                                channel_obj = channel_model.objects.get(id=channel_id_by_token)
                                video_ids = channel_obj.video_id
                                video_ids = video_ids.split(",")
                                for id in video_ids:
                                    if id == video_id:
                                        video_ids.remove(id)
                                        break
                                video_ids = ",".join(video_ids)
                                channel_obj.video_id = video_ids
                                channel_obj.save()
                                video_obj.delete()
                                error = "false"
                                message = "video delete successfully."
                                token = "empty"
                                data = {'error': error, 'message': message, 'token': token}
                                logger_function(token, message)
                                return Response(data)
                            error = "ture"
                            message = "video is not uploaded by you"
                            token = "empty"
                            data = {'error': error, 'message': message, 'token': token}
                            logger_function(token, message)
                            return Response(data)
                        error = "ture"
                        message = "video not present"
                        token = "empty"
                        data = {'error': error, 'message': message, 'token': token}
                        logger_function(token, message)
                        return Response(data)
                    error = "ture"
                    message = "user not present"
                    token = "empty"
                    data = {'error': error, 'message': message, 'token': token}
                    return Response(data)
                error = "ture"
                message = "you have not created any channel"
                token = "empty"
                data = {'error': error, 'message': message, 'token': token}
                logger_function(token, message)
                return Response(data)
            error = "ture"
            message = "invalid user"
            token = "empty"
            data = {'error': error, 'message': message, 'token': token}
            return Response(data)
        error = "ture"
        message = "incorrect token"
        token = "empty"
        data = {'error': error, 'message': message, 'token': token}
        return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def like_video(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        video_id = request.POST.get('video_id')
        if Token.objects.filter(key=token).exists() and video_class.objects.filter(id=video_id).exists():
            video_obj = video_class.objects.get(id=video_id)
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            if Employee.objects.filter(user=user).exists():
                emp_obj = Employee.objects.get(user=user)
                like_ids = emp_obj.liked
                dislike_ids = emp_obj.disliked
                dislike_ids = dislike_ids.split(",")
                if video_id in dislike_ids:
                    dislike_ids.remove(video_id)
                    video_obj.dislike -= 1
                    dislike_ids = ",".join(dislike_ids)
                    emp_obj.disliked = dislike_ids
                if like_ids == "":
                    like_ids = video_id
                else:
                    like_ids = like_ids.split(",")
                    if video_id not in like_ids:
                        like_ids.append(video_id)
                    else:
                        error = "True"
                        message = "video already liked"
                        token = "empty"
                        data = {'error': error, 'message': message, 'token': token}
                        logger_function(token, message)
                        return Response(data)
                    like_ids = ",".join(like_ids)
                emp_obj.liked = like_ids
                video_obj.like += 1
                emp_obj.save()
                video_obj.save()
                error = "False"
                message = "video liked successfully"
                token = "empty"
                data = {'error': error, 'message': message, 'token': token}
                logger_function(token, message)
                return Response(data)
            error = "True"
            message = "user is not having proper data may be admin"
            token = "empty"
            data = {'error': error, 'message': message, 'token': token}
            logger_function(token, message)
            return Response(data)
        error = "True"
        message = "invalid token received"
        token = "empty"
        data = {'error': error, 'message': message, 'token': token}
        return Response(data)
    error = "True"
    message = "invalid request received"
    token = "empty"
    data = {'error': error, 'message': message, 'token': token}
    return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def dislike_video(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        video_id = request.POST.get('video_id')
        if Token.objects.filter(key=token).exists() and video_class.objects.filter(id=video_id).exists():
            video_obj = video_class.objects.get(id=video_id)
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            if Employee.objects.filter(user=user).exists():
                emp_obj = Employee.objects.get(user=user)
                dislike_ids = emp_obj.disliked
                like_ids = emp_obj.liked
                like_ids = like_ids.split(",")
                if video_id in like_ids:
                    like_ids.remove(video_id)
                    video_obj.like -= 1
                    like_ids = ",".join(like_ids)
                    emp_obj.liked = like_ids
                if dislike_ids == "":
                    dislike_ids = video_id
                else:
                    dislike_ids = dislike_ids.split(",")
                    if video_id not in dislike_ids:
                        dislike_ids.append(video_id)
                    else:
                        error = "True"
                        message = "video already disliked"
                        token = "empty"
                        data = {'error': error, 'message': message, 'token': token}
                        logger_function(token, message)
                        return Response(data)
                    like_ids = ",".join(dislike_ids)
                emp_obj.disliked = dislike_ids
                video_obj.dislike += 1
                emp_obj.save()
                video_obj.save()
                error = "False"
                message = "video disliked successfully"
                token = "empty"
                data = {'error': error, 'message': message, 'token': token}
                logger_function(token, message)
                return Response(data)
            error = "True"
            message = "user is not having proper data may be admin"
            token = "empty"
            data = {'error': error, 'message': message, 'token': token}
            logger_function(token, message)
            return Response(data)
        error = "True"
        message = "invalid token received"
        token = "empty"
        data = {'error': error, 'message': message, 'token': token}
        return Response(data)
    error = "True"
    message = "invalid request received"
    token = "empty"
    data = {'error': error, 'message': message, 'token': token}
    return Response(data)