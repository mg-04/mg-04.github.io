---
title: AP Notes.md
permalink: /articles/ap
---

This file may not be fully adapted for web. Download the raw file [here](f24/CS3157-AP/AP-Notes.zip)

# 1. CLI Basics
```shell
X=hello
echo $X
```
### SSH
1. User inputs command
2. Shell
3. Command executed  

### Folder organization
- Top level (root) directory: `/`
- Absolute path: path from the root directory (starting with `/`)
`UpArrow` restores the previous command

## Shell shortcuts
- `Ctrl + A`: start of a line
- `Ctrl + E`: end of a line 

**Loop**
```shell
for i in 1 2 3 ; do date ; done         # runs date 3 times
```

**Alias**
```shell
declare alias ll-'ls -alF'
```
```shell
cat .bashrc     # to see all alias
```

**`diff`**
 ``` shell
diff a b        # displays difference between two files
```
- `Ctrl + R` reverse search of commands

## Vim shortcuts
- `gg` go to top
- `G` go to bottom
- `dd` delete whole line
- `Ctrl+F` scroll fwd by a screen
- `Ctrl+B` scroll back by a screen
- `{` scroll back a paragraph
- `}` scroll fwd a paragraph
- `zz` move current cursor to the center
- `v` start highlighting stuff
- `V` highlight by line
- `Ctrl+v` highlight by column
- `=` auto indents the highlighted portion

# 2. Compilation and Make
```shell
gcc hello.c
```
Compiles and links the file
```shell
gcc hello.c -o hello
```
Compiles, links the file. Named `hello`, same as `a.out`.
```shell
./hello
```
executes the `hello` program
Can't directly do `hello` like `ls`, since `ls` is in the `usr/bin/` folder (system path)

## Building a C program
How source file -> executable program
```shell
gcc myprogram.c && ./a.out      # runs first command, if works, runs the second
```
No classes in C. All functions are on the top of source file. No nesting of functions.

C program always starts from the SINGLE main function (entry point).

### Proper way: separate compilation
- For multiple source files, first compile them into multiple intermediate **OBJECT** files (`.o`)
- Then use linker to link the multiple object files

In scenario above:
```shell
gcc -c hello.c      # -c means compilation only
```
Repeat for other `.c` files

Now link all the `.o` files. Give `gcc` the `.o` intermediate file
```shell
gcc hello.o         # just gcc on hello.o
```
Can use `-o` to rename the executable

(In vim, use `:e` to edit two files at once)

Now make `myadd.c`. Compile both
```shell
gcc hello.o myadd.o -o hello        # link both togther
# warning here: myadd is not defined in hello.c
# declared myadd "implicitly" by calling it
```

- Compilation: translate C program into machine code (sequence of numbers) for the CPU (`.o`)
    - Why is it so much bigger? There is some code we didn't write `printf()`. Also some structural code

### More options
```shell
gcc -c -Wall -g myprogram.c
```
- -Wall enables ALL warnings
- -g include some information in the object file for DEBUGGING

## Declaration
```c
int add(int x, int y);      // I will define this function later
// Aka function prototype/signature
// You can also put prototype within main()
```
Before calling the function, you should either define or **declare** the function.

Create `myadd.h` to just **declare** `add`. 
```c
#include "myadd.h"      
// When you encounter this line, replace this line withe the file content
```
Compiler just copy and paste
-  `<>` looks for at system directory
-  `""` looks at cd
Code of `myadd` is actually in `myadd.c`. `myadd.h` only has the prototype

Linker links the necessary `.o` files from **standard library**.

```shell
gcc hello.o myadd.o -lm         # -lm means to look for in the math lib
```
### Prevent linking problem
Modify `myadd.c` somehow and recompile it to `myadd.o`

We **don't** need to recompile `hello.c`. Just need to update `hello` by relinking.

Now change the input property of `myadd.c` to take 3 numbers
- Compilation is OK, since `myadd.h` unchanged
- Linking is also OK. C only matches up the function names, not the parameters. 
    - Linker is not restricted to C. `.o` files can be compiled from different languages.
- When run, program displays random wrong shit.

Things fail silently!!!
```shell
objdump -d myadd.o
```
This displays content of files in hexadecimal and assembly code

Memory allocation issue

**How to solve this issue**
In `myadd.c`, include its own header file
`myadd.c`
```c
#include "myadd.h"              // myadd in .h take only 2 params
int add(int x, int y, int z){   // It will complain here
    ...
}
```

## Makefile
`make` is a program that compiles based on instruction (`Makefile`)
- **capital** M!

```make
myadd.o: myadd.c myadd.h        # myadd.o: target, others: ingredient
    gcc -c -Wall -g myadd.c     # tab here, can't be spaces
# Empty lines OK, sole spaces not allowed
```

```shell
make        # Runs the gcc command
```
Make will make `myadd.o`

If nothing changes, `make` will look at timestamp and not do anything. 

```shell
touch myadd.c       # updates timestamp to "simulate" a change in file 
```
`cat` tricks (`-ten`)
```shell
cat -ten Makefile   # t: changes tab, e: marks end of line, n: line num
```
- In vim, `2yy` means yank (copy) 2 lines, and then `p` to paste it.
- `.` repeats previous action.

`Makefile` only makes the first target it finds. 
Needs to specify target if not the first:
```shell
make myprogram.o
```

```make
myprogram: myadd.o myprogram.o
    gcc myadd.o myprogram.o -o myprogram

myadd.o: myadd.c myadd.h
    gcc -c -o myadd.o myadd.c

myprogram.o: ...
```

- When `make` typed in, `make` builds the first target: `myprogram`
- Then it looks for the prereq, comparing the time. However, `.o` files are **missing**. `make` will usually give up.
    - However, it scans down if prereq are **targets** themselves, looking for `myadd.o` as targets.
    - `make` suspends building `myprogram`, instead, starts building `myadd.o` first. (**recursively**)
    - Similarly, `make` builds `myprogram.o`.
- Once built, come back to mission of building `myprogram` and runs linking. 

**Running `make` again**

Already up to date
- Still, `make` checks if **all** sub-ingredients are up to date, since some subfiles may not. 
    - e.g. If `touch myadd.c`, `make` updates `myadd.o` and `myprogram`, not `myprogram.o`.
    - e.g. If `touch myadd.h`, 3 files updated.

### Variables

```make
CC = gcc
CFLAGS = -g -Wall

$(CC)   # uses the variable

#If linking recipe not specified, 
#   $(CC) $(LDFLAGS) <dependent-.o-files> $(LDLIBS) -o <executable name>
# so we can just omit the recipe
```
You can omit the subsequent lines

### Auto remove binary files after compilation

```make
.PHONY: clean
clean:
    rm -f *.o myprogram
```
```shell
make clean
```

```make
.PHONY: all
all: clean myprogram
# Let it first do 'clean', and then REBUILD 'myprogram'
# make clean
# make myprogram
```

Make is attempting to produce a **file** `clean`. File did not get produced, but command executed
- aka **phony target**

## Git
Version control system: take a snapshot of current progress, in case of messing up

For HW, we `clone` the lab assignments, not `init`. 

```shell
git add *.c     # can be add or modification
git commit      # actually "does" the add. Allows multiple "units" of change
# git pops a "commit message"
```
Type on the first line for `commit message`
```shell
git log         # sees commit log
git status      # displays UNTRACKED files
```
File possibilities:
1. Untracked: never added to git
2. tracked, unmodified: files haven't been modified since last commit
3. Tracked, modified, unstaged: modified but not `git add`ed. Changes in `git diff`
4. Tracked, modified, staged: modified, added, not yet committed, can't be shown on `git diff`, but can be seen with `git diff --staged`
5. After commit, those files will not show up in `git status`

# 3. C Basics
## Integer types
C doesn't specify the exact length of the types, but pretty standardized
- `char` 1 byte (8 bits), `unsigned` 0-225, or -128-127
- `short` 2 bytes, `unsigned` 0~65536, or -32768-32767
- `int` 4 bytes, `unsigned` $0\approx 4\times 10^9$
- `long` 4/8 bytes
- `long long` 8 bytes

If `unsigned` used as prefix, positives only

