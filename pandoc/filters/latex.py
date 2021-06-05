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
            ret.append(pf.Para(inlatex(r"\end{%s}" % is_in_block)))
            is_in_block = None
        if elem.level == 3:
            blocktype = ''
            blocktitle = ''
            for cname in elem.classes:
                if cname in [
                    'block', 'alertblock', 'exampleblock',
                    'theorem', 'example', 'definition', 'proof'
                ]:
                    blocktype = cname
                    blocktitle = ''.join([
                        pf.stringify(x) for x in elem.content.list
                    ])
            if blocktype != '':
                is_in_block = blocktype
                latexstr = r'\begin{%s}' % blocktype
                if blocktitle != '':
                    latexstr += '[%s]' % blocktitle
                if ':' in elem.identifier:
                    latexstr += r' \label{%s}' % elem.identifier
                ret.append(pf.Para(inlatex(latexstr)))
            else:
                ret.append(elem)
        else:
            if len(ret) == 0:
                return
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
            ret.append(pf.Para(inlatex(r'\begin{codeblock}[%s]' % caption)))
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
        new_content = r'\begin{%s} ' % math_environ
        new_content += math_content
        new_content += r'\end{%s}' % math_environ
        return pf.RawInline(new_content, format='latex')
    return


def main(doc=None):
    pf.run_filter(action=action, doc=doc)
    return


if __name__ == "__main__":
    main()
