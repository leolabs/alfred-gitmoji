#!/usr/bin/python
# encoding: utf-8

import sys, os

from workflow import Workflow3, web

gitmoji_db = 'https://raw.githubusercontent.com/carloscuesta/gitmoji/master/src/data/gitmojis.json'
emojione_assets = 'https://raw.githubusercontent.com/emojione/emojione-assets/master/png/128'

def get_gitmoji_db():
    return web.get(gitmoji_db).json()


def main(wf):
    data = wf.cached_data('gitmoji_db', get_gitmoji_db, max_age=86400)

    for emoji in data['gitmojis']:
        unicode = emoji['emoji']
        str = unicode.encode('unicode-escape')
        if str.startswith('\U000'):
            id  = str[5:]
        elif str.startswith('\u'):
            id = str.split('\u')[1]
        icon = wf.datafile(id + '.png')
        if not os.path.isfile(icon):
            request = web.get(emojione_assets + '/' + id + '.png')
            request.save_to_path(icon)

        wf.add_item(
            title=emoji['emoji'] + ' ' + emoji['code'],
            subtitle=emoji['description'],
            valid=True,
            icon=icon,
            match=emoji['name'] + ' ' + emoji['description'],
            arg=emoji['code'],
            copytext=emoji['code'],
            largetext=emoji['code']
        )

    wf.send_feedback()


if __name__ == '__main__':
    wf3 = Workflow3()
    sys.exit(wf3.run(main))
