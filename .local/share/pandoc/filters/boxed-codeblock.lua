function raw_tex(t)
    return pandoc.RawBlock('tex', t)
end

function CodeBlock(cb)
    return {raw_tex '\\begin{tcolorbox}[breakable]', cb, raw_tex '\\end{tcolorbox}'}
end

function Meta(m)
    m['header-includes'] = {raw_tex [[\usepackage[most]{tcolorbox}
        \tcbset{enhanced jigsaw}]]}
    return m
end
