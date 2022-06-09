

@ -- =========== -- @
@  Mitchell Dodson  @
@  mtd0012@uah.edu  @
@   CS309-01 2021   @
@   April 5, 2021   @
@ -- =========== -- @

@  ---  ARM Lab 5  ---

@****************************************************************************
@  (in same dir as script)
@
@  compile: as -o dodsonLab5.o dodsonLab5.s ; gcc -o dodsonLab4 dodsonLab4.o
@  debug:   gdb --args dodsonLab5
@  purpose: Simulate the operation of a gas pump.
@
@****************************************************************************

.equ READERROR, 0 @Used to check for scanf read error.
.global main

main:

welcomeScreen:
   ldr r0, =strWelcome
   bl printf

   @  load up memory addresses with default stock
   mov r1, #500  @ default stock
   ldr r7, =intRegStock
   ldr r8, =intMidStock
   ldr r9, =intPreStock
   str r1, [r7]
   str r1, [r8]
   str r1, [r9]

checkStock:
   @ check if all pumps are out of gas; if so, close the pump!
   ldr r7, =intRegStock
   ldr r7, [r7]
   ldr r8, =intMidStock
   ldr r8, [r8]
   ldr r9, =intPreStock
   ldr r9, [r9]

   cmp r7, #10
   cmplt r8, #10
   cmplt r9, #10
   blt closeGasPump

printStock:
   @ print stock header
   ldr r0, =strAmt
   bl  printf

getRegStock:
   ldr r7, =intRegStock
   ldr r7, [r7]
   cmp r7, #10  @ if <1 gal regular, don't display it.
   blt getMidStock
   ldr r0, =strRegAmt
   mov r1, r7
   bl printf
getMidStock:
   ldr r7, =intMidStock
   ldr r7, [r7]
   cmp r7, #10  @ if <1 gal mid-grade, don't display it.
   blt getPreStock
   ldr r0, =strMidAmt
   mov r1, r7
   bl printf
getPreStock:
   ldr r7, =intPreStock
   ldr r7, [r7]
   cmp r7, #10  @ if <1 gal premium, don't display it.
   blt promptUserType
   ldr r0, =strPreAmt
   mov r1, r7
   bl printf

@  Ask the user for a character; R, M, P, K
promptUserType:
   ldr r0, =strTypePrompt
   bl printf

   ldr r0, =charInputPattern
   ldr r1, =charTypeInput  @ provide scanf memory address of input
   bl scanf
   cmp r0, #READERROR
   beq charReadError

   ldr r1, =charTypeInput  @ get the memory address of the input
   ldr r3, [r1]  @ put input value into r3

   @ Check whether player entered a R
   cmp r3, #'R'
   beq buy
   cmp r3, #'r'
   mov r4, #4  @ load r4 with volume units/dollar
   beq buy

   @ Check whether player entered a M
   cmp r3, #'M'
   beq buy
   cmp r3, #'m'
   mov r4, #3  @ load r4 with volume units/dollar
   beq buy

   @ Check whether player entered a P
   cmp r3, #'P'
   beq buy
   cmp r3, #'p'
   mov r4, #2  @ load r4 with volume units/dollar
   beq buy

   @ Check whether player entered a K; the secret key!
   cmp r3, #'K'
   beq secretKey
   cmp r3, #'k'
   beq secretKey

   @ If we haven't branched yet, it wasn't a valid character!
   b   charReadError

secretKey:
   ldr r0, =strProfit
   bl  printf

   @  Print profits for regular fuel
   ldr r1, =intRegProfit
   ldr r0, =strRegProfit
   ldr r1, [r1]
   bl printf

   @  Print profits for mid-grade fuel
   ldr r1, =intMidProfit
   ldr r0, =strMidProfit
   ldr r1, [r1]
   bl printf

   @  Print profits for premium fuel
   ldr r1, =intPreProfit
   ldr r0, =strPreProfit
   ldr r1, [r1]
   bl  printf

   @  Return to first method that prints current stock
   b   printStock


@ Now that we have a value indicating units/dollar in r4,
@ ask for money and dispense the appropriate amount.
buy:
   ldr r0, =intPricePrompt
   bl  printf

   ldr r0, =intInputPattern
   ldr r1, =intUserCash
   bl  scanf

   @ if there was a readerror, try again
   cmp r0, #READERROR
   beq intReadError

   @  load r5 with the dollar amount entered
   ldr r1, =intUserCash
   ldr r5, [r1]

   @  Ask the user for a new amount if out of bounds
   cmp r5, #50
   bgt intReadError
   cmp r5, #1
   blt intReadError

   mul r6, r5, r4  @  store the volume requested in r6


