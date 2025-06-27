import smtplib
from email.mime.text import MIMEText

msg = MIMEText("Test email from Forex Analyzer")
msg["Subject"] = "Test"
msg["From"] = "palmcreditinfo@gmail.com"
msg["To"] = "maryorwahmi@gmail.com"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login("palmcreditinfo@gmail.com", "bwfr cxea okkh chwl")  # App password
server.send_message(msg)
server.quit()
