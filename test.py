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
    def test_get_converts_json_to_list(self):
        responses.add(responses.GET, 'https://dshield.org/api/backscatter?json',
                      status=200, match_querystring=True, content_type='text/json',
                      body="""
                      [{"sourceport":"6000","count":"563542","sources":"518","targets":"94654"},
                       {"sourceport":"80","count":"201888","sources":"3294","targets":"8130"},
                       {"sourceport":"53","count":"140780","sources":"3777","targets":"255"},
                       {"sourceport":"4935","count":"101361","sources":"13726","targets":"56572"},
                       {"sourceport":"12200","count":"79924","sources":"40","targets":"8040"},
                       {"sourceport":"8080","count":"78873","sources":"73","targets":"78543"},
                       {"sourceport":"68","count":"75543","sources":"104","targets":"8"},
                       {"sourceport":"137","count":"59672","sources":"902","targets":"1918"},
                       {"sourceport":"5066","count":"57052","sources":"35","targets":"57002"},
                       {"sourceport":"5070","count":"54773","sources":"23","targets":"54745"}]
                      """)
        self.assertEquals(type(dshield._get('backscatter')), list)
        json = requests.get('https://dshield.org/api/backscatter?json').json()
        for index, item in enumerate(dshield._get('backscatter')):
            self.assertEquals(json[index], item)
        self.assertEquals(len(json), 10)
        self.assertEquals(len(dshield._get('backscatter')), 10)


