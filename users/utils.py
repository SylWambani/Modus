from django.core.mail import send_mail
from django.conf import settings

def send_invite_email(invite):
    link = f"http://127.0.0.1:8000/register?token={invite.token}"

    try:
        send_mail(
        subject="You're invited to the MODUS system",
        message=f"""
        Hi,

        You've been invited to join the MODUS system.

        Click the link below to complete your registration:
        {link}

        This link expires in 24 hours.
        """,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[invite.email],
        fail_silently=False,
        )
        print(f"✅ Email sent to {invite.email}")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")



    