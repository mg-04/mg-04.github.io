---
title: "Freezer Scheduler and EZFS"
excerpt: "Implementation of Linux utilities: scheduler, page walk, and file system<br/><img src='/images/projects/planet.png' style='width:500px;'>"
collection: projects
date: 2026-05-24
---

> This page is under construction
{: .notices--info}


# 1. Linux-List
A simple Linux linked list to prepresent Pokémon

# 2. Shell
Implementation of a shell directly calling system calls

A bare-metal bootable OS using assembly

# 3. Tabletop
A simple syscall reading the file descriptor table

# 4. Fridge: In-Kernel Key-Value Store
A robust, high-concurrency, and thread-safe kernel kv pair
- Entries distributed across a fixed-length chained hash table
- Designed to prevent kernel panics, data corruption, or memory leaks. Robust against userspace abuse
- Dedicated SLAB cache, reducing memory fragmentation and improving cache locality
- Support producer-consumer blocking behaviors using Linux wait queues. Handles signals properly.

# 5. Freezer: Custom Linux Kernel Scheduler
**Freezer**: A round-robin scheduling algorithm
- Static time slice
- Symmetric multiprocessing and load balancing
- Set and stress-tested as the default scheduler

**Heater**: A FIFO scheduler with a global run queue



Extensive performance evaluation under various environments and workloads

# 6. Farfetchd: Kernel Memory Introspection & Device Driver
- Manual 5-level page walk
- Memory introspection with `bvi`
- Pseudo-device driver integration with `ioctl()`

# 7. EZFS: A lightweight Filesystem Kernel Module
- **VFS integration**: `super_operations`, `inode_operations`, `file_operations`