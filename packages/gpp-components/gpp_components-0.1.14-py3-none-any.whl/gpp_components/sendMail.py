import smtplib
import ssl
import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(config, content):
    try:
        user_name = config.get("mail_user_name").split("@")[0]
        user_email = config.get("mail_user_name")
        password = config.get("mail_user_pass")
        port = config.get("smtp_port")
        smtp_server = config.get("smtp_host_name")

        sender_email = content.get("sender")
        receiver_email = content.get("recipient")
        cc_email = content.get("cc")
        bcc_email = content.get("bcc")
        subject_email = content.get("subject")
        message_email = content.get("message")
        attachments = content.get("attachments")

        message = MIMEMultipart()
        message["Subject"] = subject_email if subject_email else ""
        message["From"] = sender_email if sender_email else ""
        message["To"] = ";".join(list(receiver_email)) if receiver_email else ""
        message["Cc"] = ";".join(list(cc_email)) if cc_email else ""
        message["Bcc"] = ";".join(list(bcc_email)) if bcc_email else ""

        to_list = list(set(receiver_email + cc_email + bcc_email))
        #

        msg = MIMEText(message_email if message_email else "", "html", "utf-8")
        message.attach(msg)

        #

        for i in attachments:
            path = i.get("path")
            hostname = os.path.join(r"\\", path.split("\\")[2])
            file_name = i.get("file_name")
            file_path = path + file_name
            file_rename = i.get("file_rename")

            new_file_path = os.path.join("D:\\mail_attachments\\", file_rename)
            os.system("net use %s /user:%s %s" % (hostname, user_name, password))
            os.system("copy /y %s %s" % (file_path, new_file_path))
            os.system("net use %s /del" % (hostname))

            open_file = open(new_file_path, "rb")
            attachPart = MIMEApplication(open_file.read())
            attachPart.add_header(
                "Content-Disposition", "attachment", filename=file_rename
            )
            message.attach(attachPart)
            open_file.close()

            os.system("del /Q %s " % (new_file_path))

        #

        context = ssl.create_default_context()

        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(user_email, password)
            server.sendmail(sender_email, to_list, message.as_string())
            pass

        return {"success": "true", "msg": "", "data": []}

    except Exception as e:
        return {"success": "false", "msg": str(e), "data": []}