C99 introduces `(u)intN_t` to specify the space. 
- E. `int8_t`, `uint8_t` (same as `char`!, it's 8 **bit**, not **byte**!)

## Binary numbers
**Signed** implementation: 
1. 1's complement
2. 2's complement (currently used)

MSB is given a **negative weight**

Properties: 
1. Negative numbers have MSB 1
2. 1111...1 = -1 (largest negative number)
3. 1000...0 = smallest negative number

Conversion: 
1. Filp all bits
2. **Add 1**

**Hex** notation: `0x12` = 12
```c
int x = 0xffffffff;             // x = -1
int y = 0x7fffffff;             // y = 2^31 - 1
int z = 0x80000000;             // z = -2^31
unsigned int a = 0xffffffff;    // a = 2^32 - 1
unsigned int b = -1;            // C will force assignment. b = 2^32 - 1
```
## Integer literals
Declaration
```c
int i = 5;      // Declared, initialized
int j;          // not yet init

i = 100;        // Assignment
i = 'A';        // 'A' (single quote) = 65
j = '\11';      // Ocatal numbers 011=9
j = '\0';       // '\0' = 0, not '0' = 48
```
## Expressions vs statements
### Statement
Typically end with semicolon/curly braces
### Expression
A **piece** of a statement that has a **type** and **value**
- `42`
- `x` (depends on assignment)
- `1 + 6` (type `int`)
- `3.14f` (specifies `float` type)
- `a == b` (type `int`, not `bool`)
- `printf("hi")` (This is a function call, with some evaluation)

Extension: `x = 1;` is both a statement and an expression.

## Bitwise operators
```c
int x = 1;      // x = 0000 .... 0001
int y = 2;      // y = 0000 .... 0010
int z = -1;

int a = x & y;  // a = 0000 .... 0000   AND operation on each bit
int b = x | y;  // b = 0000 .... 0011   OR
int c = x ^ y;  // c = 0000 .... 0000   XOR
int d = ~x;     // d = 1111 .... 1110   NOT
int e = x << 1  // e = 0000 .... 0010   left shift by 1, filing 0s.
int f = z >> 1; // Up to complier to feed a 1 or a 0.
// Typically use bitshift with signed numbers
```
### HW hint
```c
int f(int x)
{
    return  x & (1 << 5);       // picks the value of the 6th LS bit
}
```
Loops to pick each bit

## Logical operators (short circuit)
Similar, but 
```c
if (x && f(x))
{
    // code
}
```
If `x=0`, `f(x)` will **not be evaluated**. This is called **short circuit evaluation**.
- Maybe `f(x=0)` will crash. 

Same for `||`
## Assignment and `x++`
Typically for C, an expression is not a statement. 
- `3+5;` is not allowed (with a `;`)
- `x << 1;` does not change `x`! This is only an expression.
- `f(x);` is both an expression and a statement
- `x = 1;` This statement and **expression** has type `int` and value `1`.
- `int x;` is a statement (declaration), but not an expression, since no value.
- `int x = 1;` is also **not** an expression. You can't use it the same way as `(x = 1)`
- `y = x = 2;` same as `y = (x = 2);`, a compound expression, evaluated **right to left**.
- `x = x + 1;` `+` has higher precedence than `=`
- `x += 1;` Exactly the same as above
- `++x` Exactly the same. Expression and statement.

```c
int x = 1;
int y;

y = ++x;        // y = 2. ++ first, and then use x
y = x++;        // y = 2. Use x first, and then ++

x = 2;
y = (x++);      // y = 2! Same thing as above! The act of evaluating (x++) //reserves the output, and outputs 2, before the increment.

(y = x)++;      // ERROR: the value of assignments (y = x) can't be changed!
```

# 4.  Storage Classes

You can only have one name (variable or function) within a **scope**
## 1. Local variables
`foo.c`:
```c
int x = 100;            // Global static variable
void f(int p) {
    printf("%d", p);    // p is also local
    int x;              // can't access outer x. Local variable name HIDES it.
    x = 0;
    {
        int x;          // A different int x comes alive, separate from previous
        x = 1;
        printf("%d", x) // 1
    }                   // That int x gone
    printf("%d", x);    // 0
}

f(x);
```
- Variables declared inside a function/**block** are **local** variables, or **automatic** variables. They come and go automatically (**deleted** after block ends). Or called **stack** variables. **Why?**

Next time you call the function, local variables are reinitialized.
## 2. Static variables
Initialized at **program startup**. 
Value will stay there. May be changed. Persistent **through the program**.
`foo.c`
```c
int x = 100;
void f(void);
int main() {
    f(); 
    printf("%d", x);
}
```
`bar.c`
```c
void f(void) {
    x = x + 50;
    printf("%d", x);
}
```
- If compile `bar.c` **alone**, **won't compile**!, since x is undefined.
- If add a line `int x;`, both files will compile, but can't link, since **duplicate variable names**!
Need to add `extern`. Tells the compiler to "assume" that you will find (resolve) `x` at **link time**. 
```c
extern int x;
void g(void) {
    x = x + 50;
}
```

- `extern` and initialize: same as init alone
- `extern`, but **not initialize**: required for accessing global var elsewhere
- When you don't initialize, **global vars** auto init to `0`. 

### 2a. Global (static) variable
Defined outside `main()`. Always accessible, unless "covered" by a local variable
### 2b. File static variable
In declaration in `foo.c`, use `static int = 100`.
**`static`** makes `extern int x` in **other files** not work. `x` is for `foo.c` **file only**!
- Compile is fine, but **link time**, global variable not found

### 2c. Block static variable
`main.c`  

```c
//int x = 100;            // Prints 101 - 105
int f(void) {
    // int x = 100;     // If put x = 100 here, will print 101 five times
    static int x = 100;      //PRINTS 101 - 105 again
    x++;
    return x;
}

int main() {
    for (int i = 0; i < 5; i++)
    printf("%d", f());
}
```
`x` is **block static**. You can't access `x` anywhere outside `f`, but `x` **behaves** like a global variable (as if it's defined outside).

`x` only gets initialized at program startup, **before `f` called**. Every time `x` is called, `static int x = 100` is **skipped!!!**

## Process address space
- When a program runs, it's a process (running instance of a program)
- Program code is put in memory (some space left initially)

Program **thinks** they have total memory of, let's say,  512G, but actually much smaller, because OS gives **fake** addresses. OS maps each fake address to the real RAM (E. 4G)

Memory block for **one process** (long, sequential tape, top to bottom):
- Stack (local variable)
- ... (empty)
- Heap (`malloc`)
- Static variable
- Code
- Reserved
Initially, code and static variable areas are fixed. Stack and heap can grow.

## Stack allocation (an overview)
Allocates local variables 

```c
int f(void) {
    int x; 
    int y;
    ...
}
int g(void) {
    int s;
    int t;
    ...
}

int main() {
    int a;
    int b;
    f();
    g();
}
```
Stack (top-down):
- a = 100
- b = 200
- x         (after `f` returns, `x` deleted)
- ...

CPU also has embedded **special variables**: **registers**
- **Stack pointer** holds the address of stack's **bottom**
    - When a variable goes away, stack pointer moves up
    - Stack grows and shrinks
    - Recursion (if incorrectly written): stack **overflow** (enforced by OS)

# 5. Pointer
## Pointer variables
```c
foo() {
    int x = 1;
    int y = 2;

    int *p;     // type: int*
    // Can also use int* p;

    // p takes 8 bytes, holds the memory address
    // p can contain a memory address of type INT

    p = &x;         // p = address of x
    // &x: type int*
    // & is a unary operator, returning the ADDRESS of a variable

    y = *p;         // y = gets the value that p points to
    // *p: type int         PEEL OFF a *

    *p = 0;         // changes x to 0
}
```
In `int *p`, `*` declares a type, but in `y = *p`, `*` is an operator
Why `int *p`? `p` is a variable s.t. that if you **apply a `*` on it**, you'll get an `int`.

**Postfix has higher priority than prefix**, so `(*p)++` differ from `*p++`.
## Pointer types
Pointer variables have **distinct types**.
```c
int i = 1234;           // 4 bytes
double d = 3.14;        // 8 bytes

int *pi = &i;           // All pointer var are 8 bytes
double *pd = &d;

pi = pd;                // ERROR!
pi = (int *) pd;        // casted pd (double*) as int*. 
// If dereferenced, It will take the first 4 bytes of d, meaningless
```
### Void pointer
Special type: can point to any type
```c
void *pv;
pv = pd;

double x = *pv;             // WRONG! 
double x = *(double*) pv;   // Cast, then deref
```
A `void*` **can't be dereferenced!** C doesn't know how many bytes to read or what to interpret it as.
## NULL Pointer
Address `0` is special

```c
int *pi = 0 
pi = NULL;          // NULL = 0
```
Pointer in `if` block will evaluate to `0` only if pointer is `NULL`.
```c
int c = 0;
int *p = &c;
int *q = 0;

if (p)
    // runs
if (q)
    // won't run
if (*p)
    // won't run
if (*q)
    // COMPILES, but CRASHES
```

# 6. Arrays
```c
int a[4] = {100, 101, 102, 103};    // declares and inits array
int a[] = {100, 101, 102, 103};     // also OK, compiler will deduce it
int a[10] = {100, 101, 102, 103};   // compiler will init others 0
int a[] =                           // NO init: C won't init anything

a[0] = 200;
a[4] = 400;     // ILLEGAL, but may run
```
## `sizeof()`
Not a function. A **keyword** operator. Can take any expression and **type name**.
```c
int i;
int a[10];
int x;

x = sizeof(i);      // returns byte-size of i: 4
x = sizeof(int);    // 4
x = sizeof(&a[0]);  // 8        &(a[0]), postfix wins

x = sizeof(a);      // 40!      4 * 10
```

## `p++;`
Addition of pointer and `int` means the **address** of the next element the pointer points to. `+sizeof`
E. `int`, `+1` points to 4 elements later. `double` 8.

Can't do for `void*`. Undefined
```c
int a[4] = {100, 101, 102, 103};
int *p = &a[0];

for (int i = 0; i < 4; i++) {
    //printf("%d", *(p+i));
    //print("%d", a[i]);
    printf("%d", *p);
    p++;                    // p += 4 actually

    //same as 
    printf("%d", *p++);     // *(p++)
}
```
At the end, `p` points to one PAST the last element of `a`.

C guarantees it's fine. You can't deref it tho.
## GUT
Grand Unified Theory of pointers and arrays

if **`p = &a[0]`**, 
1. `a[i]` <=> `*(p+i)`
2. `a` <=> `&a[0]`. Most cases, an array name will be **converted** to the pointer of the first element.
3. `a[i]` <=> `*(p+i)` <=> `*(&a[0] + i)` <=> `*(a + i)`
4. `p[i]` <=> `(&a[0])[i]` <=> `a[i]`. 

We can **interchange** pointers and array!

**GUT**: `u[i]` <=> `*(u+i)`. 
Doesn't matter if `u` is pointer or array. Compiler will change `u[i]` to `*(u+i)`

**Prop**: `a[5] = *(a+5) = *(5+a) = 5[a]`
`5[a]` compiles and **runs normally!**
### Exceptions
1. You can do `p++`, but not `a++`.
2. `sizeof(a)` differ with `sizeof(p)`.

# 7. Heap allocation
```c
int main() {
    int *p;
    p = f();        // f returns a pointer to array
    printf("%d", p[2]);
}

int *f() {
    int a[4] = {100, 101, 102, 103};
    return a;       // returns a pointer to a[0]
}
```
**Problematic!** After `f` finishes, automatic `a` deleted (stack goes up).
-  `p` becomes a **dangling pointer**.

 How to use array out of the function then: **heap allocation: `malloc()`**
- argument: how many bytes using. 
- returns a **`void *` pointer** to the first byte of the space you want.
    - `void *` because `malloc()` doesn't know the type

```c
int *f() {
    int a[4] = {100, 101, 102, 103};
    int *p = malloc(sizeof(int) * 4);   

    return p;
}
```

## Freeing memory
Heap is not automatically managed. You have to free it manually.
```c
free(p);
```
### Memory leak
Once you disconnect a pointer to heap, the memory is lost
`valgrind` needs to say nothing is wrong!

# 8. String
String represented as `char` arrays, ending with `0`.
```c
// "abc"
char a[4] = {'a', 'b', 'c', 'd', '\0'};
char a[4] = {97, 98, 99, 100, 0};

char *p = a;          // p = &a[0]
printf("%s", p);      // printf expects p to be type char*, NOT char!!!
// printf follows the pointer, prints the character 'a'
// printf keeps going until it hits 0.
printf("%s", a+1);    // a -> &a[0], a+1 -> &a[1]
// bcd

```
## String Literals
```c
char *p = "abc";
printf("%s", "abc");    
// "abc" is an expression, type: array that turns itself into char *
```
The type of `"abc"` is `char[4]`, **anonymous array**. When `"abc"` is assigned to `*p`, it turns itself to a `char *` pointer to the first value.

Two cases where array not turned into pointer:
1. `sizeof("abc")`: 4
    - `sizeof("abc" + 1)` (converted to pointer): 8
2. Array initializer:  `char a[4] = "abc"`

Where is `"abc"` stored at?
- `p` is on the stack
- `"abc"` is in a region **between static var and code**, called **read-only data** (kind of part of code)
    - `"abc"` is immutable, just like you can't do `5 = 4`

## String library functions
`strlen()` returns string length **not including** `\0`
```c
#include <string.h>
int strlen(char *s) {
    int i = 0;
    while (*s++)
        i++;
    return i;
}
```
`strcpy()` copies
```c
#include <string.h>
void strcpy(char *t, char *s) {
    while((*t = *s) != 0){
        s++;
        t++;
    }
}

void strcpy(char *t, char*s) {
    while((*t++ = *s++) != 0)
        ;
}
```
Wrong usage:
```c
char *a = "abc";
char *b;
strcpy(b, a);
```
`b` is **not initialized**, so `"abc"` is copied to somewhere random, and the program may crash.
- Have to declare `char b[4];`

## `argv` array
How to access `./a.out hi world`?
```c
int main(int argc, char **argv)
```
- `argc` is the number of arguments **including program name**.
- `**argv` is an **array of pointers** (`char *`), ending with a *`0`*

Example: print "o" in "world"
```c
printf("%c", argv[2][1]);
printf("%c", *(*(argv + 2) + 1));
```

```c
int main(int argc, char** argv) {
    argv++;
    while(*argv)
        printf("%s\n", *argv++);    // *(argv++)
}
```

# 9. Function Pointers
## `const`
Variables that should not be changed. C won't compile if changed
### `const` pointers
```c
int * const p = &x;       // p is a pointer STUCK to an address
p = &y;                   // ERROR

const int *q = &x;        // q is not constant, but *q is
*q = 100;                 // ERROR

// To force changing *q:
*(int *)q = 100;           // cast to regular int *, and then change 
```
Example: 
```c
strcpy(char *t, const char *s);
```
`*s` should not be modified.

## `qsort`
Sorts **any** array
```c
typedef unsigned int size_t;    // optional

void qsort( void *base,         // ANY TYPE pointers accepted
            size_t nmemb,       // size_t is unsigned_int/long
            size_t size,        // size of EACH element
            int (*compar) (const void *, const void *)); 
```
`int (*compar) (const void *, const void *)` is a **pointer to function**
- var name: `compar`
- var type: `int (*) (const void *, const void *)`

- Function input: two `const void *`s
- Function output: **`int`**

`compar` is in the **code** section of the memory
- `compar`'s signature needs to **exactly** match the parameters in `qsort`.
```c
int compare_int(const void *a, const void *b) {
    int x = *(int *) a;
    int y = *(int *) b;

    if (x < y)      return -1;
    else if (x > y) return 1;
    else            return 0;
    //return x - y;
}
```
Usage:
```c
int a[5] = {100, 37, -2, 200, 0};
qsort(a, sizeof(a)/sizeof(a[0]), sizeof(int), &compare_int);
```
`&compare_int` points to the address. `&` can be omitted.
`compare_int()` will run the function.

`qsort` dereferences and calls `(*compar)(p, q)`

## Complex Declarations
C declarations **follows usage**. Postfix higher precedence.
```c
int a[3];       // array of 3 ints
char *b[3];     // array of 3 (char*)s
int (*f1) (const void *, const void *);
int *f2 (const void *, const void *);       // w/o ()
int (*f3[5]) (const void *, const void *);
```
Spiral rule:
- E. `int *p;`: `p` is a variable such that if you `*` it, it will be an `int`.
- `b` is an array of `3` pointers, where you `*` it, it becomes `char`
- `f1`
    - `(*)`: `f1` is a pointer
    - `(...)`: `*f1` is a function.
    - `int`: `*f1` is a function that returns `int`.
- `f2`
    - `(...)`: `f2` is a function.
    - `*`: `f2` returns a **pointer** to something
    - `int`: Once you deref it, becomes `int`.
- `f3`
    - `[5]`: `f3` is an **array of `5` elements**. 
    - `*`: `f3` is an array[5] of **pointers**
    - `(...)`: `f3` is an array of pointers **to functions**
    - `int`: `f3` is an array of pointers to functions **that return `int`**

`(*)` is a pointer to something that you call

# 10. Structures
Similar to Java's `class`, but you can't put functions inside
Typically defined outside `main()`. Usually in the header file. 
## `struct` layout
Don't forget the **`;`!!!**
```c
struct Point {
    int x;
    int y;
};

int main() {
    struct Point pt;
    pt.x = 2;       // dot is the member selection operator

    // Alternative initializations:
    struct Point pt = {2, 3};
    struct Point pt = {.x = 2, .y = 3};
}
```
`struct` is a new user-defined type. 

## `struct` size
When a `struct Point` is declared, on **stack**, 4 bytes are allocated for x, and 4 for y.

`sizeof(pt)` will be 4 + 4 = 8. 
```c
struct Foo {
    int x;      // 4 bytes
    char *s;    // 8 bytes
};

int i = sizeof(struct Foo);     // i = 16!
```
- First 4 bytes are for `int x`, but compiler **leaves out** a 4-byte **padding**
- Then 8 bytes for `char *x`

C allows compiler to layout the `struct` in memory. CLAC requires all 8-byte quantities must start at an address whose value is a **multiple of 8**. 4-bits must be at multiples of 4. 
- If reverse order by putting `char *s` first, compiler will still pad, in case of array `Foo[]`. 

## Pointer to `struct`
Continue from `struct point` declaration

`printf("%p", pt);` prints the pointer address.
```c
struct Point *p1;       // pointer to struct
p1 = &pt;

int *p2 = &pt.x;        // same address, but DIFF TYPE

printf("%p", p1 + 1);   // + 8 bytes!
printf("%p", p2 + 1);   // + 4 bytes

// Accessing pt.x
(*p1).x = 5;            // dereference, the select
p1->x = 5;            // same thing
```
**`->`** means dereference the **pointer**, then select

```c
struct Point pt[1];     // array of ONE element, same thing 
pt->x = 5;

struct Point a[10];     // a: xyxyxyxy...xy

// Declare on the heap
struct Point *p = malloc(10 * sizeof(struct Point));
```
By declaring array, `pt` can be used as a **pointer**, and we can use `->`.

### Memory optimization
If a `struct` variable is passed to a function, you are **copying** the entire `struct`. 

An entire array cannot be copied. Array will turn itself into a pointer.
```c
int get_num_element(int a[]) {   // As soon as you pass a, a becomes int *
    return sizeof(a) / sizeof(int);     // 8 / 2 = 4
}

int main {
    int a[10];      // here sizeof(a) / sizeof(int) = 10
    int n = get_num_elements(a);
}
```
Therefore, we usually pass **pointers to `struct`** to functions. 
- You can't have a `struct` that **contains itself**, but you can contain a **pointer** to it.

## Linked list

```c
// Linked list node
struct Node {
    struct Node *next;  // Pointer to the next node
    int val;            // value
};

struct Node *create2Nodes(int x, int y) {
    struct Node *n2 = malloc(sizeof(struct Node));
    if (!n2)    return NULL;    // check if malloc fails
    n2->val = y;
    n2->next = NULL;
    // A complete linked list with a last node

    struct Node *n1 = malloc(sizeof(struct Node));
    if (!n1)    {free(n2); return NULL;}    // have to free n2!!!
    n1->val = x;
    n1->next = n2;
    return n1;
}

int main() {
    struct Node *head;
    head = create2Nodes(100, 200);
    if (head == NULL)   exit(1);

    printf("%d -> %d", head->val, head->next->val);

    free(head->next);
    free(head);     // free tail, and then head
}
```
- A pointer of a node is our notion of linked list. 
- A `NULL` pointer is a linked-list with 0 nodes

| Stack     |       | Heap  |       |
| --------  | ---   | ----- |---    |
| head      | `n1` (-> `&n1.next`) | |
| --        |--     |       |
| `x`       |100    |       |
| `y`       | 200   |       |       |
| `n2`      | ->    |next   | NULL  |
|           |       |val    | 200   |
| `n1`      | ->    | next  | `n2` (-> `&n2.next`)|
|           |       | val   | 100   |

After return, `x`, `y`, `n2`, `n1` all gone, but the nodes are on **heap**. They remain. 
```c
free_all_nodes(head);

void free_all_nodes(struct Node *head) {    // recursion
    if (head == NULL)   return;
    free_all_nodes(head->next); 
    free(head);
}

int count_list(struct Node *head) {
    if (head == NULL)   return 0;
    return 1 + count_list(head->next);
}
```
## `struct List`
Real linked lists are more complicated and powerful.
- Previous element pointer
- Arbitrary data type storage (replace `int` by `void *`)
- Pointer to tail (easier to manipulate the back)
- Count of elements

A `struct List` can have more metadata

# 11. Libraries
## Macros
`#`s are preprocessed first and replaced
```c
#include "myadd.h"
#define PI (3.14)         // substitution
#define SQR(x)  (x * x)
// function calls are expensive (jump instruction), so macros are used
// put () everywhere to be safe
```
## `include` Guards
For code between different OS, we may need to do differently.

`mylist.h`
```c
#ifndef __MYLIST_H__    // if __MYLIST_H__ is not defined,
#define __MYLIST_H__    // define __MYLIST_H__ to exist
//...
#endif                  // closes if
```
`foo.c`
```c
#include "mylist.h"
#include "mylist.h"     // accidentally include it again
// Prevents double inclusion
```
## Archive files
Package all `.o` files into a single **archive** `.a` file
```make
ar rcs libnumbers.a power.o prime.o
```
- `r`: add `power.o` and `prime.o` to the archive (or replace them if already there)
- `c`: create archive file
- `s`: create an index to the contents to speed up linking

```shell
# link with library objects
gcc myprogram.o prime.o power.o -o myprogram

# link with library archive
gcc myprogram.o libnumbers.a -o myprogram
```
Linker knows to use object files within `libnumbers.a` directly.

## Using libraries
Headers and archives in non-standard locations
### `-I`
Look for **header** files
```shell
gcc -I/some/path -c foo.c
```
If `foo.c` `#include <some-header.h>`, it should also look for this header in `/some/path`.
Optional space or `\` after `-I`
### `-L` and `-l`
Looks for **archive** files, similar to `-I`
- `-L` tells **where** to look. Must appear **before** object files
- `-l` tells **what** archive file too look (**`lib<lib-name>.a`**). Must appear **after** object files
```shell
gcc -Lsome/path foo.o bar.o -lbaz
```
Linker will look for `libbaz.a` in `some/path`

You can pass multiple `-I`, `-L`, `-l` flags to link multiple locations of header and library files

# 12. Standard I/O
`scanf` and `printf` work on **standard input** and **standard output**

Standard channels:
- Standard input (connected to keyboard device)
- Standard output (typically terminal screen)
- Standard error (also output, connected to terminal; E. `valgrind` output)

## Redirection
```shell
vim input.txt

./isort < input.txt  
./isort > output.txt
./isort >> output.txt
```
- `isort` reads from standard input, but `<` makes shell change standard input from reading keyboard to reading `input.txt`.

- Same for `>`, changing standard output. Will overwrite original `output.txt`
    - `>>` **appends**, not overwrite
    - `2>` redirects **standard error** and overwrites; E. `valgrind` output

```shell
valgrind --leak-check=yes ./isort < input >> output 2> err
```

```shell
valgrind --leak-check=yes ./isort >> output.txt 2>&1
```
Redirect `stderr` (descriptor `2`) to where `stdout` (descriptor `1`) is going
- If `>> output.txt` and `2>&1` switched, won't work. `stderr` message will be printed out to `stdout`, which is the screen.'

## Pipes
**Pipe**: taking one program's output directly to the input of another program
```shell
echo 10 | ./isort
```
Bash runs `echo`. `|` runs two programs together. Bash redirects the standard output of `echo` and the standard input of `.\isort`.

```shell
echo 10 | ./isort | cat -n
```
If `cat` not given an argument (file name), it will behave like `echo`
- program `|` program
- program `>` file
- program `<` file

## Useful functions and examples
```Shell
cat *.txt | tr ' ' '\n' | sort | uniq > lecture-words
```
- `cat *.txt` concatenates all `.txt` files in pwd and outputs to `stdout`
- `tr ' ' '\n'` reads from `stdin`, translates every space to new line, and writes in `stdout`
- `sort
- `uniq`: removes duplicate lines. Need to be `sort`ed

```shell
w | tail -n +3 | grep "vim" | cut -d " " -f 1 | sed 's/$/@colubmia.edu/' | sort | uniq > vimusers
```
- `wc` reads a file, counts number of lines, words, and characters
- `head -n`  gives the first `n` lines
- `tail`
	- `tail -n +3`: display from 3rd line onward
- `grep`: matches REGEX 
	- E. `grep "vim.*c"`: gets all `vim` users working on `.c` files
- `cut`: cuts content afterwards
	- - **`-d " "`** specifies the delimiter `" "`to use for separating fields.
	- **`-f 1`** tells `cut` to select the first field from the split text (i.e., everything before the first space in each line).
- `sed`: find and replace
	- **`s/`**: substitute
	- **`$`**: **end of a line** in `sed`.
	- **`@colubmia.edu`** text you're appending at the end of each line.
	- **`/`** delimiters separating the parts of the `sed` command.

Collect all users using `vim` and their emails, sort them, and remove duplicated (by `uniq`). Save the output to `vimusers`.

```shell
echo hello | mutt -s hi mg4264@columbia.edu
```
Sends "`hello`" , with subject `hi`, to receiver "mg4264@columbia.edu"
```shell
for i in $(cat vimusers); do echo $i; done
```
Substitute the result of `cat` into command line. `echo`es all lines in `vimusers`
```shell
for i in $(cat vimusers); do mutt -s sorry-for-spam $i < content; done
```
If you have a separate file `content` for the body of the email. Subject is "sorry-for-spam"

For pipeline `|`, you can't control the **order** of program run. Pipe facilities have mechanisms to block some programs from running before getting input.

# 13. File I/O
`stdin`, `stdout`, `strerr` are declared in `stdio.h` by `FILE` pointers
```c
extern FILE *stdin;
extern FILE *stdout;
extern FILE *stderr;
```
Anything we can read/write are files (E. hardware device, network)

In UNIX, a file is a sequency of bytes with a position (file stream)
## FILE pointers
`ncat.c` `cat`s the file and adds line numbering
```c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
	# checks number of command line arguments
    if (argc != 2) {
        fprintf(stderr, "%s\n", "usage: ncat <file_name>");
        exit(1);
    }
```
`fprintf` prints to standard **error** instead of output

```c
    char *filename = argv[1];
    FILE *fp = fopen(filename, "r");
    # If fopen failes:
    if (fp == NULL) {
        perror(filename);
        exit(1);
    }
```
`fopen()` opens a file in `"r"` (read). It returns a `FILE *`, a **handle** for the file.
- `FILE` not a built-in type. It's `typedef`ed. Differs between OSs (opaque handling)
- Other flags: read, write, append, ...
In OS perspective, the file organization is complex (lots of metadata). Costly to refer by **name**. 
`fopen()` tells OS to **get ready**, and OS finds all metadata and prepares structure in memory, so that next time you want to read it, it knows where to go.
- `perror` passes `filename`, and prints the last thing that gets wrong

```c
    char buf[100];
    int lineno = 1;
    while (fgets(buf, sizeof(buf), fp) != NULL) {
	    # prints line number, 4 spaces wide, right justified
        printf("[%4d]", lineno++);
```
- `fgets()` reads **one line** (including `\n`) of file content and put them into `buf`, adding `\0`
- Once it reaches end of file, or if **something fails**, it will return `NULL`
```c
    char *fgets(char *buffer, int size, FILE *file);
```
- What if the line is longer than 99 characters (`buf` - `\0`)? `buf` will read up to 99, terminating with a `\0`. The next time `fgets()` is called, it will **continue**.
- What if I make size of `buf` small, like 20? 
	- When `fgets()` called, it only read 19 characters. The next iteration of `fget` picks it up, BUT `lineno` is changed no matter what. BUG!!
	- Want to see if the last read character is **`\n`**. If not, don't print the line number.

```c
        if (fputs(buf, stdout) == EOF) {
            perror("can't write to stdout");
            exit(1);
        }
    }
```
`fputs()` prints one line, opposite of `fgets`, **writing** to a given file
- Here in the code, we write in `stdout` (screen)
- `stdout` and `stderr` are **treated as files**.

```c
    if (ferror(fp)) {
        perror(filename);
        exit(1);
    }
```
`fgets()` returns `NULL` in two cases:
1. If there's nothing more to read
2. If something actually **fails** in the middle. Need to distinguish by calling `ferror()`(), "Did you terminate it normally?"

```c
	# close the file (free memory and stuff)
    fclose(fp);
    return 0;
}
```

## Open and Close
### Open
OS will locate the file, read the metadata first, and prepares some internal structures to keep track of the file. Prepares a file structure (`FILE`), and returns a pointer to it
Get a `FILE` pointer corresponding to any other file
```c
FILE *fopen(const char *pathname, const char *mode);

FILE *fp = fopen("myfile.txt", "r");
```
Returns a pointer to `FILE`, `NULL` if failed
Both arguments are **strings**
Mode argument:

| `mode` |             | if exist  | if doesn't exist | stream position                  |
| ------ | ----------- | --------- | ---------------- | -------------------------------- |
| `"r"`  | Read        |           | **fail**         | beginning                        |
| `"w"`  | Write       | overwrite | create           | beginning                        |
| `"a"`  | Append      | keep      | create           | end                              |
| `"r+"` | Read/write  |           | fail             | beginning                        |
| `"w+"` | Write/read  | overwrite | create           | beginning                        |
| `"a+"` | Append/read | keep      | create           | end (init stream pos is sys dep) |
Whatever`+` is the primary mode (treat as if you open with that `mode`)

### Binary file
Add `"b"` (E. `"wb"`, `"w+b"`) to specify the file to be opened in **binary**
Without `"b"` option, Windows translates newline `\r\n` to `\n` when reading, and vv when writing
- Windows: `"hello"` will take 7 bytes on disk, with `"\r\n"`, 6 bytes in memory
- Linux: 6 bytes
However, for non-text files, we don't want such translation

### Close
```c
fclose(fp);
```

## Writing output
```c
int fputc(int c, FILE *file);
int fputs(const char *str, FILE *file);
```
Writes `str` to `file`, **not** including the `'\0'`, returns `EOF` (-1) on error
```c
size_t fwrite(const void *p, size_t size, size_t n, FILE *file)
```
Writes an arbitrary number of bytes (`n` objects) out to a file stream, including null bytes
- `p`: Pointer to the first element of an array of these items
- `size`: size of each item
- `n`: number of items
Returns the number of successfully written objects (<`n` if error)
```c
fprintf(fp, "hello, world\n");
fputs("hello world\n", stdout);  // No string formatting
fputc('o', stderr)               // single character
```

## Reading input
```c
int fgetc(FILE *file);
char *fgets(char *buffer, int size, FILE *file);
size_t fread(void *p, size_t size, size_t n, FILE *file);
```

**Blocking**: OS can't return immediately something, so it pauses progress execution until it's ready to unblock

Example: `sleep(1)`: blocks until 1 seconds later
If you call `fgets()` on `stdin`, program will block until you type something

```c
char buf[1024];
fgets(buf, sizeof(buf), fp):     // reads at most 1023 bytes to buf ('\0')
fread(buf, 1, sizeof(buf), fp);  // reads 1024 bytes
```
`fgets()` returns either when there's a **new line** or `buffer` fills up, but it guarantees the buffer is `'\0'` terminated
- Returns `NULL` on `EOF` or error (call `ferror()` after to find error)
`fread()` better for arbitrary binary data
- Returns the number of objects successfully (not partially) read
- If less than requested, `feof()` and `ferror()` will distinguish `EOF` or fail
### `EOF`
Happens when reach the end of the byte sequence. Cursor is past the end of the stream
When reach `EOF`, `fgetc()`, `fgets()`, `fread()` will **unblock** immediately (same for error though)
- `fgetc()` returns -1
- `fgets()` returns `NULL` pointer
- `fread()` returns less than the number of items you asked for

`feof()` returns `1` at `EOF`

`EOF` also happens at `stdin`, by pressing `Ctrl-D`
## Buffering
```c
printf("hello...");
sleep(3);
printf("world\n");
```
`"hello..."` will not be printed after `sleep`
Line buffering: `printf()` and other `FILE` output functions **buffer** bytes give to `stdout` and wait until reaching **`\n`** (terminal printing is expensive)

```c
fprintf(stderr, "hello...");
sleep(3);
fprinf(stderr, "world\n");
```
`stderr` is by default, **unbuffered**, because we don't want error messages to be delayed. 

Files are **block buffered**, buffed until a **fixed-size** buffer is filled (typically 4096 bytes), sends to disk until fill, flush, or program termination

### Flush
```c
printf("hello...");
fflush(stdout);     // Immediately flushes out "hello..."
sleep(3);
printf("world\n");
```

To manually **turn off** all buffering for a `FILE` pointer, making the second argument `NULL`
```c
setbuf(stdout, NULL);
```

## File seeking
Change the current position of the underlying stream
```c
int fseek(FILE *file, long offset, int whence)
```
- New position added by `offset`, can be negative
- `whence`: 
	- `SEEK_SET`: offset from beginning
	- `SEEK_CUR`:  from current position
	- `SEEK_END`: end-of-file
- Returns `0` on success, else error

## Formatted I/O
- `%d`: `int`
- `%u`: `unsigned int`
- `%ld`: `long`
- `%uld`: `unsigned long`
- `%f`: `double`
- `%g`: `double` (trailing zeros not printed)
- `%s`: string (`char *`)
- `%p`: pointer address (`void *`)
```c
int scanf(const char *format, ...);
int fscanf(FILE *stream, const char *format, ...)
int sscanf(const char *input_string, const char *format, ...);
```
Returns the number of items assigned.
Variable number of arguments (variadic functions)
`sscanf()` parses from `input_string`!
Example: `
```c
input_string = "  \t   0xffffffff \n ;
sscanf(s, "%x", &u)
``` 
will skip all spaces, **look** what looks like a number, and terminate reading once it hits a space.

```c
int printf(const char *format, ...);
int fprintf(FILE *stream, const char *format, ...);
int sprintf(char *output_buffer, const char *format, ...);
int snprintf(char *output_buffer, size_t size, const char *format, ...)
```
All **return**  the number of `char`s printed (not including `'\0'`).
`sprintf()` writes to the `output_buffer` string. 
- `output_buffer` is assumed to be large enough, or else will overrun. **Dangerous function**, stack smashing
`snprintf()` only prints `size` number of bytes, including `'\0'`, 
- Typically, `n` in function name means there's a **size limit** of `n` bytes
- It returns the number of `char`s it **would have printed** if it is allowed more space
	- If this return value not used, there will be a **warning**
	- Use `-Wno-format-truncation` flag to disable this warning
## `cutstr.c`
If just run as it is, nothing will be run

```c
#define CASE1
```
This runs `CASE1`
Or, can `define` on command line
```shell
gcc -DCASE2 cut-str.c
```

`strncpy` similar to `strcpy`, but only copies `n` characters. However, if it goes **over** the limit, it will **not** include `'\0'`.
- `printf` will print over, random crap

## Lab 4
`mdb`: message database

Each message is 40 bytes (if 6 messages, then 240 bytes)

If you have your own database , so 
```shell
./mdb-add mdb-cs3157   # if you have write permission
```

```shell
./mdb-add-cs3157       # hard coded the database to mess with permissions
```

Size of `struct MdbRed` is 40 bytes, first 16 being `name`, second 24 being `msg`

`mdb-add` calls `fgets()` and `strcpy()` or `snprintf()` to copy `name`, cutting it off at 15 (allow **`NULL`** at the end!!). Then copies 23 characters of `msg`

For lookup, 
1. Opens the file in `"rb"` mode
2. Goes into a loop reading each record (`fread()`) for 40 bytes
	1. As it reads, appends the `struct` (**heap allocated**) into a linked list (`addAfter`)
	2. Until `fread()` returns 0 (`EOF`)
3. Prompts the keyword to lookup (calls `fgets() != EOF`): 
	1. Searches thru the list for all the records
	2. Examine the message
	3. `strstr()` tells if a string contains a substring
	4. Prints output
	5. Until `fgets()` returns `EOF
Copy `mdb-add*`, `mdb-lookup*` in the directory for reference

# 14. Endianness
Order of bytes are stored in computer memory
## Inspecting binary files
```c
int b;
while ((b = fgetc(fp)) != EOF)
	printf("%x\n", b);
```
Prints each byte from `fp` to `stdout` in hexadecimal

`endian-demo.c`: `if` block and `else` block
Example input (4-byte `int`):
`0x00010203` (`00000000 00000001 00000010 00000011` in bin) (66051 in decimal)
```shell
xxd endian-demo.host
00000000: 0302 0100
```
- Left: Byte offset of each row in hex
- Mid: file content (2 bytes, 4 hex digits) at a time
- Right: ASCII file content (`.` for non-printable)

CLAC happens to store integer in **memory** in **reverse**, in unit of **byte**
+----+----+----+----+
|  03  |  02  |  01  |  00  |
+----+----+----+----+

- This is specific to CLAC, called **little Endian** machine.
	- Before, computers are small, so they started with 8-bit register (8086). For backward **compatibility**, this reverse representation is better
- **Big Endian** machine stores in normal order, aka **network** byte order

- Typically don't care. The computer takes care of it! 
	- Does not affect MSB/LSB, or any program operation
- May be problematic: 
	- Between file systems
	- Internet IP address (packed in 4-byte native integer), which is big Endian!
```c
unsigned int n;               // = 0x00010203
fread(&n, sizeof(n), 1, f);   // in `f`: 0302 0100
char *p = (char *)&n;         // treat number as a char[4]
printf("%.2x", p[0]);         // will print "03"
```

## Conversion
`htonl`: host to network long (4 bytes)
```c
#include <apra/inet.h>

uint32_t htonl(uint32_t hostlong);
uint16_t htons(uint16_t hostshort);
uint32_t ntohl(uint32_t netlong); 
uint16_t ntohs(uint16_t netshort);
```
- Convert on little Endian host
- **No change** on big Endian host itself. 

# 15. Multiprocessing
(Not multi**threading**: 2 functions within the same process running at the same time)
## Process
Each **instance** of a running program is a **process**. There can be many processes of the same program. Example: running `vim` twice

Each process has its own ID (PID)
- `getpid()`: obtains a process's PID
- `getppid()`: obtains PID of the parent. 
## `fork()`

`fork()` is a special **system call**. Needs to ask the underlying OS to do special stuff. 
```c
pid_t fork(void);
```
When `fork()` is called, 
- The process is suspended. **Kernel** takes over. 
- OS **freeze** the process's memory address space (memory, static, heap, stack). 
- Takes a **snapshot** and **all** current status
- **Clones** the status
- Let the two processes go **independently**. Nothing shared.

### `fork()` return
Returns the PID (`pid_t`) of its **newly created** child. **Many** children can be created
- If parent, `p > 0` (returns child PID)
- If child, `p = 0` (no child, not a valid process ID)
- If failed, `p < 0` (E. too many already)
Then, both parent and child resume from the place where **`fork()` returned**. Values may be different
- No guarantee of execution **order**, unless explicitly coordinated (`waitpid()`)

`partnet-child.c`
Two branches **run at the same time**!! `fork()` splits program into two, and runs together. 
```c
pid_t pid = fork();
// Both parent and child will resume execution HERE

if (pid == 0) {
	// Child
	printf("This is the child, my PID is %d\n", getpid());
} else {
	// Parent
	printf("This is the parent, my child's PID is %d\n", pid);
}
// Both will print Hello
printf("Hello\n");
```
### Exit status and `waitpid()`
A process terminates with an integer exit status code (`0` for success, else error)
- Return value of `main()`
- Termination of `exit(int status)`

**Reaping child**: parent process waits until child terminates, retrieving the child's exit code
```c
pid_t waitpid(pid_t pid, int *wstatus, int options);
```
- `pid`: PID of the process to wait for
	- `-1` to wait for **all** its children
- `wstatus`: pointer to place to write the terminated child's exit code
	- `NULL` if not interested
- `options`
	- `0`: normal. Block until child terminates
	- `WNOHANG`: never blocks. 
		- If a child terminates, return its PID
		- If all child(ren) is still running, return `0`.
- *Returns* PID of the child process reaped, or `-1` on error

*Zombie process*: a child that has terminated but not yet reaped. OS keeps metadata on it, so parent **must reap** children
*Orphan process*: parent terminates **before** child. Adopted by `init` process and automatically reaped when terminated. Not bad
## Executing programs
When `fork()`ed, the child runs the **same program** as the parent. 
Change program through the `exec()` family of functions: `execl()`, `execlp()`, `execle()`, `execv()`, `execvp()`, `execvpe()`

`ap-shell.c`
Runs shell inside a program. 
```shell
ps af

-bash
 \_ .a/.out
	 \_ /bin/bash
```
### `execl()`
`execl()` replaces the current process image with a new process image (program). 
- Process continues: PID and PPID retained
- **Memory space completely reset** (stack, heap, ...)
- New program starts to run from its `main()`
```c
int execl(const char *pathname, const char *arg, ...
		 /* (char *)NULL */);
