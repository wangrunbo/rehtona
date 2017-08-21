# -*- coding: utf-8 -*-
import re
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from WebSites import expected_conditions as EC
from WebSites.WebSite import WebSite

__version__ = "1.0"

"""页面要素"""
# 登录画面
EMAIL_INPUT_FIELD_ID = 'ap_email'  # 账号输入栏
PASSWORD_INPUT_FIELD_ID = 'ap_password'  # 密码输入栏
LOGIN_BUTTON_ID = 'signInSubmit'  # 登录按钮
LOGIN_PAGE_TITLE = 'Amazonサインイン'  # 登录页面Title
EMAIL_MISSING_ALERT_ID = 'auth-email-missing-alert'  # "Eメールアドレスまたは携帯電話番号を入力"警告栏
PASSWORD_MISSING_ALERT_ID = 'auth-password-missing-alert'  # ”パスワードの入力”警告栏
ERROR_MESSAGE_BLOCK_ID = 'auth-error-message-box'  # ”問題が発生しました。”警告栏
WARNING_MESSAGE_BLOCK_ID = 'auth-warning-message-box'  # 認証画面がある時”重要なお知らせ”警告栏
CAPTCHA_MISSING_ALERT_ID = 'auth-guess-missing-alert'  # ”画像に表示されている文字を半角で入力してください。”警告栏
# 主页
NAV_TOOLS_BLOCK_ID = 'nav-tools'  # 主页Nav
ACCOUNT_LINK_1_ID = 'nav-link-yourAccount'  # Account Nav
ACCOUNT_LINK_2_ID = 'nav-link-accountList'  # Account Nav
ACCOUNT_BLOCK_1_ID = 'nav-flyout-yourAccount'  # Account下拉菜单
ACCOUNT_BLOCK_2_ID = 'nav-flyout-accountList'  # Account下拉菜单
LOGOUT_LINK_ID = 'nav-item-signout'  # 登出Link
# 商品页面
ADD_TO_CART_BUTTON_ID = 'add-to-cart-button'  # 加入购物车按钮
AGE_CERTIFICATION_PAGE_TITLE = '警告：アダルトコンテンツ'  # 年龄认证页面Title
# 购物车页面
CART_PAGE_TITLE = 'Amazon.co.jpショッピングカート'  # 购物车页面Title
DELETE_LINK_XPATH = '//div[@id="sc-active-cart" or @id="sc-saved-cart"]' \
                    '//input[@type="submit" and contains(@name, "submit.delete.") and @value="削除"]'  # 商品删除Link
