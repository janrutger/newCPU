. $a1 1
. $a2 1
. $dividend 1
;. $divisor 1
;. $quotient 1
. $seed 1

@init
    lda 5896
    sta $seed
ret

@swopab
    sta $a1
    stb $a2
    lma $a2
    lmb $a1
ret

@cpar
    stb $a1
    ldb 0
    sub
    lmb $a1 
ret

@rnd
    lda 75
    lmb $seed
    mul
    ; push
    ; pop
    ldb 74
    add
    ; push 
    ; pop
    ldb 65536
    call @mod
    sto $seed
    ; push
    ; pop
    ldb 655
    div
    ;out 2
ret

@mod
    sta $dividend
    ;stb $divisor
    div
    ; push
    ; pop
    mul
    ; push
    ; pop
    call @swopab
    lma $dividend
    sub
ret

@gcd
    test z
    jmpt :done_gcd
    call @swopab
    test z
    jmpt :done_gcd
;:loop_gcd
    test gt
    jmpt :sub_gcd
    call @swopab
:sub_gcd
    sub
    ; push
    ; pop
    test eq
    ;jmpf :loop_gcd
    jmp @gcd
    ldb 0
:done_gcd
    add
ret