```
- `pathname`: the name of the program that gets turned into
- `arg`: variadic function, list of strings to form the `argv` array passed to the `main()` of the next function
	- Terminated by `(char *)NULL`
```c
execl("/bin/echo", "/bin/echo", "hello", (char *)NULL);
printf("This should not be printed");
```
This imitates `/bin/echo hello`
- If `execl()` goes *well*, it **will not return**. The process is turned into `echo`, and terminates. The old program is **erased**.
### `execv()`
`execv()` takes the `argv` array directly:
```c
int execv(const char *pathname, char **argv);

char *argv[] = { "/bin/echo", "hello", NULL };
```
- `argv`: (actually `*argv[]`): the `argv` array **passed to the `main` of the next function**
	- Need to tokenize the input to take additional params
If `execvp()` used, will automatically loop through common directories (`/bin/`)

```c
while (fgets(buf, sizeof(buf), stdin) != NULL) {
	pid = fork();
	if (pid == 0) {  // child process
		// DOES NOT support additional params
		char *argv[] = { buf, NULL };
		execv(argv[0], argv);
		// Got here means something wrong with execv()
		die("execl failed");
	} else {         // parent process
		if (waitpid(pid, &status, 0) != pid) {
			// If a different child reterns, die
			die("waitpid failed");
		}
	}
}
```
`waitpid()` does not return until child **terminates**. 
- If child different, die

# 16. UNIX
- Application: ls, vim, gcc, chrome, `mdb-lookup-cs3157`
- Library functions: `printf()`, `malloc()`
- System calls: `write()`, `fork()`, `execl()`
- OS kernel: Linux, windows NT
- Hardware: processor, memory (RAM), disk, GPU, keyboard

## How shell works
### System
```shell
ps afj     # prints in a forest, shows parent-child rel
```
- `a` shows all processes
- `f` shows in forest
- `j` Shows `PPID` (parent)
- `x` shows system-wide stuff (E. `sshd`)

In the output, parent often goes first, but can't exactly control.  Unpredictable. Controlled by OS. 

When you run a program on `bash`, `bash` **forks itself**, and the child turns itself into the executed program. 

How's the very first process started? Hand-stitched by the OS kernel at startup. Called `init`. PID: 1
## Users and file permissions
`-rwxr-xr-x 1 mg4264 student 12345 Oct 31 17:04 mdb-lookup*` 
- Permissions:
	- `-`: regular file
		- `d` for directory, `p` for pipes
	- `rwx` **owner**: read, write, execute
	- `r-x` **owning group**: can't overwrite (recompile)
	- `r-x` **everyone** else: can't overwrite
- `mg4264`: owner (actually represented as number, seen from `id` command)
- `students`: owning group (number)
- `12345`: binary size of file size
- Timestamp
- File name

### Octal representation
Binary: 1 for enable, 0 for disable (`111101101`). Octal: `755`

### Change permission
Only **owner** can change!
```shell
chmod -x foo      # turns off for myself
chmod go+x foo    # turns on for g and o
chmod a+x foo     # turns on for ALL
chmod 755 foo

