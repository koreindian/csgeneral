'ALPHANUMERIC_MULTIPLICATION
'Accepts two alphanumeric strings [000, 255], and prints the multiplication
'Only works for numbers under 255

'1. INITIALIZATION
<+++++ +++++[>+++++ +<-]>++

'2. INPUT 1
.>>>>+[+++++ +++++>,----- -----]
'   A. ASCII scale down
>+++++ +++++ ++[<++++>-]<[<-<-<->>>-]
'   B. Move ONES to A[1]
<[<<<<< <+>>>>> >-]
'   C. Move TENS to A[1]
<[<<<<<+++++ +++++>>>>>-]
'   D. Move HUNDREDS to A[1]
<[<<< +++++ +++++[<+++++ +++++>-]>>>-]

'3. INPUT 2
<<<<<.>>>>----- -----[+++++ +++++>,----- -----]
'   A. ASCII scale down
>+++++ +++++ ++[<++++>-]<[<-<-<->>>-]
'   B. Move ONES to A[1]
<[<<<<< +>>>>> -]
'   C. Move TENS to A[1]
<[<<<<+++++ +++++>>>>-]
'   D. Move HUNDREDS to A[1]
<[<< +++++ +++++[<+++++ +++++>-]>>-]
'   E. CLEANING
<[-]<<<<[-]

'4. MULTIPLICATION
>[>[->+<<<+>>]>[<+>-]<<-]
'   A. CLEANING
>[-]<<

'4. CALCULATE DIGITS using Divmod algorithm
'   A. Hundreds
>>+++++ +++++[<+++++ +++++>-]<<
[->-[>+>>]>[+[-<+>]>+>>]<<<<<]
'   B. Move Hundreds to a[0]
>>>[<<<+>>>-]
'   C. Clear a[1]
<<[-]
'   D. Tens and Ones
>>+++++ +++++<[->-[>+>>]>[+[-<+>]>+>>]<<<<<]
'   E. Moving Tens to a[1]
>>>[<<<<+>>>>-]
'   F. Moving Ones to a[2]
<[<<+>>-]
'   G. CLEANING
<[-]

'5. ASCII SCALING
>+++++ +++++ ++[<++++>-]
<[<+<+<+>>>-]

'6. PRINTING
<<<.>.>.