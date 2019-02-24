#!/usr/bin/python
# encoding: utf-8

import sys, os

from workflow import Workflow3, web

gitmoji_db = 'https://raw.githubusercontent.com/carloscuesta/gitmoji/master/src/data/gitmojis.json'
emojione_assets = 'https://raw.githubusercontent.com/emojione/emojione-assets/master/png/128'

def get_gitmoji_db():
    return web.get(gitmoji_db).json()

def determine_icon_name(emoji):
    esc_seqs = ['\\U000', '\\u']
    ascii_char = emoji.encode('unicode-escape')
    codes = ascii_char
    for x in esc_seqs:
        codes = codes.replace(x, " ")
    return codes.split()[0] + ".png"

def fetch_icon(wf, emoji):
    filename = determine_icon_name(emoji)
    icon = wf.datafile(filename)
    if not os.path.isfile(icon):
        request = web.get(emojione_assets + '/' + filename)
        request.save_to_path(icon)
    return icon

def main(wf):
    data = wf.cached_data('gitmoji_db', get_gitmoji_db, max_age=86400)

    for emoji in data['gitmojis']:
        wf.add_item(
            title=emoji['emoji'] + ' ' + emoji['code'],
            subtitle=emoji['description'],
            valid=True,
            icon=fetch_icon(wf, emoji['emoji']),
            match=emoji['name'] + ' ' + emoji['description'],
            arg=emoji['code'],
            copytext=emoji['code'],
            largetext=emoji['code']
        )

    wf.send_feedback()


if __name__ == '__main__':
    wf3 = Workflow3()
    sys.exit(wf3.run(main))
