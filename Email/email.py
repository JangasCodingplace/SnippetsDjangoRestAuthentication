from django.conf import settings

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_message(message, receiver, subject='No Subject', sender=None):
    if not sender:
        sender = settings.ENV['SENDER_MAIL']
    if settings.ENV['DEBUG']:
        receiver = settings.ENV['TEST_RECEIVER_MAIL']

    message = Mail(
        from_email=sender,
        to_emails=receiver,
        subject=subject,
        html_content=message
    )

    try:
        sg = SendGridAPIClient(settings.ENV['SENDGRID_API_KEY'])
        response = sg.send(message)
        return response.status_code

    except Exception as e:
        print(e)
        return False
