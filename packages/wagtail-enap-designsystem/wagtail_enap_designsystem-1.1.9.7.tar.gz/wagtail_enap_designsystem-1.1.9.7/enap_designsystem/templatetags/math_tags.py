from django import template

register = template.Library()

@register.filter
def mul(value, arg):
	try:
		return int(value) * int(arg)
	except:
		return ''

@register.filter
def classname(obj):
	return obj.__class__.__name__

