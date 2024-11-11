
. $array 5
. $nxt 1

@program
    call @init

    ldb 0
    stb $nxt
    idx

    :loop
        lda 5
        lmb $nxt
        test eq
        jmpt :done
            call @rnd
            ;out 2
            stx $array

            lmb $nxt
            inc b
            stb $nxt
            idx
        jmp :loop
    :done
halt



