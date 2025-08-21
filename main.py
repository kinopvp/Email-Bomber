import smtplib
import time
import os
from email.mime.text import MIMEText
from datetime import datetime

# Load email
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

if not EMAIL_ADDRESS or not EMAIL_PASSWORD or not TO_EMAIL:
    print("[!] Please set EMAIL_ADDRESS, EMAIL_PASSWORD, and TO_EMAIL environment variables.")
    exit(1)

# config
MAX_EMAILS = 10
INTERVAL_SECONDS = 1  
subjects = [
    "AutoMailer: Update",
    "Python Bot Says Hi",
    "This was sent at {time}",
]

def send_email(count):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = subjects[count % len(subjects)].format(time=now)
    body = f"This is automatic email #{count + 1} sent at {now}."

    msg = MIMEText(body, "plain")  # Change "plain" -> "html" for HTML emails
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"[+] Email #{count + 1} sent at {now}")

        with open("email_log.txt", "a") as log:
            log.write(f"[{now}] Email #{count + 1} sent to {TO_EMAIL}\n")

    except Exception as e:
        print(f"[!] Failed to send email #{count + 1}: {e}")

def main():
    email_count = 0
    try:
        while email_count < MAX_EMAILS:
            send_email(email_count)
            email_count += 1
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\n[!] Stopped by user.")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")

if __name__ == "__main__":
    main()
