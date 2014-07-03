import datetime
import unittest
import responses
import requests
import isc

# Python 2/3 compat fix.
try:
    _ = unicode
except NameError:
    unicode = str


class TestInternals(unittest.TestCase):

    @responses.activate
    def test_gets_dict_if_not_type(self):
        responses.add(responses.GET, 'https://isc.sans.edu/api/infocon?json',
                      body='{"status":"green"}', status=200,
                      match_querystring=True, content_type='text/json')
        self.assertEquals(type(isc._get('infocon')), dict)
        self.assertEquals(isc._get('infocon'), {'status': 'green'})

    @responses.activate
    def test_gets_string_if_type(self):
        responses.add(responses.GET, 'https://isc.sans.edu/api/infocon?json',
                      body='{"status":"green"}', status=200,
                      match_querystring=True, content_type='text/json')
        self.assertEquals(type(isc._get('infocon', isc.JSON)), unicode)
        self.assertEquals(isc._get('infocon', isc.JSON), '{"status":"green"}')

    @responses.activate
    def test_get_converts_ordered_dict_to_list(self):
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
        self.assertFalse('METAKEYINFO' in isc._get('backscatter'))

    def test_strip_and_reformat_converts_ordered_dict_to_list(self):
        data = {
            "0": {"sourceport":"6000","count":"563542","sources":"518","targets":"94654"},
            "1": {"sourceport":"80","count":"201888","sources":"3294","targets":"8130"},
            "2": {"sourceport":"53","count":"140780","sources":"3777","targets":"255"},
            "3": {"sourceport":"4935","count":"101361","sources":"13726","targets":"56572"},
            "4": {"sourceport":"12200","count":"79924","sources":"40","targets":"8040"},
            "5": {"sourceport":"8080","count":"78873","sources":"73","targets":"78543"},
            "6": {"sourceport":"68","count":"75543","sources":"104","targets":"8"},
            "7": {"sourceport":"137","count":"59672","sources":"902","targets":"1918"},
            "8": {"sourceport":"5066","count":"57052","sources":"35","targets":"57002"},
            "9": {"sourceport":"5070","count":"54773","sources":"23","targets":"54745"},
            "METAKEYINFO": "sourceport"
        }
        self.assertEquals(type(isc._strip_and_reformat(data)), list)
        for index, item in enumerate(isc._strip_and_reformat(data)):
            self.assertEquals(data['{index}'.format(index=index)], item)
        self.assertEquals(len(data), 11)
        self.assertEquals(len(isc._strip_and_reformat(data)), 10)
        self.assertFalse('METAKEYINFO' in isc._strip_and_reformat(data))


class TestPublicMethods(unittest.TestCase):

    @responses.activate
    def test_backscatter(self):
        responses.add(responses.GET, 'https://isc.sans.edu/api/backscatter?json',
                      body='{"METAKEYINFO": "", "0": "test"}', status=200,
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET,
                      'https://isc.sans.edu/api/backscatter/2011-12-01?json',
                      body='{"METAKEYINFO": "", "0": "2011-12-01"}', status=200, match_querystring=True,
                      content_type='text/json')
        responses.add(responses.GET,
                      'https://isc.sans.edu/api/backscatter/2011-12-01/10?json',
                      body='{"METAKEYINFO": "", "0": "10"}', status=200, match_querystring=True,
                      content_type='text/json')
        self.assertEquals(isc.backscatter(), ["test"])
        self.assertEquals(isc.backscatter("2011-12-01"), ["2011-12-01"])
        self.assertEquals(isc.backscatter(datetime.date(2011, 12, 1)), ["2011-12-01"])
        self.assertEquals(isc.backscatter("2011-12-01", 10), ["10"])
        self.assertEquals(isc.backscatter("2011-12-01", "10"), ["10"])
        self.assertEquals(isc.backscatter("2011-12-01", "10", isc.JSON),
                          '{"METAKEYINFO": "", "0": "10"}')

    @responses.activate
    def test_handler(self):
        responses.add(responses.GET, 'https://isc.sans.edu/api/handler?json',
                      body='{"name": "test"}', status=200,
                      match_querystring=True, content_type='text/json')
        self.assertEquals(isc.handler(), {'name': 'test'})
        self.assertEquals(isc.handler()['name'], 'test')
        self.assertEquals(isc.handler(isc.JSON), '{"name": "test"}')

    @responses.activate
    def test_infocon(self):
        responses.add(responses.GET, 'https://isc.sans.edu/api/infocon?json',
                      body='{"status": "test"}', status=200,
                      match_querystring=True, content_type='text/json')
        self.assertEquals(isc.infocon(), {'status': 'test'})
        self.assertEquals(isc.infocon()['status'], 'test')
        self.assertEquals(isc.infocon(isc.JSON), '{"status": "test"}')

    @responses.activate
    def test_ip(self):
        responses.add(responses.GET, 'https://isc.sans.edu/api/ip/4.4.4.4?json',
                      body='{"ip":{"test":"unknown"}}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET, 'https://isc.sans.edu/api/ip/badip?json',
                      body='{"error":"bad IP address"}', status=200,
                      match_querystring=True, content_type='text/json')
        self.assertEquals(isc.ip('4.4.4.4'), {'ip': {'test': 'unknown'}})
        self.assertEquals(isc.ip('4.4.4.4', isc.JSON), '{"ip":{"test":"unknown"}}')
        self.assertRaises(isc.Error, isc.ip, 'badip')

    @responses.activate
    def test_port(self):
        responses.add(responses.GET, 'https://isc.sans.edu/api/port/80?json',
                      body='{"port":80}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET, 'https://isc.sans.edu/api/port/badport?json',
                      body='{"error":"bad port number"}', status=200,
                      match_querystring=True, content_type='text/json')
        self.assertEquals(isc.port('80'), {'port': 80})
        self.assertEquals(isc.port(80), {'port': 80})
        self.assertEquals(isc.port('80', isc.JSON), '{"port":80}')
        self.assertRaises(isc.Error, isc.port, 'badport')
