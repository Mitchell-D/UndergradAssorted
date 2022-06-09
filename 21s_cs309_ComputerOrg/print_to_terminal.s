@  name:   Mitchell Dodson
@  email:  mtd0012@uah.edu
@  class:  CS309-01 2020

.global main

main:

@ print first line to stdout
    MOV   r0, #0x01
    MOV   r2, #0x17
    MOV   r7, #0x04
    LDR   r1, =s1
    SVC   0

@ print second line using printf
    LDR   r0, =s2
    BL    printf

@ print third line to stdout
    MOV   r0, #0x01
    MOV   r2, #0x39
    MOV   r7, #0x04
    LDR   r1, =s3
    SVC   0

@ exit and return
    MOV   r7, #0x01
    SVC   0


.data

.balign 4
s1: .asciz "Mitchell Thomas Dodson\n"

.balign 4
s2: .asciz "mtd0012@uah.edu\n"

.balign 4
s3: .asciz "This is my first ARM Assembly program for CS309-01 2020.\n"

.global printf

