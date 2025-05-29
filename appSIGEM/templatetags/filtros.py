from django import template

register = template.Library()

@register.filter
def dict_get(diccionario, clave):
    if isinstance(diccionario, dict):
        return diccionario.get(clave)
    return None


from django import template

register = template.Library()

@register.filter
def dictget(d, key):
    if isinstance(d, dict):
        return d.get(key)
    return None
