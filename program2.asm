@program
    call @init
    call @kernel_init
    call @read_input
halt

. $t1 1
. $t2 1
. $dst 8
. $cds 1
. $str_in 8
. $_plus 2
. $_gcd 4 

@kernel
    @kernel_init
; set datastack counter
        ldb 0
        stb $cds
;def "+" string
        ldb 0
        idx
        lda 6
        add
        stx $_plus

        inc x
        lda 0
        add
        stx $_plus
;def "gcd" string
        ldb 0
        idx
        lda 36
        add
        stx $_gcd
        inc x
        lda 32
        add
        stx $_gcd
        inc x
        lda 33
        add
        stx $_gcd
        
        inc x
        lda 0
        add
        stx $_gcd          
    ret

    @read_input
        in 1
        ;ldb 1
        ;test eq
        ;jmpf :read_int 
        test z
        ; what if the input is an digit
        jmpt :read_int
        ; What if the input is an string
        ; get the char
        in 1
        ; check for end-off char
        ldb 0
        test eq
        jmpt :end_read_input

        ; check for sepreator " "
        ldb 20
        test eq
        jmpt @read_input

        ldb 0
        idx
        ; first char
        ldb 0
        add
        stx $str_in

        :next_char
            in 1
            in 1
            ;ldb 0
            ;test eq
            test z
            jmpt :done_read_char
            ldb 20
            test eq
            jmpt :read_seperator

            inc x
            ldb 0
            add
            stx $str_in
            jmp :next_char

        :read_seperator
            ; write null to str_in as end char
            inc x
            stx $str_in
            call @cmp_string_input
            call @do_instuction
            jmp @read_input
        
        :done_read_char
            ; write null to str_in as end char
            inc x
            stx $str_in
            call @cmp_string_input
            call @do_instuction
            jmp :end_read_input


        :read_int
            ; first digit
            in 1
            ldb 10
            sub
            sto $t1

            ;check for next
        :next_digit
            in 1
            ;ldb 1
            ;test eq
            test z
            jmpf :done_read_int
                lma $t1
                ldb 10
                mul
                sto $t1
                in 1
                ldb 10
                sub
                lmb $t1
                add
                sto $t1
            jmp :next_digit


        :done_read_int
            lma $t1
            ldb 0
            sub
            call @dst_push
            in 1
            ; check fo seperator " "
            ldb 20
            test eq
            jmpt @read_input

    :end_read_input
    ret

    @dst_push
        lmb $cds 
        idx
        stx $dst
        inc b
        stb $cds
    ret

    @dst_pop
        stb $t2
        lmb $cds
        dec b
        idx
        lxa $dst
        ;dec b
        stb $cds
        lmb $t2
    ret

    @cmp_string_input
        ; compare with "+"
        ldb 0
        idx
        :loop_cmp_str_+
            lxa $str_in
            lxb $_plus
            test eq
            jmpf :cmp_next_gcd
            test z
            inc x
            jmpf :loop_cmp_str_+
            ; return 1 if str is "+"
            lda 1
            ldb 0
            add
            jmp :str_cmp_done
        
        ; compare with "gcd"
        :cmp_next_gcd
        ldb 0
        idx
        :loop_cmp_str_gcd
            lxa $str_in
            lxb $_gcd
            test eq
            jmpf :str_not_eq
            test z
            inc x
            jmpf :loop_cmp_str_gcd
            ; return 2 if str is "gcd"
            lda 2
            ldb 0
            add
            jmp :str_cmp_done


    
        :str_not_eq
            lda 0
            ldb 0 
            add
    :str_cmp_done
    ret

    @do_instuction
        ldb 1
        test eq
        skip 
        jmp :_plus

        ldb 2
        test eq
        skip
        jmp :_gcd
        jmp :end_instuction

    :_plus
        call @dst_pop
        call @swopab
        call @dst_pop
        add
        call @dst_push
        ;halt
    jmp :end_instuction

    :_gcd    

    :end_instuction
    ret



