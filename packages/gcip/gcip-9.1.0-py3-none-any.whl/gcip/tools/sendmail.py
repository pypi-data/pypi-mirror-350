# send_mail.py
import argparse
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""
A simple script to send an email over an SMTP server.

See documentation of 'gcip.addons.notification.mail.SendMail' for usage.
"""


def send_email(
    *,
    smtp_server_var: str,
    smtp_port_var: str,
    smtp_user_var: str,
    smtp_password_var: str,
    from_email_var: str,
    to_emails_var: str,
    subject_var: str,
    email_body_var: str,
    email_body_path_var: str,
) -> None:
    # email configuration
    smtp_server = os.environ[smtp_server_var or "SMTP_SERVER"]
    smtp_port = int(os.getenv((smtp_port_var or "SMTP_PORT"), 587))
    smtp_user = os.environ[smtp_user_var or "SMTP_USER"]
    smtp_password = os.environ[smtp_password_var or "SMTP_PASSWORD"]
    from_email = os.getenv((from_email_var or "FROM_EMAIL"), smtp_user)
    to_emails = os.environ[to_emails_var or "TO_EMAILS"]
    subject = os.environ[subject_var or "SUBJECT"]
    email_body = os.getenv((email_body_var or "EMAIL_BODY"))
    email_body_path = os.getenv((email_body_path_var or "EMAIL_BODY_PATH"))

    if email_body and email_body_path:
        print(
            f"""
            Warning: Both {(email_body_var or 'EMAIL_BODY')} and {(email_body_path_var or 'EMAIL_BODY_PATH')} are set.
            Using {(email_body_var or 'EMAIL_BODY')}.
            """
        )

    if email_body:
        body = email_body
    elif email_body_path:
        try:
            with open(email_body_path, "r") as file:
                body = file.read()
        except Exception as e:
            print(f"Failed to read email body from file: {e}")
            sys.exit(1)
    else:
        raise ValueError(
            f"Error: Either {(email_body_var or 'EMAIL_BODY')} or {(email_body_path_var or 'EMAIL_BODY_PATH')} must be set."
        )

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_emails
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Send the emails
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        for to_email in to_emails.split(","):
            server.sendmail(from_email, to_email.strip(), text)
            print(f"Email to {to_email.strip()} sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Send an email using an external SMTP server."
    )
    parser.add_argument(
        "--smtp_server_var",
        required=False,
        help="Env for SMTP server address (default: SMTP_SERVER)",
    )
    parser.add_argument(
        "--smtp_port_var",
        required=False,
        help="Env for SMTP server port (default: SMTP_PORT)",
    )
    parser.add_argument(
        "--smtp_user_var",
        required=False,
        help="Env for SMTP server user (default: SMTP_USER)",
    )
    parser.add_argument(
        "--smtp_password_var",
        required=False,
        help="Env for SMTP server password (default: SMTP_PASSWORD)",
    )
    parser.add_argument(
        "--from_email_var",
        required=False,
        help="Env for From email address (default: FROM_EMAIL)",
    )
    parser.add_argument(
        "--to_emails_var",
        required=False,
        help="Env for To email addresses (comma separated) (default: TO_EMAILS)",
    )
    parser.add_argument(
        "--subject_var", required=False, help="Env for Email subject (default: SUBJECT)"
    )
    parser.add_argument(
        "--email_body_var",
        required=False,
        help="Env for Email body (default: EMAIL_BODY)",
    )
    parser.add_argument(
        "--email_body_path_var",
        required=False,
        help="Env for Email body file path (default: EMAIL_BODY_PATH)",
    )

    args = parser.parse_args()

    send_email(
        smtp_server_var=args.smtp_server_var,
        smtp_port_var=args.smtp_port_var,
        smtp_user_var=args.smtp_user_var,
        smtp_password_var=args.smtp_password_var,
        from_email_var=args.from_email_var,
        to_emails_var=args.to_emails_var,
        subject_var=args.subject_var,
        email_body_var=args.email_body_var,
        email_body_path_var=args.email_body_path_var,
    )
