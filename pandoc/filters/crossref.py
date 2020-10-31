#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import re
import panflute as pf


def inlatex(s):
    return pf.RawInline('latex', s)


def get_label(label):
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
    return(inlatex(r"\%s{%s}" % (refcommand, label)))


class PandocContents():
    def __init__(self, text):
        self.contents = list()
        self.id = None
        self.classes = list()
        self.keyvals = dict()
        attr = re.compile(r'{(.+?)}')
        attrs = ' '.join(attr.findall(text)).split(' ')
        for att in attrs:
            if att.startswith('#'):
                self.id = att[1:]
            elif att.startswith('.'):
                self.classes.append(att[1:])
            elif '=' in att:
                keyvals = att.split("=")
                self.keyvals[keyvals[0]] = keyvals[1]
        ref = re.compile(r'[@(.+?)]')
        for c in re.split(r's+', attr.sub('', str).strip()):
            if len(c) == 0:
                pass
            if len(self.contents) > 0:
                self.contents.append(pf.Space())
            start = 0
            end = len(c)
            while start < end:
                tref = ref.search(c, start, end)
                if tref is None:
                    self.contents.append(pf.Str(c[start:end]))
                    start = end
                else:
                    if tref.start() > start:
                        self.contents.append(pf.Str(c[start:tref.start()]))
                    label = ref.split(c[tref.start():tref.end()])[1]
                    self.contents.append(get_label(label))
                    start = tref.end()
        return

    def get_contents_with_label(self):
        contents = self.contents[:]
        if self.id is not None:
            contents.append(inlatex(r"\label{%s}" % self.id))
        if len(contents) == 0:
            return []
        return contents


def action(elem, doc):
    if isinstance(elem, pf.Table):
        if len(elem.caption) == 0:
            return
        caption = PandocContents(pf.stringify(elem.caption))
        return [pf.Table(
            caption.get_contents_with_label(),
            elem.alignment, elem.data, elem.header, elem.rows
        )]
    elif isinstance(elem, pf.Math):
        if elem.value[0]["t"] == 'DisplayMath':
            [mathtype, mathcode] = elem.value
        attr = re.compile(r'{#(.+?)}')
        if attr.search(mathcode) is None:
            return
        labels = attr.findall(mathcode)
        for label in labels:
            ml = r"\\\\label{%s}" % label
            mathcode = attr.sub(ml, mathcode, count=1)
        return [pf.Math(mathtype, mathcode)]
    elif isinstance(elem, pf.Cite):
        ret = list()
        [citeinfo, contents] = elem.value
        for ci in citeinfo:
            label = ci['citationId']
            ret.append(get_label(label))
        if len(ret) > 0:
            return ret
        return


def main(doc=None) -> None:
    pf.run_filter(action=action, doc=doc)
    return


if __name__ == "__main__":
    main()
