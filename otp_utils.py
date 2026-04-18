import smtplib
from email.message import EmailMessage
# Remove "from turtle import st" -> it causes crashes

def send_transaction_mail(to_email, subject, body_html):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = "vedavyaskodandapani@gmail.com" 

    msg.add_alternative(body_html, subtype='html') 

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("vedavyaskodandapani@gmail.com", "kxva dlgt ebts oxnx") 
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Mail Error: {e}") # Use print here as 'st' isn't defined in this file
        return False