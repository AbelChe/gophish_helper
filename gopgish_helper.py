import requests
import datetime
import urllib3
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def timeutl(str_time):
    s = datetime.datetime.strptime(str_time[0:19], '%Y-%m-%dT%H:%M:%S')
    o = (s + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    return o


def set_args():
    if len(sys.argv) != 5:
        print('Usage: python gophish_helper.py <gopgish_url> <api_key> <from_index> <how_much>')
        print('  例如: 获取300到350的任务数据')
        print('       python gophish_helper.py https://1.1.1.1:3333 xxxxxxxxxxxxxxxxxxxxxxxxxxxxx 300 50')
        exit()
    gophish_url = sys.argv[1]
    api_key = sys.argv[2]
    from_index = int(sys.argv[3])
    numbers = int(sys.argv[4])
    return gophish_url, api_key, from_index, numbers


if __name__ == '__main__':
    gophish_url, api_key, from_index, numbers = set_args()
    HEADERS = {
        'Authorization': 'Bearer {0}'.format(api_key)
    }
    click = []
    for i in range(from_index, from_index+numbers):
        url = gophish_url + '/api/campaigns/' + str(i) + '/results?{}'
        r = requests.get(url, headers=HEADERS, verify=False)
        js = r.json()
        if js.get('results'):
            for i in js.get('results'):
                if i.get('status') == 'Clicked Link':
                    email = i.get('email')
                    ip = i.get('ip')
                    this_obj = {'email': email, 'ip': ip, 'time': []}
                    sys.stdout.write('.')
                    sys.stdout.flush()
                    for j in js.get('timeline'):
                        if j.get('email') == email and j.get('message') == 'Clicked Link':
                            this_obj['time'].append(timeutl(j.get('time')))
                    click.append(this_obj)
    print('\n')
    sorted_click = []
    for i in click:
        print(i.get('email') + '\t' + i.get('ip') + '\t' + sorted(i.get('time'),
              key=lambda date: datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timestamp())[-1])
    print(len(click))
