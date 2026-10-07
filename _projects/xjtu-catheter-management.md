---
layout: page
title: Motorized Catheter Storage and Management System
description: A translating-pulley accumulator and motion-control software for industrial inspection
img: assets/img/projects/xjtu-catheter-management.jpg
importance: 4
category: research
---

As a **Research Assistant at Xi'an Jiaotong University during July–August 2026**, supervised by **Prof. Qiji Ze**, I developed a catheter management module for the group's magnetically steerable industrial-inspection system. The module manages excess catheter length during insertion and retraction to reduce uncontrolled bending and entanglement.

## My contribution

I designed and built a **motorized translating-pulley accumulator**. Moving the pulley by Δx provides approximately **ΔL ≈ 2Δx** of catheter-length compensation. I developed the assembly in **Fusion 360 and SolidWorks**, integrating a **120-mm guide pulley, 608 bearings, an MGN12H carriage, and a T8 lead screw**, with custom 3D-printed interfaces and supports.

I implemented the motion-control stack using a **Python/Tkinter interface**, USB serial communication, **Arduino UNO firmware**, and a **TB6600 stepper driver**. It supports manual calibration, jogging, fixed-distance motion, speed and acceleration settings, software travel limits, and a communication watchdog.

{% include figure.liquid loading="eager" path="assets/img/projects/xjtu-catheter-management.jpg" title="The laboratory's industrial-inspection setup, including the catheter management module and PC control interface I developed" class="img-fluid rounded z-depth-1" %}

The photograph shows the broader laboratory setup. My work focused on the catheter management module and its control software; the robot-assisted magnetic manipulation and complete inspection system were team infrastructure. This work addressed **industrial inspection**, with no claim of medical or clinical validation.

[View the research portfolio](/assets/pdf/Shuwei_Zhao_Research_Portfolio.pdf?v=20261006).
