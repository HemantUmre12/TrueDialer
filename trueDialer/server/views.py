from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Contact, SpamReport
from .serializers import RegisterUserSerializer, SpamReportSerializer


class RegisterView(APIView):
    def post(self, request):
        # ! Check if phone number is valid
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        errors = serializer.errors
        if "phone" in errors:
            return Response(
                {"error": "Phone number already exists"},
                status=status.HTTP_409_CONFLICT,
            )

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")
        user = authenticate(
            request=request, phone_number=phone_number, password=password
        )
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response(
            {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
        )


class MarkSpamView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # !! Check if user already marked the phone number as spam

        data = request.data
        serializer = SpamReportSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def sort_contacts_by_name(self, contacts, query):
        query = query.lower()

        # Custom sort key function
        def sort_key(item):
            name_lower = item["name"].lower()
            # Check if the name starts with the query
            if name_lower.startswith(query):
                return (0, name_lower)
            return (1, name_lower)

        sorted_contacts = sorted(contacts, key=sort_key)
        return sorted_contacts

    def get(self, request, search_query):
        is_query_a_number = search_query.isdigit()

        if is_query_a_number:
            contacts = Contact.objects.filter(phone_number=search_query)
            if contacts.filter(is_registered_user=True).exists():
                contacts = contacts.filter(is_registered_user=True)
        else:
            contacts = Contact.objects.filter(name__icontains=search_query)

        result_data = []
        for contact in contacts:
            spam_reports = SpamReport.get_spam_report_cnt(contact.phone_number)
            result_data.append(
                {
                    "name": contact.name,
                    "phone_number": contact.phone_number,
                    "spam_reports": spam_reports,
                }
            )

        if not is_query_a_number:
            result_data = self.sort_contacts_by_name(result_data, search_query)

        return Response(result_data, status=status.HTTP_200_OK)


class DetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        contact = get_object_or_404(Contact, pk=id)

        res = {
            "id": contact.id,
            "name": contact.name,
            "phone_number": contact.phone_number,
        }

        if not contact.is_registered_user:
            return Response(res, status=status.HTTP_200_OK)

        registered_user = contact.owner
        if registered_user.email is None:
            return Response(res, status=status.HTTP_200_OK)

        # Check if the current user is in the registered user's contact list
        is_user_in_personal_contacts = Contact.objects.filter(
            owner=registered_user, phone_number=request.user.phone_number
        ).exists()

        if is_user_in_personal_contacts:
            res["email"] = registered_user.email

        return Response(res, status=status.HTTP_200_OK)
