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
        if level == 3:
            blocktype = ''
            blocktitle = ''
            for cname in class_names:
                if cname in [
                    'block', 'alertblock', 'exampleblock',
                    'theorem', 'example', 'definition', 'proof'
                ]:
                    blocktype = cname
                    blocktitle = pf.stringify(contents_list)
            if blocktype != '':
                is_in_block = blocktype
                latexstr = r"\begin{%s}" % blocktype
                if blocktitle != '':
                    latexstr += "[%s]" % blocktitle
                if label != '':
                    latexstr += r" \label{%s}" % label
                ret.append(pf.Para([inlatex(latexstr)]))
            else:
                ret.append(pf.Header(3, classes, contents_list))
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
            ret.append(pf.Para([inlatex(r"\begin{codeblock}[%s]" % caption)]))
        ret.append(pf.CodeBlock(classes, contents_list))
        ret.append(pf.Para([inlatex(r"\end{codeblock}")]))
        return ret
    elif isinstance(elem, pf.RawBlock):
        [rawtype, contents] = elem.value
        if contents.startswith('<!--') and is_in_block is not None:
            ret = list()
            ret.append(pf.Para([inlatex("\\end{%s}" % is_in_block)]))
            ret.append(pf.RawBlock(rawtype, contents))
            is_in_block = None
            return ret
    elif isinstance(elem, pf.Para):
        ret = list()
        normal_contents = list()
        for c in elem.value:
            if c["t"] == 'Math' and c["c"][0]["t"] == 'DisplayMath':
                math_content = c["c"][1]
                if '&' in math_content or '\\\\' in math_content:
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
                new_content = "\\begin{%s}" % math_environ
                new_content += math_content
                new_content += "\\end{%s}" % math_environ
                ret.append(pf.RawBlock("latex", new_content))
            elif c["t"] == 'SoftBreak' and len(normal_contents) == 0:
                pass
            else:
                normal_contents.append(c)
        if len(normal_contents) > 0:
            ret.append(pf.Para(normal_contents))
        return ret


def main(doc=None):
    pf.run_filter(action=action, doc=doc)
    return


if __name__ == "__main__":
    main()
