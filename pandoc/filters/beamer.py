#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import panflute as pf

is_in_block = None


def inlatex(text: str) -> pf.RawInline:
    return pf.RawInline(text=text, format='latex')


def action(elem, doc):
    global is_in_block
    if isinstance(elem, pf.Header):
        ret = list()
        if is_in_block is not None:
            ret.append(pf.Para(inlatex(r'\end{%s}' % is_in_block)))
            is_in_block = None
        if elem.level == 1:
            content = list()
            content.append(inlatex(r'\begin{center}{\large '))
            for x in elem.content.list:
                content.append(x)
            content.append(inlatex(r' }\end{center}'))
            attributes = {'label': 'noheader'}
            ret.append(elem)
            ret.append(pf.Header(level=2, attributes=attributes))
            if ':' in elem.identifier:
                ret.append(pf.Para(
                    inlatex(r'\label{%s}' % elem.identifier)
                ))
            ret.append(pf.Para(*content))
        elif elem.level == 2:
            elem.attributes['label'] = 'header'
            ret.append(elem)
            if ':' in elem.identifier:
                ret.append(pf.Para(
                    inlatex(r'\label{%s}' % elem.identifier)
                ))
        elif elem.level == 3:
            blocktype = ''
            blocktitle = ''
            for cname in elem.classes:
                if cname in [
                    'alertblock', 'exampleblock',
                    'theorem', 'example', 'definition', 'proof'
                ]:
                    blocktype = cname
            blocktitle = ''.join([
                pf.stringify(x) for x in elem.content.list
            ])
            if blocktype == '':
                blocktype = 'labeledblock'
            elif blocktype == 'alertblock':
                blocktype = 'labeledalertblock'
            elif blocktype == 'exampleblock':
                blocktype = 'labeledexampleblock'
            elif blocktype == 'proof':
                blocktype = 'labeledproof'
            is_in_block = blocktype
            latexstr = r'\begin{%s}[%s]' % (blocktype, blocktitle)
            if ':' in elem.identifier:
                latexstr += r" \label{%s}" % elem.identifier
            ret.append(pf.Para(inlatex(latexstr)))
        else:
            ret.append(elem)
        return ret
    elif isinstance(elem, pf.CodeBlock):
        ret = list()
        if is_in_block is not None:
            ret.append(pf.Para(inlatex(r'\end{%s}' % is_in_block)))
            is_in_block = None
        caption = elem.attributes.get('caption')
        if caption is None:
            ret.append(pf.Para(inlatex(r'\begin{codeblock}')))
        else:
            ret.append(pf.Para(inlatex(r'\begin{codeblock}{%s}' % caption)))
        ret.append(elem)
        ret.append(pf.Para(inlatex(r'\end{codeblock}')))
        return ret
    elif isinstance(elem, pf.RawBlock):
        if elem.text.startswith('<!--') and is_in_block is not None:
            ret = list()
            ret.append(pf.Para(inlatex(r'\end{%s}' % is_in_block)))
            ret.append(elem)
            is_in_block = None
            return ret
    elif isinstance(elem, pf.Math):
        if elem.format == 'InlineMath':
            return
        ret = list()
        math_content = elem.text
        if '&' in math_content or r'\\' in math_content:
            math_environ = 'align'
        else:
            math_environ = 'equation'
        new_content = r'\begin{%s}' % math_environ
        new_content += math_content
        new_content += r'\end{%s}' % math_environ
        return pf.RawInline(new_content, format='latex')
    elif isinstance(elem, pf.Image):
        return [
            pf.RawInline(r'\begin{center}', format='latex'),
            elem,
            pf.RawInline(r'\end{center}', format='latex'),
        ]
    return


def main(doc=None):
    pf.run_filter(action=action, doc=doc)
    return


if __name__ == "__main__":
    main()
