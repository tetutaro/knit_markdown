#!/usr/bin/env python
# -*- coding:utf-8 -*-
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


def action(elem, doc):
    if isinstance(elem, pf.Caption):
        raw_caption = ''.join([
            pf.stringify(x) for x in elem.content.list
        ])
        if len(raw_caption) == 0:
            return
        tbl_pat = re.compile(r'{#((tbl|table):([0-9a-zA-Z]+?))}')
        labels = tbl_pat.findall(raw_caption)
        if len(labels) == 0:
            return
        caption = tbl_pat.sub('', raw_caption).strip()
        ret = list()
        ret.append(pf.Str(caption))
        for label in labels:
            ret.append(pf.RawInline(r'\label{%s}' % label[0], format='latex'))
        return pf.Caption(pf.Para(*ret))
    elif isinstance(elem, pf.Math):
        mathcode = elem.text
        eq_pat = re.compile(r'({#((eq|equation):([0-9a-zA-Z]+?))})')
        labels = eq_pat.findall(mathcode)
        if len(labels) == 0:
            return
        for label in labels:
            lb = r'\\label{%s}' % label[1]
            mathcode = re.sub(label[0], lb, mathcode)
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
