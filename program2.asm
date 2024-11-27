@program
    call @init
    call @kernel_init
    :lus
    call @read_input
    jmp :lus
halt

. $t1 1
. $t2 1
. $zero 1
;datastack and pointer
. $dst 24
. $cds 1
; input string and pointer
. $str_in 8
. $str_in_i 1
; variable area and pointer
. $_vars_ 24
. $_vars_i_ 1
. $_vars_index 1


. $_stub 2
. $_plus 2
. $_gcd 4 
. $_mod 2
. $_exit 5
. $_prt_num 2
. $_prt_char 3
. $_prt_str 3
. $_prt_quote 3

% $_stub #
% $_gcd gcd
% $_plus +
% $_mod %
% $_exit exit
% $_prt_num .
% $_prt_char .c 
% $_prt_str .s
% $_prt_quote .'

. $str_lut 9
. $adr_lut 9
. $lut_i 1
. $lut_len 1

@kernel
    @kernel_init
        ldb 0
        ; set datastack counter
        stb $cds  

        ; set vars buffer and pointer to zero
        stb $_vars_i_
        stb $_vars_

        ; set zero
        stb $zero 

        ; set Lookup Indexes to zero
        stb $lut_i  
        stb $str_in_i
        ; set size of lookup table (=number of(insctructions))
        ldb 9
        stb $lut_len
    ; setup lookup table
        ; stub at 0
        lda $_stub
        ldb @_sto_str_dst
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
        ; exit at 4
        lda $_exit
        ldb @_exit
        call @lut_add

        ; Print number  at 5
        lda $_prt_num
        ldb @_prt_num
        call @lut_add

        ; Print char  at 6
        lda $_prt_char
        ldb @_prt_char
        call @lut_add

        ; Print string  at 7
        lda $_prt_str
        ldb @_prt_str
        call @lut_add

        ; Print quote  at 8
        lda $_prt_quote
        ldb @_prt_quote
        call @lut_add   
    ret

    @lut_add
        ; expects pointer to str in regA
        ; and pointer to adr in regB
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
        ldb 30
        test eq
        jmpt @read_input

        ldb 0
        idx
        ; first char
        call @cpar
        stx $str_in

        :next_char
            in 1
            in 1
            test z
            jmpt :done_read_char
            ldb 30
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
            ;call @prt_newline 
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
            ldb 30
            test eq
            jmpt @read_input

    :end_read_input
        call @prt_newline
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
        ; index = 0 points to a stub routine, for unkown instructions
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

        @_exit
            halt
        jmp :end_instuction

        @_prt_num
            lda 0
            call @cpar
            out 3
            call @dst_pop
            call @cpar
            out 3
        jmp :end_instuction

        @_prt_char
            lda 1
            call @cpar
            out 3
            call @dst_pop
            call @cpar
            out 3
        jmp :end_instuction

        @_prt_str
            call @dst_pop
            sta $_vars_i_
            
            
            :prt_next_char
            lix $_vars_i_
            lxa $_vars_
            test z
            jmpt :prt_space

            lda 1
            call @cpar
            out 3
            lxa $_vars_
            ;test z 
            ;jmpt :prt_space
            call @cpar
            out 3
            iix $_vars_i_
            jmp :prt_next_char


            ; lda 1
            ; call @cpar
            ; out 3
            ; call @dst_pop
            ; test z
            ; jmpt :prt_space
            ; call @cpar
            ; out 3
            ; jmp @_prt_str
            :prt_space
                lda 1
                call @cpar
                out 3
                lda 30
                call @cpar
                out 3
        jmp :end_instuction

        @_prt_quote
            ldb 24
            in 1
            in 1
            test eq
            jmpt :end_instuction
            call @swopab
            lda 1
            call @cpar
            out 3
            call @swopab
            call @cpar
            out 3
            jmp @_prt_quote
        jmp :end_instuction

        @_store_var_value
           ;!
        jmp :end_instuction

        @_sto_str_dst
            ;call @dst_push_str
            call @sto_var_name
        jmp :end_instuction

    :end_instuction
    ret

    @prt_newline
        lda 1
        call @cpar
        out 3
        lda 99
        call @cpar
        out 3
    ret

    @sto_var_name
        ldb 0
        stb $str_in_i
        stb $_vars_i_

        lix $_vars_i_
        lxa $_vars_

        test z
        jmpt :add_var_name
            lmb $_vars_i_
            stb $_vars_index

            lix $str_in_i
            lxb $str_in
            
            :check_i
            ; comparee regA (var) and regB (input)
                test eq
                jmpf :find_next_var
                test z  
                jmpt :found_var
                    iix $_vars_i_
                    lxa $_vars_

                    iix $str_in_i
                    lxb $str_in
            jmp :check_i

            :find_next_var
                :next_i
                    test z
                    jmpt :found_var_end 
                    iix $_vars_i_
                    lxa $_vars_
                    ;test z 
                jmpf :next_i

                :found_var_end
                ; skip value index
                iix $_vars_i_

                ; Next is the next var, or a new var
                lix $_vars_i_
                lxa $_vars_
                test z 
                jmpt :add_var_name
                    ; set the index to the next var on the list
                    lma $_vars_i_
                    sta $_vars_index

                    ldb 0
                    stb $str_in_i
                    lix $str_in_i
                    lxb $str_in
            jmp :next_i
 
        :add_var_name
            ; set de var index
            lma $_vars_i_
            sta $_vars_index

            ldb 0
            stb $str_in_i
            
            :loop_add_var_name
                lix $str_in_i
                lxa $str_in
                call @cpar

                lix $_vars_i_
                stx $_vars_

                test z 
                jmpt :added_var
                    iix $_vars_i_
                    iix $str_in_i
                jmp :loop_add_var_name

        :added_var
            iix $_vars_i_
            iix $_vars_i_
            lda 0
            call @cpar
            iix $_vars_i_
            stx $_vars_
            

        :found_var
            lma $_vars_index
            call @cpar
            call @dst_push
            jmp :end_var_add

    :end_var_add
    ret

    @dst_push_str
        ; expect $str_in string en put on the stack
        ldb 0
        stb $str_in_i
        lix $str_in_i

        :loop_findlast_0char
            lxa $str_in
            test z
            jmpt :do_push_str
            iix $str_in_i
            jmp :loop_findlast_0char

        :do_push_str
            dix $str_in_i
            lxa $str_in
            call @cpar
            call @dst_push
            lma $str_in_i
            test z
            jmpf :do_push_str
            
        :done_push_str
    ret

   



