import requests


r =requests.get('http://194.58.92.160:8001/kf_checks/kf_checks/kf96792_1893883161.pdf')

with open('12234.pdf', 'wb') as f:
    f.write(r.content)