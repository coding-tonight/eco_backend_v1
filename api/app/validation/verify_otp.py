from django.contrib.auth.models import User

from app.models import OTP

def verify_opt_validation(request):
    try:
        data = request.data
        otp = data.get('otp')
        error_list = []

        if not OTP.objects.filter(otp=otp).exists():
            error_list.append('Otp does not exits or time is exceeded please sending otp again.')
        
        # otp exits then get user instance
        email = OTP.objects.get(otp=otp)
        user = User.objects.get(email=email.email)
        return error_list, otp, user
    
    except Exception as exe:
        raise Exception(exe)


    