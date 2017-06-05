from django import template
from random import randint
register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})

@register.assignment_tag
def evaluator_filter(evals, evaluator):
   return evals.filter(evaluator= evaluator)

@register.assignment_tag
def random(id):
    return randint(0,10000) + id

@register.simple_tag
def add(a , b):
    return a+b