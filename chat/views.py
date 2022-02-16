from rest_framework.views import APIView
from .models import User , Message
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer
from django.core import serializers


class Signup(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        try:
            user = User.objects.create(first_name=request.data['first_name']
                                       ,last_name=request.data['last_name']
                                       , username=request.data['username']
                                       , email=request.data['email'])
            user.set_password(request.data['password'])
            user.save()
            return Response({
                'message': 'success'
            }, status=200)
        except Exception as _:
            return Response({
                'message': 'bad request'
            }, status=400)


class Logout(APIView):

    def post(self, request, **kwargs):
        request.user.auth_token.delete()
        return Response(data={
                'message': 'success'
            }, status=200)


class UsersView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):

        return Response(data=
                serializers.serialize('json', User.objects.all())
            , status=200)


class MessagesView(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self,request , **kwargs):

        sender = request.user
        receiver = User.objects.filter(username=request.data['receiver'])

        sender_message = Message.objects.filter(sender=sender, receiver=receiver[0])
        receiver_message = Message.objects.filter(sender=receiver[0] ,receiver=sender)

        return Response(data={
                'sender_message': serializers.serialize('json',sender_message),
                'receiver_message': serializers.serialize('json',receiver_message),
            },status=200)