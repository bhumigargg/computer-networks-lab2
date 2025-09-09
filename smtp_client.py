#!/usr/bin/env python3
import argparse
import logging
import smtplib
from email.message import EmailMessage

logging.basicConfig(
    filename='smtp.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def send_email(server: str, port: int, sender: str, recipient: str, subject: str, body: str,
               username: str = None, password: str = None, use_tls: bool = False, timeout: int = 15):
    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.set_content(body)

    logging.info(f"Connecting to SMTP server {server}:{port} (TLS={use_tls}) ...")
    with smtplib.SMTP(server, port, timeout=timeout) as smtp:
        smtp.set_debuglevel(1)  # prints SMTP conversation to stdout
        smtp.ehlo()
        if use_tls:
            smtp.starttls()
            smtp.ehlo()
        if username and password:
            logging.info("Logging in ...")
            smtp.login(username, password)
        logging.info("Sending message ...")
        smtp.send_message(msg)
        logging.info("Email sent successfully.")

def main():
    parser = argparse.ArgumentParser(description="SMTP client to send a test email with logging")
    parser.add_argument('--server', default='localhost', help='SMTP server hostname')
    parser.add_argument('--port', type=int, default=1025, help='SMTP server port (1025 for local debug server)')
    parser.add_argument('--sender', default='you@example.com', help='Sender email address')
    parser.add_argument('--recipient', default='friend@example.com', help='Recipient email address')
    parser.add_argument('--subject', default='CN Lab Test', help='Email subject')
    parser.add_argument('--body', default='Hello from SMTP client!', help='Email body text')
    parser.add_argument('--username', help='SMTP username (if needed)')
    parser.add_argument('--password', help='SMTP password (if needed)')
    parser.add_argument('--use-tls', action='store_true', help='Use STARTTLS (e.g., on port 587)')
    parser.add_argument('--timeout', type=int, default=15, help='Timeout in seconds')
    args = parser.parse_args()

    try:
        send_email(
            server=args.server,
            port=args.port,
            sender=args.sender,
            recipient=args.recipient,
            subject=args.subject,
            body=args.body,
            username=args.username,
            password=args.password,
            use_tls=args.use_tls,
            timeout=args.timeout
        )
    except Exception as e:
        logging.exception(f"SMTP send failed: {e}")

if __name__ == '__main__':
    main()
