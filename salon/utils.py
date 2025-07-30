from django.contrib.sessions.models import Session

def get_or_create_session_key(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key
