
@ -- =========== -- @
@  Mitchell Dodson  @
@  mtd0012@uah.edu  @
@   March 21, 2021  @
@      CS309-01     @
@ -- =========== -- @

@****************************************************************************
@  (in same dir as script)
@
@  compile: as -o dodsonLab4.o dodsonLab4.s ; gcc -o dodsonLab4 dodsonLab4.o
@  debug:   gdb --args dodsonLab4
@
@****************************************************************************


.equ READERROR, 0 @Used to check for scanf read error.
.global main @ Have to use main because of C library uses.

@*******************
main:
@*******************
@  Ask the user to enter a number.
   ldr r0, =numInPrompt
   bl  printf

@*******************
getInput:
@*******************
@  Asks the user for an integer between 1 and 12,
@  exits the program if the provided value not
@  an integer or not within the constraints.

@  collect number entered by user
   ldr r0, =numInputPattern
   ldr r1, =numInput
   bl  scanf

   cmp r0, #READERROR
   beq intReadError

@  reset registers and load r4 with user value
   ldr r1, =numInput
   ldr r4, [r1]
   ldr r1, [r1]

@  repeat number back to user
   ldr r0, =numEcho
   bl  printf

@  check whether user's input value is less than 13
   mov r1, r4
   cmp r1, #12
   bgt intReadError

@  check whether user's input is greater than  0
   cmp r1, #1
   blt intReadError

@  set up registers for factorial calculation
@  r4 is the user-entered max n value
   mov r5, #1    @ counter
   mov r6, #1    @ return value
   mov r7, #1    @ buffer value

   ldr r0, =facHeader
   bl  printf

@*******************
getFactorial:
@*******************
@  Recursively calculates the factorial of the provided integer,
@  printing the factorial value of every number in between 1
@  and the given value.

@  multiply the counter and factorial value
   mul r7, r6, r5
   mov r6, r7

@  print the updated counter
   ldr r0, =facCounterTmp
   mov r1, r5
   bl printf

@  print the updated factorial value
   ldr r0, =facValueTmp
   mov r1, r6

   bl printf

@  increment the counter
   add r7, r5, #1
   mov r5, r7

@  if the counter is greater than the user-entered value, exit.
   cmp r5, r4
   bgt myexit

@  otherwise, continue calculating the factorial with new value.
   b   getFactorial

@*******************
intReadError:
@*******************
@  handle a readerror from the integer input
   ldr r0, =intReaderrorMsg
   bl  printf

   ldr r0, =strInputPattern
   ldr r1, =strInputError     @ Put address into r1 for read.
   bl scanf                   @ scan the keyboard.
   b  myexit

@*******************
myexit:
@*******************
@ End of my code. Force the exit and return control to OS

   mov r7, #0x01 @SVC call to exit
   svc 0         @Make the system call.


.data

@  declare static strings

.balign 4
numInPrompt: .asciz "Enter a number between 1 and 12: \n"
.balign 4
intReaderrorMsg: .asciz "int readerror encountered; please try again...\n"   @ Location used to store the user input.
.balign 4
facHeader: .asciz "n    n!\n"


@  declare strings with value params

.balign 4
facCounterTmp: .string "%d    "
.balign 4
facValueTmp: .string "%d\n"
.balign 4
numEcho: .asciz "You provided: %d\n"


@  declare input patterns

.balign 4
numInputPattern: .string "%d"  @ integer format for read.
.balign 4
strInputPattern: .asciz "%[^\n]" @ Used to clear the input buffer for invalid input.


@ declare buffer skip values

.balign 4
strInputError: .skip 100*4  @ User to clear the input buffer for invalid input.


@  declare user input word memory locations

.balign 4
numInput: .word 0   @ Location used to store the user input.

.global printf
.global scanf

