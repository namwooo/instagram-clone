from rest_framework import serializers


def phone_number(value):
    value = value.replace('-', '')
    if len(value) != 10 or len(value) != 11:
        raise serializers.ValidationError('length of phone number is not valid')
    if not value.startswith('0'):
        raise serializers.ValidationError('phone number must start with 0')


def sms_length(value):
    encoded_str = value.encode('cp949')
    if len(encoded_str) > 90:
        raise serializers.ValidationError(
            f'You are able to send 90 characters (Your request length: {len(encoded_str)})'
        )
