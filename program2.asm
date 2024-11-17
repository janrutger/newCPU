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
. $_mod 2

% $_stub #
% $_gcd gcd
% $_plus +
% $_mod %

. $str_lut 4
. $adr_lut 4
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
        ldb 4
        stb $lut_len
    ; setup lookup table
        ; stub at 0
        lda $_stub
        ldb @_stub
        call @lut_add
        ; plus "+" at 1
        lda $_plus
        ldb @_plus
        call @lut_add
        ; gcd at 2
        lda $_gcd
        ldb @_gcd
        call @lut_add
        ; modulo "%" at 3
        lda $_mod
        ldb @_mod
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
            call @cpar
            stx $str_in
            jmp :next_char

        :read_seperator
            ; write null to str_in as end char
            inc x
            stx $str_in
            call @lookup_input_string
            call @lookup_intruction
            jmp @read_input
        
        :done_read_char
            ; write null to str_in as end char
            inc x
            stx $str_in
            call @lookup_input_string
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
            call @cpar
            call @dst_push
            in 1
            ; check for seperator " "
            ldb 20
            test eq
            jmpt @read_input

    :end_read_input
    ret

    @dst_push
        iix $cds
        stx $dst
    ret

    @dst_pop
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

        @_mod
            call @dst_pop
            call @swopab
            call @dst_pop
            call @mod
            call @dst_push  
        jmp :end_instuction


        @_stub
        jmp :end_instuction

    :end_instuction
    ret

   



