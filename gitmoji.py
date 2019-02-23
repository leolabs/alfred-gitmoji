#!/usr/bin/python
# encoding: utf-8

import sys, os

from workflow import Workflow3, web

gitmoji_db = 'https://raw.githubusercontent.com/carloscuesta/gitmoji/master/src/data/gitmojis.json'
emojione_assets = 'https://raw.githubusercontent.com/emojione/emojione-assets/master/png/128'
esc_seqs = {'\\U000': ' ', '\\u': ' '}

def get_gitmoji_db():
    return web.get(gitmoji_db).json()


def main(wf):
    data = wf.cached_data('gitmoji_db', get_gitmoji_db, max_age=86400)

    for emoji in data['gitmojis']:
        unicode_emoji = emoji['emoji']
        ascii_emoji = unicode_emoji.encode('unicode-escape')
        for r,s in esc_seqs.items():
            ascii_emoji = ascii_emoji.replace(r,s)
        codes = ascii_emoji.split()
        filename = codes[0]
        icon = wf.datafile(filename + '.png')
        if not os.path.isfile(icon):
            request = web.get(emojione_assets + '/' + filename + '.png')
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
