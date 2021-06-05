#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import annotations
import re
import panflute as pf


def get_label(label: str) -> str:
    label = label.replace('[', '').replace(']', '').replace('@', '')
    if ':' in label:
        reftype = label.split(':')[0]
        if reftype == 'sec' or reftype == 'section':
            refcommand = 'jsecref'
        elif reftype == 'eq' or reftype == 'equation':
            refcommand = 'jeqref'
        elif reftype == 'fig' or reftype == 'figure':
            refcommand = 'jfigref'
        elif reftype == 'tbl' or reftype == 'table':
            refcommand = 'jtblref'
        elif reftype == 'theo' or reftype == 'theorem':
            refcommand = 'jtheoref'
        elif reftype == 'def' or reftype == 'definition':
            refcommand = 'jdefref'
        elif reftype == 'exam' or reftype == 'example':
            refcommand = 'jexamref'
        else:
            refcommand = 'ref'
    else:
        refcommand = 'cite'
    return r'\%s{%s}' % (refcommand, label)


class PandocContents():
    def __init__(self: PandocContents, text: str) -> None:
        self.contents = ''
        self.id = None
        self.classes = list()
        self.keyvals = dict()
        attr_pattern = re.compile(r'{(.+?)}')
        attrs = (' '.join(attr_pattern.findall(text))).split(' ')
        for att in attrs:
            if att.startswith('#'):
                self.id = att[1:]
            elif att.startswith('.'):
                self.classes.append(att[1:])
            elif '=' in att:
                keyvals = att.split("=")
                self.keyvals[keyvals[0]] = keyvals[1]
        ref_pattern = re.compile(r'[@(.+?)]')
        for c in re.split(r'\s+', attr_pattern.sub('', text).strip()):
            if len(c) == 0:
                pass
            if len(self.contents) > 0:
                self.contents += ' '
            start = 0
            end = len(c)
            while start < end:
                tref = ref_pattern.search(c, start, end)
                if tref is None:
                    self.contents += c[start:end]
                    start = end
                else:
                    if tref.start() > start:
                        self.contents += c[start:tref.start()]
                    label = ref_pattern.split(
                        c[tref.start():tref.end()]
                    )[1]
                    self.contents += get_label(label)
                    start = tref.end()
        return

    def get_string_with_label(self) -> str:
        contents = self.contents[:]
        if self.id is not None:
            contents += r' \label{%s}' % self.id
        if len(contents) == 0:
            return ''
        return contents

    def get_caption_with_label(self) -> pf.Caption:
        ret = list()
        ret.append(pf.Str(self.contents))
        if self.id is not None:
            ret.append(pf.Space())
            ret.append(pf.RawInline(
                r'\label{%s}' % self.id, format='latex'
            ))
        return pf.Caption(pf.Para(*ret))


def action(elem, doc):
    if isinstance(elem, pf.Caption):
        caption = elem.content.to_json()[0]['c'][0]['c']
        if len(caption) == 0:
            return
        return PandocContents(
            caption
        ).get_caption_with_label()
    elif isinstance(elem, pf.Math):
        attr = re.compile(r'{#(.+?)}')
        if attr.search(elem.text) is None:
            return
        labels = attr.findall(elem.text)
        mathcode = elem.text
        for label in labels:
            ml = r'\\label{%s}' % label
            mathcode = attr.sub(ml, mathcode, count=1)
        return pf.Math(text=mathcode, format=elem.format)
    elif isinstance(elem, pf.Cite):
        label = get_label(
            ''.join([pf.stringify(x) for x in elem.content.list])
        )
        return [pf.RawInline(label, format='latex')]


def main(doc=None) -> None:
    pf.run_filter(action=action, doc=doc)
    return


if __name__ == "__main__":
    main()
