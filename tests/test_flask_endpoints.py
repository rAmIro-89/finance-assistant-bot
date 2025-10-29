import re
from web_app import app


def test_health_and_user_cookie_and_graph_defaults():
    with app.test_client() as c:
        # health
        r = c.get('/health')
        assert r.status_code == 200
        assert r.get_json().get('status') == 'ok'

        # api/chat sets uid cookie
        r2 = c.post('/api/chat', json={'message': 'hola', 'when': 'web'})
        assert r2.status_code == 200
        assert 'uid=' in (r2.headers.get('Set-Cookie') or '')

        # api/user now exists
        r3 = c.get('/api/user')
        j3 = r3.get_json()
        assert j3.get('exists') is True

        # login with DNI
        r4 = c.post('/api/login', json={'dni': '12345678'})
        assert r4.status_code == 200
        assert 'uid=' in (r4.headers.get('Set-Cookie') or '')

        # presupuesto: persist ingreso then graph default uses it
        c.post('/api/chat', json={'message': 'presupuesto de $123000', 'when': 'web'})
        r6 = c.get('/api/grafico/presupuesto')
        j6 = r6.get_json()
        values = j6.get('data', [{}])[0].get('values', [])
        assert abs(sum(values) - 123000) < 1e-6


def test_whatsapp_linking_flow():
    with app.test_client() as c:
        r = c.post('/whatsapp-webhook', data={'From': 'whatsapp:+111', 'Body': 'vincular'})
        assert r.status_code == 200
        body = r.get_data(as_text=True)
        m = re.search(r'/claim/([A-Za-z0-9_-]+)', body)
        assert m
        token = m.group(1)

        r2 = c.get(f'/claim/{token}', follow_redirects=False)
        assert r2.status_code in (301,302,303,307,308)
        assert 'uid=' in (r2.headers.get('Set-Cookie') or '')
