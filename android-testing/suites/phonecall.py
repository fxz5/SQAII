from utils.utils import AppManager
import time
import json


class PhoneCall:
    def __init__(self, d, adb_only=False):
        self.device = d
        self.app = "Phone"
        print "Initializing Phonecall Component"

    def call_number_adb(self):
        self.test_conditions()
        time.sleep(1)
        self.device.get_device()(resourceId="com.google.android.dialer:id/fab") \
            .click()

        with open('data/phone.json') as json_file:
            data = json.load(json_file)
            phone_number = data['phone_number']
            print "Dialing: " + phone_number
            for i in range(len(phone_number)):
                self.device.get_device()(
                    text=phone_number[i],
                    resourceId="com.google.android.dialer:id"
                               "/dialpad_key_number") \
                    .click()
                time.sleep(1)
            self.device.get_device()(
                resourceId="com.google.android.dialer:id"
                           "/dialpad_voice_call_button") \
                .click()

    def test_conditions(self):
        AppManager.open_app(self.device, self.app)
