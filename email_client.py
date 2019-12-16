# coding=utf-8

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr


class EmailClient(object):
    def __init__(self, sender_info):
        self._sender_mail = sender_info.get("sender_email", "")  # 发件人邮箱
        self._sender_mail_auth_code = \
            sender_info.get("sender_email_auth_code", "")  # 发件人邮箱 smtp 授权码
        self._sender_name = sender_info.get("sender_email_name", "")  # 发件人显示名字
        self._sender_smtp_address = sender_info.get("sender_email_smtp_address", "")
        self._sender_smtp_port = sender_info.get("sender_email_smtp_port", "")

    def _msg_add_attach(self, msg, attachs):
        if len(attachs) == 0:
            return msg

        for singleAttach in attachs:
            filepath, filename = os.path.split(singleAttach)

            attach_msg = MIMEApplication(open(singleAttach, 'rb').read())
            attach_msg.add_header('Content-Disposition', 'attachment', filename=filename,
                                  encoding='utf-8')
            msg.attach(attach_msg)
        return msg

    def sendmail(self, mail_info, single_display=True):
        msg = MIMEMultipart()
        msg['From'] = formataddr([self._sender_name, self._sender_mail])
        msg['Subject'] = mail_info.get("subject", "")

        email_reveivers = mail_info.get("receivers", [])

        email_body = mail_info.get("body", "")
        email_body_type = mail_info.get("bodyType", "plain")

        body_msg = MIMEText(email_body, email_body_type)
        msg.attach(body_msg)

        email_attachments = mail_info.get("attachments", [])
        msg = self._msg_add_attach(msg, email_attachments)

        server = smtplib.SMTP(self._sender_smtp_address, self._sender_smtp_port)
        server.login(self._sender_mail, self._sender_mail_auth_code)

        if not single_display:
            msg['To'] = ",".join(email_reveivers)
            server.sendmail(self._sender_mail,
                            email_reveivers,
                            msg.as_string())
        else:
            for receiver in email_reveivers:
                del msg['To']
                msg['To'] = receiver
                server.sendmail(self._sender_mail, receiver, msg.as_string())

        server.quit()
