---
layout: page
title: research
permalink: /research/
description: Selected projects in robotic mechanisms, actuation, embedded control, and experimental validation.
nav: true
nav_order: 1
display_categories: false
horizontal: true
---

My projects explore how mechanical design, actuation, sensing, and embedded control can be integrated into functional robotic systems. They span motorized catheter management for industrial inspection, magnetically steerable imaging devices, soft actuators, and miniature robotic mechanisms. Each project identifies my contributions and the scope of experimental validation. This experience provides a foundation for my intended PhD research in cable-driven and wearable robotics.

[Research Portfolio (PDF)](/assets/pdf/Shuwei_Zhao_Research_Portfolio.pdf?v=20261022) &nbsp;&middot;&nbsp; [CV (PDF)](/assets/pdf/Shuwei_Zhao_CV.pdf?v=20261022)

<!-- pages/projects.md -->
<div class="projects">
{% if site.enable_project_categories and page.display_categories %}
  <!-- Display categorized projects -->
  {% for category in page.display_categories %}
  <a id="{{ category }}" href=".#{{ category }}">
    <h2 class="category">{{ category }}</h2>
  </a>
  {% assign categorized_projects = site.projects | where: "category", category %}
  {% assign sorted_projects = categorized_projects | sort: "importance" %}
  <!-- Generate cards for each project -->
  {% if page.horizontal %}
  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
  {% endfor %}

{% else %}

<!-- Display projects without categories -->

{% assign sorted_projects = site.projects | sort: "importance" %}

  <!-- Generate cards for each project -->

{% if page.horizontal %}

  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
{% endif %}
</div>
