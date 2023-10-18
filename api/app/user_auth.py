import base64

def user_validation(request):
    try:
        # split the auth header to retirve the base64 encoded data
        encoded_data = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        # decode the data and split them into the list
        decoded_data = base64.b64decode(encoded_data).decode('utf-8').split(':')
        username = decoded_data[0]
        password = decoded_data[1]
        
        return username, password 
    
    except Exception as exe:
        raise Exception(exe)