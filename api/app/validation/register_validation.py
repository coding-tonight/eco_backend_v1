def register_validation(request):
    try:
        data = request.data
        username = data.get('username')
        first_name = data.get('first_name') # nullable value
        last_name = data.get('last_name')  # nullable value
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        error_list = []
        

        if password is confirm_password:
            error_list.append('Password does not match retry.')
        
        if username is None or email is None:
            error_list.append('Field can not be null')
        
        if len(password) > 5:
            error_list.append('password must be minimum 5 charaters')

        
        return username, email, password, first_name, last_name, error_list
    
    except Exception as exe:
        raise Exception(exe)
            