# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template
from selenium.common.exceptions import WebDriverException
from Config import config
from Config.datasource import Session, or_
from Config.const import *
from WebSites import WebSite, Amazon
# noinspection PyUnresolvedReferences
from Model import *
import time
app = Flask(__name__)
sites = dict()


@app.route('/', methods=['get'])
def index():
    return render_template('index.html', url=WEB_URL)


@app.route('/cart', methods=['post'])
def cart():
    """
    商品加入购物车
    :return:
    """
    order = request.json
    session = Session()
    amazon = None
    global sites

    print(f'收到来自IP[{request.remote_addr}]的Cart请求，使用账号[{order["amazon_account"]}]开始进行处理！')

    try:
        amazon_account: AmazonAccount = session.query(AmazonAccount).filter(
            AmazonAccount.email == order['amazon_account'],
            or_(
                AmazonAccount.amazon_account_status_id == AmazonAccountStatus.IDLE,
                AmazonAccount.amazon_account_status_id == AmazonAccountStatus.USING
            )
        ).one()

        if amazon_account.email in sites:
            amazon = sites[amazon_account.email]
        else:
            amazon = sites[amazon_account.email] = Amazon(amazon_account.email, amazon_account.password)

        try:
            amazon.visit(amazon.cart_page)
        except WebDriverException:
            # 被人为手动关掉的浏览器
            clean_up(amazon)
            amazon = sites[amazon_account.email] = Amazon(amazon_account.email, amazon_account.password)

        amazon.login()
        amazon.clear_cart()

        # 将商品加入购物车
        for asin in order['order_details'].keys():
            amazon.get(asin)

        amazon.visit(amazon.cart_page)
        products = amazon.cart(order['order_details'])

        result = {
            'result': True,
            'products': products
        }
    except Exception as exception:
        result = clean_up(amazon, exception)

    return jsonify(result)


@app.route('/checkout', methods=['post'])
def checkout():
    """
    填写地址
    :return:
    """
    print(f'收到来自IP[{request.remote_addr}]的Checkout请求，使用账号[{request.json["amazon_account"]}]开始进行处理！')

    session = Session()
    amazon = None
    global sites

    try:
        amazon_account: AmazonAccount = session.query(AmazonAccount).filter(
            AmazonAccount.email == request.json['amazon_account'],
            AmazonAccount.amazon_account_status_id == AmazonAccountStatus.USING
        ).one()

        amazon = sites[amazon_account.email]

        address = {
            'name': amazon_account.depository_address.name,
            'postcode': amazon_account.depository_address.postcode,
            'prefecture': amazon_account.depository_address.prefecture.name,
            'address1': amazon_account.depository_address.address1,
            'address2': amazon_account.depository_address.address2,
            'company': amazon_account.depository_address.company,
            'tel': amazon_account.depository_address.tel
        }

        price, summaries = amazon.checkout(address)

        result = {
            'result': True,
            'price': price,
            'summaries': summaries
        }
    except Exception as exception:
        result = clean_up(amazon, exception)

    return jsonify(result)


def clean_up(site, exception=False):
    """
    登出账号，关闭浏览器，删除全局变量中的该存储
    :param WebSite site:
    :param bool|Exception exception:
    :return:
    """
    if exception is not False:
        print(f'异常：【{str(exception)}】！', '程序终止！', sep='\n')

    if site:
        site.close()

        if site.email in sites:
            del sites[site.email]

    return {
        'result': False,
        'message': str(exception)
    }


@app.route('/test', methods=['post'])
def test():
    print(1)

    email = request.json['email']
    print(email)

    time.sleep(10)

    return jsonify({'email': email})


if __name__ == '__main__':
    app.run(debug=config.debug, threaded=True, port=config.port, host='0.0.0.0')
