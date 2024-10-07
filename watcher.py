import os
import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import subprocess

load_dotenv()

# Settings
VM_IP = os.getenv("MACHINE")
GRADIO_UI_URL = "http://paffenroth-23.dyn.wpi.edu:8005/"
CHECK_INTERVAL = 60   # 60 seconds
RECOVERY_SCRIPT_PATH = 'recovery-deployment.sh'


# Email settings (if EMAIL_ALERT is True)
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email_alert(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, text)
        print("Email alert sent successfully!")
    except Exception as e:
        print(f"Failed to send email alert: {e}")


def check_vm_status():
    response = os.system(f"ping -c 1 {VM_IP}")  # send one ICMP echo request
    return response == 0  # successful ping


def check_ui_status():
    try:
        response = requests.get(GRADIO_UI_URL)
        if response.status_code == 200:
            return True
        else:
            print(f"UI returned status code {response.status_code}")
            return False
    except requests.ConnectionError:
        print(f"{time.ctime()} ---- Failed to connect to UI.")
        return False


def monitor_vm(EMAIL_ALERT = False):
    while True:
        ui_status = check_ui_status()
        # vm_status = check_vm_status()
        if ui_status:  # and vm_status:
            print(f"{time.ctime()} ---- Meowthematical chatbot is up and running")
        else:
            if not ui_status:
                print(f"{time.ctime()} ---- PRODUCT is DOWN!!!")
                if check_vm_status():  # check if VM is up and running
                    print(f"{time.ctime()} ---- VM {VM_IP} is up and running, starting recovery process...")
                    try:
                        result = subprocess.run(['bash', RECOVERY_SCRIPT_PATH],
                                                check=True,
                                                capture_output=True,
                                                text=True)
                        # Output from the script
                        # print("Output of the script:")
                        # print(result.stdout)  # Standard output of the script
                        # print("Errors (if any):")
                        # print(result.stderr)  # Standard error output of the script
                    except subprocess.CalledProcessError as e:
                        print(f"An error occurred: {e}")
                        print(f"Return code: {e.returncode}")
                        print(f"Output: {e.output}")
                        print(f"Error: {e.stderr}")

                    if EMAIL_ALERT:
                        send_email_alert(
                            subject="MEOWTHMATICAL Down Alert",
                            body=f"MEOWTHEMATICAL with IP {VM_IP} is down as of {time.ctime()}"
                        )
                else:  # both product and VM is gone
                    if EMAIL_ALERT:
                        send_email_alert(
                            subject="VM Down Alert",
                            body=f"Vitural Machine at IP {VM_IP} is down as of {time.ctime()}"
                        )
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitor_vm(EMAIL_ALERT=False)
