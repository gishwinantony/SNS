from datetime import timedelta

from django.contrib.auth import authenticate
from django.db.models import Q
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .Exceptions import CustomException
from .models import FriendRequests, CustomUser
from .serializers import UserRegister, FriendRequestsSerializer, CustomSearchUserSerializer
from .utils import get_user_id_from_token


class CreateUserAPIView(APIView):
    authentication_classes = []

    def post(self, request):
        try:
            user = UserRegister(data=request.data)
            if user.is_valid():
                user.save()
                return Response("SignUp Successfull")
            else:
                return Response({"errors": user.errors}, status=400)
        except Exception as e:
            return Response({"message": str(e)}, status=500)


class AuthenticateUserAPIView(APIView):
    authentication_classes = []

    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                return Response({"error": "Please provide both email and password"}, status=400)
            user = authenticate(email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                refresh_token = str(refresh)
                access_token = str(refresh.access_token)
                return Response({
                    "acess_token": access_token,
                    "refresh_token": refresh_token,
                    "email": user.email
                })
            else:
                return Response({"error": "Please provide valid credentials"}, status=401)
        except Exception as e:
            return Response({"message": str(e)}, status=500)


class SendRequestAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            sender_id = request.data.get('sender_id')
            requested_id = request.data.get('requested_id')

            if not requested_id or not sender_id:
                return Response({"error": "Please provide both sender_id and requested_id"}, status=400)
            sender = CustomUser.objects.filter(id=sender_id).first()
            if not sender:
                raise CustomException("Sender id is invalid", 400)

            requested = CustomUser.objects.filter(id=requested_id).first()
            if not requested:
                raise CustomException("Requested id is invalid", 400)
            if FriendRequests.objects.filter(sender=sender, requested=requested, request_status__in=[0, 1]).exists():
                raise CustomException("Request already send.....", 400)

            one_minute_ago = timezone.now() - timedelta(minutes=1)
            recent_requests_count = FriendRequests.objects.filter(sender=sender, created_at__gte=one_minute_ago).count()
            if recent_requests_count >= 3:
                raise CustomException("You can only send 3 friend requests per minute", 400)
            FriendRequests.objects.create(sender=sender, requested=requested)
            return Response({"message": "Request Send Successfully"})

        except CustomException as e:
            return Response(
                {"error_message": e.message, "error_code": e.error_code},
                status=e.error_code,
            )
        except Exception as e:
            return Response({"message": str(e)}, status=500)


class UpdateRequestAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        try:
            action = request.query_params.get('action', '')
            if not action:
                raise CustomException("Action keyword is required", 400)
            token = request.headers.get('Authorization').split()[1]
            user_id = get_user_id_from_token(token)
            send_request = FriendRequests.objects.filter(id=id, requested_id=user_id).first()
            if not send_request:
                raise CustomException("Request not found", 404)
            if action == '1':
                send_request.request_status = 1
                send_request.save()
                return Response({"message": "Request Accepted"}, status=200)
            elif action == '0':
                send_request.request_status = 2
                send_request.save()
                return Response({"message": "Request Rejected"}, status=200)
            return Response({"message": "action keyword value should be either 1 or 0"}, status=200)

        except CustomException as e:
            return Response(
                {"error_message": e.message, "error_code": e.error_code},
                status=e.error_code,
            )
        except Exception as e:
            return Response({"message": str(e)}, status=500)


class PendingRequestsAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            token = request.headers.get('Authorization').split()[1]
            user_id = get_user_id_from_token(token)
            send_request = FriendRequests.objects.filter(requested_id=user_id, request_status=0)
            if not send_request:
                raise CustomException("Requests not found", 404)

            serializer = FriendRequestsSerializer(send_request, many=True)
            return Response(serializer.data, status=200)


        except CustomException as e:
            return Response(
                {"error_message": e.message, "error_code": e.error_code},
                status=e.error_code,
            )
        except Exception as e:
            return Response({"message": str(e)}, status=500)


class FriendsAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            token = request.headers.get('Authorization').split()[1]
            user_id = get_user_id_from_token(token)
            friends = FriendRequests.objects.filter(
                request_status=1
            ).filter(
                (Q(sender_id=user_id) | Q(requested_id=user_id))
            )
            if not friends:
                raise CustomException("Friends not found", 404)

            serialized_data = []
            for friend in friends:
                if friend.sender.id == user_id:
                    friend_info = {
                        "friend_id": friend.requested.id,
                        "friend_name": friend.requested.name,
                        "friend_email": friend.requested.email,
                    }
                else:
                    friend_info = {
                        "friend_id": friend.sender.id,
                        "friend_name": friend.sender.name,
                        "friend_email": friend.sender.email,

                    }
                serialized_data.append(friend_info)
            return Response(serialized_data, status=200)

        except CustomException as e:
            return Response(
                {"error_message": e.message, "error_code": e.error_code},
                status=e.error_code,
            )
        except Exception as e:
            return Response({"message": str(e)}, status=500)


class UserSearchAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            search_keyword = request.query_params.get('search_term', '')
            if not search_keyword:
                raise CustomException("Search keyword is required", 400)

            # Exact match on email
            email_match = CustomUser.objects.filter(email__iexact=search_keyword)
            if email_match.exists():
                serializer = CustomSearchUserSerializer(email_match, many=True)
                return Response(serializer.data, status=200)

            # Partial match on name
            name_match = CustomUser.objects.filter(name__icontains=search_keyword)
            if not name_match.exists():
                raise CustomException("No users found matching the search criteria", 404)

            # Pagination
            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(name_match, request)
            serializer = CustomSearchUserSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except CustomException as e:
            return Response(
                {"error_message": e.message, "error_code": e.error_code},
                status=e.error_code,
            )
        except Exception as e:
            return Response({"message": str(e)}, status=500)
