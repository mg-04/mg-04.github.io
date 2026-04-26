---
title: "C2cpp Notes: Smart Pointers"
permalink: /articles/cpp/3new
---

{% include toc %}

> This page is under construction.
{: .notice--warning}


# 17. Smart Pointer
> **Suicidal Pointer**  
> A class with **pointer inside** and acts like a pointer (`op*()`, `op->()`)
> - Self-delete when goes out of scope
> - How making two copies? Who's deleting it?
> 	- Shared pointer: know each other; deleted only after all gone
> 	- Unique pointer: Only one can hold it; can only be moved
{: .notice--info}


## Shared Pointer

### Implementation
```cpp
template <typename T> class SharedPtr {
	T* ptr;
	int* count;	
public:
	explicit SharedPtr(T* p = nullptr): ptr{p}, count{new int{1}} {}
	~SharedPtr() {
		if(--*count == 0) {
			delete count; delete ptr;
		}
	}

	T& operator*() const { return *ptr; }
	T* operator->() const { return ptr; }
	
	operator void*() const { return ptr; }   // for if (sp)
	T* get_prt() const { return ptr; }       // get() in STL
	int get_count() const { return *count; }
```
- Constructed with a pointer (E. `new string{}`)
- Manages **heap-allocated** data and `count`
- Last one out of scope is responsible for deletion

```cpp
	SharedPtr*(const SharedPtr<T>& sp): ptr(sp.ptr), count(sp.count) {
		++*count;
	}
	SharedPtr<T>& operator=(const SharedPtr<T>& sp) {
		if (this != &sp) {    // delete, and then construct
			if (--*count == 0) {delete count; delete sp;}
			ptr = sp.ptr;
			count = sp.count;
			++*count;
		}
		return *this;
	}
};
```
- Copy constructor makes a **shallow copy** of `ptr` and `count`; increments `*count`
- Copy assignment, need **detach first**

**Example**
```cpp
SharedPtr<string> p1 = {new string{"hello"}};
auto foo = [=] (SharedPtr<string> p) {  // take p by value, CC!
	cout << p.get_count() << endl;
}
foo(p1);
```
This will invoke copy constructor, incrementing `count`
After `foo()` returns, `p` goes out of scope, and `count` decrements back

### Vector
Let `SharedPtr<string>` contain a `string*` inside
```cpp
auto create_vec1() {
	SharedPtr<string> p1 { new string{"hello"} };
	SharedPtr<string> p2 { new string{"c"} };
	SharedPtr<string> p3 { new string{"students"} };

	vector v { p1, p2, p3 };
	return v;
}

vector v1 = create_vec1();
```
1. Shared pointers themselves `p1`... are stack-allocated
	- `string` objects are heap allocated
2. When creating a vector, will make another **copy** of the string!
	- Should be `vector<SharedPtr<s`
3. Return by value: `v` will get moved/elided
	- Stack-allocated `p1` goes out of scope, `count` goes back to 1
![](/articles/s26/cpp/img/17-vec-1.svg)
When `create_vec1()` returns, stack pointers destroyed, and `v` moved/elided
Now modify it:
```cpp
vector v2 = v1;   // copy pointers, but still same underlying string
*v2[1] = "c2cpp";
*v2[2] = "hackers"; 

// print v1 again
for (auto&& p : v1) { cout << *p + " "; } cout << '\n';
```
1. **Copy construct** `v1` to `v2`
	- `count` goes up to 2
2. Modify `v2`: Dereference `SharedPtr` as *raw* pointer and modify it! 
3. Print original `v1`: **also modified**!
![](/articles/s26/cpp/img/17-vec-3.svg)

## Make Shared Pointer
Does the `new` with **any number** of arguments to construct `T`
- [Forwarding Reference](#forwarding-reference)!

```cpp
template <typename T, typename... Args>
SharedPtr<T> MakeSharedPtr(Args&&... args) {
	return SharedPtr<T>{ new T{forward<Args>(args)...} };
}
```

```cpp
auto p1 { MakeSharedPtr<string>("hello") };    // My implementation
auto p2 { make_shared<string>("c") };          // STL

static_assert(is_same_v< decltype(p2), shared_prt<string> >);
```

```cpp
{
	string* p0 { new string(50, 'A') };           // leak string and char[]
	shared_ptr<string> p1 { new string(50, 'B') };
	shared_ptr<string> p2 { new MakeSharedPtr<string>(50, 'C') };
}
```
`MakeSharedPtr` has one **fewer** allocation from Valgrind
- Library notices that `new string` is on the heap, so it combines the control block `count` and `string` in a single allocation (placement `new`)
- Our implementation uses `new string`, no such freedom

## Deletion
```cpp
{
SharedPtr<string> p0 { new string[2] {"a", "b"} };
}
```
Construction fine, but deletion **crashes** for `string[2]` ! Need `delete[]`

Need to write custom functor for `delete`

```cpp
SharedPtr<string> p0 {new string[2] {"a", "b"}, 
	[](string* s) {delete[] s;}
}
```

Can also do for `FILE`s
```cpp
shared_ptr<FILE> sp { fp,
	[](FILE* fp) {fclose(fp);}
}
```

Or, directly put `<string[]>` as the type for STL


```cpp
for (SharedPtr<string> p : v1) { cout << *p + " "; }
for (auto p : v1) 
for (auto& p : v1)
for (const auto& p : v1)
for (auto&& p : v1)
```
- `auto&&` declares a [forwarding reference](#forwarding-reference)
	- `x` can either be an L-value ref or R-value ref, depending on category of `*v1.begin()`
	- Useful if iterator return is unknown
	- E. `vector<bool>`
