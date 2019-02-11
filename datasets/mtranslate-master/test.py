#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mtranslate import translate


def main():
    to_translate = 'Bonjour comment allez vous?'
    print(translate(to_translate))
    print(translate(to_translate, 'ar'))
    print(translate(to_translate, 'ru'))
    print(translate(to_translate, 'ko'))

if __name__ == '__main__':
    main()
