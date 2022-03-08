import os
import json
import base64
import requests
from lxml import etree


def base64_api(img):
    name = os.environ.get('BKAPP_CODE_API_USERNAME')
    password = os.environ.get('BKAPP_CODE_API_PASSWORD')
    base64_data = base64.b64encode(img)
    b64 = base64_data.decode()
    data = {"username": name, "password": password, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]


def get_information(cookies, username, name):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/60.0.3112.90 Safari/537.36',

        'Referer':
            base_url + "xs_main.aspx?xh=" + username,
        'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }
    information_url = base_url + 'xsgrxx.aspx?xh=' + username + '&xm=' + name + '&gnmkdm=N121501'
    data = requests.get(information_url, cookies=cookies, headers=headers)
    data.encoding = data.apparent_encoding
    dom_tree = etree.HTML(data.text)
    sex = dom_tree.xpath('//span[@id="lbl_xb"]/text()')[0]
    academic = dom_tree.xpath('//span[@id="lbl_xy"]/text()')[0]
    major = dom_tree.xpath('//span[@id="lbl_zymc"]/text()')[0]
    stu_class = dom_tree.xpath('//span[@id="lbl_xzb"]/text()')[0]
    return {
        'user_name': username,
        'user_real_name': name,
        'user_sex': sex,
        'user_college': academic,
        'user_major': major,
        'user_class': stu_class
    }


def identify_user(username, password):
    global base_url

    base_url = "http://202.200.112.200/"
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 '
            'Safari/537.36',
        'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }

    login_url = base_url
    res = requests.get(login_url, allow_redirects=False)
    login_url = login_url + res.headers['location']
    login_url = login_url.replace('Default', 'default2')
    login_url = login_url.replace(r'/(', '(')
    checkcode_url = login_url.replace(r'/default2.aspx', r'/CheckCode.aspx?')
    base_url = login_url.replace(r'/default2.aspx', r'/')

    cookies = res.cookies
    checkcode = requests.get(checkcode_url, cookies=cookies, headers=headers)  # 伪装成浏览器
    code = base64_api(checkcode.content)
    post_data = {
        '__VIEWSTATE': 'dDwtNTE2MjI4MTQ7Oz4v9xUqkOgkwu+22N3B4gSg7V/qCg==',
        'txtUserName': username,
        'Textbox1': '',
        'TextBox2': password,
        'txtSecretCode': code,
        'RadioButtonList1': '学生'.encode("gb2312"),
        'Button1': '',
        'lbLanguage': '',
        'hidPdrs': '',
        'hidsc': '',
    }
    resource = requests.post(url=login_url,
                             data=post_data,
                             cookies=cookies,
                             headers=headers).text

    if '活动报名' in resource:
        dom_tree = etree.HTML(resource)
        name = dom_tree.xpath('//span[@id="xhxm"]/text()')
        name = name[0].split('同')[0]
        user_info = get_information(cookies, username, name)
        return True, user_info, '认证成功'
    elif '密码错误' in resource:
        return False, None, '密码错误'
    elif '用户名不存在' in resource:
        return False, None, '用户名不存在'
    else:
        return False, None, "未知错误，请联系管理员"
