.text
main:
	# save return address ($ra) to the stack, since we may change $ra later
	# grow stack to allocate some space
	addi $sp, $sp, -4		# to grow stack, DECREMENT stack pointer address $sp
	sw $ra, 0($sp)			# (store word) FROM (return address $ra) TO (stack pointer in memory (with 0 pointer offset))

	# call strlen(teststring)
	la $a0, teststring		# put address of teststring at register a0 (function argument)
	# lui $at 4097 [teststring]
	# ori $a0, $at, 0 [teststring]
	jal strlen				# call strlen
	# strlen returns HERE

	# print result
	# MIPS system call: two things to setup
	# 1. System call code, put it in $v0
	# Service			System call code	Arguments		Result
	# print integer		1					$a0 = value		(none)
	move $a0, $v0			# move data from v0 (result) to a0 (input)
	li $v0, 1				# put call code into register v0
	syscall					# this prints to the screen
	# the code above prints 2378 correctly, but jal overwrote return address, updating $ra to point to the next (move instruction)
	# when it comes to jr $ra, it brings you again to move $a0, $v0, infinite loop!!

	# restore $ra from stack
	lw $ra, 0($sp)			# (load word) TO (return address) FROM (stack pointer in memory)
	addi $sp, $sp, 4		# roll stack back up

	jr $ra					# returns
	
strlen:
	# init length counter 
	li $v0, 0				# (or immediate) (function result) as 0

# linear execution resumes
strlen_top:
	# read a char
	lbu $t0, 0($a0)			# (load bit unsigned) (temporary) (content of pointer to [teststring]: current ascii value of the character)
	beqz $t0, strlen_return		# shortcut. ascii value = 0, return

	# if non-0 char, fall thru
	# need to increment length count (stored in v0)
	addi $v0, $v0, 1		# functionr result ++
	
	# increment pointer
	addi $a0, $a0, 1		# function input ++ (+1 here)

	# repeat
	# avoid reinitialization, go to strlen_top, NOT strlen
	b strlen_top
strlen_return:
	jr $ra				# returns right after jal strlen


.data
teststring: .asciiz "Hello, Class!"	# telling spim to interpret what follows as a \0 terminated ASCII string
