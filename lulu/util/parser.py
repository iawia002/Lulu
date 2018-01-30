# coding=utf-8

from bs4 import BeautifulSoup


def get_parser(page):
    parser = BeautifulSoup(page, 'html.parser')
    return parser
