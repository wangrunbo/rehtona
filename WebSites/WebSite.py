# -*- coding: utf-8 -*-
from selenium.webdriver import Chrome  # TODO
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException


class WebSite:
    """
    网店
    """
    browser = None
    _wait = 10

    top_page = None
    login_page = None
    cart_page = None

    def __init__(self, email, password, driver='Drivers/chromedriver'):
        self.browser = Chrome(driver)
        self.email = email
        self.password = password

    def visit(self, url, until=None, type=True):
        """
        载入页面
        :param url:
        :param until:
        :param type:
        :return:
        """
        self.browser.get(url)

        if until is not None:
            wait = WebDriverWait(self.browser, self._wait)
            msg = '页面' + url + '载入失败！'

            if type:
                wait.until(until, msg)
            else:
                wait.until_not(until, msg)

    def login(self):
        """
        登录
        :return:
        """
        pass

    def logout(self):
        """
        登出
        :return:
        """
        pass

    def clear_cart(self):
        """
        清空购物车
        :return:
        """
        pass

    def get(self, product):
        """
        商品加入购物车
        :param product:
        :return:
        """
        pass

    def cart(self, products):
        """
        操作购物车
        :param products:
        :return:
        """
        pass

    def checkout(self, info):
        """
        支付操作
        :param info:
        :return:
        """
        pass

    def order(self):
        """
        确认支付
        :return:
        """
        pass

    def get_order_code(self, products):
        """
        取得交易单号
        :param products
        :return:
        """
        pass

    def close(self):
        try:
            self.logout()
        except:
            pass
        finally:
            self.browser.quit()

    def is_active(self):
        try:
            active = self.browser.service.is_connectable() and self.browser.title
        except WebDriverException:
            return False

        return active


if __name__ == '__main__':
    website = WebSite()
    website.visit('https://www.amazon.co.jp/')
