from datetime import datetime

def get_file_path(image_obj):
    currentDate = datetime.now()
    timestamp = currentDate.strftime("%Y%m%d%H%M%S%f")
    fileExt = image_obj[image_obj.index('.'):]
    newFileName = f'{timestamp}{fileExt}'
    path = f'images_mngt/{image_obj.id}/{newFileName}'
    return path
