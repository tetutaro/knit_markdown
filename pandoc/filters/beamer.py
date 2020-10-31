#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import panflute as pf

is_in_block = None


def inlatex(s):
    return pf.RawInline('latex', s)


def action(elem, doc):
    global is_in_block
    if isinstance(elem, pf.Header):
        ret = list()
        if is_in_block is not None:
            ret.append(pf.Para([inlatex(r"\end{%s}" % is_in_block)]))
            is_in_block = None
            [level, classes, contents_list] = elem.value
            [label, class_names, class_options] = classes
            if elem.level == 1:
                new_class_options = class_options[:]
                new_class_options.append(['label', 'noheader'])
                new_classes = [label, class_names, new_class_options]
                new_contents_list = [
                    inlatex(r"\begin{center}{\large ")
                ] + contents_list + [
                    inlatex(r" }\end{center}")
                ]
                ret.append(pf.Header(1, classes, contents_list))
                ret.append(pf.Header(2, new_classes, []))
                ret.append(pf.Para([inlatex(r"\label{%s}" % label)]))
                ret.append(pf.Para(new_contents_list))
            elif elem.level == 2:
                new_class_options = class_options[:]
                new_class_options.append(['label', 'header'])
                new_classes = [label, class_names, new_class_options]
                ret.append(pf.Header(2, new_classes, contents_list))
                ret.append(pf.Para([inlatex(r"\label{%s}" % label)]))
            elif elem.level == 3:
                blocktype = ''
                blocktitle = pf.stringify(contents_list)
                for cname in class_names:
                    if cname in [
                        'alertblock', 'exampleblock',
                        'theorem', 'example', 'definition', 'proof'
                    ]:
                        blocktype = cname
                    if blocktype == '':
                        blocktype = 'labeledblock'
                    elif blocktype == 'alertblock':
                        blocktype = 'labeledalertblock'
                    elif blocktype == 'exampleblock':
                        blocktype = 'labeledexampleblock'
                    elif blocktype == 'proof':
                        blocktype = 'labeledproof'
                    is_in_block = blocktype
                    latexstr = r"\begin{%s}[%s]" % (blocktype, blocktitle)
                    if label != '':
                        latexstr += r" \label{%s}" % label
                    ret.append(pf.Para([inlatex(latexstr)]))
            else:
                ret.append(pf.Header(level, classes, contents_list))
            return ret
        elif isinstance(elem, pf.CodeBlock):
            ret = list()
            if is_in_block is not None:
                ret.append(pf.Para([inlatex(r"\end{%s}" % is_in_block)]))
                is_in_block = None
                [classes, contents_list] = elem.value
                [label, class_names, class_options] = classes
                caption, _, _ = pf.get_caption(class_options)
                caption = pf.stringify(caption)
                if caption == '':
                    ret.append(pf.Para([inlatex(r"\begin{codeblock}")]))
                else:
                    ret.append(pf.Para([
                        inlatex(r"\begin{codeblock}{%s}" % caption)
                    ]))
                if label != '':
                    ret.append(pf.Para([inlatex(r" \label{%s}" % label)]))
            ret.append(pf.CodeBlock(classes, contents_list))
            ret.append(pf.Para([inlatex(r"\end{codeblock}")]))
            return ret
        elif isinstance(elem, pf.RawBlock):
            [rawtype, contents] = elem.value
            if contents.startswith('<!--') and is_in_block is not None:
                ret = list()
                ret.append(pf.Para([inlatex(r"\end{%s}" % is_in_block)]))
                ret.append(pf.RawBlock(rawtype, contents))
                is_in_block = None
                return ret
        elif isinstance(elem, pf.Para):
            ret = list()
            normal_contents = list()
            for c in elem.value:
                if c["t"] == 'Math' and c["c"][0]["t"] == 'DisplayMath':
                    math_content = c["c"][1]
                    if '&' in math_content or r'\\' in math_content:
                        math_environ = 'align'
                    else:
                        math_environ = 'equation'
                    if len(normal_contents) > 0 and (
                        normal_contents[-1]["t"] == 'SoftBreak'
                    ):
                        normal_contents.pop()
                    if len(normal_contents) > 0:
                        ret.append(pf.Para(normal_contents))
                        normal_contents = list()
                    new_content = r"\begin{%s}" % math_environ
                    new_content += math_content
                    new_content += r"\end{%s}" % math_environ
                    ret.append(pf.RawBlock("latex", new_content))
                elif c["t"] == 'SoftBreak' and len(normal_contents) == 0:
                    pass
                else:
                    normal_contents.append(c)
            if len(normal_contents) > 0:
                ret.append(pf.Para(normal_contents))
                return ret
    return


def main(doc=None):
    pf.run_filter(action=action, doc=doc)


if __name__ == "__main__":
    main()
