import re
from web_app import app

print('--- scratch_test_flask_endpoints start ---')
with app.test_client() as c:
    r = c.get('/health')
    print('health_status:', r.status_code, r.get_json())

    r2 = c.post('/api/chat', json={'message': 'hola', 'when': 'web'})
    print('chat_status:', r2.status_code, 'set_cookie_has_uid:', 'uid=' in (r2.headers.get('Set-Cookie') or ''))

    r3 = c.get('/api/user')
    print('user_exists:', r3.get_json().get('exists'))

    r4 = c.post('/api/login', json={'dni': '12345678'})
    print('login_status:', r4.status_code, 'set_cookie_has_uid:', 'uid=' in (r4.headers.get('Set-Cookie') or ''))

    c.post('/api/chat', json={'message': 'presupuesto de $123000', 'when': 'web'})
    r6 = c.get('/api/grafico/presupuesto')
    j6 = r6.get_json()
    values = j6.get('data', [{}])[0].get('values', [])
    print('grafico_sum_matches:', abs(sum(values) - 123000) < 1e-6, 'sum=', sum(values))

with app.test_client() as c:
    r = c.post('/whatsapp-webhook', data={'From': 'whatsapp:+111', 'Body': 'vincular'})
    print('whatsapp_webhook_status:', r.status_code)
    body = r.get_data(as_text=True)
    m = re.search(r'/claim/([A-Za-z0-9_-]+)', body)
    print('found_token:', bool(m))
    token = m.group(1) if m else None

    if token:
        r2 = c.get(f'/claim/{token}', follow_redirects=False)
        print('claim_status:', r2.status_code, 'set_cookie_has_uid:', 'uid=' in (r2.headers.get('Set-Cookie') or ''))

print('--- scratch_test_flask_endpoints end ---')
