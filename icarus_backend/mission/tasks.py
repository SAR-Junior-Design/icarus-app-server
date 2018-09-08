from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from users.tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from icarus_backend.celery import app


@app.task
def new_mission_registered_email(username, email, user_id, domain):
    mail_subject = '[Icarus] New Mission Registered'
    message = render_to_string('new_mission_registered.html', {
        'user': username,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user_id)).decode(),
        'token': account_activation_token.make_token(username),
    })
    email = EmailMessage(
        mail_subject, message, to=[email]
    )
    email.send()