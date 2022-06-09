

@ -- =========== -- @
@  Mitchell Dodson  @
@  mtd0012@uah.edu  @
@   CS309-01 2020   @
@ -- =========== -- @


.equ READERROR, 0 @Used to check for scanf read error.
.global main @ Have to use main because of C library uses.

@*******************
main:
@*******************
@  Ask the user to enter a number.
   ldr r0, =numInPrompt
   bl  printf

@*******************
getIntInput:
@*******************
@  set up registers for user input
   ldr r0, =numInputPattern
   ldr r1, =numInput

@  get and store input from user or handle readerrors
   bl  scanf
   cmp r0, #READERROR
   beq intReaderror
   ldr r1, =numInput
   ldr r1, [r1]

@  check whether user's input value is less than 100
   cmp r1, #100
   blt printLT

@*******************
printGEQ:
@*******************
@  If user input is greater than or equal to 100, print as such
   ldr r0, =numGTE
   bl  printf
   b   getCharInput

@*******************
printLT:
@*******************
@  If user input is less than 100, print as such
   ldr r0, =numLT
   bl  printf

@*******************
getCharInput:
@*******************
@  prompt user for a character
   ldr r0, =charInPrompt
   bl  printf

@  read user's provided character into register 1, handle readerrors
   ldr r0, =charInputPattern
   ldr r1, =charInput
   bl  scanf
   cmp r0, #READERROR
   beq charReaderror
   ldr r1, =charInput
   ldr r1, [r1]

@  check whether the provided character is less than A in the ASCII table
@  if so, branch to print the special character message
   cmp r1, #'A'
   blt printSpecial

@  check whether the provided character is less or equal to Z in the ASCII table
@  if so, it must be in the range of upper case letters, so print uppercase message
   cmp r1, #'Z'
   ble printUpper

@  check whether the provided character is less than a in the ASCII table
@  if so, it must be a special character between Z and a; print the special char message
   cmp r1, #'a'
   blt printSpecial

@  check whether the provided character is less than Z in the ASCII table
@  if so, it must be in the range of lower case letters, so print lowercase message
   cmp r1, #'z'
   ble printLower

@  If the user's character gets this far, it must be a special character,
@  print out the special character message.
   b   printSpecial


@*******************
printSpecial:
@*******************
@  print that the provided character is a special character
   ldr r0, =charSpecial
   bl  printf
   b   myexit

@*******************
printLower:
@*******************
@  print that the provided character is lowercase
   ldr r0, =charLower
   bl  printf
   b   myexit

@*******************
printUpper:
@*******************
@  print that the provided character is uppercase
   ldr r0, =charUpper
   bl  printf
   b   myexit


@*******************
intReaderror:
@*******************
@  handle a readerror from the integer input
   ldr r0, =intReaderrorMsg
   bl  printf

   ldr r0, =strInputPattern
   ldr r1, =strInputError     @ Put address into r1 for read.
   bl scanf                   @ scan the keyboard.
   b  getIntInput

@*******************
charReaderror:
@*******************
@  handle a readerror from the character input
   ldr r0, =charReaderrorMsg
   bl  printf

   ldr r0, =strInputPattern
   ldr r1, =strInputError     @ Put address into r1 for read.
   bl scanf                   @ scan the keyboard.
   b getCharInput


@*******************
myexit:
@*******************
@ End of my code. Force the exit and return control to OS

   mov r7, #0x01 @SVC call to exit
   svc 0         @Make the system call.


.data

@  declare static strings

.balign 4
numInPrompt: .asciz "Enter a number: \n"
.balign 4
numGTE: .asciz "The provided number value is greater than or equal to 100\n"
.balign 4
numLT: .asciz "The provided number is less than 100\n"
.balign 4
charInPrompt: .asciz "Enter a character: \n"
.balign 4
charSpecial: .asciz "The provided character is a special character\n"
.balign 4
charUpper: .asciz "The provided character is uppercase\n"
.balign 4
charLower: .asciz "The provided character is lowercase\n"
.balign 4
charReaderrorMsg: .asciz "char readerror encountered; please try again...\n"
.balign 4
intReaderrorMsg: .asciz "int readerror encountered; please try again...\n"   @ Location used to store the user input.

@  declare input patterns

.balign 4
numInputPattern: .asciz "%d"  @ integer format for read.
.balign 4
charInputPattern: .asciz "%s"
.balign 4
strInputPattern: .asciz "%[^\n]" @ Used to clear the input buffer for invalid input.

@ declare buffer skip values

.balign 4
strInputError: .skip 100*4  @ User to clear the input buffer for invalid input.

@  declare user input word memory locations

.balign 4
numInput: .word 0   @ Location used to store the user input.
.balign 4
charInput: .word 0   @ Location used to store the user input.

@ Let the assembler know these are the C library functions.

.global printf
.global scanf

