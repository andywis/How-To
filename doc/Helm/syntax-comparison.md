# Helm

(Aug 2020)

An overview of some differences between Helm and Jinja2 syntax

## What is Helm (and Helm Charts)

Helm provides a templating language for Yaml files used to define a
configuration in Kubernetes, and includes tools to deploy the
config.

It is written in Go, and uses {{ var }} syntax, which makes it look
very similar to Ansible and Jinja2 (a Python templating language)

But they're not the same

Here are some simplistic examples. (apologies for the monospaced table)

```
Helm                                      Jinja2
----                                      -------
{{ if thing }}                            {% if thing %}
  something                                 something
{{ end }}                                 {% endif %}

# Iterating
{{- range .Values.pizzaToppings }}        {% for item in navigation %}
- {{ . | title | quote }}                   <li>{{ item.name }}"</li>
{{- end }}                                {% endfor %}

# suppress whitespace                     # strip whitespace 
{{- if expression }}                      {% for item in seq -%}
```


## Sources
https://helm.sh/docs/chart_template_guide/control_structures/

https://jinja.palletsprojects.com/en/2.11.x/templates/#list-of-control-structures

https://youtu.be/fy8SHvNZGeE