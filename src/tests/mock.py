import os
import shutil


'''
We need to test 'local' files - meaning files we already have downloaded. But we don't want
to have to put an audio file into Git. So we're using this static URL to download first,
to mock a local file. Downloading the file itself it just setting up the test.

This static link was chosen because it's reliably available and the file is small/short.
'''
permalink = 'https://pnsne.ws/3mVuTax'

env_vars = {
        'OnAirPC': 'nothing',
        'ProductionPC': 'mocked_value2',
        'syslog_server': 'mocked_value2',
        'fromEmail': 'mocked_value2',
        'toEmail': 'mocked_value2',
        'mail_server_external': 'mocked_value2',
        'twilio_sid': 'mocked_value2',
        'twilio_token': 'mocked_value2',
        'twilio_from': 'mocked_value2',
        'twilio_to': 'mocked_value2',
    }

def mock_destinations():
    destinations = ['dest1', 'dest2', 'dest3']
    for destination in destinations:
        if not os.path.exists(destination):
            os.mkdir(destination)
    return destinations

def remove_destinations():
    for destination in mock_destinations():
        shutil.rmtree(destination)