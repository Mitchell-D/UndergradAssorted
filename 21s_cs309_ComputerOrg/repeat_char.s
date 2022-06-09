

@ -- ============= --
@    Mitchell Dodson
@    mtd0012@uah.edu
@    CS 309-01, 2021
@ -- ============= --

.equ READERROR, 0 @Used to check for scanf read error.

.global main @ Have to use main because of C library uses.

main:

@*******************
prompt:
@*******************

@ Ask the user to enter a number.

   ldr r0, =strInputPrompt @ Put the address of my string into the first parameter
   bl  printf              @ Call the C printf to display input prompt.

@*******************
get_input:
@*******************

@ Set up r0 with the address of input pattern.
@ scanf puts the input value at the address stored in r1. We are going
@ to use the address for our declared variable in the data section - intInput.
@ After the call to scanf the input is at the address pointed to by r1 which
@ in this case will be intInput.

   ldr r0, =numInputPattern @ Setup to read in one number.
   ldr r1, =intInput        @ load r1 with the address of where the
                            @ input value will be stored.
   bl  scanf                @ scan the keyboard.
   cmp r0, #READERROR       @ Check for a read error.
   beq readerror            @ If there was a read error go handle it.
   ldr r1, =intInput        @ Have to reload r1 because it gets wiped out.
   ldr r1, [r1]             @ Read the contents of intInput and store in r1 so that
                            @ it can be printed.

@ Print the input out as a number.
@ r1 contains the value input to keyboard.

   ldr r0, =strOutputNum
   bl  printf
   b   repeatCharacter  @ go to character input

@***********
readerror:
@***********
@ Got a read error from the scanf routine. Clear out the input buffer then
@ branch back for the user to enter a value.
@ Since an invalid entry was made we now have to clear out the input buffer by
@ reading with this format %[^\n] which will read the buffer until the user
@ presses the CR.

   ldr r0, =strInputPattern
   ldr r1, =strInputError   @ Put address into r1 for read.
   bl scanf                 @ scan the keyboard.
@  Not going to do anything with the input. This just cleans up the input buffer.
@  The input buffer should now be clear so get another input.

   b prompt


@*******************
repeatCharacter:
@*******************

   ldr r0, =charInPrompt
   bl printf

   ldr r0  =charInputPattern @ load data type
   ldr r1, =charInput        @ load word location for input
   bl  scanf                 @ call scanf
                             @ %s can be any input type, so no need for readerror checking.
   ldr r1, =charInput
   ldr r1, [r1]              @ load r1 with the provided string

   ldr r0, =charOutTemplate  @ load r0 with the template for returning the string as a character
   bl  printf                @ print the string as a character
   b   myexit                @ call the exit routine


@*******************
myexit:
@*******************
   mov r7, #0x01 @ SVC call to exit
   svc 0         @ Make the system call.

.data

@ Declare the strings and data needed
.balign 4
strInputPrompt: .asciz "Input the number: \n"
.balign 4
strOutputNum: .asciz "The number value is: %d \n"
@ Format pattern for scanf call.
.balign 4
numInputPattern: .asciz "%d"  @ integer format for read.
.balign 4
strInputPattern: .asciz "%[^\n]" @ Used to clear the input buffer for invalid input.
.balign 4
strInputError: .skip 100*4  @ User to clear the input buffer for invalid input.
.balign 4
intInput: .word 0   @ Location used to store the user input.


.balign 4
charInPrompt: .asciz "Input any character: \n"
.balign 4
charOutTemplate .asciz "The provided character value was: %c \n"
.balign 4
charInputPattern: .asciz "%s"
.balign 4
charInput: .word 0


@ Let the assembler know these are the C library functions.

.global printf

.global scanf
@ End of code and end of file. Leave a blank line after this.

