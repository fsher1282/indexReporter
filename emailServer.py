import indexCollector as Indexes
import smtplib
import ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Credentials for email service
smtp_server = "smtp.gmail.com"
sender_email = "Sender email"
receiver_email = "Receiver email"
password = 'password'

# Components of email message
message = MIMEMultipart("alternative")
message["Subject"] = "Weekly Index Report"
message["From"] = sender_email
message["To"] = receiver_email

# Collect data
try:
    my_results = Indexes.collect_data()

except Exception as e:
    my_results = "Something went wrong... \n " + str(e)
    print(my_results)
try:
    intro = """<html>
               <head>
               <p>Here is your weekly report for the market Indexes...</p>
               </head>
    """

    conclusion = """
        <body>
            <p style='color:red;'>Have a good day </p>
        </body>
    </html>"""

    # Combine all parts of message
    message_content = intro + my_results + conclusion
    data = MIMEText(message_content, "html")

    # Attach message to email
    message.attach(data)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
    server.ehlo()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    # Ensure email service is shutdown
    server.quit()
except Exception as e:
    # Print Error
    print(e)
