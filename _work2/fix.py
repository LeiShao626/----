# -*- coding: utf-8 -*-
import re, io
path = r"D:\论文\_work2\build_docx2.py"
with io.open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

out = []
i = 0
n = len(lines)
while i < n:
    line = lines[i]
    # Detect a variable assignment that starts a parenthesized string block
    m = re.match(r'^(\s*)([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\(', line)
    if m:
        indent = m.group(1)
        var = m.group(2)
        # Gather the full parenthesized block (handle nested parens minimally)
        # We scan until the block closes (the line with ')') 
        block_lines = [line]
        j = i
        # Count parentheses balance from start
        depth = 0
        # start scanning from the block
        # We'll detect the closing by looking for the line where the parens balance returns to the assignment depth
        # Simpler: collect lines until we find a line that ends with ')' and the paren count balances
        # Reconstruct the source of the block text
        src = ""
        k = i
        cnt = 0
        while k < n:
            src += lines[k]
            cnt += lines[k].count("(") - lines[k].count(")")
            block_lines.append(lines[k])
            if cnt > 0 and lines[k].rstrip().endswith(")"):
                # check balance consumed
                pass
            # if cnt == 0 we've closed
            if cnt == 0:
                break
            k += 1
        # Now src is the full assignment including closing paren.
        # Find the comma-splice: search for '", size=' or '",\n' followed by 'size='
        # We want to split so the string part is a plain string and the rest becomes add_para(var, ...)
        # Strategy: find the last occurrence of a comma that separates the string content from kwargs.
        # The matching close paren is the final ')'. Remove it, split on the comma that begins 'size='.
        # Locate index where kwargs begin: search for ', size=' OR a comma immediately before 'size='
        m2 = re.search(r',\s*size=', src)
        if m2:
            head = src[:m2.start()]   # includes the string literal(s) and opening paren
            tail = src[m2.start()+1:] # includes ' size=...' WITHOUT the comma
            # head is like:   var = ("....\n...",  (no closing paren)
            # tail is like:    size=..., align=..., space_after=6)\n
            tail = tail.rstrip()
            if tail.endswith(")"):
                tail = tail[:-1]  # remove the closing paren
            tail = tail.rstrip()
            # Now build:
            #   var = ("....\n...")     -- but head includes 'var = (' and the string, need closing paren
            if ',' in head:
                # there's a comma separating trailing string; head may end with '",' or '",' on a line
                head = head.rstrip()
                if head.endswith('",'):
                    head = head[:-1] + '")'   # close string + paren
                elif head.endswith('"'):
                    head = head + ')'         # close paren (no trailing comma)
                else:
                    # head ends possibly with '",' already handled; else append ) 
                    head = head.rstrip() + ')'
            else:
                head = head.rstrip() + ')'
            # The var assignment line
            out.append(indent + var + ' = ' + ''.join(head.split('\n',1)[1:] if False else []) if False else head + "\n")
            # Actually head already contains 'var = (...' ; ensure it's a proper assignment
            # Ensure head starts with 'var = (' 
            head = head.lstrip()
            out[-1] = head + "\n"
            # add_para call
            out.append(indent + "add_para(%s, %s)\n" % (var, tail))
            # advance i past the block
            i = k + 1
            continue
    out.append(line)
    i += 1

with io.open(path, "w", encoding="utf-8") as f:
    f.writelines(out)
print("processed", n, "lines")
