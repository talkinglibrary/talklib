import pytest
from unittest.mock import patch, MagicMock

from ...show import TLShow
from ..mock import env_vars

import xml.etree.ElementTree as ET


# this RSS feed chosen as template feed because it is reliably updated every day 
# (many times per day) and because the audio file is short/small!
url = 'https://feeds.npr.org/500005/podcast.xml'


@pytest.fixture
def template_rss():
    with patch.dict('os.environ', env_vars):
        test = TLShow()
    test.show = 'Delete Me'
    test.show_filename = 'delete_me'
    test.url = url
    # disable notifications for testing. Need separate tests for these!
    test.notifications = False
    test.syslog_enable = False

    return test

# ---------- Misc Methods ----------

def test_get_feed(template_rss: TLShow):
    '''check whether return object is an instance of ET.Element class'''
    assert (isinstance(template_rss.get_feed(), ET.Element))

def test_get_feed_fails_with_invalid_url(template_rss: TLShow):
    '''check an exception is raised when an invalid url is used'''
    template_rss.url = 'nourl'
    with pytest.raises(Exception):
        template_rss.run()

def test_check_feed_updated(template_rss: TLShow):
    assert template_rss.check_feed_updated()

def test_get_audio_url(template_rss: TLShow):
    assert type(template_rss.get_RSS_audio_url()) == str

def test_check_feed_loop(template_rss: TLShow):
    assert type(template_rss.check_feed_loop()) == bool

def test_remove_yesterday_files(template_rss: TLShow):
    '''if we pass an invalid file to delete, it should be handled gracefully without exceptions'''
    template_rss.remove(fileToDelete='not_a_file.wav')



# ---------- attribute checks ----------

# first, make sure there are no exceptions thrown for our correctly set up instance
def test_check_attributes_are_valid_1(template_rss: TLShow):
    template_rss.check_attributes_are_valid()

def test_gen(template_rss: TLShow):
    assert type(template_rss.create_output_filename()) == str

# now, start deliberatly triggering exceptions with invalid attributes.

def test_check_attributes_are_valid_1a(template_rss: TLShow):
    template_rss.show = 42
    with pytest.raises(Exception):
        template_rss.check_attributes_are_valid()

def test_check_attributes_are_valid_2(template_rss: TLShow):
    template_rss.show_filename = 42
    with pytest.raises(Exception):
        template_rss.check_attributes_are_valid()

def test_check_attributes_are_valid_3(template_rss: TLShow):
    template_rss.url = 42
    with pytest.raises(Exception):
        template_rss.check_attributes_are_valid()

def test_check_attributes_are_valid_6(template_rss: TLShow):
    template_rss.breakaway = True
    with pytest.raises(Exception):
        template_rss.check_attributes_are_valid()

def test_check_attributes_are_valid_7(template_rss: TLShow):
    template_rss.ff_level = True
    with pytest.raises(Exception):
        template_rss.check_attributes_are_valid()

def test_check_attributes_are_valid_8(template_rss: TLShow):
    template_rss.check_if_above = [1,2]
    with pytest.raises(Exception):
        template_rss.run()

def test_check_attributes_are_valid_9(template_rss: TLShow):
    template_rss.check_if_below = [1,2]
    with pytest.raises(Exception):
        template_rss.run()

def test_check_attributes_are_valid_10(template_rss: TLShow):
    template_rss.notifications = 5
    with pytest.raises(Exception):
        template_rss.run()

def test_check_attributes_are_valid_11(template_rss: TLShow):
    template_rss.twilio_enable = 4.5
    with pytest.raises(Exception):
        template_rss.run()
 
def test_check_attributes_are_valid_12(template_rss: TLShow):
    '''exception should be raised if both url & is_local are declared'''
    template_rss.is_local = True
    with pytest.raises(Exception):
        template_rss.run()

