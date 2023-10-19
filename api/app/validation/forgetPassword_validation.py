from django.contrib.auth.models import User

def forget_password_validation(request):
    try:
        data = request.data
        email = data.get('email')
        error_list = []

        if not User.objects.filter(email=email, is_active=True).exists():
            error_list.append('Email does not exits')

        #  if email exit then return user model instance
        user = User.objects.get(email=email)
        return error_list, email, user
    
    except Exception as exe:
        raise Exception(exe)
