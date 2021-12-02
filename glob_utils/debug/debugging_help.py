

def print_obj_type_dict(obj):
    type_obj= type(obj)
    dict_obj = obj.__dict__ if hasattr(obj,'__dict__') else None
    print(f'{obj=}\n{type_obj=}\n{dict_obj=}')