CART_FORM_ID = 'activeCartViewForm'  # 购物车商品Form
CART_ITEM_LIST_BLOCK_CSS = 'div.sc-list-body'  # 购物车待购买商品
CART_ITEM_BLOCK_CSS = 'div.a-row.sc-list-item.sc-list-item-border'  # 购物车商品详细
CART_ITEM_BLOCK_XPATH = './div[@data-asin="%s" and @class="a-row sc-list-item  sc-list-item-border"]'  # 购物车商品详细
QUANTITY_INPUT_FIELD_NAME = 'quantityBox'  # 数量输入栏
QUANTITY_SELECT_DISABLED_CLASS = 'a-button-disabled'  # 数量选择栏Disable时被追加的CSS
QUANTITY_SELECT_NAME = 'quantity'  # 数量选择栏
CHECKOUT_BUTTON_NAME = 'proceedToCheckout'  # “レジに進む”按钮
# 地址画面
SAVED_ADDRESS_BLOCK_ID = 'address-book-entry-%d'  # 已存地址
LOADING_SPINNER_BLOCK_ID = 'loading-spinner-blocker-doc'  # 加载中
DELETE_ADDRESS_LINK_TEXT = '削除'  # 地址删除Button
NAME_INPUT_FIELD_ID = 'enterAddressFullName'
POSTCODE1_INPUT_FIELD_ID = 'enterAddressPostalCode1'
POSTCODE2_INPUT_FIELD_ID = 'enterAddressPostalCode2'
PREFECTURE_SELECT_FIELD_ID = 'enterAddressStateOrRegion'
ADDRESS1_INPUT_FIELD_ID = 'enterAddressAddressLine1'
ADDRESS2_INPUT_FIELD_ID = 'enterAddressAddressLine2'
COMPANY_INPUT_FIELD_ID = 'enterAddressAddressLine3'
TEL_INPUT_FIELD_ID = 'enterAddressPhoneNumber'
ADDRESS_NEXT_BUTTON_NAME = 'shipToThisAddress'
# 配送方式选择画面
SHIPPING_PAGE_TITLE = '配送オプションの選択 - Amazon.co.jp レジ'
SHIPPING_FORM_ID = 'shippingOptionFormId'
# 支付方式选择画面
PAYMENT_PAGE_TITLE = '支払い方法の選択'
PAYMENT_LOADING_SPINNER_BLOCK_ID = 'spinner-anchor'
PAYMENT_NEXT_BUTTON_ID = 'continue-top'
# 注文确认画面
ORDER_PAGE_TITLE = '注文の確定 - Amazon.co.jp レジ'
ORDER_BUTTON_NAME = 'placeYourOrder1'
ORDER_SUMMARY_BLOCK_ID = 'subtotals-marketplace-table'
# 注文完成画面
ORDER_COMPLETE_PAGE_TITLE = 'Amazon.co.jpをご利用いただき、ありがとうございました'
ORDER_CODE_XPATH = '//h5[contains(text(), "注文番号:")]/span[matches(@id, "order-number-\d{3}-\d{7}-\d{7}")]'
# 注文履历画面
HISTORY_PAGE_TITLE = '注文履歴'
HISTORY_BLOCK_ID = 'ordersContainer'
HISTORY_ORDER_BLOCK_XPATH = './div[@class="a-box-group a-spacing-base order"]'  # 同一注文番号的商品组
HISTORY_ORDER_CODE_BLOCK_XPATH = './div[@class="a-box a-color-offset-background order-info"]' \
                                 '/div[@class="a-box-inner"]/div[@class="a-fixed-right-grid"]' \
                                 '/div[@class="a-fixed-right-grid-inner"]' \
                                 '/div[@class="a-fixed-right-grid-col actions a-col-right"]' \
                                 '/div[@class="a-row a-size-mini"]' \
                                 '/span[contains(@class, "label") and contains(text(), "注文番号")]' \
                                 '/following-sibling::span[contains(@class, "value")]'  # 注文番号
HISTORY_ITEM_BLOCK_XPATH = './div[@class="a-box shipment shipment-is-delivered"]' \
                           '/div[@class="a-box-inner"]' \
                           '/div[@class="a-fixed-right-grid a-spacing-top-medium"]' \
                           '/div[@class="a-fixed-right-grid-inner"]' \
                           '/div[@class="a-fixed-right-grid-col a-col-left"]' \
                           '/div[@class="a-row"]' \
                           '/div[contains(@class, "a-fixed-left-grid")]' \
                           '/div[@class="a-fixed-left-grid-inner"]'  # 商品
HISTORY_ITEM_NAME_XPATH = './div[@class="a-fixed-left-grid-col a-col-right"]' \
                          '/div[@class="a-row"]' \
                          '/a[@class="a-link-normal" and starts-with(@href, "/gp/product/")]'  # 商品名


