import datetime
import unittest
import responses
import requests
import dshield

# Python 2/3 compat fix.
try:
    _ = unicode
except NameError:
    unicode = str


class TestInternals(unittest.TestCase):

    @responses.activate
    def test_gets_dict_if_not_type(self):
        responses.add(responses.GET, 'https://dshield.org/api/infocon?json',
                      body='{"status":"green"}', status=200,
                      match_querystring=True, content_type='text/json')
        self.assertEquals(type(dshield._get('infocon')), dict)
        self.assertEquals(dshield._get('infocon'), {'status': 'green'})

    @responses.activate
    def test_gets_string_if_type(self):
        responses.add(responses.GET, 'https://dshield.org/api/infocon?json',
                      body='{"status":"green"}', status=200,
                      match_querystring=True, content_type='text/json')
        self.assertEquals(type(dshield._get('infocon', dshield.JSON)), unicode)
        self.assertEquals(dshield._get('infocon', dshield.JSON), '{"status":"green"}')

    @responses.activate
    def test_get_converts_ordered_dict_to_list(self):
        responses.add(responses.GET, 'https://dshield.org/api/backscatter?json',
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
        self.assertEquals(type(dshield._get('backscatter')), list)
        json = requests.get('https://dshield.org/api/backscatter?json').json()
        for index, item in enumerate(dshield._get('backscatter')):
            self.assertEquals(json['{index}'.format(index=index)], item)
        self.assertEquals(len(json), 11)
        self.assertEquals(len(dshield._get('backscatter')), 10)
        self.assertFalse('METAKEYINFO' in dshield._get('backscatter'))

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
        self.assertEquals(type(dshield._strip_and_reformat(data)), list)
        for index, item in enumerate(dshield._strip_and_reformat(data)):
            self.assertEquals(data['{index}'.format(index=index)], item)
        self.assertEquals(len(data), 11)
        self.assertEquals(len(dshield._strip_and_reformat(data)), 10)
        self.assertFalse('METAKEYINFO' in dshield._strip_and_reformat(data))


class TestPublicMethods(unittest.TestCase):

    @responses.activate
    def test_backscatter(self):
        responses.add(responses.GET, 'https://dshield.org/api/backscatter?json',
                      body='{"METAKEYINFO": "", "0": "test"}', status=200,
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET,
                      'https://dshield.org/api/backscatter/2011-12-01?json',
                      body='{"METAKEYINFO": "", "0": "2011-12-01"}', status=200, match_querystring=True,
                      content_type='text/json')
        responses.add(responses.GET,
                      'https://dshield.org/api/backscatter/2011-12-01/10?json',
                      body='{"METAKEYINFO": "", "0": "10"}', status=200, match_querystring=True,
                      content_type='text/json')
        self.assertEquals(dshield.backscatter(), ["test"])
        self.assertEquals(dshield.backscatter("2011-12-01"), ["2011-12-01"])
        self.assertEquals(dshield.backscatter(datetime.date(2011, 12, 1)), ["2011-12-01"])
        self.assertEquals(dshield.backscatter("2011-12-01", 10), ["10"])
        self.assertEquals(dshield.backscatter("2011-12-01", "10"), ["10"])
        self.assertEquals(dshield.backscatter("2011-12-01", "10", dshield.JSON),
                          '{"METAKEYINFO": "", "0": "10"}')

    @responses.activate
    def test_handler(self):
        responses.add(responses.GET, 'https://dshield.org/api/handler?json',
                      body='{"name": "test"}', status=200,
                      match_querystring=True, content_type='text/json')
        self.assertEquals(dshield.handler(), {'name': 'test'})
        self.assertEquals(dshield.handler()['name'], 'test')
        self.assertEquals(dshield.handler(dshield.JSON), '{"name": "test"}')

    @responses.activate
    def test_infocon(self):
        responses.add(responses.GET, 'https://dshield.org/api/infocon?json',
                      body='{"status": "test"}', status=200,
                      match_querystring=True, content_type='text/json')
        self.assertEquals(dshield.infocon(), {'status': 'test'})
        self.assertEquals(dshield.infocon()['status'], 'test')
        self.assertEquals(dshield.infocon(dshield.JSON), '{"status": "test"}')

    @responses.activate
    def test_ip(self):
        responses.add(responses.GET, 'https://dshield.org/api/ip/4.4.4.4?json',
                      body='{"ip":{"test":"unknown"}}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET, 'https://dshield.org/api/ip/badip?json',
                      body='{"error":"bad IP address"}', status=200,
                      match_querystring=True, content_type='text/json')
        self.assertEquals(dshield.ip('4.4.4.4'), {'ip': {'test': 'unknown'}})
        self.assertEquals(dshield.ip('4.4.4.4', dshield.JSON), '{"ip":{"test":"unknown"}}')
        self.assertRaises(dshield.Error, dshield.ip, 'badip')

    @responses.activate
    def test_port(self):
        responses.add(responses.GET, 'https://dshield.org/api/port/80?json',
                      body='{"port":80}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET, 'https://dshield.org/api/port/badport?json',
                      body='{"error":"bad port number"}', status=200,
                      match_querystring=True, content_type='text/json')
        self.assertEquals(dshield.port('80'), {'port': 80})
        self.assertEquals(dshield.port(80), {'port': 80})
        self.assertEquals(dshield.port('80', dshield.JSON), '{"port":80}')
        self.assertRaises(dshield.Error, dshield.port, 'badport')

    @responses.activate
    def test_portdate(self):
        responses.add(responses.GET, 'https://dshield.org/api/portdate/80/2011-07-03?json',
                      body='{"portdate":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET, 'https://dshield.org/api/portdate/80?json',
                      body='{"portdate":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET, 'https://dshield.org/api/portdate/badport?json',
                      body='{"error":"bad port number"}', status=200,
                      match_querystring=True, content_type='text/json')
        self.assertEquals(dshield.portdate('80'), {'portdate': 'test'})
        self.assertEquals(dshield.portdate(80), {'portdate': 'test'})
        self.assertEquals(dshield.portdate('80', datetime.date(2011, 7, 3)), {'portdate': 'test'})
        self.assertEquals(dshield.portdate('80', '2011-07-03'), {'portdate': 'test'})
        self.assertEquals(dshield.portdate('80', return_format=dshield.JSON), '{"portdate":"test"}')
        self.assertRaises(dshield.Error, dshield.portdate, 'badport')

    @responses.activate
    def test_topports(self):
        responses.add(responses.GET, 'https://dshield.org/api/topports/records/10/2011-07-23?json',
                      body='{"topports":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET, 'https://dshield.org/api/topports/records/10?json',
                      body='{"topports":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET, 'https://dshield.org/api/topports/records?json',
                      body='{"topports":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET, 'https://dshield.org/api/topports?json',
                      body='{"topports":"test"}',
                      match_querystring=True, content_type='text/json')
        data = {'topports': 'test'}
        self.assertEquals(dshield.topports(), data)
        self.assertEquals(dshield.topports('records'), data)
        self.assertEquals(dshield.topports('records', 10), data)
        self.assertEquals(dshield.topports('records', '10', datetime.date(2011, 7, 23)), data)
        self.assertEquals(dshield.topports('records', 10, '2011-07-23'), data)
        self.assertEquals(dshield.topports('records', return_format=dshield.JSON), '{"topports":"test"}')

    @responses.activate
    def test_topips(self):
        responses.add(responses.GET, 'https://dshield.org/api/topips/records/10/2011-07-23?json',
                      body='{"topips":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET, 'https://dshield.org/api/topips/records/10?json',
                      body='{"topips":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET, 'https://dshield.org/api/topips/records?json',
                      body='{"topips":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET, 'https://dshield.org/api/topips?json',
                      body='{"topips":"test"}',
                      match_querystring=True, content_type='text/json')
        data = {'topips': 'test'}
        self.assertEquals(dshield.topips(), data)
        self.assertEquals(dshield.topips('records'), data)
        self.assertEquals(dshield.topips('records', 10), data)
        self.assertEquals(dshield.topips('records', '10', datetime.date(2011, 7, 23)), data)
        self.assertEquals(dshield.topips('records', 10, '2011-07-23'), data)
        self.assertEquals(dshield.topips('records', return_format=dshield.JSON), '{"topips":"test"}')

    @responses.activate
    def test_sources(self):
        responses.add(responses.GET, 'https://dshield.org/api/sources/ip/10/2012-03-08?json',
                      body='{"sources":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET, 'https://dshield.org/api/sources/ip/10?json',
                      body='{"sources":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET, 'https://dshield.org/api/sources/ip?json',
                      body='{"sources":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET, 'https://dshield.org/api/sources?json',
                      body='{"sources":"test"}',
                      match_querystring=True, content_type='text/json')
        data = {'sources': 'test'}
        self.assertEquals(dshield.sources(), data)
        self.assertEquals(dshield.sources('ip'), data)
        self.assertEquals(dshield.sources('ip', 10), data)
        self.assertEquals(dshield.sources('ip', '10', datetime.date(2012, 3, 8)), data)
        self.assertEquals(dshield.sources('ip', 10, '2012-03-08'), data)
        self.assertEquals(dshield.sources('ip', return_format=dshield.JSON), '{"sources":"test"}')

    @responses.activate
    def test_porthistory(self):
        responses.add(responses.GET,
                      'https://dshield.org/api/porthistory/80/2011-07-20/2011-07-23?json',
                      body='{"porthistory":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET,
                      'https://dshield.org/api/porthistory/80/2011-07-20?json',
                      body='{"porthistory":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET, 'https://dshield.org/api/porthistory/80?json',
                      body='{"porthistory":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET, 'https://dshield.org/api/porthistory?json',
                      body='{"porthistory":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET, 'https://dshield.org/api/porthistory/badport?json',
                      body='{"porthistory":{"error":"bad port number"}}',
                      match_querystring=True, content_type='text/json')
        data = {'porthistory': 'test'}
        self.assertEquals(dshield.porthistory(80), data)
        self.assertEquals(dshield.porthistory('80'), data)
        self.assertEquals(dshield.porthistory(80, datetime.date(2011, 7, 20)), data)
        self.assertEquals(dshield.porthistory(80, '2011-07-20', datetime.date(2011, 7, 23)), data)
        self.assertEquals(dshield.porthistory(80, '2011-07-20', '2011-07-23'), data)
        self.assertEquals(dshield.porthistory(80, return_format=dshield.JSON), '{"porthistory":"test"}')
        self.assertRaises(dshield.Error, dshield.porthistory, 'badport')

    @responses.activate
    def test_asnum(self):
        responses.add(responses.GET,
                      'https://dshield.org/api/asnum/10/4837?json',
                      body='{"asnum":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET, 'https://dshield.org/api/asnum/10?json',
                      body='{"asnum":"test"}',
                      match_querystring=True, content_type='text/json')
        data = {'asnum': 'test'}
        self.assertEquals(dshield.asnum(10), data)
        self.assertEquals(dshield.asnum('10'), data)
        self.assertEquals(dshield.asnum(10, 4837), data)
        self.assertEquals(dshield.asnum(10, '4837'), data)
        self.assertEquals(dshield.asnum(10, return_format=dshield.JSON), '{"asnum":"test"}')
