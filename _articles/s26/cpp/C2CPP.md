---
title: "C2cpp Notes: Fundamentals"
permalink: /articles/cpp/new
---

{% include toc %}


---
# 1. C to C++

## Makefile
```makefile
CC  = g++
CXX = g++

CXXFLAGS = -g -Wall -std=c++20
```
- `CC`: compiler for C source files
- `CXX`: compiler for C++
- `-std=c++20`

`hello.cpp`
```cpp
#include <iostream>           // cpp headers don't have .h
int main() {
    std::cout << "hello world c" << 2 << "cpp" << std::endl;
}
```
- `cout`: **console** output
C++ has **namespace**. In C, if two library have the same function names, **linker** can't link  
`int` and `char *` are mixed
- Left shift `<<` **redefined** for `char *` (can't redefine for `int`)

### Target
`target: source`
- **Tab**: recipe

```makefile
CC = g++
CXX = g++
```
If `CC = gcc`, `gcc` will invoke linker `ld` with the **C standard libraries**, problematic!!!
- Or specify `ld hello.o libstdc++...` in the recipe line

```makefile
hello: hello.o
	g++ hello.o -o hello

hello: hello.cpp
	g++ -g -Wall -std=c++20 -c hello.c -o hello.o
```

```makefile
.PHONY: clean
clean: 
	rm *.o hello
	
.PHONY: all
all: clean hello
```

## Namespace
```cpp
#include <iostream>           // cpp headers don't have .h
int main() {
	using namespace std;
    cout << "hello world c" << 2 << "cpp" << endl;
}
```

Define your own namespace:
```cpp
#include <iostream>
namespace c2cpp {
    int main() {
        using namespace std;
        cout << "hello c" << 2 << "cpp!" << endl;
        return 0;
    }
} // namespace c2cpp

int main() {     // global namespace
    return c2cpp::main();
}
```

## String
In standard library: `string`
```cpp
string s; 
s = "hello"; 
s = s + "world"
```

- Can't concatenate by `s + t`
- `s = s + 100` won't work. `operator+()` undefined
- `s += 100` works. `operator+=()` **overloaded**


---
# 2. Basic 4
## Class

### Member Functions
Adding functions in a `struct`
```cpp
struct Pt {
	double x;
	double y;
	
	void print() {
		std::cout << this->x << ",", y << std::endl
	}
};
```

**Refer object members**
- **Explicit**: `y` 
- **Implicit**: `this->x` (`this` is implicit pointer)

**Refer** member function
```cpp
int main() {
	struct Pt p1 = { 1.0, 2.0 };     // you can drop struct in cpp
	p1.print();
	(&p1)->print();
}
```

### Public vs Private
Replace `struct` with `class`
- `class`: `private` by default
- `struct`: `public` by default

```cpp
class Pt {
public: 
	double x;
	double y;
	void print();
};
```

Early cpp compiler translates member functions as:

```cpp
void Pt_print(struct Pt *this);

int main() {
	Pt_print(&p1);
}
```

## Stack Allocation
### Constructor
**Same name** as the `class`
```cpp
class Pt {
public:
	double x; double y;
	Pt() {
		x = 4.0; y = 5.0;
	}
};

int main() {
	Pt p1;      // constructor automatically invoked
}
```
When declared, **allocate** space and call the constructor

Can **overload** with different **parameters** and **default** parameters
```cpp
	Pt();
	Pt(double _x);
	Pt(double _x = 4.0);
```

Construction syntax
```cpp
Pt p1(6, 7);     // old cpp style
Pt p1();         // does NOT compile, taken as a FUNCTION PROTOTYPE
Pt p1 = {6, 7};  // C style
Pt p1 {6, 7};    // modern cpp
Pt p1;           // implied no argument
```

### Destructor
Use `~class_name` (negation)
```cpp
	~Pt() {
		std::cout << "bye" << std::endl;
	}
```
- Called when the object goes **out of scope**
	- If enclose object in `{}`, will go away early
	- **Always called** when you leave the scope (exception)
- Constructor: `malloc()`, `fopen()`
- Destructor: `free()`, `fclose()`

## Heap Allocation
In `cpp`, `void *` **cannot** be assigned as a regular pointer, unless you **cast** it
```cpp
	Pt *p2 = (Pt *)malloc(sizeof(Pt));
	p2->print();
	free(p2);
```

**Constructor** and **Destructor** did **not** involve, since `malloc()` and `free()` are for `void* `

### `new()` and `delete()`
Wrapper around `malloc()` and `free()`
```cpp
	Pt* p2 = new Pt {6, 7};
	p2->print();
	delete p2;
```
- No `delete` in Java

### Array Allocation
{% raw %}
```cpp
Pt* p3 = new Pt[5] {{6, 7}, {8, 9}, {10}};

delete[] p3;
```
{% endraw %}
1. Allocate for an array of 5 (80 bytes)
	- On the **heap**, an **8-byte integer** pads in **front** to hold `5`
	- Can access through `((int_64_t *)p3) - 1`![](/articles/s26/cpp/img/02-basic4-new-array.svg)
2. **Each** constructor is called
3. At `delete[]`, each destructor called
	- Passing `p3` (pointer to the first element)
	- If not `delete[]`, will leak **88** bytes!

> Why doesn't cpp do this when allocating a **single** object?
> Efficiency.

## Value vs Reference
### Passing by Value
```cpp
void transpose(Pt p) { // no hi
	double t = p.x;
	// something
	p.print();         // (5, 4)
}                      // bye

int main() {
	Pt p4 = {4, 5};
	p4.print();        // (4, 5)
	transpose(p4);     // passing by value
	p4.print();        // (4, 5), unchanged
}
```
When you pass by value, `p` is **copied**
- Our own constructor **not called**. An internal [[#Copy Constructor]] called!!!
- After `transpose()` done, its **destructor** called

### Passing by Reference in C
```cpp
void transpose(Pt* p) {
	double t = p->x;
	// something
}

int main() {
	Pt p4 = {4, 5};
	p4.print();        // (4, 5)
	transpose(&p4);    // passing by pointer
	p4.print();        // (5, 4)!
}
```
- No copying

> When passing `Pt *`, technically it's still passing an address *value*, *simulating* reference

### Passing by Reference in Cpp
CPP supports this natively. Change **parameter** from `Pt` to `Pt&`
```cpp
void transpose(Pt& p) {   // type Pt&
	double t = p.x;
}
```
Can use reference **as if** using the value.
- Automatic dereferencing
- Think `p` as a **reference** (alias) for `p4`
- Pointer, but without deref

> When seeing `transpose(p4)` in cpp, less readable. Can't tell if value/reference

```cpp
    Pt p1 {100. 5}, p2 {200, 5}; 

    Pt* p;       // we declare a pointer variable, uninitialized
    p = &p1;     // p points to p1
    p = &p2;     // p now points to p2

    Pt& r = p1;  // we create a reference to p1 named r
    // Pt& r;    // error: references must be initialized when declared
    r = p2;      // this does NOT change r to refer to p2
                 // instead, it is equivalent to p1 = p2;

    p1.print();  // will print "(200,5)"
```
- You have to bind a **reference** to an object **at creation**
- aka stuck pointer
- In reassignment, will reassign the **referenced objects**
	- For all purposes of `r`, it *means* `p1`
	- but avoids making a separate object
- Always stack-allocated

## Copy Constructor
Regular constructor that takes **another object reference**
**ONLY CALLED AT INITIALIZATION**
```cpp
	Pt(Pt& orig) {    // copy constructor
		x = orig.x;
		y = orig.y;
		std::cout << "copy" << std::endl;
	}
```
When copying **by value**, copy constructor invoked
- If not defined, compiler will generate one for you that mimics the C behavior

> cpp invented reference for copy constructor
> 	If you call `Pt(Pt other)`, the copy constructor has to be recursively called...

### `const`
If you take something by `const` reference, the value won't be changed
```cpp
	Pt(const Pt& orig);
```

If you declare `const` on `p4`, but:
```cpp
	void print();
	const Pt p4;    // p4 won't be modified
	p4.print();     // WON'T COMPILE
```

`this.print()` will execute `Pt* this = &p4;`, but `const Pt* &p4` can't be converted to regular `Pt* this`!
- `print()` suggests *possible* mutation


Need to declare as `const` **member function**!!!
```cpp
	void print() const;
```
- implies `this` as a `const Pt*`
- If member function not *modifying* objects, always declare as `const`.

### Direct Invocation
Directly make a copy
```cpp
	{
		// copy construction semantics
		Pt p5 {p4};    
		Pt p5(p4);
		Pt p5 = {p4}; // C
		Pt p5 = p4;   // C init
		
		// COPY ASSIGNMENT!
		Pt p5; p5 = p4;
	}
```
Pass values of `p4` to `p5`

### Return by Value
Compile of `-fno-elide-constructors -std=c++14`  
Also invokes copy constructor  
When `expand()` **returns by value**, it creates a **temporary unnamed object**, which is again copy constructed to be assigned
```cpp
Pt expand(Pt p) {    // copy construction by value
    Pt q;            // construction
    q.x = p.x * 2;
    q.y = p.y * 2;
    return q;        // copy construction: return value
                     // q destroyed
}					 // p destroyed

int main() {
    const Pt p4;
    cout << "*** p6: returning object by value" << endl;
    {
        Pt p6 
        {      
	        // tmp created here // copy of q when expand() returns
	        expand(p4) 
	    };  // copy construction on p6
	        // tmp destroyed
    }     // p6 destroyed
	cout << "Thats all folks!" << endl;
}         // p4 destroyed
```

```sh
g++ -fno-elide-constructors -std=c++14 # ...

hi                                 # p4's constructor
*** p6: returning object by value
copy                               # call expand()
hi                                 # q's constructor
copy                               # copy of tmp
bye                                # q's destructor
copy                               # p6 copy from tmp
bye                                # tmp or p
bye                                # tmp or p
bye                                # p6 destroyed
Thats all folks!
bye                                # p4's destructor
```

**3 copy calls:**
1. Passing `p4` to `expand()`, copying to `p`
2. `expand()` return `q`, creating a `tmp` object (**different** from `q`)
	- `main()` allocates space for such `tmp`.
3. Copy of `tmp` to `p6`

**5 destructor calls**
1. `q` destroyed after `expand()` returns
2. `tmp` destroyed after `p6` constructed
3. `p` destroyed after `expand()` returns
4. `p6` destroyed
5. `p4` destroyed

Now compile **without** `-no-elide-constructors`
```shell
hi                                 # p4's constructor
*** p6: returning object by value
copy                               # p construct
hi                                 # q construct
bye
bye
Thats all folks!
bye                                # p4's destructor
```

`p6` and `tmp` not constructed
- When returning object, it is typically constructed in the stack frame of the **caller** `main()`
- When compiler is allowed to `elide`, this temporary (just used to copy into another object), is omitted
- `p6`, `tmp`, `q` get **collapsed** to one

By cpp 17, `elide` is forced

## Copy Assignment
Assign one `struct` to another, so each member is assigned
```cpp
int main() {
    const Pt p4;

    cout << "*** p7: copy assignment" << endl;
    {
        Pt p7 {8,9};
        p7.print();
        p7 = p4;
        p7.print();
    }
    cout << "That's all folks!" << endl;
}
```

```
hi                       // p4's constructor
*** p7: copy assignment
hi                       // p7's constructor                 
(8,9)                    // p7.print() before the assignment
(4,5)                    // p7.print() after the assignment
bye                      // p7's destructor
That's all folks!
bye                      // p4's destructor
```

Same behavior as C

You can use `operator=()` to define the **copy assignment** operator
- Invoked from `b = a;`
- Assignment is an **expression** with a value

```cpp
Pt& operator=(const Pt& rhs) {
	x = rhs.x;                // (this.)x = rhs.x
	y = rhs.y;
	std::cout << "op()" << std::endl;
	return *this;             
}
```
- LHS comes as this `this` object
- RHS comes as parameter `rhs`
- It you return by value `Pt`, it will make another copy

## Compiler Default
- **Constructor**: generated if no constructor or **copy** constructor. Invoke member constructors
- **Destructor**: invoke member destructor
- **Copy constructor**: generated if not present. Will copy by member (invoke their CC)
- **Copy assignment**: same

---
# 3. `MyString` Class
Header function: class definition with all member functions **declared**
- Except for short functions (let compiler `inline` it)
- Define them in the `cpp` file, prepended with `MyString::`

`mystring.h`  
```cpp
class MyString {
public:
	MyString();
	MyString(const char* p);
	~MyString();
	MyString(const MyString& s);             // copy constructor
	MyString& operator=(const MyString& s);  // copy assignment
	int length() const {return len;}

    friend MyString operator+(const MyString& s1, const MyString& s2);
    friend std::ostream& operator<<(std::ostream& os, const MyString& s);
    friend std::istream& operator>>(std::istream& is, MyString& s);
    char& operator[](int i);
    const char& operator[](int i) const;
    
private:
	char* data;
	int len;
};
```

## `Makefile`
```makefile
executables = test1 test2 test3
objects = mystring.o test1.o test2.o test3.o

.PHONY: default
default: $(executables)

$(executables): mystring.o
$(objects): mystring.h
```

- `default` has all executables we want to build. Will get expanded to `test1 test2 test3`
- For each `$(executables)` and `$(objects)` gets expanded to  

```makefile
test1: test1.o mystring.o
	g++ test1.o mystring.o -o test1
	
test1.o: test1.cpp mystring.h
	g++ -g -Wall -std=c++14 -c test1.cpp
```
The variables will be expanded. `*.o` and `*.cpp` ingredients are **implied**

## Basic 4

> Don't forget the `nullptr` case, as well as allocating `len + 1`
{: .notice--warning}

```cpp
#include "mystring.h"

int main() {
    using namespace std;
    MyString s1;
    MyString s2("hello");   
    MyString s3(s2);       // copy construct
    s1 = s2;               // copy assignment
    cout << s1 << "," << s2 << "," << s3 << endl;
}
```
### Constructor
When you initialize `"hello"`:
- Type: `char [6]`
- Value: pointer at `.rodata`, between`code` and `data`
	- However, string there will be **immutable**.
	- Need to allocate a copy

```cpp
MyString::MyString(const char* p) {
	if (p) {
		len = strlen(p);
		data = new char[len + 1];
		strcpy(data, p);
	} else {/* allocate a null string */}
}
```
- `new char[6]`: allocate 6 elements of `char` on **heap**
	- If `new` fails to allocate, throws **exception**
- Can't allocate on stack due to scope

> If string is empty, allocating 1 byte is unfortunate. Why not make it `NULL`?
> - Creates an **invariant** property, better testing integrity
> - real `std::string` has a short (E. 32-byte) **buffer** to avoid heap allocation

### Destructor
```cpp
MyString::~MyString() {
	delete[] data;
}
```

### Copy Constructor
Consider this code
```cpp
void f(MyString s2)
	cout << s2;
	
int main() {
	MyString s1("hello");
	f(s1);
	cout << s1;
}
```

If copy constructor not defined, `s2` will be copied on the stack, member-wise
- When `f` returns, `s2` goes away, and its **destructor** gets called!!!
- `s1.data` deleted!!!
- Shallow copy!

Need make every copy carry its own heap allocated string
```cpp
MyString::MyString(const MyString& s) {
    len = s.len;
    data = new char[len+1];
    strcpy(data, s.data);
}
```

### Copy Assignment
Need do a little more, 
```cpp
MyString& MyString::operator=(const MyString& rhs) {
	// if s1 = s1, DON'T change anything
    if (this == &rhs)    
        return *this;

    // first, deallocate memory that 'this' used to hold
    delete[] data;

    // same as copy constructor
    len = rhs.len;
    data = new char[len+1];
    strcpy(data, rhs.data);

    return *this;
}
```

> What if I use `*this == rhs`?
> - Same result, but not efficient to compare all `struct` contents
> - Depends on `operator==()` definition

> **Rule of 3**  
> If you implement any of *destructor, copy constructor, and copy assignment*, you probably need to do all 3 of them
{: .notice--info}

### Inline Functions
Entire body defined in `mystring.h`
- Tell compiler to `inline` it
- Compiler may refuse (E. long/recursive/virtual functions)

## Operators
### `operator+()`

```cpp
MyString operator+(const MyString& s1, const MyString& s2) {
    MyString temp;
    delete[] temp.data;

    temp.len = s1.len + s2.len;
    temp.data = new char[temp.len+1];
    strcpy(temp.data, s1.data);
    strcat(temp.data, s2.data);

    return temp;
}
```
> `operator+()` is **not** a **member function** (no `this` pointer, no `MyString::`). It's **global**
{: .notice--warning}

> **How does it access `private` data?**  
> Declared as `friend` in prototype
{: .notice--info}


```cpp
friend MyString operator+(const MyString& s1, const MyString& s2);
```

After `return temp`, a copy of `temp` is created, which goes into `rhs` for `operator=()`

> **Why is `operator=()` member, but `operator+()` global?**   
> Either works syntax-wise
> - `operator=()` modifies LFS, so make it member
> - lhs and rhs of `operator+()` are symmetrical, so make it global
{: .notice--info}


`(s1 + "world")` also works
- Compiler first looks for overload of `operator+(MyString, char*)`
- Next, sees if can **promote** one of the mismatched argument into `MyString`
	- By invoking constructor `MyString(char*)`
	1. Finds a constructor of `MyString` that takes `char*`
	2. Constructs a temporary object from `char*`
		- Only works if `operator+()` is a global function 
`"hello" + "world"` doesn't work
- Preserves C behavior

### `operator<<`
- `cout` is `std::ostream` that represents `stdout`
- Return it by **reference**
	- So associativity not violated

```cpp
friend std::ostream& operator<<(std::ostream& os, const MyString& s);
```

> **Why not make it a member function of `std::ostream`? Why make it global?**  
> - Don't want to redefine the code in `std`
{: .notice--info}


```cpp
std::ostream& operator<<(std::ostream& os, const MyString& s) {
    os << s.data;    // give os the char*
    return os;       // return BY REFERENCE
}

(cout << s1) << "something else";   // LHS is still cout
```

### `operator>>()`

```cpp
friend std::istream& operator>>(std::istream& is, MyString& s);

std::istream& operator>>(std::istream& is, MyString& s) {
    std::string temp;
    is >> temp;

    delete[] s.data;

    s.len = strlen(temp.c_str());
    s.data = new char[s.len+1];
    strcpy(s.data, temp.c_str());

    return is;
}
```
Cheated with `std::string`
- Actually, need to read each character from `stdin`, and get whitespace right
- `.c_str` gives the regular `char*`

### `operator[]()`
Gives the i-th character
- `char&` return, because need to write into the string

If `MyString` is `const`, both of the following would work:
```cpp
const char& operator[](int i) const;
char& operator[](int i) const;
```

```cpp
char& MyString::operator[](int i) {
    if (i < 0 || i >= len) {
        throw std::out_of_range{"MyString::op[]"};
    }
    return data[i];
}
```

### `operator[]() const`
If `this` is `const`, **all its members** will be `const`
- Cast away `const`ness
- `*this` has type `const MyString*`
- When you dereference `const MyString*`, it becomes `const MyString&`
- Cast to regular `MyString&`
- Can invoke the regular `operator[]()`, which returns a `char&`
- Assigning `char&` into `const char&` is fine  
```cpp
const char& MyString::operator[](int i) const {
    // illustration of casting away constness
    return ((MyString&)*this)[i];
}
```

The cpp syntax is:
```cpp
	return const_cast<MyString&>(*this)[i];
```
- Also checks if `*this` is `MyString&` to begin with

## Exception Handling
```cpp
	throw std::out_of_range{"MyString::op[]"};
	
	// same as
	std::out_of:range ex{"MyString::op[]"};  // construct a temp object
	throw ex                                 // return by value
```
- `std::out_of_range` is a type, **constructs** a temporary object `ex`, and returns **by value**

If not `catch`ed, and the exception goes out of `main()`, a library function will `catch` it, and terminate the program

```cpp
	try {
		f1();    // function call that may throw an exception
	}
	catch (const out_of_range& e) {
		cout << e.what() << endl;
	}
```

Catch with `const` **reference** (if by value, has a copy construct...)
- Then invoke the member function `what()`

If `throw`ing an exception makes a function **exit in the middle**, the **local variables** *will* be properly destructed

---
# 4. Function Template
```cpp
int Max(int x, int y)
	return x > y ? x : y;

std::string Max(std::string x, std::string y);
	return x > y ? x : y;
```

CPP allows **templates** for the **same implementation**, so you don't have to repeat

```cpp
template <typename T>
T Max(T x, T y)
	return x > y ? x : y;
	
const T& Max(const T& x, const T& y);
	// better
```

Above is *not* *actual* cpp code. The **compiler** **generates** from the `template`
- Figure out the actual type, and replace `T` with it
- Better write with `const T&`, since not modifying

> Need **definition** in **header** file, **not in** another cpp file, since it has to be seen at **compile** time
{: .notice--warning}

## Template Overloading
But if use `Max("AAA", "BBB")`, will fail, since comparing two pointers, unpredictable
- Compiler generates a version of `Max()` with `char*`s

Want a template that **specializes** the type by giving a **concrete definition** for certain types
```cpp
const char* Max(const char* x, const char* y)
	return strcmp(x, y) > 0 ? x : y;
```
- Even if you **declare** this specialization, the compiler will stop using the `template`

> Make it `static` in header file, and `inline` if short
{: .notice--info}


## Compilation
Build a wrapper `func1()` around `Max()` in `func1.cpp`
```cpp
#include "max.h"

// wrappers on Max() template
int func1(int x, int y)   // defined for int
	return Max(x, y);
	
int func2(int x, int y)
	return Max(x, y);
```
- When `func1.cpp`, in `func1.o`, the compiler puts the definition of `Max()` for `int`
Do the same at `func2.cpp`

> When linking, how is it not a duplicate definition?

In the object dumps, 
- `func1` is **renamed** as `_Z5func1ii` in cpp due to overloading
	- Encodes its parameters `ii`
- Linker is aware that the `Max()` are duplicates, and throws one of them out
	- `WEAK` binding (may have multiple instances)
	- `GLOBAL` binding in normal functions
	- `LOCAL` binding for `static` functions (only in current object)

