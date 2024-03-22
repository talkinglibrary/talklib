from email.message import EmailMessage
import logging
from logging.handlers import SysLogHandler
import smtplib

from twilio.rest import Client

from talklib.ev import EV

class Syslog:
    def __init__ (self):
        self.syslog_host = EV().syslog_host
        self.syslog_port = 514

    def get_level(self, level: str):
        if level.lower() == 'info':
            return logging.INFO
        if level.lower() == 'debug':
            return logging.DEBUG
        if level.lower() == 'warning':
            return logging.WARNING
        if level.lower() == 'error':
            return logging.ERROR
        if level.lower() == 'critical':
            return logging.CRITICAL

    def send_syslog_message(self, message: str, level: str = 'info'):
        '''
        Send message to Syslog server.
        Levels: info (default), debug, warning, error, critical.
        '''
        my_logger = logging.getLogger('MyLogger')
        my_logger.setLevel(self.get_level(level=level))
        handler = SysLogHandler(address=(self.syslog_host, self.syslog_port))
        my_logger.addHandler(handler)

        my_logger.info(message)
        my_logger.removeHandler(handler) # don't forget this after you send the message!

class Notify:
    def __init__ (self,
                  syslog_enable: bool = True,
                  twilio_enable: bool = True,
                  email_enable: bool = True,
                  ):
        
        self.syslog_enable = syslog_enable
        self.twilio_enable = twilio_enable
        self.email_enable = email_enable
        self.syslog = Syslog()
        self.EV = EV()

    def send_syslog(self, message: str, level: str) -> None:
        '''send message to syslog server'''
        if not self.syslog_enable:
            return
        self.syslog.send_syslog_message(message=message, level=level)
    
    def send_call(self, message: str) -> None:
        '''send voice call via twilio'''
        if self.twilio_enable:
            client = Client(self.EV.twilio_sid, self.EV.twilio_token)

            call = client.calls.create(
                                    twiml=f'<Response><Say>{message}</Say></Response>',
                                    to=self.EV.twilio_to,
                                    from_=self.EV.twilio_from
                                )
            call.sid

    def send_sms(self, message: str) -> None:
        '''send sms via twilio. '''
        if self.twilio_enable:
            client = Client(self.EV.twilio_sid, self.EV.twilio_token)
            SMS = client.messages.create(
                body=message,
                from_=self.EV.twilio_from,
                to=self.EV.twilio_to
            )
            SMS.sid

    def send_mail(self, message: str, subject: str) -> None:
        '''send email to TL gmail account via relay address'''
        if self.email_enable:
            format = EmailMessage()
            format.set_content(message)
            format['Subject'] = subject
            format['From'] = self.EV.fromEmail
            format['To'] = self.EV.toEmail

            mail = smtplib.SMTP(host=self.EV.mail_server)
            mail.send_message(format)
            mail.quit()