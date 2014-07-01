import unittest
import responses
import isc
from isc import requests

# Python 2/3 compat fix.
try:
    _ = unicode
except NameError:
    unicode = str

class TestISC(unittest.TestCase):

    @responses.activate
    def test_gets_dict_if_not_type(self):
        responses.add(responses.GET, 'https://isc.sans.edu/api/infocon?json',
                      body='{"status":"green"}', status=200,
                      match_querystring=True, content_type='text/json')
        self.assertEquals(type(isc._get('infocon')), dict)
        self.assertEquals(isc._get('infocon'), {u'status': u'green'})

    @responses.activate
    def test_gets_string_if_type(self):
        responses.add(responses.GET, 'https://isc.sans.edu/api/infocon?json',
                      body='{"status":"green"}', status=200,
                      match_querystring=True, content_type='text/json')
        self.assertEquals(type(isc._get('infocon', isc.JSON)), unicode)
        self.assertEquals(isc._get('infocon', isc.JSON), u'{"status":"green"}')

    @responses.activate
    def test_converts_ordered_dict_to_list(self):
        responses.add(responses.GET, 'https://isc.sans.edu/api/backscatter?json',
                      status=200, match_querystring=True, content_type='text/json',
                      body="""
                      {"0":{"sourceport":"6000","count":"563542","sources":"518","targets":"94654"},
                       "1":{"sourceport":"80","count":"201888","sources":"3294","targets":"8130"},
                       "2":{"sourceport":"53","count":"140780","sources":"3777","targets":"255"},
                       "3":{"sourceport":"4935","count":"101361","sources":"13726","targets":"56572"},
                       "4":{"sourceport":"12200","count":"79924","sources":"40","targets":"8040"},
                       "5":{"sourceport":"8080","count":"78873","sources":"73","targets":"78543"},
                       "6":{"sourceport":"68","count":"75543","sources":"104","targets":"8"},
                       "7":{"sourceport":"137","count":"59672","sources":"902","targets":"1918"},
                       "8":{"sourceport":"5066","count":"57052","sources":"35","targets":"57002"},
                       "9":{"sourceport":"5070","count":"54773","sources":"23","targets":"54745"},
                       "METAKEYINFO":"sourceport"}
                      """)
        self.assertEquals(type(isc._get('backscatter')), list)
        json = requests.get('https://isc.sans.edu/api/backscatter?json').json()
        for index, item in enumerate(isc._get('backscatter')):
            self.assertEquals(json['{index}'.format(index=index)], item)
        self.assertEquals(len(json), 11)
        self.assertEquals(len(isc._get('backscatter')), 10)
        self.assertNotIn('METAKEYINFO', isc._get('backscatter'))
