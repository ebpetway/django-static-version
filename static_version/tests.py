import unittest

from django.conf import settings
from static_version.templatetags.add_version import version
from static_version.context_processors import static_urls

class TestPackage(unittest.TestCase):

    def test_context_processor(self):
        feaux_request = {
            'testkey':"testvalue"
        }

        updated_request = static_urls(feaux_request)

        # Make sure the version shows up properly
        self.assertEqual(updated_request['static_version'], settings.STATIC_VERSION)
        # Make sure the rest of the request doesn't disappear
        self.assertEqual(feaux_request['testkey'], updated_request['testkey'])

    def test_templatetag_simple(self):
        test_url = "http://fake.com/"

        tagged_url = version(test_url, settings.STATIC_VERSION)

        # Make sure the url is just the old url plus the version query
        self.assertEqual(test_url + "?v={}".format(settings.STATIC_VERSION), tagged_url)

    def test_templatetag_add(self):
        test_url = "http://fake.com/?frontier=final"

        tagged_url = version(test_url, settings.STATIC_VERSION)

        # Make sure the new url has both query components
        self.assertIn("v={}".format(settings.STATIC_VERSION), tagged_url)
        self.assertIn("frontier=final", tagged_url)
