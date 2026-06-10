---
title: "ASP Zookeeper"
excerpt: "(Subsets of) `malloc`, `grep`, chat server, `gdb`, `ld`, and a container manager<br/><img src='/images/projects/asp.png' style='width:500px;'>"
collection: projects
date: 2025-05-18
authors:
    - Ming Gong
    - David Juarez
    - Keshav Beriwal
---

{% include toc %}


{% if page.authors %}
<div class="page__meta" style="margin: 0 0 1rem 0;">
  <strong>Authors:</strong> {{ page.authors | join: ", " }}
</div>
{% endif %}


From [COMS 4157](https://cs4157.github.io/www/2025-1/) Advanced Systems Programming

---
# Malloctupus: A Memory Allocator Library
[Assignment](https://cs4157.github.io/malloctopus/) | [Repo](https://github.com/mgongd/hw1-The-Debuggers)  
A custom memory allocator library in C
- Implicit free list allocator
- Explicit free list
- Segregated free list


# Greptile: Multi-Threaded `grep`
[Assignment](https://cs4157.github.io/greptile/) | [Repo](https://github.com/mgongd/hw2-The-Debuggers)    
Multi-threaded command-line search tool
- POSIX regex matching
- Directory traversal, handling file permissions, symlinks, and hidden files
- Multi-threaded parallelization


# Cowchat: A Chat Server
[Assignment](https://cs4157.github.io/cowchat/) | [Repo](https://github.com/mgongd/hw3-The-Debuggers)    
Multi-room, real-time chat server and client application
- Socket networking and protocol parsing
- Multi-client server concurrency with `poll` and `select`
- State management and broadcast routing

# Ladebug: A Rudimentary Debugger
[Assignment](https://cs4157.github.io/ladebug/) | [Repo](https://github.com/mgongd/hw4-The-Debuggers)    
Functional, scriptable command-line debugger, a subset of `gdb`
- Process control and tracing via `ptrace` system call
- Register inspection and software breakpoints by replacing instruction with interrupt opcode
- ELF Symbol table parsing and scripted automation

# Seald: A Simple Linker
[Assignment](https://cs4157.github.io/seald/) | [Repo](https://github.com/mgongd/hw5-The-Debuggers)    
Static linker, subset of `ld`
- ELF object file parsing
- Symbol resolution and global symbol table across different source files
- Object relocation and executable layout calculation

# Zookeeper: A Container Manager
[Zookeeper](https://cs4157.github.io/zookeeper/) | [Repo](https://github.com/mgongd/hw6-The-Debuggers)    
- Namespace isolation and virtualization
- File system permissions and resource limits with `cgruops`
- System call filtering via `seccomp`