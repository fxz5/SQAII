import json

from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse


class TwilioManager:
    def __init__(self, phone_number):
        with open("conf/credentials.json") as f:
            data = json.load(f)
            data = data['twilio']
            account = data['client_id']
            token = data['token']
            print data
        self.phone_number = phone_number
        self.client = Client(account, token)

    def make_call(self, number):
        call = self.client.calls.create(to=number, from_=self.phone_number,
                                        url="https://handler.twilio.com/twiml/EH8c0d49f80eab93bfac2ff3d821e46e6d")
        print call.sid

    @staticmethod
    def generate_voice_dialogue():
        r = VoiceResponse()
        r.say("You are my favorite pizza place, please don't hang up")
        print str(r)
