---
layout: page
title: "Columbia Fall 24"
permalink: /f24
---
This is not meant to be a comprehensive review or reflection. Just a few personal experiences and opinions
# SSD
Exam time was really tight, and apparently the prof doesn't realize that (it's her second year teaching). Midterm 2 was 15 pages 75 minutes (5 minutes/**PAGE!**). To that point, you basically need to turn yourself into GNU Make and just plug in the numbers:

Here's Midterm 2, Problem 1:
![alt text](images/image-3.png)

```Makefile
W: epsilon, V0, q, Na, Nd
    W = sqrt(2*epsilon*V0/q * (1/Na + 1/Nd))
Vo: kT/q, Na, Nd, ni
    Vo = kT/q * ln(Na*Nd / ni^2)
kT/q: k, T, q
    kT/q = k * T / q
epsilon: eSi, e0
    epsilon = eSi * e0
```

```shell
$ ls -l
q       1.6E-19
kT/q    0.026
e0      8.85E-14
eSi     11.8
ni      1.5E10
Na      2E19
Nd      8E15

$ make W
kT/q = k * T / q
Vo = kT/q * ln(Na * Nd / ni^2)
epsilon = eSi * e0
W = sqrt(2 * epsilon * V0 / q * (1/Na + 1/Nd))
```
And here was what GNU Ming put down for zero bias:

![alt text](images/image-4.png)
# Circuits

![alt text](images/image-1.png)

The answer is:

$$
\begin{bmatrix}
\frac 1 R + j\omega C_1 + \frac 1 {j\omega L} & -\frac 1 {j\omega L}\\
-\frac 1 {j\omega L} - \frac{\beta}{j\omega L} & \frac 1 {j \omega L} + \frac{\beta}{j\omega L} + j\omega C_2
\end{bmatrix}
\begin{bmatrix}
\pmb{V_1}\\ \pmb{V_2}
\end{bmatrix}=\begin{bmatrix}
-\pmb{I_{S1}} + \frac{\pmb{V_S}}{R} \\
\pmb{I_{S1}} + \pmb{I_{S2}}
\end{bmatrix} 
$$

This looks complicated, but every bit of it makes sense, with beautiful linear algebra. 
If after some derivation, any of these does not seem obvious to you, consider dropping the major. Period.

Unfortunately, working out the algebra and solving for $\vec{\pmb{V}}$ is quite annoying. If there are number, I actually recommend to stay with the symbols until the very last step. 


# ELEN 3801 Signals and Systems
Another beautiful course

Exams are really, I mean really, fair game. Questions directly come from the book, lecture, or homework, and there is never anything incredibly difficult. Midterms does have some time pressure (10 minutes/problem), so make sure to practice those key problems. Speed and consistency is the key.

One rant is with exam cheat sheets. The intention is good--reducing our memorization. However, creating a cheat sheet often becomes another form of brute work. You have to admit that copying down every proof instead of trying to fully understand the derivation is easier and faster during prepration, and it's definitely much faster at the exam. Having more time and harder problems would reduce the reward to such practices. However, given the current stands, although I don't like cheat sheets, I still take full advantage of it...

Showing off my final grade there (I actually got 100%, since lowest HW and first two midterms dropped loll)

![alt text](images/image-2.png)
# CS 3157 AP

> You've probably heard of some horror stories of this class

Yes, after surviving an intensive 15-week brain workout, I can confirm the horror, but it's definitely manageable with the correct approach.

> Students are denied exceptions for the sake of fairness to the whole class

Yes, cheaters outscoring me on homework is infuriating!

## Material
> This stuff is not easy, even for those who like it

The class is basically 3 parts:
### 1. C programs
Theme: pointers and applications 
- E. array, heap, string, `struct`, function

### 2. Multiple programs
Now let's move beyond a single program, and learn how programs interact with others.
- Libraries
- Standard and file IO
- Multiprocessing: `fork()` and `execl()`
- UNIX: IO redirection, shell scripts

### 3. The internet
Now let's move beyond our local machine
- TCP/IP: `netcat`
- HTTP

and that's it! There's nothing too much to remember

## Labs
> Workload can be a bit lighter, or could be a lot heavier

I can confirm that the labs are pretty...easy, with clear instructions, expectations, and hints.

Most problems are fair-game coding problems. Not much Data Structures background needed. You don't need to be a competitive programmer. 

Do start the labs EARLY. It's not that they would take the full week to complete. However, it's important to reinforce your understanding. This is a tight class, and knowledge does build up.

## Exams
> Exams may not be super accurate in terms of assessing your understanding. That's a trade off that I have to make.

Yes, Jae admits this first day. Yet it takes a semester for me to understand.

- Exam 1 appears tricky, but if you know what you're doing, and what the *programs* are doing, you'll be fine. Just directly approach with memory diagrams.

- Exam 2 may have open-ended coding problems, which got me. There are a few tricky details to keep in mind when coding from scratch. Still, don't panic. Approach them normally.

- Exam 3 focused on multiprocessing and the internet, actually easier to prepare. No need to remember the boiler plates, but be sure to remember the structure of all Jae's codes.
 
Generally, there are two types of coding problems:
1. Write the code
    
    This is relatively straightforward. Open-ended coding problems are much easier than fill-in-the-blanks, as there's more room to forget details (E. initializing buffer)
2. Predict the output

    I don't quite like this, because it's very easy to miss a line of the code, or forget a particular behavior of a function. We are taught to be more skilled in *programming*, than *compiling*, which should be the job of gcc.
    - Problems vary in difficulty. Some have useful hints and checkpoints. Some have generous partial credit, while others are just "do-or-die". And you can't complain. They are just the nature of those problems. 

> You may not do well even if you try

**Claim:** any grade below an A- is easily achievable via hard and smart work. Everything above may not.

**Proof:** *This proof will be completed after Jae posts his cutoffs.* which is still not there by 1/2/2025, which irritates me!

It's not that the problems are impossible--anyone is *able* to get an 100 on any exam. Rather, it's the soul-sucking stress and the meticulous attention to detail.


From my personal perspective, getting a decent (90+) exam grade often comes down to a bit of luck. Everyone's intelligent and well-prepared. It's just a matter of whether or not you catch your mistake, and if you don't, you may be *very* heavily penalized. 

- Time may or may not be a factor here. Generally, the more time you spend checking, the more likely you'll catch your mistake, but for human brains, this relationship is far from linear.

- Part of your consistency can be improved by repeated practices, but there may always be something that is beyond your control. Again, far from linear.

At the end of the day, we are human, not machines, not computers, not gcc -g -Wall. We make mistakes, and that's part of what makes us human.

The takeaway is: don't over-stress about your AP grade, and don't let Jae Lee hurt your confidence in your ability, intelligence, carefulness, or hard work. As he said, in the end, this is just another course, and you have other priorities in life. 

> Some people think I'm a great professor. Some people think I'm a horrible human being.

In fact, this course is perfect in every aspect: the instructor, TAs, CLAC, lectures, labs, exams, and grading. You may not get the result you want, but you can't say anything wrong about its design and content. It is *that* good. I thoroughly enjoyed a dense portion of it--the only exceptions being the three (actually 6) instants when exam solutions/scores are released. 

This isn't meant to be a survivor's tale. Whether I get an A+ or end up with a C, my opinion remains unchanged: CS 3157 AP is an *awesome* class!