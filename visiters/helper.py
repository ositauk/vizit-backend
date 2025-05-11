from .models import print_tag

def task_count(request):
    return {
        'printtag_count': print_tag.objects.filter(status=1).count()
    }