chown root foo    # change owner to root
```

For `mdb-cs3157`, you don't have the **write** permission. If you run some program (`vim`), permission check still fails. You can't change it via regular programs
- `mdb-add-cs3157` has permission `rws`. 
	- `s`: set user id. When you run it, it runs as the **owner** of the program
Gives **limited** permission to others

### Directory permissions
- `r` allows reading content 
	- `ls` allowed,
	- `ls -l` (metadata) needs `x` permission
- `wx` allows modifying content (create, delete, move)
	- `w` alone is meaningless!
- `x` for **entering**
```shell
drwx------  2 jae jae  5 Nov 12 23:50 2bin/      # not accessible
drwxr-xr-x  2 jae jae 13 Nov 12 23:50 bin/       # accessible
```
Need to give `x` permission to **all parent** directories
- You may not have `r` permission to see the contents, but you can **physically be** there and redirect yourself to the subfolders.

## Shell scripts
Text file that can be interpreted by some program
`ls4.sh`
```shell
for i in {1..4}
do
	ls
done
```
```shell
/bin/bash ls4.sh
```
Can't do `./ls4` on shell. Must do `bash ls4`, because you don't have **execution** permission by the file owner.

To give execution permission:
```shell
chmod +x ls4.sh
./ls4.sh
```
Now `ls4.sh` has the `*` label in `ll` listing.

Using `ap-shell.c`:
```shell
./ap-shell
AP> ./ls4.sh
```
**Fail!** `execv()`(carried by the OS) does not accept `./ls4.sh`. 
How did it work in our `bash` shell? 
- `bash` calls `execv()`. 
- If failed, `bash` tries running it directly. 
Will not work for shells other than `bash`, that uses a different language

### `shebang` directive
At the **top line** of the shell script, put the full **path** of the program that can run the rest of the file
```shell
#!/bin/bash/
for i in {1..4}
do
	ls