class Amazon(WebSite):
    """
    Amazon
    """
    top_page = 'https://www.amazon.co.jp/'
    login_page = 'https://www.amazon.co.jp/login'
    cart_page = 'https://www.amazon.co.jp/gp/cart/view.html'
    item_page = 'https://www.amazon.co.jp/dp/%s/ref=twister_dp_update?_encoding=UTF8&psc=1'
    history_page = 'https://www.amazon.co.jp/gp/css/order-history/ref=nav_nav_orders_first'

    def login(self):
        """
        登录
        :return: 登入成功/失败
        """
        if not self.browser.title == LOGIN_PAGE_TITLE:
            self.visit(self.login_page, EC.title_is(LOGIN_PAGE_TITLE))

        email_input_field = self.browser.find_element_by_id(EMAIL_INPUT_FIELD_ID)
        password_input_field = self.browser.find_element_by_id(PASSWORD_INPUT_FIELD_ID)
        submit_button = self.browser.find_element_by_id(LOGIN_BUTTON_ID)

        email_input_field.clear()
        email_input_field.send_keys(self.email)
        password_input_field.clear()
        password_input_field.send_keys(self.password)
        submit_button.click()

        WebDriverWait(self.browser, self._wait).until(login_complete(), '登录后页面异常。')

        return not EC.title_is(LOGIN_PAGE_TITLE)(self.browser)

    def logout(self):
        """
        登出
        :return: True
        """
        if EC.presence_of_all_elements_located((By.ID, NAV_TOOLS_BLOCK_ID))(self.browser):
            loop = 2
            for i in range(0, loop):
                try:
                    if EC.presence_of_all_elements_located((By.ID, ACCOUNT_LINK_1_ID))(self.browser):
                        account_link = self.browser.find_element_by_id(ACCOUNT_LINK_1_ID)
                    else:
                        account_link = self.browser.find_element_by_id(ACCOUNT_LINK_2_ID)

                    ActionChains(self.browser).move_to_element(account_link).perform()
                    WebDriverWait(self.browser, 1).until(
                        lambda driver: EC.visibility_of_any_elements_located((By.ID, ACCOUNT_BLOCK_1_ID))(driver)
                                       or EC.visibility_of_any_elements_located((By.ID, ACCOUNT_BLOCK_2_ID))(driver)
                    )
                except TimeoutException:
                    if i == loop - 1:
                        raise
                else:
                    break

            try:
                logout = self.browser.find_element_by_id(LOGOUT_LINK_ID)
            except NoSuchElementException:
                pass
            else:
                logout.click()
                WebDriverWait(self.browser, self._wait).until(EC.title_is(LOGIN_PAGE_TITLE))

        return True

    def clear_cart(self):
        """
        清空购物车
        :return: 购物车清空成功/失败
        """
        if self.browser.title != CART_PAGE_TITLE:
            self.visit(self.cart_page, EC.title_is(CART_PAGE_TITLE))

        for delete in self.browser.find_elements_by_xpath(DELETE_LINK_XPATH):
            try:
                WebDriverWait(self.browser, self._wait).until(EC.element_is_enabled(delete))
            except TimeoutException:
                return False

            delete.click()

        return True

    def get(self, asin):
        """
        将商品加入购物车
        :param asin:
        :return: 加入购物车成功/失败
        """
        self.visit(self.item_page % asin, item_page_loaded())

        if self.browser.title == AGE_CERTIFICATION_PAGE_TITLE:
            # 成人商品
            return False

        add = self.browser.find_element_by_id(ADD_TO_CART_BUTTON_ID)
        if add.is_enabled():
            add.click()
        else:
            raise Exception(f'商品[{asin}]无法加入购物车！')

        return True

    def cart(self, products):
        """
        购物车操作
        :param products:
        :return: 操作完成后的商品情报
        """
        # 操作完成后，购物车中的商品情报
        cart = dict()

        if self.browser.title != CART_PAGE_TITLE:
            self.visit(self.cart_page, EC.title_is(CART_PAGE_TITLE))

        # 购物车中的商品列表
        container = self.browser.find_element_by_id(CART_FORM_ID)
        try:
            container = container.find_element_by_css_selector(CART_ITEM_LIST_BLOCK_CSS)
        except NoSuchElementException:
            raise Exception('操作失败，购物车中无商品！')
        items = container.find_elements_by_css_selector(CART_ITEM_BLOCK_CSS)

        if len(items) != len(products):
            # 加入到购物车中的商品数与购买商品数不一致
            raise Exception('加入到购物车中的商品数与购买商品数不一致！')

        # 循环购物车中商品列表，检查商品状态的同时修改购买数量
        for item in items:
            asin = item.get_attribute('data-asin')
            quantity = int(item.get_attribute('data-quantity'))

            try:
                # 处理中的商品
                product = products[asin]
            except KeyError:
                # 购物车中存在未被购买的商品
                raise Exception(f'未购买商品{asin}存在于购物车中！')

            # 保证price与quantity均为int型
            product['price'] = int(product['price'])
            product['quantity'] = int(product['quantity'])

            if quantity != product['quantity']:
                quantity_input_field = item.find_element_by_name(QUANTITY_INPUT_FIELD_NAME)
                if quantity_input_field.is_displayed():
                    # 当数量输入栏可见时，直接输入购买数量后Enter
                    quantity_input_field.clear()
                    quantity_input_field.send_keys(product['quantity'])
                    quantity_input_field.send_keys(Keys.ENTER)

                else:
                    # 当数量输入栏不可见时，选择购买数量
                    if product['quantity'] < 10:
                        Select(item.find_element_by_name(QUANTITY_SELECT_NAME)).select_by_value(
                            str(product['quantity']))

                    else:
                        Select(item.find_element_by_name(QUANTITY_SELECT_NAME)).select_by_value('10')
                        WebDriverWait(self.browser, self._wait).until(EC.element_is_displayed(quantity_input_field))

                        quantity_input_field.clear()
                        quantity_input_field.send_keys(product['quantity'])
                        quantity_input_field.send_keys(Keys.ENTER)

                WebDriverWait(self.browser, self._wait).until(cart_quantity_changed(container, asin))

            # 检查价格与数量
            item = container.find_element_by_xpath(CART_ITEM_BLOCK_XPATH % asin)

            cart[asin] = {
                'price': int(item.get_attribute('data-price')),
                'quantity': int(item.get_attribute('data-quantity'))
            }

        return cart

    def checkout(self, address):
        """
        支付操作
        :param address
        :return:
        """
        checkout_button = self.browser.find_element_by_name(CHECKOUT_BUTTON_NAME)
        if not checkout_button.is_enabled():
            raise Exception('无法进行支付！')

        checkout_button.click()

        # 如跳转到登录页面，进行登录
        if self.browser.title == LOGIN_PAGE_TITLE:
            self.login()

        # 清空已存地址
        self._clear_address()

        # --输入地址--
        name_input_field = self.browser.find_element_by_id(NAME_INPUT_FIELD_ID)
        postcode1_input_field = self.browser.find_element_by_id(POSTCODE1_INPUT_FIELD_ID)
        postcode2_input_field = self.browser.find_element_by_id(POSTCODE2_INPUT_FIELD_ID)
        prefecture_select = self.browser.find_element_by_id(PREFECTURE_SELECT_FIELD_ID)
        address1_input_field = self.browser.find_element_by_id(ADDRESS1_INPUT_FIELD_ID)
        address2_input_field = self.browser.find_element_by_id(ADDRESS2_INPUT_FIELD_ID)
        company_input_field = self.browser.find_element_by_id(COMPANY_INPUT_FIELD_ID)
        tel_input_field = self.browser.find_element_by_id(TEL_INPUT_FIELD_ID)

        # 初始化
        name_input_field.clear()
        postcode1_input_field.clear()
        postcode2_input_field.clear()
        Select(prefecture_select).select_by_value('')
        address1_input_field.clear()
        address2_input_field.clear()
        company_input_field.clear()
        tel_input_field.clear()

        # 姓名
        name_input_field.send_keys(address['name'])

        # 邮政编码
        postcode1_input_field.send_keys(address['postcode'][:-4])
        postcode2_input_field.send_keys(address['postcode'][-4:])

        # 都道府县
        WebDriverWait(self.browser, self._wait).until(EC.value_is_not(prefecture_select, ''))
        Select(prefecture_select).select_by_value(address['prefecture'])

        # 住所1
        WebDriverWait(self.browser, self._wait).until(EC.value_is_not(address1_input_field, ''))
        if re.match(address1_input_field.get_attribute('value'), address['address1']):
            address1_input_field.clear()
            address1_input_field.send_keys(address['address1'])
        else:
            raise Exception('地址与邮编不符！')

        # 住所2
        address2_input_field.send_keys(address['address2'])

        # 公司
        company_input_field.send_keys(address['company'])

        # 电话号码
        tel_input_field.send_keys(address['tel'])

        # 下一步
        self.browser.find_element_by_name(ADDRESS_NEXT_BUTTON_NAME).click()

        # --配送方式选择--
        WebDriverWait(self.browser, self._wait).until(EC.title_is(SHIPPING_PAGE_TITLE))
        self.browser.find_element_by_id(SHIPPING_FORM_ID).submit()

        # --支付方式选择--TODO
        WebDriverWait(self.browser, self._wait).until(EC.title_is(PAYMENT_PAGE_TITLE))
        self.browser.find_element_by_name('paymentMethod').click()
        self.browser.find_element_by_id(PAYMENT_NEXT_BUTTON_ID).click()

        # 检查
        WebDriverWait(self.browser, self._wait).until(EC.title_is(ORDER_PAGE_TITLE))
        if not self.browser.find_element_by_name(ORDER_BUTTON_NAME).is_enabled():
            raise Exception('无法完成支付，请确认交易信息！')

        price = None
        gift = None
        summaries = list()
        for summary in iter(self.browser.find_element_by_id(ORDER_SUMMARY_BLOCK_ID).find_elements_by_tag_name('tr')):
            td = summary.find_elements_by_tag_name('td')
            if len(td) == 2:
                label = re.sub(r'[：:]\s*$', '', td[0].text)
                value = self._price(td[1].text)
                if label == 'ご請求額':
                    price = value
                elif label == 'Amazonギフト券':
                    gift = value

                summaries.append({
                    'label': label,
                    'price': value
                })

        if len(summaries) == 0 or price is None or gift is None:
            raise Exception('交易价格明细取得失败！')

        return price - gift, summaries

    def order(self):
        """
        确认支付
        :return:
        """
        WebDriverWait(self.browser, self._wait).until(EC.title_is(ORDER_COMPLETE_PAGE_TITLE))

        self.browser.get_screenshot_as_file('xxxx.png')  # TODO

    def get_order_code(self, asins):
        """
        取得Amazon单号
        :return:
        """
        if EC.title_is(ORDER_COMPLETE_PAGE_TITLE)(self.browser):
            # 从注文完成页面中取得
            orders = self.browser.find_elements_by_xpath(ORDER_CODE_XPATH)
            for order in orders:
                print(order.text)
        else:
            # 非注文完成页面，从注文履历中取得
            self.visit(self.history_page)

            # 如跳转到登录页面，进行登录
            if self.browser.title == LOGIN_PAGE_TITLE:
                self.login()

            WebDriverWait(self.browser, self._wait).until(EC.title_is(HISTORY_PAGE_TITLE))

            # 注文番号取得
            orders = iter(
                self.browser.find_element_by_id(HISTORY_BLOCK_ID).find_elements_by_xpath(HISTORY_ORDER_BLOCK_XPATH))
            for order in orders:
                # 每组商品的注文番号
                code = order.find_element_by_xpath(HISTORY_ORDER_CODE_BLOCK_XPATH).text

                # 检查该注文内的所有商品
                items = iter(order.find_elements_by_xpath(HISTORY_ITEM_BLOCK_XPATH))
                for item in items:
                    item_name = item.find_element_by_xpath(HISTORY_ITEM_NAME_XPATH)
                    asin = re.search('(?<=^https://www\.amazon\.co\.jp/gp/product/)[A-Z0-9]{10}(?=/)',
                                     item_name.get_attribute("href")).group()
                    print(asin)
                    # TODO
        return True

    def close(self):
        try:
            self.clear_cart()
        except:
            pass

        super(Amazon, self).close()

    def _clear_address(self):
        """
        所有已保存的地址删除
        :return:
        """
        i = 0
        while True:
            try:
                delete = self.browser \
                    .find_element_by_id(SAVED_ADDRESS_BLOCK_ID % i) \
                    .find_element_by_link_text(DELETE_ADDRESS_LINK_TEXT)
            except NoSuchElementException:
                break

            delete.click()

            WebDriverWait(self.browser, self._wait).until(address_can_be_deleted(delete))

            i += 1


    @staticmethod
    def _price(price):
        """
        字符串价格转整型
        :param str price:
        :return:
        """
        if type(price) is not str:
            return price

        return int(re.sub(r'[￥\s,]', '', price))


