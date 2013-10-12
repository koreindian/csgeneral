'STRING_LENGTH
'Takes a string as input, and returns its length
'Only handles strings under 10 characters

'1. INITIALIZATION
>>+++++ +++++[>+++++ + < -]>++.

'2. INPUT
>>+[+++++ +++++>,[<]<<+>>>[>]<----- -----]

'3. ADJUSTMENT 
<[<]<<-

'4. COPY and MODULATE
[[>]>[>]>+<<[<]<<-]
>[>]>[>]>>
'   A. Hundreds
>+++++ +++++[<+++++ +++++>-]<<
[->-[>+>>]>[+[-<+>]>+>>]<<<<<]
'   B. Move Hundreds to a[0]
>>>[<<<<<[<]<<<<+>>>>>[>]>>>>-]
'   C. Tens and Ones
+++++ +++++<[->-[>+>>]>[+[-<+>]>+>>]<<<<<]
'   D. Moving Tens to a[1]
>>>[<<<<< <<[<]<<<+>>>>[>]> >>>>>-]
'   E. Moving Ones to a[2]
<[<<<<< <[<]<<+>>>[>]>>>>>-]

'5. ASCII SCALING and PRINT
'   A. Move to A[3]
<<<<< <[<]<
'   B. Set A[3] to 48
----- ----- ----
'   C. Scale A[0-2] up by 48
[<+<+<+>>>-]
'   D. Print
<<<.>.>.