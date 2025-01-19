gcd:
    beq $a0, $a1, exit
    slt $v0, $a1, $a0
    bne $v0, $0, suba
    subu $a0, $a0, $a1
    b gcd

suba:
    subu $a1, $a1, $a0
    b gcd

exit:
    move $v0, $a0
    jr $ra