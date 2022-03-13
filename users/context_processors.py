from users.models import CustomUser


def message_processor(request):
    notifications = CustomUser.objects.filter(is_active=False, is_teacher=False).count()
    
    return {'notifications' : notifications}