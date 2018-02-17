#!/usr/bin/python
# encoding: utf-8

import sys

from workflow import Workflow3, web

gitmoji_db = 'https://raw.githubusercontent.com/carloscuesta/gitmoji/master/src/data/gitmojis.json'


def get_gitmoji_db():
    return web.get(gitmoji_db).json()


def main(wf):
    data = wf.cached_data('gitmoji_db', get_gitmoji_db, max_age=86400)

    for emoji in data['gitmojis']:
        wf.add_item(
            title=emoji['emoji'] + ' ' + emoji['code'],
            subtitle=emoji['description'],
            valid=True,
            icon='9B7FE8AC-6582-4825-917E-92D0E0291CC1.png',
            match=emoji['name'] + ' ' + emoji['description'],
            arg=emoji['code'],
            copytext=emoji['code'],
            largetext=emoji['code']
        )

    wf.send_feedback()


if __name__ == '__main__':
    wf3 = Workflow3()
    sys.exit(wf3.run(main))
