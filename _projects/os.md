---
title: "Freezer Scheduler and EZFS"
teaser: '/images/projects/os/5.png'
excerpt: "Implementation of Linux utilities: in-kernel key-value store, custom round-robin scheduler, page walk, and a lightweight filesystem."
course: "Operating Systems, Spring 2026"
collection: projects
date: 2026-05-24
authors:
    - Ming Gong, Ryan Wang, Chris Henry
---

{% include toc %}


{% if page.authors %}
<div class="page__meta" style="margin: 0 0 1rem 0;">
  <strong>Authors:</strong> {{ page.authors | join: ", " }}
</div>
{% endif %}


# 1. Linux-List
A simple Linux linked list to prepresent Pokémon

# 2. Shell
Implementation of a shell directly calling system calls

A bare-metal bootable OS using assembly

# 3. [Tabletop](/articles/os/1-asp#hw3)
A simple syscall reading the file descriptor table

# 4. [Fridge](/articles/os/2-sched#hw-4): In-Kernel Key-Value Store
[Assignment](https://columbia-os.github.io/fridge/) | [Repo](https://github.com/columbia-os-hw-s2026/hw4-Team1)  
A robust, high-concurrency, and thread-safe kernel kv pair
- Entries distributed across a fixed-length chained hash table
- Designed to prevent kernel panics, data corruption, or memory leaks. Robust against userspace abuse
- Dedicated SLAB cache, reducing memory fragmentation and improving cache locality
- Support producer-consumer blocking behaviors using Linux wait queues. Handles signals properly.

# 5. [Freezer](/articles/os/2-sched#hw-5-scheduler): Custom Linux Kernel Scheduler
[Assignment](https://columbia-os.github.io/freezer-Sp2026/) | [Repo](https://github.com/columbia-os-hw-s2026/hw5-Team1)  
**Freezer**: A round-robin scheduling algorithm
- Static time slice
- Symmetric multiprocessing and load balancing
- Set and stress-tested as the default scheduler

**Heater**: A FIFO scheduler with a global run queue

Extensive performance evaluation under various environments and workloads

![](/images/projects/os/5.png)

# 6. [Farfetchd](/articles/os/3-mm#hw-6): Kernel Memory Introspection & Device Driver
[Assignment](https://columbia-os.github.io/farfetchd/) | [Repo](https://github.com/columbia-os-hw-s2026/hw6-Team-Gengar)
- Manual 5-level page walk
- Memory introspection with `bvi`
- Pseudo-device driver integration with `ioctl()`

![](/images/projects/os/6.png)

# 7. [EZFS](/articles/os/4-io#hw7): A Lightweight Filesystem
[Assignment](https://columbia-os.github.io/ezfs/) | [Repo](https://github.com/columbia-os-hw-s2026/hw7-Team-Gengar)
- **VFS integration**: `super_operations`, `inode_operations`, `file_operations`
- **Core operations**: file lookup, directory reading/editing, custom file boundaries
- **Fine-grained concurrency**: thread-safe metadata handling
- **Kernel module integration**

![](/images/projects/os/7.png)