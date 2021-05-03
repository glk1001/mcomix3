# -*- coding: utf-8 -*-

import configparser

from mcomix import log

DOUBLE_PAGES_SECTION = 'double_pages'
PAGE_NUMBERS_SECTION = 'page_numbers'
ROMAN_NUMERALS = {
    1: 'i',
    2: 'ii',
    3: 'iii',
    4: 'iv',
    5: 'v',
    6: 'vi',
    7: 'vii',
    8: 'viii',
    9: 'ix',
    10: 'x',
}


class PageData:
    def __init__(self):
        self.__do_not_display_as_double = set()
        self.__page_display_strings = {}
        self.__body_page_num = 1

    def clear(self):
        self.__do_not_display_as_double = set()
        self.__page_display_strings = {}
        self.__body_page_num = 1

    def add_not_double_page(self, page_num: int):
        self.__do_not_display_as_double.add(page_num)

    def can_display_as_double_page(self, page_num: int):
        return page_num not in self.__do_not_display_as_double

    def set_body_page_num(self, page_num: int):
        self.__body_page_num = page_num
        if self.__body_page_num == 1:
            return
        for front_page_num in range(1, self.__body_page_num):
            self.__page_display_strings[front_page_num] = ROMAN_NUMERALS[front_page_num]

    def get_page_display_str(self, page_num: int) -> str:
        if page_num >= self.__body_page_num:
            return str(page_num - self.__body_page_num + 1)
        return self.__page_display_strings[page_num]


def get_previous_first_page_of_double_page_run(page_data: PageData, page_num: int) -> int:
    if not page_data.can_display_as_double_page(page_num):
        return -1

    pg = page_num
    while pg >= 1:
        if not page_data.can_display_as_double_page(pg):
            return pg + 1
        pg -= 1

    return 0


def is_page_second_part_of_double(page_data: PageData, page_num: int) -> bool:
    first_of_double_run = get_previous_first_page_of_double_page_run(page_data, page_num)
    if first_of_double_run <= 0:
        return False
    is_first_odd = first_of_double_run % 2 != 0
    if is_first_odd:
        return page_num % 2 == 0
    return page_num % 2 != 0


class Metadata(object):
    def __init__(self):
        self.__page_data = PageData()

    @property
    def page_data(self):
        return self.__page_data

    def clear(self):
        self.__page_data.clear()

    def load(self, filename: str):
        log.debug(f'Reading metadata from "{filename}".')
        config = configparser.ConfigParser()
        config.read(filename)
        self.load_page_data(config)

    def load_page_data(self, config: configparser.ConfigParser):
        self.__page_data.clear()

        for key in config[DOUBLE_PAGES_SECTION]:
            if not config[DOUBLE_PAGES_SECTION].getboolean(key):
                log.debug(f'Do not display as double page: {int(key)}.')
                self.__page_data.add_not_double_page(int(key))

        self.__page_data.set_body_page_num(config[PAGE_NUMBERS_SECTION].getint('body_start', 1))
