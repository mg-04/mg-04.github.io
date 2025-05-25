---
#layout: post
title:  "AP Does Not Mean APlus"
date:   2025-1-10 14:05:30 -0500
permalink: /posts/2025/01/ap
tags:
    - academia
    - cs
excerpt: >
 After the long, long wait, Jae finally posted his grades.
---
After the long, long wait, Jae finally posted his grades.
## Metrics
With some simple calculation, we can analyze a few metrics related to this grade cutoff. 
- **Percentage**: Your score normalized to 96.95121951, the maximum possible raw score
- **Diff**: The grade **window** of each letter
- **Exam loss**: The maximum allowable missed points for all three exams combined, assuming a perfect lab score.

| Grade | Raw     | Percentage   | Diff    | Exam Loss |
|-------|---------|---------|---------|-----------|
| A+    | 94.896  | 97.88%  | 2.06%   | 8.22      |
| A     | 86.683  | 89.41%  | 8.47%   | 41.07     |
| A-    | 75.756  | 78.14%  | 11.27%  | 84.78     |
| B+    | 67.329  | 69.45%  | 8.69%   | 118.49    |
| B     | 56.640  | 58.42%  | 11.03%  | 161.24    |
| B-    | 49.689  | 51.25%  | 7.17%   | 189.05    |
| C+    | 41.181  | 42.48%  | 8.78%   | 223.08    |
| C     | 32.457  | 33.48%  | 9.00%   | 257.98    |
| C-    | 21.866  | 22.55%  | 10.92%  | 300.34    |
| D     | 0.000   | 0.00%   | 22.55%  | 387.80    |


Typically, the allowed *exam loss* decreases exponentially with difficulty (or GPA), but Jae Jae's A+ requires an exam average above 97%, destroying the pattern.

## Trivia
A few fun facts about the stats:
- At least 41/321 students were busted for cheating
    - Jae probably spent the time combating the cheaters
- The first place scored **0.054** points above the A+ line
- The upper quartile got A-
- If you take the non-zero mean and median stats from each lab and exam, the computed median will be two points lower than the actual final median
    - This is due to people dropping, which is crazy considering that the median delta is 0.14

    
## Finish off the proof (sort of)
> **Claim:** Any grade below an A- is easily achievable via hard and smart work. Everything above may not.

It's hard to formulate an actual *proof*, because "easily", "hard", "smart" are not well-defined. so we'll make a few assumptions and *not-so-rigorous* definitions, simulating a student's exam performance

Also I don't wish to write any complete *proof*s, as this whole article is completely pointless. Just some rant to 抛砖引玉

### Part 1: if you get below A- you suck

Assume the following:

1. You live in Fall 2024.
2. Your lab average is above 95%
3. Your exam average can be extrapolated from your exam 3 score, based on the median ratios
    - People with low scores in e1, e2 are more likely to drop the class, so the median score of e1, e2 for those that survived through should be significantly higher than actual
4. Assume there are 3 types of problems:
    - **Free points**: As long as you spend some time and effort through the material and practice exams, or show up to the exam. You get 100% on these.
    - **Trick Questions**: Fully solvable but tricky. You have 60% accuracy here.
    - **Almost Impossible**: Really out-of-scope or out-of-the-box. (*very* rare in a Jae exam). You get 0% on these.
5. Let's dissect exam 3:
    - 36 points for free
    - 62 points are tricky
    - 2 points are almost impossible

Given these assumptions, your expected e3 score would sum up to be **73.2%**, which estimates to a raw score of **76.5**, placing you right above the A- line.
$$\square$$

### Part 2: if you get above A- you don't suck


Let's simulate an *okay* student. in every exam, on average, you lose around 10 points.
- 2 points from the "impossible"
- 8 points from the "tricky" (87% accuracy)
    - This is fair, since you'll check over tricky problems



I here present a more sophisticated formula on your score estimate

$$\mathrm{score} = k_{\mathrm{free}}p_{\mathrm{free}} + (1-(1-k_{\mathrm{trick}}) r^{T-t_\mathrm{free}-t_{\mathrm{imp}}}) p_{\mathrm{trick}}, $$

where 
- $$p$$ is the probability (weight) of each problem type
- $$k$$ is the your average accuracy on each type
- $$T$$ is the time allowed
- $$t$$ is the time to complete/give up on questions
- $$r$$ is a rate constant for efficient during review

Let's take $$T = 90$$, $$t_\mathrm{free} = 18$$ (30 s/point), and $$t_\mathrm{imp} = 30$$ (unfortunately some of our time do become nothing). Therefore, we are left with 57 minutes on trick questions. Suppose it also takes half minute per point to check over trick questions, and $$ r = 0.5$$ Suppose your trick question miss rate halves each time you go over it.

---

***Below is under construction
***
{% comment %}

In the end, your 20% miss rate will be improved to a 5.2%. That's somewhat close to a 7.2% loss, combined with the impossible. For all 3 exams, it's 21.6%

This is an average, but I'm pretty sure there can exist cases where you hit that 10.9% on an entire 25-point problem. If you do it once, that's 46%, slightly below the A range

For A-, you have more room, affording about 2.52 times the senario above. 

How can the model be improved? Of course, there should be $$k$$, $$p$$, $$r$$ values associated with all types of problems, and there may be more types of problem as well. Furthermore, we can approximate the difficulty of the problems as a probability distribution, and $$k$$, $$p$$, $$r$$ can be made to be functions of such difficulty. 

{% endcomment %}

## Conclusion
- A+: #1 in the class
- A: 70% first-time accuracy, plus room for ~1 huge mistake
- A-: 70% first-time accuracy, plus room for ~2.5 huge mistakes $$\square$$

As you can see, $$t$$ and $$r$$ are dependent on $$p$$, so this model can be better refined. 

Of course, there is a lot to improve with this crude model. For instance, you can fit your accuracy with a normal distribution, and calculate, let's say, the 90% confidence interval for A and A-

## p.s. To Cheaters
If you chose to cheat, took the risk of getting busted, used some smart method to not get caught, and suffered through all the mental anxieties, and got an A, congratulations! Fully deserved!