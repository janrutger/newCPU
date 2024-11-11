
. $pre 1
. $nxt 1
. $cf 1

@program
    call @fly
    halt

@fly
   ldb 0
   lda 1
   add 
   out 2
   out 2
   sto $pre
   
   ldb 2
   stb $nxt

@loop
    ldb 700
    lma $nxt 
    test eq
    jmpt @done

    lma $pre
    lmb $nxt
    call @gcd
    sto $cf


    lma $cf
    ldb 1
    test eq
    jmpf @cf

    lma $pre
    lmb $nxt
    add
    ; push
    ; pop
    ldb 1
    add
    jmp @next

@cf
    lmb $cf
    lma $pre
    div


@next
    sto $pre
    out 2
    lma $nxt
    ldb 1
    add
    sto $nxt

jmp @loop

@done

ret

