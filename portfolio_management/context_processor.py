from .models import Notification  # Example model for notifications



def notification_context(request):
    """
    Add notifications and unread count to the context for all templates.
    """
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
        notification_count = notifications.filter(is_read=False).count()
    else:
        notifications = []
        notification_count = 0

    return {
        'notifications': notifications,
        'notification_count': notification_count,
    }
