@program
    call @init
    call @kernel_init
    call @read_input
halt

. $t1 1
. $t2 1
. $zero 1
. $dst 8
. $cds 1
. $str_in 8

. $_stub 2
. $_plus 2
. $_gcd 4 

% $_stub #
% $_gcd gcd
% $_plus +

. $str_lut 3
. $adr_lut 3
. $lut_i 1
. $lut_len 1

@kernel
    @kernel_init
        ldb 0
        ; set datastack counter
        stb $cds  
        ; set zero
        stb $zero 
        ; set Lookup Index to zero
        stb $lut_i  
        ldb 3
        stb $lut_len
    ; setup lookup table
    ; stub at 0
        ; iix $lut_i
        ; lda $_stub
        ; call @cpar
        ; stx $str_lut

        ; lda @_stub
        ; call @cpar
        ; stx $adr_lut
        lda $_stub
        ldb @_stub
        call @lut_add
    ; plus "+" at 1
        ; iix $lut_i
        ; lda $_plus
        ; call @cpar
        ; stx $str_lut

        ; lda @_plus
        ; call @cpar
        ; stx $adr_lut
        lda $_plus
        ldb @_plus
        call @lut_add
    ; gcd at 2
        ; iix $lut_i
        ; lda $_gcd
        ; call @cpar
        ; stx $str_lut

        ; lda @_gcd
        ; call @cpar
        ; stx $adr_lut
        lda $_gcd
        ldb @_gcd
        call @lut_add
    ret

    @lut_add
        ; expects pointer to str in regA
        ; and pointer to adr in reg b
        iix $lut_i
        call @cpar
        stx $str_lut
        call @swopab
        call @cpar
        stx $adr_lut
    ret

    @read_input
        in 1 
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
        call @cpar
        ; ldb 0
        ; add
        stx $str_in

        :next_char
            in 1
            in 1
            test z
            jmpt :done_read_char
            ldb 20
            test eq
            jmpt :read_seperator

            inc x
            ; ldb 0
            ; add
            call @cpar
            stx $str_in
            jmp :next_char

        :read_seperator
            ; write null to str_in as end char
            inc x
            stx $str_in
            ;call @cmp_string_input
            call @lookup_input_string
            ;call @do_instuction
            call @lookup_intruction
            jmp @read_input
        
        :done_read_char
            ; write null to str_in as end char
            inc x
            stx $str_in
            ;call @cmp_string_input
            call @lookup_input_string
            ;call @do_instuction
            call @lookup_intruction
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
            ;ldb 0
            ;sub
            call @cpar
            call @dst_push
            in 1
            ; check fo seperator " "
            ldb 20
            test eq
            jmpt @read_input

    :end_read_input
    ret

    @dst_push
        ; lmb $cds 
        ; idx
        ; stx $dst
        ; inc b
        ; stb $cds
        iix $cds
        stx $dst
        ;iix $cds
    ret

    @dst_pop
        ; stb $t2
        ; lmb $cds
        ; dec b
        ; idx
        ; lxa $dst
        ; ;dec b
        ; stb $cds
        ; lmb $t2
        dix $cds
        lxa $dst
    ret

    @cmp_string
        ; expects adres pointers in regA and regB
        ; returns 0 (true) when eq, 1 when not eq
        ise
        jmpf :end_cmp_string
            isz
        jmpt :end_cmp_string
            inc a
            inc b 
        jmp @cmp_string

        :end_cmp_string
        ret

    @lookup_input_string
        ; find index of $str_in, return 0 if not found, 
        ; else  returns index
        lma $lut_len
        sta $lut_i

        :lookup_loop
            dix $lut_i
            lma $lut_i
            test z 
            jmpt :lookup_not_found
            lda $str_in
            lxb $str_lut
            call @cmp_string
            jmpf :lookup_loop
            lma $lut_i

        :lookup_not_found
            call @cpar
    ret
    ; @cmp_string_input
    ;     ; compare with "+"
    ;     lda $str_in
    ;     ldb $_plus

    ;     call @cmp_string
    ;     jmpf :cmp_next_gcd
    ;     lda 1
    ;     ;ldb 0
    ;     ;add
    ;     call @cpar
    ;     jmp :str_cmp_done

        
    ;     ; compare with "gcd"
    ;     :cmp_next_gcd
    ;     lda $str_in
    ;     ldb $_gcd

    ;     call @cmp_string
    ;     jmpf :str_not_eq
    ;     lda 2
    ;     ; ldb 0
    ;     ; add
    ;     call @cpar
    ;     jmp :str_cmp_done

    
    ;     :str_not_eq
    ;         lda 0
    ;         ; ldb 0 
    ;         ; add
    ;         call @cpar
    ; :str_cmp_done
    ; ret

    ; @do_instuction
    ;     ldb 1
    ;     test eq
    ;     skip 
    ;     jmp @_plus

    ;     ldb 2
    ;     test eq
    ;     skip
    ;     jmp @_gcd
    ; jmp :end_instuction

    @lookup_intruction
        ; expects the index of the inctruction in regA
        call @swopab
        idx
        jmpx $adr_lut


        @_plus
            call @dst_pop
            call @swopab
            call @dst_pop
            add
            call @dst_push
        jmp :end_instuction

        @_gcd
            call @dst_pop
            call @swopab
            call @dst_pop
            call @gcd
            call @dst_push  
        jmp :end_instuction 


        @_stub
        jmp :end_instuction

    :end_instuction
    ret

   



