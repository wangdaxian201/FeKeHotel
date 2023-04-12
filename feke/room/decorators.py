import os
import json
import time
import base64
import logging
import traceback
import functools
from io import BytesIO

from django.urls import path
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from utils.error import APIError
from urls import urlpatterns


logger = logging.getLogger(__name__)


def api(func):

    @csrf_exempt
    @functools.wraps(func)
    def view(request):
        start = time.time()

        try:
            params = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            error_log(request.path, request.body, e)
            return error(APIError(APIError.REQUEST_BODY_ERROR))
        try:
            result = func(**params)
        except APIError as e:
            return error(e)
        except TypeError as e:
            if 'required positional argument' in str(e):
                return error(APIError(APIError.PARAM_MISSING, str(e).split(':')[1]))
            elif 'unexpected keyword' in str(e):
                return error(APIError(APIError.UNEXPECT_PARAM, str(e).split('argument')[1]))
            else:
                return error(APIError(APIError.SERVER_ERROR))
        except FileNotFoundError as e:
            return error(APIError(APIError.FILE_MISSING, e.filename))
        except APIError as e:
                e = APIError(APIError.RESULTS_LENGTH_NOT_EQUAL)
                return error(e)
            e = APIError(APIError.SERVER_ERROR)
            return error(e)
        except Exception as e:
            error_log(request.path, params, e)
            e = APIError((50001, f'{e}'))
            # e = APIError(APIError.SERVER_ERROR)
            return error(e)

        if settings.DEBUG:
            print('api use time: ', time.time() - start)
        if isinstance(result, dict):
            return success(result)
        else:
            return result

    urlpatterns.append(path('api/%s/' % view.__name__, view))

    return view

def error(error):
    return JsonResponse({'success': False, 'result':{'code': error.code, 'msg': error.msg}})


def success(result):
    result['code'] = 50000
    return JsonResponse({'success': True, 'result': result if result else ''})