###################################################################################
# ############################# Expected Conditions ############################# #
###################################################################################


class login_complete:
    """登录完成"""

    def __call__(self, driver):
        return not EC.title_is(LOGIN_PAGE_TITLE)(driver) \
               or EC.presence_of_element_located((By.ID, EMAIL_MISSING_ALERT_ID))(driver) \
               or EC.presence_of_element_located((By.ID, PASSWORD_MISSING_ALERT_ID))(driver) \
               or EC.presence_of_element_located((By.ID, ERROR_MESSAGE_BLOCK_ID))(driver) \
               or EC.presence_of_element_located((By.ID, WARNING_MESSAGE_BLOCK_ID))(driver) \
               or EC.presence_of_element_located((By.ID, CAPTCHA_MISSING_ALERT_ID))(driver)


class item_page_loaded:
    """商品页面载入完成"""

    def __call__(self, driver):
        return EC.title_is(AGE_CERTIFICATION_PAGE_TITLE)(driver) \
               or EC.element_to_be_clickable((By.ID, ADD_TO_CART_BUTTON_ID))(driver)


class cart_quantity_changed:
    """购物车商品数量更改完成"""

    def __init__(self, container, asin):
        self.container = container
        self.asin = asin

    def __call__(self, driver):
        try:
            input = self.container \
                .find_element_by_xpath(CART_ITEM_BLOCK_XPATH % self.asin) \
                .find_element_by_name(QUANTITY_INPUT_FIELD_NAME)
        except StaleElementReferenceException:
            # 页面恰好在时间节点变化，重新取得元素
            input = self.container \
                .find_element_by_xpath(CART_ITEM_BLOCK_XPATH % self.asin) \
                .find_element_by_name(QUANTITY_INPUT_FIELD_NAME)

        if input.is_displayed():
            return EC.element_is_enabled(input)(driver)
        else:
            return not EC.presence_of_all_elements_located((By.CLASS_NAME, QUANTITY_SELECT_DISABLED_CLASS))(driver)


