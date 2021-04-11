import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def Test():
    message = Mail(
        from_email='sirjanbaniya@gmail.com',
        to_emails='sirjanbaniya@gmail.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print("Email :", e)


def SendVerifyToken(pin, to_email):
    message = Mail(
        from_email='no-reply@hamrofutsal.com',
        to_emails=to_email,
        subject='Verification Pin',
        html_content="Your Verification Pin No is"+pin)
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print("Email :", e)


def SendBookingInformation(user_book_time,user_book_date, to_email):
    message = Mail(
        from_email='booking@hamrofutsal.com',
        to_emails=to_email,
        subject='Your Booking',
        html_content="Your Booking has been registered for "+ user_book_date + "at" + user_book_time)
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print("Email :", e)
