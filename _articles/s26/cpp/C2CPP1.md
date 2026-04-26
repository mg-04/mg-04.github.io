---
title: "C2cpp Notes: Container and Inheritance"
permalink: /articles/cpp/1new
---

{% include toc %}

---
# 5. Dynamic Array
> Implementation of `std::vector` (templatized class)

Dynamically growable integer array (add to back)
- Allocate `sz + 1` elements on the heap
- When you call `push_back()`, add to the provision element, and `size++`

> **Member initializer list**  
> Preferred, since members already constructed and initialized simultaneously
> - Avoids default construct, then assignment in the body
{: .notice--info}


```cpp
class IntArray {
private:
	size_t sz;
	size_t cap;      // need cap declared before a
	int* a;      
public:
	IntArray() : sz{0}, cap{1}, a{new int[cap]}  // member initializer list
	{
		// sz  = 0;  
		// cap = 1;
		// a = new int[cap];
	}
	
	void push_back(int x) {
		if (sz == cap) {
			int* a2 = new int[cap * 2];   // if new fails, exits, but cap intact
			cap *= 2;                     // strong exception guarantee
			std::copy(a, a+sz, a2);       // [first, last+1), dst
			delete[] a;
			a = a2;
		}
		a[sz++] = x;
	}
	// ...
```
- If have capacity, put the next element ($$O(1)$$)
- If not, allocate **double** the capacity, copy over, and add ($$O(n)$$)
- **Overall** complexity: $$O(2n) = O(n)$$ for $$n$$ elements
	- Average: amortized $$O(1)$$

> **Strong exception guarantee**  
> If an exception happens in the middle, it won't mess up your object
{: .notice--info}


Not planning to use copy constructor and copy assignment, so use `delete`
- Undefine the compiler generated one
	- Copy attempts will fail to compile
- Use `default` for compiler generated

``` cpp
	// ...
	~IntArray() {
		delete[] a;
	}

	IntArray(const IntArray&) = delete;
	IntArray& operator=(const IntArray&) = delete;

	int& operator[](int i) { return a[i]; }
	const int& operator[](int i) const { return a[i]; }

	size_t size() const { return sz; }
	size_t capacity() const { return cap; }
};
```

**Usage:**
```cpp
int main() {
	using namespace std;
	IntArray ia;
	for (int i = 0; i < 20; i++) {
		ia.push_back(i);
		cout << ia << endl;
	}
}
```

