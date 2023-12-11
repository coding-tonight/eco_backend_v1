from category.models import Category 
from app import globalParameters


def product_validation(request):
    data = request.data
    error_list = []

    product_name = data.get('product_name')
    product_code = data.get('product_code')
    description = data.get('desciption')
    category_ref_id = data.get('category')
    is_featured = data.get('is_featured')
    is_recommeded = data.get('is_recommeded')
    rating = data.get('rating')
    thumbnail = data.get('thumbnail')
    discount = data.get('discount')
    size = data.get('size')
    colors = data.getlist('colors')
    price =  data.getlist('price')   
    stock = data.get('stock')
    image = data.getlist('price')
    


    # product_validation = data.get('')

    if product_code is None:
        error_list.append(f"Product Code:{globalParameters.NULL_VALUE}")
    
    if product_name is None:
        error_list.append(f"Product Name: {globalParameters.NULL_VALUE}")
    
    if category_ref_id is None or not Category.objects.get(reference_id=category_ref_id):
        error_list.append(f"Category: {globalParameters.NULL_VALUE}")
    

    return error_list, product_name, product_code, description , is_featured

