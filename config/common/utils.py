

from rest_framework.response import Response
from rest_framework import status
import uuid




def makeResponse(data):


    # if data.get('code') == 200:
        return Response(data=data, status=status.HTTP_200_OK)
    # else:
    #     return Response(data=data, status=status.HTTP_403_FORBIDDEN)




def isValidUuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False




def getSafeFromJson(json, key):
    try:
        return json[key]
    except KeyError:
        return None




def getUnAuthError():
    return {
        'code': 403,
        'msg': 'Access denied!'
    }


def getErrorMessage(msg):
    return {
        'code': 403,
        'msg': msg
    }


def getSussessMessage(msg):
    return {
        'code': 200,
        'msg': msg
    }    
