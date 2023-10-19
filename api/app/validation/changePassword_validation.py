import logging

from  django.contrib.auth.models import User


logger = logging.getLogger('django')

def change_password_validation(request):
    try:
        data = request.data
        # user_id = data.get('user_id')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        error_list = []

        if password is not confirm_password and password != confirm_password:
            error_list.append('Password does not match')

        if len(password) < 5:
            error_list.append('Password must be minimum 5 digits.')
        
        # if not user_id:
        #     logger.error('user id not pass from the client site.')
        #     error_list.append('Ops something went wrong please try sometime later.')
        
        return error_list, password
    
    except Exception as exe:
        raise Exception(exe)
