

# Assuming user is instance of contrib.auth.UserModel
# implying user.id and user.get_username() both exist.
def castle_userid(user=None):
    castle_id = "<no-id>"
    if user:
        castle_id = (str(user.id) if user.id else "00") + '_' + user.get_username()
    return castle_id