class TestPublicMethods(unittest.TestCase):

    @responses.activate
    def test_backscatter(self):
        responses.add(responses.GET, 'https://dshield.org/api/backscatter?json',
                      body='["test"]', status=200,
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET,
                      'https://dshield.org/api/backscatter/2011-12-01?json',
                      body='["2011-12-01"]', status=200, match_querystring=True,
                      content_type='text/json')
        responses.add(responses.GET,
                      'https://dshield.org/api/backscatter/2011-12-01/10?json',
                      body='["10"]', status=200, match_querystring=True,
                      content_type='text/json')
        self.assertEquals(dshield.backscatter(), ["test"])
        self.assertEquals(dshield.backscatter("2011-12-01"), ["2011-12-01"])
        self.assertEquals(dshield.backscatter(datetime.date(2011, 12, 1)), ["2011-12-01"])
        self.assertEquals(dshield.backscatter("2011-12-01", 10), ["10"])
        self.assertEquals(dshield.backscatter("2011-12-01", "10"), ["10"])
        self.assertEquals(dshield.backscatter("2011-12-01", "10", dshield.JSON),
                          '["10"]')

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
        responses.add(responses.GET, 'https://dshield.org/api/sources/attacks/10?json',
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
        responses.add(responses.GET,
                      'https://dshield.org/api/porthistory/80/{date}?json'.format(date=(datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")),
                      body='{"porthistory":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET,
                      'https://dshield.org/api/porthistory/badport/{date}?json'.format(date=(datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")),
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

    @responses.activate
    def test_dailysummary(self):
        responses.add(responses.GET,
                      'https://dshield.org/api/dailysummary/2012-05-01/2012-05-03?json',
                      body='{"dailysummary":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET,
                      'https://dshield.org/api/dailysummary/2012-05-01?json',
                      body='{"dailysummary":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET,
                      'https://dshield.org/api/dailysummary/{date}?json'.format(date=datetime.datetime.now().strftime("%Y-%m-%d")),
                      body='{"dailysummary":"test"}',
                      match_querystring=True, content_type='text/json')
        data = {'dailysummary': 'test'}
        self.assertEquals(dshield.dailysummary(), data)
        self.assertEquals(dshield.dailysummary('2012-05-01'), data)
        self.assertEquals(dshield.dailysummary(datetime.date(2012, 5, 1)), data)
        self.assertEquals(dshield.dailysummary('2012-05-01', '2012-05-03'), data)
        self.assertEquals(dshield.dailysummary('2012-05-01', datetime.date(2012, 5, 3)), data)
        self.assertEquals(dshield.dailysummary(return_format=dshield.JSON), '{"dailysummary":"test"}')

    @responses.activate
    def test_daily404summary(self):
        responses.add(responses.GET,
                      'https://dshield.org/api/daily404summary/2012-02-23?json',
                      body='{"daily404summary":"test"}',
                      match_querystring=True, content_type='text/json')
        data = {'daily404summary': 'test'}
        self.assertEquals(dshield.daily404summary('2012-02-23'), data)
        self.assertEquals(dshield.daily404summary(datetime.date(2012, 2, 23)), data)
        self.assertEquals(dshield.daily404summary('2012-02-23', return_format=dshield.JSON),
                          '{"daily404summary":"test"}')

    @responses.activate
    def test_daily404detail(self):
        responses.add(responses.GET,
                      'https://dshield.org/api/daily404detail/2012-02-23/10?json',
                      body='{"daily404detail":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET,
                      'https://dshield.org/api/daily404detail/2012-02-23?json',
                      body='{"daily404detail":"test"}',
                      match_querystring=True, content_type='text/json')
        data = {'daily404detail': 'test'}
        self.assertEquals(dshield.daily404detail('2012-02-23'), data)
        self.assertEquals(dshield.daily404detail(datetime.date(2012, 2, 23)), data)
        self.assertEquals(dshield.daily404detail('2012-02-23', 10), data)
        self.assertEquals(dshield.daily404detail('2012-02-23', '10'), data)
        self.assertEquals(dshield.daily404detail('2012-02-23', return_format=dshield.JSON),
                          '{"daily404detail":"test"}')

    @responses.activate
    def test_glossary(self):
        responses.add(responses.GET,
                      'https://dshield.org/api/glossary?json',
                      body='{"glossary":"test"}',
                      match_querystring=True, content_type='text/json')
        responses.add(responses.GET,
                      'https://dshield.org/api/glossary/test?json',
                      body='{"glossary":"test"}',
                      match_querystring=True, content_type='text/json')
        data = {'glossary': 'test'}
        self.assertEquals(dshield.glossary(), data)
        self.assertEquals(dshield.glossary('test'), data)
        self.assertEquals(dshield.glossary(return_format=dshield.JSON),
                          '{"glossary":"test"}')

    @responses.activate
    def test_webhoneypotsummary(self):
        responses.add(responses.GET,
                      'https://dshield.org/api/webhoneypotsummary/2012-12-10?json',
                      body='{"webhoneypotsummary":"test"}',
                      match_querystring=True, content_type='text/json')
        data = {'webhoneypotsummary': 'test'}
        self.assertEquals(dshield.webhoneypotsummary('2012-12-10'), data)
        self.assertEquals(dshield.webhoneypotsummary(datetime.date(2012, 12, 10)), data)
        self.assertEquals(dshield.webhoneypotsummary('2012-12-10', return_format=dshield.JSON),
                          '{"webhoneypotsummary":"test"}')

    @responses.activate
    def test_webhoneypotbytype(self):
        responses.add(responses.GET,
                      'https://dshield.org/api/webhoneypotbytype/2012-12-10?json',
                      body='{"webhoneypotbytype":"test"}',
                      match_querystring=True, content_type='text/json')
        data = {'webhoneypotbytype': 'test'}
        self.assertEquals(dshield.webhoneypotbytype('2012-12-10'), data)
        self.assertEquals(dshield.webhoneypotbytype(datetime.date(2012, 12, 10)), data)
        self.assertEquals(dshield.webhoneypotbytype('2012-12-10', return_format=dshield.JSON),
                          '{"webhoneypotbytype":"test"}')

class TestRealAPI(unittest.TestCase):

    def test_no_functions_throw_exceptions(self):
        try:
            dshield.backscatter()
            dshield.handler()
            dshield.infocon()
            dshield.ip('8.8.8.8')
            dshield.port(80)
            dshield.portdate(80)
            dshield.topports()
            dshield.topips()
            dshield.sources()
            dshield.porthistory(80)
            dshield.asnum(1)
            dshield.dailysummary()
            dshield.daily404summary(datetime.date(2011, 12, 1))
            dshield.daily404detail(datetime.date(2011, 12, 1))
            dshield.glossary()
            dshield.webhoneypotsummary(datetime.date(2011, 12, 1))
            dshield.webhoneypotbytype(datetime.date(2011, 12, 1))
        except requests.RequestException:
            # don't care about network errors
            pass
        except Exception:
            # anything else is a fail
            self.assertTrue(False)

    def test_limits_respected(self):
        self.assertEquals(len(dshield.topips(limit=100)), 100)
