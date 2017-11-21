import sys

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

from .serializers import SMSSerializer


class SendSMS(APIView):
    def post(self, request):
        serializer = SMSSerializer(request.data)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        API_KEY = "NCSGLMHSQ2FTVZUA"
        API_SECERT = "2ZNM5ZPZR07QHSLHVIFAH3XZR1GAGM2F"

        receiver = request.data['receiver']
        message = request.data['message']

        ## 4 params(to, from, type, text) are mandatory. must be filled
        params = dict()
        params['type'] = 'sms'  # Message type ( sms, lms, mms, ata )
        params['to'] = receiver  # Recipients Number '01000000000,01000000001'
        params['from'] = '01029953874'  # Sender number
        params['text'] = message  # Message

        cool = Message(API_KEY, API_SECERT)
        try:
            response = cool.send(params)
            print("Success Count : %s" % response['success_count'])
            print("Error Count : %s" % response['error_count'])
            print("Group ID : %s" % response['group_id'])

            if "error_list" in response:
                print("Error List : %s" % response['error_list'])

        except CoolsmsException as e:
            print("Error Code : %s" % e.code)
            print("Error Message : %s" % e.msg)

        return Response(status=status.HTTP_200_OK)
