
class UserService:

    @staticmethod
    def user_info(user):
        userInfo = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
        return userInfo