done
```
OS looks at the first 2 bytes of the file. If  begins with `#!`, 
- `execv()` syscall executes the specified process `/bin/bash` 
- The original script file `ls4.sh` is passed to the `argv` array.
- Same as `/bin/bash ls4.sh`
Now *any* shell can interpret it, including `ap-shell`

## Lab 5
### Part 1(a)
- `$$`: PID of the shell running the script
- `$1`: first argument

### Part 1(b)
```shell
\_ sshd: mg4264 [priv]
	\_ sshd: mg4264@pts/2
		\_ -bash
			\_ ./jaes-nc-1 5201
				# execl of child process. PID printed
		         \_ /bin/bash ./mdb-lookup-server-nc.sh 5201
		            \_ cat mypipe-364820
			        \_ nc -l 5201
				    \_ /bin/sh /home/jae/cs3157-pub/bin/mdb-lookup-cs3157
		                \_ /home/jae/cs3157-pub/bin/mdb-lookup /home/jae/cs3157-pub/bin/mdb-cs3157

```
Find process tree of all ancestors: Trace thru all `PPID`s, such as `1` (`init`) . `0` is not a valid process. 
Then you can launch another child process. Printing order is messed up. Do not `sleep()`. 
### Part 1(c)
Improved version that asks you for a port number
- Keeps `fork()`ing child processes and launching multiple servers
	- If permission denied, remove FIFO
	- If quit on client side, remove FIFO
	- Before printing another prompt, report which process has terminated so far. 
		- (Can't report it right away because blocked by `fgets()`, then parse into a number). 
		- A new process can be simultaneously launched there
		- After child terminates, sit there and waits for parent retrieval. 
		- Need to find out whether children have terminated
			- Can't simply call `waitpid()` normally. Stuck in case not terminated
			- `pid = waitpid( (pid_t) -1, NULL, WNOHANG)`. Never block. Returns immediately whether the children. 
				- `-1` is a special number, indicating that ANY child has terminated.
		- Finally, print another prompt
~ 30 lines of code

# 17. TCP/IP
## Internet Protocol Layers
Interconnection between *networks*
Do minimal first, and let the **higher layers** figure out the next.
Layers:
1. **Physical**: radio wave, light, wire
2. **Link**: sends packets over connection, rather than voltage variations (E. ethernet, wifi)
3. **Network**: (global) receive info, and **forward** it to the next direction (E. Internet Protocol-**IP**, IPv4, IPv6)
	- **Routers** carry packets between places by IP address. 
		- Address should contain certain location information.
		- MAC address: unique to each device. Won't work for IP, since does not carry any location info. 
	- IP address (E. 128.59.2.5) 
		- Dotted quad notation. Each number is a **single** byte (0-255). 
		- Packets have header in source/destination IP addresses (network order)
		- Running out of addresses! Use **N**etwork **A**ddress **T**ranslation. Router gives out fake public IP addresses to all its devices, and have a mapping between the fake address to the real. (range, private IP addresses: 192.168.x.x)
	- If you send a package to China (Chinese IP)
		- Goes through nearest gateway router (Columbia)
		- Gateway sends it west (based on location info)
		- The **closer** you get to destination, the routers know more
		- Boarder gateway protocol -- BGP
	- IP protocol doesn't guarantee anything. If packet dropped in the middle, **No recovery** -> 4
4. **Transport**: manages packet flow **pipeline** (E. TCP, UDP)
	- Using this unreliable IP, build a clean, working pipeline, **in order** 
	- Broken into sequential chunks
	- Congestion control
	- Multiplexing (port number)
5. **Application**: Interpret transported data (E. HTTP, SMTP (email), SSH, `ncat` (does nothing, simply exposes L4 layer))
	 - Access through sockets API (application programming interface, lab3 is linked list API)
IP is the bottle neck. Top/bottom layer needs to take a lot of stuff

## TCP/IP Networking
TCP establishes reliable bidirectional channel. (`ncat`)
- Reliable: packets never dropped, corrupted, reordered
- Bidirectional: both server and client can send and receive
![tcp.png](f24/CS3157-AP/images/tcp.png)
Hosts are identified by 
- IP address
- or domain name `clac.cs.columbia.edu` (`clac` within local network). Translated to IP address using Domain Name System (DNS)

### Port number
a 2-byte integer (`short`)
```shell
dig clac.cs.columbia.edu
nc 34.145.159.110 10000

nc localhost 10000
nc 127.0.0.1 10000           # localhost IP address
```

- Server **listens** to a port number
- Client **connects** to the server with server's IP and port number the server is listening on
Convert host name to address:
```c
struct hostent *he;
if ((he = gethostbyname(serverName)) == NULL) 
    die("gethostbyname failed");
char *serverIP = inet_ntoa(*(struct in_addr *)he->h_addr);
```

## `netcat`: TCP/IP tool
Similar to `cat`, but thru network

**Server mode**: runs first, then **listen** for incoming connections
```shell
nc -l 20000
```
- `ssh` is a client program that connects to a server program `sshd`
	- Find a server in `clac.cs.columbia.edu` and knock on its `sshd` program

**Client mode**: specifies the server to knock on, and then make connections. 
```shell
nc clac.cs.columbia.edu 20000
```

**Flags**
- `-N`: close connection upon `EOF` on `stdin`
- `-C`: end lines with `\r\n`, useful for HTTP

Now they have made a TCP connection (Transport connect protocol)
- Hides all the complexity and gives a clean pipeline of sending/receiving files
Whatever entered on one end will show up on the other end. Done on **both** sides
- `netcat` reads from `stdin`, and sends via network
- Other side receives, until something comes from the network, spits to `stdout

How is it possible? You are stuck on `fgets()`! How can it print out simultaneously: **fork** (or something more advanced)  
### Turn `mdb-lookup` to network server
Server side:
```shell
nc -l 20000 < tmp | ./mdb-lookup-cs3157 > tmp
```
Sends server input to `mdb-lookup`
Won't work with normal file!
- Pipe **blocks** until the first program outputs, before the second program reads
	- There is no `EOF` for a pipe. It will just wait
- File redirection: no guarantee. If `EOF` encountered, done

Need a special file that *acts like a pipe*: **named pipe**, created by `mkfifo` (make first-in-first-out, aka pipe)
This file will never have content. Size always 0. Just an entry point
```shell
mkfifo mypipe

nc -l 20000 < mypipe | ./mdb-lookup-cs3157 > mypipe

cat mypipe | nc -l 20000 | ./mdb-lookup-cs3157 > mypipe    # same thing
```
`stdout` of `nc`  piped to `mdb-lookup`, whose output goes to `mypipe`, which is fed back into `nc`
## File Descriptors
- In UNIX, native file handles are **integers** called *file descriptors*.
- C file descriptors are **wrappers** on top. `fopen()`, `fread()`, `fwrite()` eventually call its UNIX counterparts: `open()`, `read()`, `write()` **system calls**
- `stdin`: 0
- `stdout`: 1
- `stderr`: 2
- New files opened fd: likely 3
`toupper.c` needs to be compiled with `STDIO` or `UNIX` defined. Reads stuff and prints capitalized.
`UNIX`
```c
ssize_t write(int fd, const void *buf, size_t count);
int open(const char *pathname, int flags);
```

`toupper.c`
```c
#ifdef UNIX
	int fd_in = 0;
	int fd_out = 1;

	while (read(fd_in, &c, 1) == 1) {
		c = toupper(c);
		write(fd_out, &c, 1);
	}
#endif
```

Once a TCP connection is made, it will be made to a **file descriptor**. 

## Sockets API
*Socket*: **Endpoint** for a reliable, bidirectional connection (E. TCP)
- Bound to IP address and port number
- Something you can plug in, but won't go anywhere
Associated with **file** descriptors. Can use with I/O system calls `read()`, `write()`, `close()`
```c
int socket(int domain, int type, int protocol);
```
- `AF_INET`: IPV4 protocol
- `SOCK_STREAM`: layer-4 technology using: TCP
- `0`: 
Return: if `< 0`, failed!

### Client
`connect()` the socket file descriptor to the server address
```c
int fd = socket(...);
connect(fd, ... /* server address */);
// Communicate with the server thru read() and write()
close(fd);
```
A `connect()`ed socket will be create later by `accept()` on the server side

### Server
1. `socket()` creates a **listening** socket
2. `bind()` socket to a **port** that should be known to the client
3. `listen()` sets up listening socket for incoming connections. Client can `connect()` at here.
	- Clients can queue up, waiting for server to call `accept()`.
4. `accept()` incoming connections
	- Will **block** until a client connects
	- Returns **file descriptor** of a **new** socket (`clnt_fd`) for each new client
		- `servsock` is a template to create the new `clntsock` connection.
	-  Now there is a virtual pipeline where packets are byte flow.
5. One side calls `close()` after communication done
	- Other side detects it and calls `close()` as well
```c
int serv_fd = socket(...);
bind(serv_fd, ... /* server address */);
listen(serv_fd, ... /* max pending connections */);
while (1) {
	int clnt_fd = accept(serv_fd, ...);
	// Communicate with client thru read() and write()
	close(clnt_fd);  // terminates TCP connection
}
```

![sockets](f24/CS3157-AP/images/socket.png)

### Socket address `struct`
`connect()` and `bind()` requires specifying **server**'s address and port using `struct sockaddr`
```c
// connect requires struct sockaddr. Need to be casted
struct sockaddr {
	sa_family_t sa_family;
	char sa_data[14];
};
struct sockaddr_in {
	sa_family_t sin_family;            // address family: AF_INET
	uint16_t sin_port;                 // port in network order
	struct in_addr sin_addr;           // address
};
struct in_addr {
	uint32_t s_addr;                   // address in network order
}

// destination address
strcut sockaddr_in servaddr;
memset(&servaddr, 0, sizeof(servaddr));     // zero out memory
servaddr.sin_family = AF_INET;              // address family
servaddr.sin_addr.s_addr = inet_addr(ip);   // address in network order
servaddr.sin_port = htons(port);            // port in network order
```
`connect()` looks at the first two bytes, and casts pointers to address the contents (polymorphism)
Send connection packet to server, wait for acknowledgement. 
- `sock`: your end of the TCP connection
- IP address of server and port number connected in `struct`
Return `0` if successful. Now socket is an **established** connection. Good endpoint for established virtual pipeline
- `<0`: failed
Very crude way of OOP

## Sockets I/O
Once TCP/IP connection established on a socket, can communicate with `read()`, `write()`
```c
int write(int fd, const void *buf, size_t len);
int read(int fd, void *buf, size_t len);

int send(int sockfd, const void *buf, size_t len, int flags);
int recv(int sockfd, void *buf, size_t len, int flags);
```
- `sockfd`: destination
- `buffer`: with characters sent
- `length`: how many bytes to send/receive
- `flags`: `0` means normal behavior (`write(sock, buf, len)`, where `sock` ana. `FILE`), **blocks** until sends all bytes requested
`send()`
- Return: number of bytes sent, `-1` on error
`recv()`
**Blocks** until it has received at least 1 byte
- Return num bytes received
	- `0` if **connection closed** by other party
	- `-1` in error

### Wrapped `FILE` Descriptor
No syscalls equivalent to `fgets()` or `fprintf()` :(
We can **wrap** a file descriptor using `fdopen()` (*d*!), returns a **`FILE *`** 
```c
FILE *sock_fp = fdopen(sock_fd, "wb");
fprintf(sock_fp, ...);
fclose(sock_fp);                      // will close() underlying socket fd
```
May need `setbuf()` or `fflush()` to ensure **buffered** output actually sent through

Not good to use it for **both** read and write (`r+`) on the **same** `FILE *`. C requires to `fseek()` every time you switch between read and write
Or use `dup()` to duplicate socket descriptor and create two separate `FILE *`s
```c
FILE *input = fdopen(socket_descriptor, "r");       // read-only FILE pointer  
FILE *output = fdopen(dup(socket_descriptor), "w"); // write-only FILE pointer  
// ...  
fclose(input); 
fclose(output);
```

## `echo` server example
`tcp-echo-client.c` and `tcp-echo-server.c`
One a connection is established, 4 couples:
1. IP address of server
2. Port number server is listening on
3. IP address of client (unseen)
4. Port number where client came from (unnoticed, underneath. OS randomly picks a number for client and sends to server at initialization. Server remembers it so it can reach client)

Client sends server a packet of characters. Sometimes receive all characters, but sometime split. **You can't control message boundaries in TCP**
If messages are bigger, don't know how things will be broken up. 

- Client **quits** once it receives everything. 
- Server is perpetual, waiting for new client after current one ends

### Client
```c
// ./client <server-ip> <server-port>
const char *ip = argv[1];
unsigned short port = atoi(argv[2]);   // port number is short

// socket(): your end of the connection
// Like a file descriptor, pass to read and write
// open socket has a descriptor, likely #3, after stderr
int sock = socket(AF_INET, SOCK_STREAM, 0);    
connect(sock, (struct sockaddr *)&servaddr, sizeof(servaddr));

char buf[100];
fgets(buf, sizeof(buf), stdin);
size_t len = strlen(buf);

send(sock, buf, len, 0);

int r;
while (len > 0 && (r = recv(sock, buf, sizeof(buf), 0)) > 0) {
	fwrite(buf, 1, r, stdout);   // only printing r chars
	len -= r;
}

close(sock);
return 0;
```

### Server
```c
// ./server <server-port>
unsigned short port = atoi(argv[1]);

int servsock = socket(AF_INET, SOCK_STREAM, 0);

strcut sockaddr_in servaddr;
memset(&servaddr, 0, sizeof(servaddr));
servaddr.sin_family = AF_INET;
servaddr.sin_addr.s_addr = htonl(INADDR_ANY);  // any netowrk interface, 
// INADDR_ANY = 0.0.0.0. If you want WIFI, only, you'll pass specified
servaddr.sin_port = htons(port);               // port # you choose to listen on

// Bind to local address, grab the port. 
// Other program will fail to bind the same port
bind(servsock, (struct sockaddr *) &servaddr, sizeof(servaddr));

// Start accepting client connections. Queue (5) requests up at OS level
// Now clienct can connect()
listen(servsock, 5);

// CLIENT address
struct sockaddr_in clntaddr; 
int r;  char buf[10];
while (1)
{
	socklen_t clntlen = sizeof(clntaddr);

	// accept() gives client side info
	// clntsock is a NEW socket for further communication
	int clntsock = accept(servsock, (struct sockaddr *) &clntaddr, &clntlen);

	// only pass CLIENT side
	// keep receiving and sends back the chunk it reads (until client closed)
	// recv() blocks until at least 1 byte received
	while ((r = recv(clntsock, buf, sizeof(buf), 0)) > 0)
		send(clntsock, buf, r, 0);

	close(clntsock);
}
```
## File transfer program
File transfer program that runs on any TCP communication program
Sender:
```shell
./sender 127.9.9.1 10000 <filename>
```

Receiver:
```shell
./recver 10000 foo
```
Files received will be named `foo.0`, `foo.1`, ...

Not complete. Does not check file name or error
### `tcp-sender.c` 
(client side)
0. Boiler plate code, `socket()`, prepare address `struct`, `connect()`

1. Send file **size** as 4-byte `uint` in **network** order
```c
FILE *fp = fopen(filename, "rb");
struct stat st;
stat(filename, &st);
uint32_t size_net = htonl(st.st_size);
send(sock, &size_net, sizeof(size_net), 0);
```
`stat(filename)` gives you info about file by filling in `struct stat`

2. Sends actual file content in 4K chunks  

	```c
	char buf[4096];               // 4K is an optimal for disk read
	unsigned int n; 
	unsigned int total = 0;

	while ((n = fread(buf, 1, sizeof(buf), fp)) > 0) {
		send(sock, buf, n, 0);    // if != n, die
		total += n;               // collect total bytes sent
	}
	// check for ferror()
	fclose(fp);
	fprintf(stderr, "bytes sent: %u\n", total);
	```

	Use `fread(buf, 1, sizeof(buf), fp)`. We may need to **partial** read 4K and know how many bytes read.
	For `send()`, the size needs to be **`n`**, to **prevent writing garbage**

3. Receive and verify file size **acknowledgement** from server
```c
uint32_t ack, ack_net;
int r = recv(sock, &ack_net, sizeof(ack_net), MSG_WAITALL);
ack = ntohl(ack_net);
```
*`MSG_WAITALL`* tells `recv()` to **block** until full request is satisfied (4-byte `ack_net` filled).
If still problem:
- If `r != sizeof(ack_net)`,
	- `r < 0`, `recv()` failed
	- `r == 0`, connection closed prematurely
	- `r > 0`, type is not `uint32`
- If `ack != size`, something content missing
	- Does not account for bit flips

4. Expects **server** to close connection

	```c
	char x;   // just receive a single byte (0)
	r = recv(sock, &x, 1, 0);
	assert(r == 0);

	close(sock);
	```

	`recv()` returns 0 when **server closes**

### `tcp-recver.c` 
(server side)
0. Boiler plate: `socket()`, set up `struct`, `bind()`, `listen()`

	```c
	FILE *fp;
	unsigned int filesuffix = 0;
	char filename[strlen(filebase) + 100];

	int r;
	char buf[4096];
	uint32_t size, size_net, remaining, limit;
	struct stat st;

	while (1) {
		accept();
		// generates file name and writes
		snprintf(filename, "%s.%u", filebase, filesuffix++);
		fp = fopen(filename, "wb");
	```
	`filename`'s size is dynamic. (stack allocated) 
	- Problem: no error checking. If it fails, program misbehaves. `malloc()` will return `NULL`

1. Receive file size
	```c
		r = recv(clntsock, &size_net, sizeof(size_net), MSG_WAITALL);
		// error checking here
		size = ntohl(size_net);
		fprintf(stderr, "size received: %u\n", size);
	```

2. Receive file content
```c
	remaining = size;    // supposed to receive
	while (remaining > 0) {
		limit = remaining > sizeof(buf) ? sizeof(buf) : remaining  // min
		r = recv(clntsock, buf, limit, 0);
		if (r > 0) {
			remaining -= r;
			fwrite(buf, 1, r, fp);
		}   // error check if r <= 0
	}
	assert(remaining == 0);
	fclose(fp);
```
Loop to keep `recv()`ing and write to the disk
Make sure to write only the *exact* number of bytes received.
In lab 6 part 2, we wrapped `recv()` with `fgets()` and `fread()`

3. Send file size back as acknowledgement
```c
	stat(filename, &st);
	size_net = htonl(st.st_size);
	send(clntsock, &size_net, sizeof(size_net), 0);
```

4. Close client connection, can `accept()` next client
```c
	close(clntsock);
}
```

# 18. HTTP
HyperText Transfer Protocol, application level
- HTTP clients request resources (E. html) from HTTP servers over a TCP connection

## URL anatomy
`http://www.clac.cs.columbia.edu:80/index.html`
- `http` HTTP protocol
- `www.clac.cs.columbia.edu` Domain name, translated to IP address
- `80` Port number
- `/index.html` **URI**
Once connection made, speak to HTTP to request `/index.html`. 

**URI** (Uniform Resource Identifier, `/index.html`) tells server the resource you want. 
- The server *interprets* "`/index.html`" and decides what resources to serve
- Typically, URI appended to some **web root** directory of server 
	- E. root is `/home/www/web`, server will respond with file at `/home/www/web/index.html`
- **Static**: server file content directly comes from **file system** 
- **Dynamic** web server may query other databases

## Browsing HTTP
1. Browser establishes a TCP connection with the server with the IP address
2. Browser sends HTTP request to the server for resource
3. Server responds, over the same TCP connection (fulfill or deny)
4. Browser parses HTML, makes subsequent requests for other resources, and renders the webpage

### Command-line
```shell
curl http://example.com/index.html     # prints to stdout
wget http://example.com/index.html      # saves page to disk
```
`curl --http1.0` forces using HTTP/1.0

### Client `GET` request
Getting index page from `ncat` (stored in `/var/www/html`)

```shell
nc clac.cs.columia.edu 80

GET /index.html HTTP/1.0            # request line
Host: clac.cs.columbia.edu:80       # header
									# /r/n blank line
```
- Request line: method (`GET`), URI (`index.html`), HTTP version (`HTTP/1.0`), space separated
- Header: field name, colon, field value
- New line is **`\r\n`!!**
Sends a metadata header (browser receives all these), separated by **blank line**, followed by actual file (HTML, binary, music, video, etc.)

### Server response
- Status line: HTTP version, status code, optional phrase (space separated)
	- HTTP version of server response may be different
- Header
- `\r\n`
- Beginning of file content (arbitrary **binary** data)
- Server **closes TCP connection** after file sent

```shell
nc -l 8888

HTTP/1.0 200 OK                     # status line
Content-Type: text/html             # header
									# \r\n
<html> <h1>                         # resource content...
Hello, world!
</h1> </html>
```

## Lab 6 part 2
Look for two bytes?
Build a web **client**

E. GNU make manual: `https://www.gnu.org/software/make/manual/make.html`

```shell
wget https://www.gnu.org/software/make/manual/make.html

./http client <host name> <port number> <file path>
./http-client https://www.gnu.org 80 /software/make/manual/make.html
```
Start from client boiler plate
1. Connect
2. Send request file via `HTTP/1.0`, terminating with `/r/n`
	1. Little more thing
3. Get response. parse it. Look for `200 OK`. If not, report
	1. skip header ,skip blank line
4. Loop: 
	1. read (`fread()`) 4K chunk
	2. save
Must work for all binary files

## Lab 7
### Part 1
`clac:80` files are in `/var/www/html` folder
When `GET /index.html HTTP/1.0`, we don't start from **root directory**. `/var/ww/html` is **configured** to be the **web root** by a configuration file

`https://clac.cs.columbia.edu:80/~jae/index.html` will look to **user specific** web root directory, configured to be `~/html` if it sees "`/~jae`"

Challenge: get the permission right. Needs `x` permission for all intervening directories

### Part 2(a)
`http-server`: Now write server that receives a `GET` request, parse, read file, and send to browser

Use browser to test webserver
`./http-server 8000 /home/jae/html/cs3157 127.0.0.1 9000`
`./http-server 5201 ~/html/cs3157 localhost 9201`
On browser go to `clac.cs.columbia.edu:5201/tng`
Now connect to `http://clac:8000/tng/index.html`, it will send `GET /tng/index.html HTTP/1.0`
Now the page displayed will be served by **my own server**
- Browser receives `index.html` from first GET, will render it, and then makes **another** `GET` request to fetch the image
	- When `GET` file downloaded ended, the server **closes** the connection (read, save, ..., until `fread()` returns 0)
- Each `GET` gets a connection. The server closes when done, and browser connects again
	- **3 separate** TCP connections for `HTTP/1.0`
	- Fixed in `HTTP/1.1`, before sending content, in header, server specifies content length.
	- The first time, browser asks for `/favicon.ico`, the icon in URL bar. Server sends `404 Not Found`

### Part 2(b)
If send **hard-coded** URL `clac:8000/mdb-lookup`, my server would respond with a textbox.
May see weird `" " 400 Bad Request`s, just respond
When type something in window, browser will send `GET /mdb-lookup/key=AP`, `mdb-lookup` will respond, server will make it pretty, and send it to browser

The source page can be downloaded, with a `<form>`
- On "submit", browser will compose a `GET` request with the `?key=`
- `GET` sent to my server
- In server, if `GET` without `key`, send empty form
	- If `key=`something, server will look for it
	- Do the `mdb-lookup` query (empty query will print everything)
	- Get the result
	- Format it (need to wrap it up with table and stuff)
	- Send it back
(a) is static. Look for the file. If there, send it to browser.
- If the file name is special `mdb-lookup`, do the special processing.
Nothing dynamic on browser. Browser is just static page

Nowadays JS script running on browser

### 3-tier architecture

![three-tier.jpg](f24/CS3157-AP/images/three-tier.jpg)
# Extra. C++
Most C code are valid in C++

Start by writing a simple C program

`struct` (aka **`class`**)
- You can omit `struct` keyword
- Can contain other **methods**
- Access rights
	- `struct` are by default public
	- `class` are by default private
- Constructor
- Destructor, called automatically when variable out of scope (here it's `main()`)
	- E. free allocated memory
- Heap allocation: need to cast `void *` to `Pt *`
	- Did not invoke constructor and destructor
	- `malloc()` grabs this of memory for this object. Has no idea to insert constructor calls.
	- **New syntax**: `new` (constructor + heap), `delete` (destructor)

```cpp
#include <stdio.h>
class Pt {         // you can drop the struct 
public:            // everything below is public
	double x;
	double y;
	Pt() {         // constructor
		x = 1;
		y = 2;
		printf("hi\n");
	}
	~Pt() {        // destructor, called automatically when var goes out of scope
		printf("bye\n");
	}
	void print()   // method
		printf("(%g, %g)\n", x, y);
}；

int main() {
	// Stack allocation
	Pt p;          
	p.print();
	
	// Heap allocation
	//Pt *pp = (Pt *)malloc(sizeof(Pt));
	Pt *pp = new Pt();
	pp->print();
	//free(pp);
	delete(pp);
}
```

## Translating C to C++
- `class` -> `struct`
- Access: check through all calls, make sure legit
- *Member functions* are removed and added as global functions
	- rename `print()` to `Pt_print()`
	- Add a parameter `this` 
	- Similar to Lab 3 that takes a pointer to a `List`
```c
void Pt_print(struct Pt *this) {
	printf("(%g, %g)\n", this->x this->y);
}
```
- Take constructor/destructor as a global function
	- Call it right after variable declaration (allocate room on stack)
- More: inheritance, polymorphism

## Java
Pointers become references
Everything is a pointer
```java
// Heap allocation
Pt pp;
pp = new Pt();
// no need to delete()

// Stack allocation
// CAN'T!!!
// IMPOSSIBLE!!!
```
Java does **not** allow object creation on the **stack**. Therefore, Java virtual machine needs a tiny stack
Background garbage collector to delete inactive pointers