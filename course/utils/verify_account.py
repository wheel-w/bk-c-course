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
    return result


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
    information_url = base_url.replace('default2.aspx',
                                       '') + 'xsgrxx.aspx?xh=' + username + '&xm=' + name + '&gnmkdm=N121501'
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

    base_url = os.environ.get('BKAPP_CODE_XAUT_OFFICIAL_WEB')
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 '
            'Safari/537.36',
        'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }

    login_url = base_url
    res = requests.get(login_url, allow_redirects=False)
    checkcode_url = login_url.replace(r'/default2.aspx', r'/CheckCode.aspx?')

    cookies = res.cookies
    checkcode = requests.get(checkcode_url, cookies=cookies, headers=headers)  # ??????????????????
    result = base64_api(checkcode.content)
    if result["success"]:
        code = result["data"]["result"]
    else:
        raise Exception("?????????????????????????????????????????????. base64??????????????????: {}".format(result["message"]))
    post_data = {
        '__VIEWSTATE': 'dDwtNTE2MjI4MTQ7Oz4v9xUqkOgkwu+22N3B4gSg7V/qCg==',
        'txtUserName': username,
        'Textbox1': '',
        'TextBox2': password,
        'txtSecretCode': code,
        'RadioButtonList1': '??????'.encode("gb2312"),
        'Button1': '',
        'lbLanguage': '',
        'hidPdrs': '',
        'hidsc': '',
    }
    resource = requests.post(url=login_url,
                             data=post_data,
                             cookies=cookies,
                             headers=headers).text

    if '????????????' in resource:
        dom_tree = etree.HTML(resource)
        name = dom_tree.xpath('//span[@id="xhxm"]/text()')
        name = name[0].split('???')[0]
        user_info = get_information(cookies, username, name)
        return True, user_info, '????????????'
    elif '????????????' in resource:
        return False, None, '????????????'
    elif '??????????????????' in resource:
        return False, None, '??????????????????'
    else:
        return False, None, "?????????????????????????????????"