@ move the stock of the selected fuel into r4 and load
@ r10 with the memory location of the profit for this type
@ use the units/dollar value in r4 to determine type
buyReg:
   ldr r7, =intRegStock
   cmp r4, #4
   ldreq r4, [r7]
   ldreq r10, =intRegProfit
   beq executeTransaction
buyMid:
   ldr r7, =intMidStock
   cmp r4, #3
   ldreq r4, [r7]
   ldreq r10, =intMidProfit
   beq executeTransaction
buyPre:
   ldr r7, =intPreStock
   cmp r4, #2
   ldreq r4, [r7]
   ldreq r10, =intPreProfit


@ increment profit, decriment stock, and report the amount dispensed
executeTransaction:

   @ if amt requested greater than stock, ask for a lower amt
   cmp r4, r6
   blt notEnoughGas

   @ store the post-transaction stock in memory
   sub r4, r4, r6

   str r4, [r7]

   @ add current profit for this type with this
   @ transaction and store back into memory.
   ldr r1, [r10]
   add r0, r1, r5
   str r0, [r10]

   @ print amount of gasoline dispensed
   ldr r0, =strAmtDispensed
   mov r1, r6
   bl printf
   b  checkStock


@  Invalid cash entry amount
intReadError:
   ldr r0, =invalidIntValue;
   bl printf

   ldr r0, =strInputPattern
   ldr r1, =strInputError
   bl  scanf
   b   buy


@  Not enough gas for dollar value entered
notEnoughGas:
   ldr r0, =strNotEnoughGas
   bl printf

   ldr r0, =strInputPattern
   ldr r1, =strInputError
   bl  scanf
   b   checkStock

@  User entered invalid char code
charReadError:
   ldr r0, =invalidCharValue
   bl  printf

   ldr r0, =strInputPattern
   ldr r1, =strInputError
   bl  scanf
   b   checkStock

@  End services and close the gas pump
closeGasPump:
   ldr r0, =strOutOfFuel
   bl printf
   mov r7, #0x01  @ SVC call to exit
   svc 0          @ Make system call


.data

@  declare static strings

.balign 4
strWelcome: .asciz "Welcome to the gas pump\n"
.balign 4
strOutOfFuel: .asciz "We're out of fuel! Goodbye."
.balign 4
strTypePrompt: .asciz "Enter desired fuel type: (R) (M) (P)\n"
.balign 4
intPricePrompt: .asciz "Enter Dollar amount (from 1 to 50) for this purchase:\n"
.balign 4
invalidCharValue: .asciz "Invalid gas type provided; try again.\n"
.balign 4
invalidIntValue: .asciz "Invalid dollar amount provided; try again.\n"
.balign 4
strNotEnoughGas: .asciz "We don't have enough fuel of that type, try entering less money.\n"

@  declare strings with value params

@ strings for returning fuel stock values
.balign 4
strAmt: .asciz "Stock remaining (1/10 gal):\n"
.balign 4
strRegAmt: .asciz "\tRegular:  \t%d\n"
.balign 4
strMidAmt: .asciz "\tMid-Grade:\t%d\n"
.balign 4
strPreAmt: .asciz "\tPremium  :\t%d\n"
.balign 4

@ strings for returning secret key values
.balign 4
strProfit: .asciz "Secret key entered!\n\nAmount Sold ($):\n"
.balign 4
strRegProfit: .asciz "\tRegular:  \t%d\n"
.balign 4
strMidProfit: .asciz "\tMid-Grade:\t%d\n"
.balign 4
strPreProfit: .asciz "\tPremium  :\t%d\n"
.balign 4
strAmtDispensed: .asciz "You've recieved %d tenths of gallons of gas.\n"


@  declare input patterns

.balign 4
intInputPattern: .string "%d"  @ integer format for read.
.balign 4
strInputPattern: .asciz "%[^\n]" @ Used to clear the input buffer for invalid input.
.balign 4
charInputPattern: .asciz "%s"  @ read with integer ascii format


@ declare buffer skip values

.balign 4
strInputError: .skip 100*4  @ User to clear the input buffer for invalid input.

@  declare memory locations

@ Integers storing dollar profit for each gas type
.balign 4
intRegProfit: .word 0
.balign 4
intMidProfit: .word 0
.balign 4
intPreProfit: .word 0

@ Integers storing 1/10 gal stock for each gas type
.balign 4
intRegStock: .word 0
.balign 4
intMidStock: .word 0
.balign 4
intPreStock: .word 0

@ character entered by user
.balign 4
charTypeInput: .word 0
@ dollar amount entered by user
.balign 4
intUserCash: .word 0

.global printf
.global scanf

