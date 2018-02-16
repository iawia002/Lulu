# coding=utf-8

from html import unescape

from lulu.util.fs import legitimize


def get_filename(htmlstring):
    return legitimize(unescape(htmlstring))


def parameterize(string):
    return "'{}'".format(string.replace("'", r"'\''"))