---
# 6. Move Operation
> Continuation of [2. Basic 4](../new/#2-basic-4)

## Motivation
Construct a local array and return **by value**
- Will invoke 2 copy constructions

```cpp
IntArray createIntArray() {
	IntArray tmp;
	for (int i = 0; i < 20; i++) {
		tmp.push_back(i);
		std::cout << tmp << std::endl;
	}
	return tmp;   // copy by value
}

int main() {
	IntArray ia { createIntArray() };  // make another copy
}
```
> **Fail to compile**  
> Earlier, `delete`d the copy constructor!
{: .notice--warning}

It's very cumbersome to return an object **by value** by copying!
- Want to pass a **reference**, and allocate the structure **outside** the function

```cpp
void createIntArray(IntArray* ia_ptr) {
	for (int i = 0; i < 20; i++) {
		ia_ptr->push_back(i);
		std::cout << *ia_ptr << std::endl;
	}
}

int main() {
	IntArray ia;    // allocate locally on the stack
	createIntArray(&ia); 
}
```

## Move Constructor
> Move constructor only kicks in when assigning to a temporary object that will go away
> - More efficient than copy
{: .notice--info}


1. Do a **shallow** copy of each element from `tmp` to the new object `this`
2. **Sever** the connection to the **original** pointer `.a`

```cpp
IntArray(IntArray&& tmp) : sz{tmp.sz}, cap{tmp.cap}, a{tmp.a} {
	tmp.sz = tmp.cap = 0;
	tmp.a = nullptr;
	std::cout << "move ctor" << std::endl;
}
```
> Instead of making a deep copy of original `tmp`, "steals" what `tmp` used to have, and move to the return 

Now, when `tmp` -> unnamed return -> `ia`, each old object gets destroyed
- Instead of making a brand object and making a copy, steal the internals
- Two **copies** becomes two **movements**
- Old object gets destroyed, and `delete nullptr` is okay

> Move constructor can be elided as well
{: .notice--info}


### `&&` rvalue Reference
> Will be on exam
{: .notice--danger}


- Regular variables are **lvalue**
	- `int i = 5`, 
		- `i` **can** be on the LHS, lvalue
		- `5` can't be lvalue, can't do `5 = i`
- `MyString{"xyz"}` is rvalue

```cpp
struct X {
	X() : d{100} {}   // set X.d to 100
	double d;
};

void f1(X& t)       { t.d *= 2;  cout << t.d << endl; }

void f2(const X& t) { cout << "can't change t" << endl; }

void f3(X&& t)      { t.d *= 3;  cout << t.d << endl; }

int main() {
	X x;           // x is an lvalue
	f1(x);         // passing an lvalue to X&       --> ok
	f2(x);         // passing an lvalue to const X& --> ok
	f3(x);         // passing an lvalue to X&&      --> not ok

	// X{} creates a temp object (rvalue)
	f1( X{} );     // passing an rvalue to X&       --> not ok
	f2( X{} );     // passing an rvalue to const X& --> ok
	f3( X{} );     // passing an rvalue to X&&      --> ok
}
```
- Copy constructor take `const` reference, since old object not modified
- Move operator take **revalue reference** to bind to rvalue
	- Only allow stealing from **temporary objects**
	- Not named!!!

## Move Assignment
```cpp
IntArray& operator=(IntArray&& tmp) {
	if (this != &tmp) {
		delete[] a;

		sz = tmp.sz;
		cap = tmp.cap;
		a = tmp.a;

		tmp.sz = tmp.cap = 0;
		tmp.a = nullptr;
	}
	std::cout << "move assignment" << std::endl;
	return *this;
}
```

### Usage
```cpp
IntArray ia = { createIntArray() }
IntArray ia2;
ia2 = ia;        // we don't have copy assignment, 
```
Won't work since `ia` is an **lvalue**, not allowed to move!!

Need to **cast** to force a move assignment 
```cpp
ia2 = (IntArray&&) ia;     // not recommended
// or 
ia2 = std::move(ia);
```
Original `ia` loses its content

## Summary
Compiler can generate a move constructor and move assignment

> There are some edge cases for that
{: .notice--warning}

- When **no** destructor, copy constructor, or copy assignment declared
	- Compatibility with copy rules, if legacy code write copy but not move
	- Move will fall back to copy
		- rvalues can be bound to `const` lvalues
	- Member-wise move
- If *either* move constructor *or* move assignments are declared, compiler will **implicitly delete** the copy constructor *and* copy assignment
 
> **Rule of 5**  
> If you declare *any* of destructor/copy/move (including `default` and `delete`), very likely need to declare all of them
{: .notice--info}


> **Rule of 0**  
> If all **class members** already have their 5 defined correctly (E. library class), and you class has **no special resource management**, no need to declare in *your* class
> - Some prefer to declare with `=default`
{: .notice--info}

---
# 7. `vec` Class
- `template <typename T>`
- Change `int` to `T`
- Make functions **template functions** parameterized by `T`

```cpp
template <typename T>
std::ostream& operator<<(std::ostream& os, const vec<T>& ia);

Vec<int> CreateIntVec() {
	Vec<int> tmp;       // need to explicitly specify the type
	// ...
}
```

```cpp
void push_back(int x) {
	if (sz == cap) {
		int* a2 = new int[cap * 2];
		cap *= 2;
		std::copy(a, a+sz, a2);   // uses copy assignment
		delete[] a;
		a = a2;
	}
	a[sz++] = x;
}

int main() {
	Vec<MyString> v;    // (1)
	v.push_back("abc"); // (2)
	v.push_back("def"); // (3)
	MyString s{"xyz"};  // (4)
	v.push_back(s);     // (5)
}
```
1. Constructs `v` on the *stack* `{size_t size, size_t cap, MyString a[1]}`
	- `sz = 0; cap = 1;`
	- `a` is an allocated 1-element array
		- Calls `MyString()`
			- Makes a **default** `MyString` object on the heap, with
2. `const T&` requires a promoted temporary object
	- Temp (rvalue) `MyString("abc")` object *constructed* on **stack**
		- `len = 3`
		- `data = "abc\0"`
	- Temp comes into `push_back()` as `const T& x` (reference)
		- Must have `const`, else won't accept rvalue
	- `a[sz++] = x`
		- Copy  **assignment**
	- `x` destroyed after `push_back()` return, and temp
3. `push_back("def")`
	1. Same temp creation 
	2. Allocation needed! (two levels)
		1. `new MyString[2]` allocated on **heap**
			- Both members are **default constructed** `MyString()`
		2. `std::copy()`
			- Copy **assignment**
				- `delete` old data
				- Data pointer updated
		3. `delete[] a`
			- `delete[]` all string allocations
	3. `x` (and its members) gets copy assigned to its `a[1]`, and destroyed
4. `MyString s{"xyz"}`
	- `s` created on stack
		- `"xyz\0"` on heap
5. `v.push_back(s)`
	1. `s` passed by reference
	2. Need to reallocate again
		- Every `MyString` gets default constructed
		- Copy assign the `MyString`s over
		- The vector entry `v.a[3].data` has a *different* copy with `s.data`
	- Last slot left "empty", but a `MyString` object

STL containers hold its **own copy** of the data (by **value**)

> This is **NOT** how `vector` works. Default construction is wasteful!  
> `std::vector` will not initialize the memory (no default constructor `new`, just `malloc()`)
> - But how would `a[sz++] = x` work?
> 	- This is an **assignment**. The LHS object must be constructed
> - Solution: **Placement** `new`
{: .notice--info}



## Placement `new`

```cpp
char s_buf[sizeof(MyString)];
MyString* sp = new (s_buf) MyString{"hello"};
```
**Casting** decouples memory allocation and constructor call!
- No memory allocation 
- Only calls constructor
Can't directly invoke `delete`, need to **manually** invoke the destructor
```cpp
sp->~MyString();
```

## Strong Exception Guarantee
For `push_back(Int)`, exception can only happen in `new`. `std::copy()` of integers is *trivial*
- Need to guarantee that `IntArray` won't be changed

For `push_back(MyString)`,
1. If `new` throws, nothing created
2. If `copy()` throws, 
	- `operator=(MyString)` uses `new`, may throw
3. Assignment `a[sz++] = x` may throw

```cpp
void push_back(const T& x) {
	if (sz == cap) {
		T* a2 = new T[cap * 2];       // no issue
		try {
			std::copy(a, a+sz, a2);
		} catch (...) {               // catch any exception
			delete[] a2;              // cleanup before throw
			throw;
		}
		cap *= 2;
		delete[] a;
		a = a2;
	}
	a[sz] = x;          // if throw here, all did was increasing cap
	sz++;               // separate sz++
}
```
> **Still issues!**  
> On `a[sz] = x`, `operator=(MyString)` may leave the default constructor in a *bad* state
> 	- Assume if copy assignment fails, it still leaves a valid object there 
{: .notice--warning}

> **Might be more efficient if the elements are moved, rather than copy**  
> `std::vector` tries to move elements during reallocation, but
> - Move may not easy to roll back on **exception**
{: .notice--info}


`std::vector` uses the criteria:
1. **Moved** if move constructor marked `noexcept`
2. Copy else
3. If copy constructor deleted, the fall back to move (forgo strong exception guarantee)

---
# 8. Inheritance
> Not to useful in cpp, mostly on template and OOP mechanisms

Based class -> derived class
- Derived classes need to be constructed, if its base class constructor takes arguments

```cpp
class B {
public:
	uint64_t sum() const { return b; }

// protected
private:
	uint64_t b = 100;
};

class D : public B {
public:
	// return b + d;
	uint64_t sum() const { return B::sum() + d; }

private:
	uint64_t d = 200;
};
```
`D` has the derived `sum()` from `B`, and its **own** version


> Don't forget `public`!
{: .notice--warning}


**Scope**:
- `private` members can't be accessed by derived classes. Need `B::sum()`
- `protected` members are accessible, but not to general outside

`sizeof(D)` is 16 bytes,
- 8 for `.b = 100` (inherited)
- 8 for `.d = 200`

Can cast to find it:

```cpp
uint64_t* p = (uint64_t*) &x;
uint64_t*p = reinterpret_cast<uint64_t*>(&x);
```

## Static Binding
> By default how cpp works, translated to C

`x` is a `D` object, but the compiler **picks the function** to invoke based on the object **type**
```cpp
int main() {
	using namespace std;

	D x;
	w( x.sum() );

	B *pb = &x;
	D *pd = &x;
	w( pb );
	w( pd );
	w( pb->sum() );    // compiler generates B_sum(pb)
	w( pd->sum() );    // compiler generates D_sum(pb)
}
```

## Dynamic Binding
> Java behavior: call the underlying object type, not **pointer** type

Use keyword `virtual` in base class
- Optionally `override` in derived class

```cpp
class B {
public:
	virtual uint64_t sum() const { return b; }
}

// not required
class D : public B {
public:
	uint64_t sum() const override { return B::sum() + d; }
}
```

> **How did compiler know that `pb` is pointing to a `D` object?**  
> What if in a different cpp file that has `foo(B* pb) { pb-> sum();}`
> Any `pb` derived from `B` can be called here
> - Without `virtual`, compiler will translate everything to `B_sum`
> - How does `virtual` work?
{: .notice--info}


Now, `sizeof(x) = 24`, object gets elongated
- `.vptr` is some address
	- Virtual Table Pointer, array of function pointers for each virtual function in the class
		- One table **for class**
	- For `D`, one entry: `D::sum()`
- `.b = 100`
- `.d = 200`

If a `B` object instantiated, 
- `.vptr` will point to a different V table for `B` class
	- `B::sum()`

When `pb -> sum();`
- `D::sum()` is always called, regardless the pointer type of `pb`
 - When declared, `pb` is pointing to the vtable of `D`
 - Directly invoke `D::sum()` from the vtable pointer entry
 - Compiler generates `pb->vptr[0] (pb)`
	 - Call `sum()` by passing `pb`

Even if `ptr` is `B` type, `B::sum()` invoked through `B`'s vtable


### Virtual Table
Manually invoke `sum()` manually
- `sum` has type `uint64_t (const D*)`
- vtable entry `uint64_t (const D*)`
- vtable **pointer** in `D x` has type `uint64_t (**) (const D*)`
- `B* pb` has type `uint64_t (***) (const D*)`
Reference 3 times, and deref twice

```cpp
D x;
B* pb = &x;
(uint64_t (***) (const D*)) pb )[0][0](&x);
```

## Multiple Inheritance
> CPP class can derive from **multiple** base classes (not used much)
> - Can't do java. Only can memberless classes: interface

```cpp
// similar class C
class D: public B, public C {
public:
	uint64_t sum() const { return B::sum() + C::sum() + d; }
private:
	uint64_t d = 200;
};
```

With **static binding**, initialize `B` and `B*, C*, D*`,
- `B*, D*` point to the beginning
- `C*` point to the `C` portion, a different pointer!
	- When assign `C* pc = &x;`, compiler **silently changes** the pointer
	- Since the base portion of `C` is in the middle

### `static_cast`
**Downcast** base pointer `C*` **back** to the original object pointer `D*`
- Opposite of `C* pc = &x;` (upcast)
- with `static_cast`

```cpp
	D* pd2 = static_cast<D*> (pc);    // cast C* to D*
	w( pc );
	w( pd2 );
```

Different pointers are printed

**Not perfect**
```cpp
C y;
pd2 = static_cast<D*> (&y);     // compiler allowed
pd2->sum();                     // crash
```
- `y` has type `C`, bad
- `* pd2` has type `D`, originally, OK

### Multiple Virtual Inheritance
- Add `virtual` to base classes `B::sum()` and `C::sum()`
- Add `override` to `D::sum()`

![](/articles/s26/cpp/img/08-multi-d-2.svg)
Now, `sizeof(x) = 40` (5 slots)
- Without `virtual`, was `24`, with `.b, .c, .d`
Two vtable pointers, to **different places** of the **same** vtable
- `[0] .vptr1`
- `[1] .b = 100`
- `[2] .vptr2`
- `[3] .c = 150`
- `[4] .d = 200`

- 01: `B` portion
- 23: `C` portion

```cpp
D x;
C* pc = &x;
pc->sum();      // calls C portion, D[2], and invoke D::sum();
```
- When calling from `C`, `this` is **not** pointing to the beginning of the object
- Need to **adjust** `this` by subtracting `sizeof(B)`

Translated to the C version in the object file:
```c
uint64_t thunk_of_D_sum(const C* this_ptr) {
	char* adjusted_this_ptr = (char*)this_ptr - sizeof(B);  // B portion size
	return D::sum( (const D*)adjusted_this_ptr );           // actual this
}
```

### `dynamic_cast`
In **vtable**, there are information for **crosscast** and **downcast** with more checking
- Point to global `std::type_info` (1 per class)

At compile, still checks
- Inputs needs to be **pointers**
- Classes have `virtual` functions, so vtable can be accessed.

```cpp
D x;
B* pb = &x;
C* pc = &x;
D* pd = &x;
assert(dynamic_cast<B*>(pc) == pb);    // cross cast C (actual D) to B
assert(dynamic_cast<D*>(pc) == pd);    // down cast  C (actual D) to D
```

```cpp
C y;
C* pc2 = &y;
assert(dynamic_cast<B*>(pc2) == nullptr);  // fails, can't cast (actual) C to B
assert(dynamic_cast<D*>(pc2) == nullptr);  // fails, can't upcast C to D
```

## Virtual Inheritance
### Diamond Problem
```cpp
class A {
public:
	virtual uint64_t sum() const { return a; }
private:
	uint64_t a = 5;
};

class B : public A {
public:
	virtual uint64_t sum() const { return b; }
private:
	uint64_t b = 100;
};

class C : public A {
public:
	virtual uint64_t sum() const { return c; }
private:
	uint64_t c = 150;
};

class D : public B, public C {
public:
	uint64_t sum() const override { return B::sum() + C::sum() + d; }
	// A::sum() is ambiguous and does not compile:
	// uint64_t sum() const override { return A::sum() + B::sum() + C::sum() + d; }
private:
	uint64_t d = 200;
};
```
`D` is derived from both `B` and `C`, which is derived in `D`

```cpp
D x;
A* pa = &x;    // compilation error!
```
- Can't `static_cast` or `dynamic_cast` to `(D*)` either

> **Diamond Problem**  
> Compiler won't know **which** `A` portion to point to!
> - `A::sum()` can't be called in `D` either!
{: .notice--warning}

![](/articles/s26/cpp/img/08-diamond-problem.svg)

### Solution
Derive classes `B`, `C` `virtual` from `A`
- Eliminates **duplication** of `A`

```cpp
class B : virtual public A {
	// ...
};
```

Now all will compile properly and sum 455:
```cpp
	D x;
	
	A* pa = &x;
	B* pb = &x;
	C* pc = &x;
	D* pd = &x;
	w( pa );           // 0de8, off=40 (16+24)
	w( pb );           // 0dc0
	w( pc );           // 0dd0, off=16
	w( pd );           // 0dc0
	w( pa->sum() );
	w( pb->sum() );
	w( pc->sum() );
	w( pd->sum() );    // all 455
```

Will no longer copy `A` in each `B C` instance. Put it at the **end**


In vtable, new `vbase_offset`, `vcall_offset`
![](/articles/s26/cpp/img/08-virtual-d-2.svg)

## Misc
### Construction Order
Sock and shoes (opposite for destruction)
1. Base class constructed
2. All members constructed
3. Derived class itself constructed

### Virtual Function & Abstract Class
Abstract class have purely virtual function
- aka interface in Java
```cpp
virtual uint64_t sum() const = 0;
```
No code, meant purely to be **overwritten** by derived classes
- The class itself **cannot** be instantiated
- Only its derived classes that **overrides** this method can

### Virtual Destructor
```cpp
int main() {
	B* pb = new D;
	delete pb;      // only destructor of B called
}
```
The destructor is **not virtual**, (static binding), so the `B` destructor will be invoked

Need to `virtual` the destructor
```cpp
struct B {
	virtual ~B() { cout << "B::~B()" << endl; }
};

struct D : public B {
	~D() override { cout << "D::~D()" << endl; }
};
```
All members, `D`, `M`, `B`, will be destroyed properly

---
# 9. `iostream`
```cpp
int sum_ints(std::istream& is) {     
	int i, sum = 0;
	while (is >> i) {      // extract a number to int i
		sum += i;
		std::cout << "current sum: " << std::setw(4) << sum;// 4 space, right align
		print_io_states(is);
	}
	return sum;
}
```
Keeps printing the sum and stats
```sh
echo "5 7 9 " | ./io1
```

## `istream`
```cpp
while (is >> i);

istream& istream::operator>>(int& value);     // modifies istream (this)
ios::operator bool() const;
// same as !ios::fail
```
- Return `istream` so can keep chaining things
- `operator <type>` is a **conversion operation**
	- Invoked when `<type>` is required
- `istream` is a *base class* of `ios`

- `std::setw()` is a function that returns an **object** `WidthManipulator`
```cpp
ostream& operator<<(ostream& os, const WidthManipulator& wm) {
	os.width(wm.get_width());
	return os;
}
```


## Hierarchy
![](/articles/s26/cpp/img/09-io-stream-hierarchy.svg)
- `std::cout` and `std::cin` are instances of `ostream` and `istream`
- `ostingstream` prints into a string
- `ofstream` prints into a file

### `iostate`
> Top level `ios_base` contains flags and constants, such as `ios_base::iostate`

`iostate` is a set of flags telling the state of the IO, can be combined
- `failbit`: formatting/extraction error/EOF 
- `badbit`: irrecoverable error (E. disk crashed)
- `eofbit

In class `ios`, flags can be accessed by:
- `fail()` (`failbit` **OR** `badbit`)
	- `operator bool()` same as `!fail()`
- `bad()`
- `eof()`
```shell
echo "10 2 3 4" | ./io1
```
Only *after* summing `4`, and trying to read for **one more time**, hits EOF
- `echo` adds a `\n` at the end of "4". `ios` hits the `\n` first and parses the 4 okay


Now suppress `\n` by `echo -n`
```sh
echo -n "10 2 3 4" | ./io1
```
- Now, *when* summing "4", `eof()` set, since hit EOF directly after "4"
	- `fail() = 0`, `eof() = 1`
	- `is >> i` still evaluated to `1`, so loop executes one more time
- Last time, `fail() = 1`, `eof() = 1` (still)

## Error Recovery
Keep recovering until `eof()`
```cpp
int sum_ints(std::istream& is) {
	int i, sum = 0;
	while (!is.eof()) {
		is >> i;      // skip all leading whitespaces
		
		if (is.bad()) {
			throw std::runtime_error{"bad istream"};
		} 
		
		else if (is.fail()) {    // fail(), but not bad()
			if (is.eof()) {
				// failbit && eofbit: this is normal (trailing whitespace)
				break;
			}
			// failbit && !eofbit: probably non-digit; just skip it
			is.clear();
			char c;
			is.get(c);  // consume a single char
			std::cout << "  skipped: " << c << '\n';
		} 
		
		else {    // read i successfully;
			// we could have hit eof or not (depends on trailing whitespace)
			sum += i;
			std::cout << "current sum: " << std::setw(4) << sum;
			print_io_states(is);
		}
	}
	return sum;
}
```
- If get `char`, consume **one** character at a time
- If get `int`, consume a chunk

### C vs Cpp
By *default*: `std::cin` is sync with `stdin`, and for out and err
- Cpp streams are **unbuffered**
- Each IO operation on cpp stream is *immediately* applied to the corresponding C stream's buffer
- Underneath, call the C functions (E. `printf()`, `scanf()`)
	- Thin wrapper

Can detach Cpp stream from C stream, automatically add its own buffer:
```cpp
std::ios_base::sync_with_stdio(false);
```
- Cpp streams are allowed to buffer its IO *independently*
- Lose the following:
	- No longer **thread-safe**
		- No 
	- `\n` may not **flush** `stdout` to terminal
		- Use `'\n'` instead of `std::endl` for terminal output

## Polymorphic `ios`
`pair<T1, T2>` is a library template with two types
```cpp
void f1(istream& is) {
	while (!is.eof()) {
		is >> std::ws;          // discard leading whitespace
		if (!is || is.eof())    // break if nothing else
			break;
		
		pair<string,double> e;
		is >> e;                // overload >> to read from istream
	
		if (is.fail())
			break;
		cout << e << '\n';
	}

	if (is.bad())
		throw runtime_error{"bad istream"};
	else if (is.fail())      // fail but not just eof
		throw invalid_argument{"bad grade format"};
}

int main(int argc, char **argv) {
	try {
		f1(cin);
	} catch (const exception& x) {
		cerr << x.what() << '\n';
	}
}
```

Now parse `pair` from `istream`:
```cpp
std::istream& getline(std::istream& is, std::string& str, char delim);

static istream& operator>>(istream& is, pair<string,double>& e) {
	char c;
	// 1. read opening quote, skipping whitespace
	if (is >> c && c == '"') {
		string student;
		// 2. read all chars into student, stop at closing quote, then discard it
		if (std::getline(is, student, '"')) {
			// 3. read a comma, skipping whitespace
			if (is >> c && c == ',') {
				double grade;
				// 4. read double grade
				if (is >> grade) {
					e = make_pair(student, grade);
					return is;
				}
			}
		}
	}
	// if fall here, fail :(
	is.setstate(ios_base::failbit);
	return is;
}

static ostream& operator<<(ostream& os, const pair<string,double>& e) {
	return os << "[" << e.first << "] (" << e.second << ")";
}
```
- `make_pair()`

### String Stream
**Issue** with `f1()`: one failed record failed will fail `break` and `throw` 
- Want recover and move on

`f2()` adds another layer of buffer
1. Read an entire line
2. Construct `istringstream` object from the line, as backup
3. Call `f1(iss)`
	- `iss` becomes the `istream` source of `f1()`, instead of `cin`
	- If error, print

```cpp
void f2(istream& is) {
	string str;

	while (std::getline(is, str)) {
		istringstream iss(str);

		try {
			f1(iss);
		} catch (const invalid_argument& x) {
			cerr << x.what() << ": " << str << '\n';
		}
	}
}
```

### File Stream
`f3()` constructs `ifstream` object
```cpp
void f3(const char* filename) {
	ifstream ifs { filename };
	if (!ifs) {
		if (filename != nullptr)
			throw runtime_error{"can't open file: "s + filename};
		else
			throw runtime_error{"no file name provided"};
	}
	f2(ifs);
}
```

---
# 10. Sequence Containers
Standard Template Library (STL)

## Array
```cpp
int a[2] = {6, 7};
int a[2] {6, 7};              // preferred in cpp
```

Now wrap C array in **class** template `Array`
```cpp
template <typename T, size_t N>
struct Array {
	// typedef T value_type;
	using value_type = T;
	// T(&)[N] is a reference to array of N elements of type T
	using TA = T(&)[N];

	T& operator[](int i) { return a[i]; }
	const T& operator[](int i) const { return a[i]; }

	// member function, done in compile time
	constexpr int size() const { return N; }
	TA underlying() { return a; }

	T a[N];
};
```
- `using` **declaration**: another way to do `typedef`. Define new
	- `value_type` means `T`
	- `TA` references to the array 
- `constexpr` can be designated to any (member) function. Tells compiler that such call can be evaluated at **compile** time
- `underlying()` pass out the reference to the *entire* array
	- Avoids decaying array into a pointer, by using `T(&)[N]`

> ```c
> int *p = a;
> // pa is a pointer to an array of 5 ints and points to the array a
> int (*pa)[5] = &a;
> // ra is a reference to an array of 5 ints and refers to the array a
> int (&ra)[5] = a;
> ```
> `pa` is a **pointer**. After dereferencing `pa`, you will get `int[5]`
> - `pa` has type `int (*)[5]`
> - `pa` same value as `a`, but different type
> - `pa + 1` will point to 5 elements after
{: .notice--info}


```cpp
	Array<int,5> v { 100, 101, 102, 103, 104 };
	constexpr size_t n = sizeof(v.underlying()) /
							sizeof(decltype(v)::value_type);  
						 // sizeof(Array<int,5>::value_type);
	static_assert(v.size() == n);
```
- `decltype()` to get type of a variable

## `std::array`
Same fixed size
```cpp
	std::array<int,5> v { 100, 101, 102, 103, 104 };
	for (size_t i = 0; i < v.size(); ++i)  { print_int(v[i]); }
```

## `std::vector`
Initialization similar to array
- Also guarantees elements are **contiguous**
- `push_back()` may **invalidate** pointers and <span style="color:rgb(255, 0, 0)">refs</span>!

```cpp
	std::vector<int> v { 100, 101, 102, 103, 104 };
	v.push_back(105);
	for (size_t i = 0; i < v.size(); ++i)  { print_int(v[i]); }
```

Can use directly list-initialization. The compiler can deduce type `T`
```cpp
	std::vector v { 100, 101, 102, 103, 104 };
```

## `std::deque`
**Double-ended** queue
- Vector with `push_front()` in $O(1)$, 
	- vs vector $O(n)$ (must shift everything)
	- Existing elements **never move**, pointer and refs are preserved on pushing front/back
		- **Not preserved** if `insert()` or `delete()` in the middle :(
- **No contiguity** guarantee
	- Chunks (still good cache locality)
	- Slower access
```cpp
	deque<int> v { 100, 101, 102, 103, 104 };
	v.push_front(99);
	v.push_back(105);
```

### Implementation
Deque maintains a chunk pointer array
- Allocate a new chunk if needed
- Allocate new chunk pointer array, same as vector

![](/articles/s26/cpp/img/10-deque.svg)

## `std::list`
**Doubly** linked list
```cpp
	list<int> v { 100, 101, 102, 103, 104 };
	v.push_front(99);
	v.push_back(105);
	while (!v.empty())  {
		print_int(v.front());
		v.pop_front();
	}
```
No `operator[]()`!!! Need to traverse yourself
- Avoid providing an inefficient version

Push and `insert()` all in $$O(1)$$
- Slower than vector in practice

## `std::forward_list`
Minimal singly linked list
- Just `push_back()`
```cpp
	forward_list<int> v { 100, 101, 102, 103, 104 };
	v.push_front(99);
	while (!v.empty())  {
		print_int(v.front());
		v.pop_front();
	}
```

`sizeof(forward_list<int>) = 8`
- **Header** is 8 bytes (single head pointer)
- Middle nodes will have size 12.

