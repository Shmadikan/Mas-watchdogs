from plantweb.render import render_file
CONTENT = """
digraph finite_state_machine {
    rankdir=LR;
    size="8,5"
    node [shape = doublecircle]; LR_0 LR_3 LR_4 LR_8;
    node [shape = circle];
    LR_0 -> LR_2 [ label = "SS(B)" ];
    LR_0 -> LR_1 [ label = "SS(S)" ];
    LR_1 -> LR_3 [ label = "S($end)" ];
    LR_2 -> LR_6 [ label = "SS(b)" ];
    LR_2 -> LR_5 [ label = "SS(a)" ];
    LR_2 -> LR_4 [ label = "S(A)" ];
    LR_5 -> LR_7 [ label = "S(b)" ];
    LR_5 -> LR_5 [ label = "S(a)" ];
    LR_6 -> LR_6 [ label = "S(b)" ];
    LR_6 -> LR_5 [ label = "S(a)" ];
    LR_7 -> LR_8 [ label = "S(b)" ];
    LR_7 -> LR_5 [ label = "S(a)" ];
    LR_8 -> LR_6 [ label = "S(b)" ];
    LR_8 -> LR_5 [ label = "S(a)" ];
}
"""


if __name__ == '__main__':

    infile = 'mygraph.dot'
    with open(infile, 'wb') as fd:
        fd.write(CONTENT.encode('utf-8'))

    print('==> INPUT FILE:')
    print(infile)

    outfile = render_file(
        infile,
        renderopts={
            'engine': 'graphviz',
            'format': 'png'
        },
        cacheopts={
            'use_cache': False
        }
    )

    print('==> OUTPUT FILE:')
    print(outfile)