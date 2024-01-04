function raw_tex(t)
    return pandoc.RawBlock('tex', t)
end

function CodeBlock(cb)
    if cb.classes[1] == "mermaid" or cb.classes[1] == "unboxed" then
        return cb
    end
    return {raw_tex '\\begin{tcolorbox}[breakable]', cb, raw_tex '\\end{tcolorbox}\\vspace{0.5em}'}
end

function Meta(m)
    m['header-includes'] = {raw_tex [[\usepackage[most]{tcolorbox}
        \tcbset{enhanced jigsaw}
        \usepackage{fvextra}
        \DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaklines,commandchars=\\\{\}}]]}
    return m
end
