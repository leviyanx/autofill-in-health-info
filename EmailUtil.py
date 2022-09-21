from smtplib import SMTP_SSL
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.header import Header
from util import load_json_data


def notify_manager(subject, context="Without body context"):
    """Notify manager with given info through email

    :param subject: email subject
    :param context: email body context
    :return: none
    """
    email_me(subject, context)


def email_me(subject, send_content):
    """Email me the given message

    :param subject: email subject
    :param send_content: email body context
    :return: none
    """

    # load manager email info from file
    manager_email_data = load_json_data("manager_email_info.json")
    print(manager_email_data)

    # sender information
    from_address = manager_email_data['from_address']  # sender email address
    from_address_pwd = manager_email_data['from_address_pwd'] # qq mail passcode
    # receiver information
    to_address = manager_email_data['to_address']  # receiver email address

    # email use qq mail
    host_server = 'smtp.qq.com'
    # ssl login
    smtp = SMTP_SSL(host_server)
    # set_debuglevel() for debug, 1 enable debug, 0 for disable
    # smtp.set_debuglevel(1)
    smtp.ehlo(host_server)
    smtp.login(from_address, from_address_pwd)

    # construct message
    msg = EmailMessage()
    msg = MIMEText(send_content, "plain", 'utf-8')
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = Header(subject, 'utf-8')
    to_addrs = [to_address]

    # send message
    smtp.sendmail(from_address, to_addrs, msg.as_string())
    smtp.quit()