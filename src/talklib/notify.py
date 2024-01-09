from email.message import EmailMessage
import logging
from logging.handlers import SysLogHandler
import smtplib

from twilio.rest import Client

from talklib.ev import EV

class Notify:
    def __init__ (self,
                  syslog_enable: bool = True,
                  twilio_enable: bool = True,
                  email_enable: bool = True
                  ):
        
        self.syslog_enable = syslog_enable
        self.twilio_enable = twilio_enable
        self.email_enable = email_enable

    def send_syslog(self, message: str) -> None:
        '''send message to syslog server'''
        if self.syslog_enable:
            port = int('514')
            my_logger = logging.getLogger('MyLogger')
            my_logger.setLevel(logging.DEBUG)
            handler = SysLogHandler(address=(EV().syslog_host, port))
            my_logger.addHandler(handler)

            my_logger.info(message)
            my_logger.removeHandler(handler) # don't forget this after you send the message!
    
    def send_call(self, message: str) -> None:
        '''send voice call via twilio'''
        if self.twilio_enable:
            client = Client(EV().twilio_sid, EV().twilio_token)

            call = client.calls.create(
                                    twiml=f'<Response><Say>{message}</Say></Response>',
                                    to=EV().twilio_to,
                                    from_=EV().twilio_from
                                )
            call.sid

    def send_sms(self, message: str) -> None:
        '''send sms via twilio. '''
        if self.twilio_enable:
            client = Client(EV().twilio_sid, EV().twilio_token)
            SMS = client.messages.create(
                body=message,
                from_=EV().twilio_from,
                to=EV().twilio_to
            )
            SMS.sid

    def send_mail(self, message: str, subject: str) -> None:
        '''send email to TL gmail account via relay address'''
        if self.email_enable:
            format = EmailMessage()
            format.set_content(message)
            format['Subject'] = subject
            format['From'] = EV().fromEmail
            format['To'] = EV().toEmail

            mail = smtplib.SMTP(host=EV().mail_server)
            mail.send_message(format)
            mail.quit()