class address_can_be_deleted:
    """地址可以被删除"""

    def __init__(self, delete):
        self.delete = delete

    def __call__(self, driver):
        return EC.invisibility_of_element_located((By.ID, LOADING_SPINNER_BLOCK_ID))(
            driver) and EC.element_is_clickable(self.delete)


###################################################################################
###################################################################################
###################################################################################

if __name__ == '__main__':
    from selenium import webdriver

    asins = [
        'B073D17KT7',  # 成人商品
        'B018XATM7K'  # 双重商家
    ]

    products = {
        '4041061016': {
            'price': 1000,
            'quantity': 15
        },
        'B0043TXMWM': {
            'price': 1166,
            'quantity': 4
        },
        'B0029ZFYJQ': {
            'price': 4744,
            'quantity': 11
        },
        'B00WB32H28': {
            'price': 7980,
            'quantity': 2
        },
        'B01MZBFNZN': {
            'price': 11228,
            'quantity': 15
        }
    }

    address = {
        'name': 'wangrunbo',
        'postcode': '2790002',
        'prefecture': '千葉県',
        'address1': '浦安市北栄',
        'address2': 'aaaa',
        'tel': '07012780921',
        'company': 'mamol'
    }
    import sys

    # print(sys.path)
    # exit()

    amazon = Amazon('../Drivers/chromedriver')

    amazon.visit('https://www.amazon.co.jp/login')

    result = amazon.login()
    result = amazon.logout()

    # amazon.visit(amazon.cart_page)

    # result = amazon.checkout(address)

    print(result)
