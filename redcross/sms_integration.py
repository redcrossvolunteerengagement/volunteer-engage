import os
from twilio.rest import TwilioRestClient
import threading

TW_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TW_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TW_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

class Notifier(object) :
  def __init__(self, trc, returner_func) :
    self.trc = trc
    self.returner_func = returner_func

  def __del__(self) :
    self.returner_func(self.trc)

  def send(self, phone_number, message) :
    return self.trc.sms.messages.create(to=phone_number, from_=TW_PHONE_NUMBER, body=message)

class Notifiers(object) :
  client_set = list()
  client_lock = threading.Lock()

  @classmethod
  def get(cls) :
    with cls.client_lock :
      if cls.client_set :
        return cls.client_set.pop()
      else :
        return Notifier(TwilioRestClient(account=TW_ACCOUNT_SID, token=TW_AUTH_TOKEN), cls.give)

  @classmethod
  def give(cls, trc) :
    with cls.client_lock :
      cls.client_set.insert(0, trc)
