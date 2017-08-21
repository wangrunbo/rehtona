# -*- coding: utf-8 -*-
from selenium.webdriver.support.expected_conditions import *

__version__ = "1.0"


class element_is_enabled:
    """元素非disabled"""
    def __init__(self, element):
        self.element = element

    def __call__(self, driver):
        return self.element.is_enabled()


class element_is_displayed:
    """元素可见"""
    def __init__(self, element):
        self.element = element

    def __call__(self, driver):
        return self.element.is_displayed()


class element_is_clickable:
    """元素可见"""
    def __init__(self, element):
        self.element = element

    def __call__(self, driver):
        return self.element.is_displayed and self.element.is_enabled


class value_is_not:
    """值变化"""
    def __init__(self, element, value):
        self.element = element
        self.value = value

    def __call__(self, driver):
        return self.element.get_attribute('value') != self.value
