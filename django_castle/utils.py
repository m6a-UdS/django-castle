from django.contrib import messages


# Assuming user is instance of contrib.auth.UserModel
# implying user.id and user.get_username() both exist.
def castle_userid(user=None):
    castle_id = "<no-id>"
    if user:
        castle_id = (str(user.id) + '_' + user.get_username() if user.id else str(user))
    return castle_id


def logmessage(request, msg):
    messages.error(request, msg)
