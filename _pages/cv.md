---
layout: page
permalink: /cv/
title: CV
nav: true
nav_order: 3
cv_pdf: /assets/pdf/Shuwei_Zhao_CV.pdf?v=20261022
description: Education, research experience, publications, honors, and technical skills.
toc:
  sidebar: left
---

[Download CV (PDF)](/assets/pdf/Shuwei_Zhao_CV.pdf?v=20261022) &nbsp;&middot;&nbsp; [Research Portfolio (PDF)](/assets/pdf/Shuwei_Zhao_Research_Portfolio.pdf?v=20261022)

{% assign cv = site.data.cv.cv %}

<div class="cv">
  <div class="card mt-3 p-3">
    <h2 class="card-title font-weight-medium">Professional Summary</h2>
    <p>{{ cv.summary }}</p>
    <p>{{ cv.name }} · {{ cv.label }} · {{ cv.location }} · {% al_email_protect_link cv.email %}</p>
    <p><a href="https://github.com/shuwei-zhao">GitHub</a> · <a href="https://www.linkedin.com/in/shuwei-zhao-5116382b1/">LinkedIn</a></p>
  </div>
  {% for section_pair in cv.sections %}
    {% assign section_title = section_pair[0] %}
    {% assign entries = section_pair[1] %}
    <div class="card mt-3 p-3">
      <h2 class="card-title font-weight-medium" id="{{ section_title | slugify }}">{{ section_title }}</h2>
      {% case section_title %}
        {% when 'Education' %}
          {% include cv/education.liquid %}
        {% when 'Research Experience' %}
          {% include cv/experience.liquid %}
        {% when 'Selected Course Project' %}
          {% for entry in entries %}
            <h3>{{ entry.title }}</h3>
            <p>{{ entry.position }} · {{ entry.company }} · October 2024–January 2025<br>{{ entry.summary }}</p>
            <ul>{% for item in entry.highlights %}<li>{{ item }}</li>{% endfor %}</ul>
          {% endfor %}
        {% when 'Publications' %}
          {% include cv/publications.liquid %}
        {% when 'Awards' %}
          {% include cv/awards.liquid %}
        {% when 'Skills' %}
          {% include cv/skills.liquid %}
        {% else %}
          <ul>{% for entry in entries %}<li>{{ entry.bullet }}</li>{% endfor %}</ul>
      {% endcase %}
    </div>
  {% endfor %}
</div>
