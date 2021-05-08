from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.db.models import Q
from profileUser.models import Profile
from random import randint
from users.usecases.usescases import UserRecoverPassword


class UserRepository(object):

    def find_user(query):
        return User.objects.filter(Q(username__contains=query) | Q(first_name__contains=query))

    def create_user(data):
        user = User.objects.create_user(username=data["email"], email=data["email"], password=data["password"], first_name=data["first_name"], is_superuser=data["is_superuser"]).save()
        if data['phone'] is not None:
            profile = Profile()
            profile.user = user
            profile.phone = data['phone']
            profile.save()
        return user

    def reset_password(self, email):
        try:
            user = User.objects.get(email=email)
            new_password = self.random_password()
            user.set_password(new_password)
            user.save()
            self.send_mail_recover(user.first_name, email, new_password)
            return email
        except User.DoesNotExist:
            raise UserRecoverPassword.Exception("Email no existe")

    @staticmethod
    def random_password():
        range_start = 10 ** (8 - 1)
        range_end = (10 ** 8) - 1
        return randint(range_start, range_end)

    @staticmethod
    def send_mail_recover(user_name, email, new_password):
        mail = EmailMultiAlternatives(
            'Colosal mini market',
            ''
            ,
            to=[email]
        )
        mail.attach_alternative('<h3>Hola {}</h3> </br> <p>Espero tengas excelente dia.</p> </br> </br> <p>Tu nueva contraseña provisional es: <b>{}</b> </p> </br> </br> <p>http://minimarketcolosal.com</p>'.format(user_name, new_password), "text/html")
        mail.send()
