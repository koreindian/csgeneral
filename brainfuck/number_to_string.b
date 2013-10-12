'Number to String
'Takes in a number [0, 255] and prints it as a string.

'1. INITIALIZATION
>>>+++++ +++++[>+++++ +<-]>++

'2. INPUT
.>>,

'3. CALCULATE DIGITS using Divmod algorithm
'   A. Hundreds
>>+++++ +++++[<+++++ +++++>-]<<
[->-[>+>>]>[+[-<+>]>+>>]<<<<<]
'   B. Move Hundreds to a[0]
>>>[<<<<< <<<<+>>>>> >>>>-]
'   C. Tens and Ones
+++++ +++++<[->-[>+>>]>[+[-<+>]>+>>]<<<<<]
'   D. Moving Tens to a[1]
>>>[<<<<< <<<<<+>>>>> >>>>>-]
'   E. Moving Ones to a[2]
<[<<<<< <<<+>>>>> >>>-]

'4. ASCII SCALING
>+++++ +++++ ++[<++++>-]
<[<<<<< <<< + <+ <+ >>>>> >>>>>-]

'5. PRINTING
<<<<< <<<<<.>.>.