from django.shortcuts import render

# Create your views here.
from session_api.models import session_client_data, AuthToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from datetime import timedelta
import json
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from session_api.auth import CustomAuthentication
from session_api.exceptions import TokenExpired
from session_api.generators import generate_client_id, generate_client_secret
from session_api.serializers import AuthTokenCreateSerializer, SessionCreateSerializer

class LoginAccessView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = (JSONParser,)

    @swagger_auto_schema(
        operation_description="Get the Access token and refresh token for the Client_id and Client_Secret Provided",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['client_id', 'client_secret'],
            properties={
                'client_id': openapi.Schema(type=openapi.TYPE_STRING),
                'client_secret': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        security=[],
        tags=['GetAccessToken'],
        responses={200: AuthTokenCreateSerializer}
    )
    def post(self, request, *args, **kwargs):
        """[Get the Access token and refresh token for the Client_id and Client_Secret Provided]
        Arguments:
            {
                'client_id': str,
                'client_secret': str
            }
        Returns:
            {
                application: integer
                access_token: string
                refresh_token: string
                expiry_date: string($date-time)
                refresh_token_expiry: string($date-time)
                expired: boolean
                created_on: string($date-time)
            }
        """
        details = request.data
        req_client_id = details["client_id"]
        req_client_secret = details["client_secret"]
        try:
            client_present = session_client_data.objects.get(client_id=req_client_id)
            if check_password(req_client_secret, client_present.client_secret):
                pass
            else:
                return Response(data={"status": "Client invalid"}, status=status.HTTP_403_FORBIDDEN)
            try:
                token = AuthToken.objects.get(session_application=client_present)
                if (timezone.now() < token.expiry_date) and (timezone.now() < token.refresh_token_expiry):
                    res = (
                    AuthToken.objects.filter(session_application=client_present)
                    .order_by("-session_application_id")[0:1]
                    .values()
                    )[0]
                else:
                    token.access_token = generate_client_secret()
                    token.expiry_date = timezone.now() + timedelta(hours=2)
                    token.refresh_token = generate_client_secret()
                    token.refresh_token_expiry = timezone.now() + timedelta(days=7)
                    token.save()
                    res = (
                        AuthToken.objects.filter(session_application=client_present)
                        .order_by("-session_application_id")[0:1]
                        .values()
                    )[0]
            except Exception:
                AuthToken.objects.create(
                    session_application=client_present,
                    access_token=generate_client_secret(),
                    refresh_token=generate_client_secret(),
                    refresh_token_expiry = timezone.now() + timedelta(days=7),
                    expiry_date=timezone.now() + timedelta(minutes=5),
                )
                res = AuthToken.objects.filter(session_application=client_present).values()[0]
                return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            res = "Client not found"
            return Response(data={"status": "Client not found"}, status=status.HTTP_403_FORBIDDEN)
        return Response(res, status=status.HTTP_200_OK)


class CreateAccessView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = (JSONParser,)

    @swagger_auto_schema(
        operation_description="Get the Access token and refresh token for the Client_id and Client_Secret Provided",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['client_id', 'client_secret'],
            properties={
                'client_id': openapi.Schema(type=openapi.TYPE_STRING),
                'client_secret': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        security=[],
        tags=['GetAccessToken'],
        responses={200: AuthTokenCreateSerializer}
    )

    def post(self, request, *args, **kwargs):
        """[Get the Access token and refresh token for the Client_id and Client_Secret Provided]
        Arguments:
            {
                'client_id': str,
                'client_secret': str
            }
        Returns:
            {
                application: integer
                access_token: string
                refresh_token: string
                expiry_date: string($date-time)
                refresh_token_expiry: string($date-time)
                expired: boolean
                created_on: string($date-time)
            }
        """
        details = request.data
        req_client_id = details["client_id"]
        req_client_secret = details["client_secret"]
        try:
            client_present = session_client_data.objects.get(
                client_id=req_client_id, client_secret=req_client_secret
            )
            print(client_present)
            return Response(data={"status": "Client has existed, try to login using username"}, status=status.HTTP_403_FORBIDDEN)
        except:
            serializer = SessionCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data={"status": "Created account success"}, status=status.HTTP_200_OK)
            else:
                return Response(data={"status": "Created account failed"}, status=status.HTTP_403_FORBIDDEN)

class CheckSessionView(APIView):
    authentication_classes = [ CustomAuthentication ]
    permission_classes = []
    parser_classes = (JSONParser,)
    def get(self, request):
        return Response(data={"status": "session not expired"}, status=status.HTTP_200_OK)
