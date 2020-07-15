from django import template

register = template.Library()

@register.filter(name='reformat_hari')
def reformat_hari(value):
    # print(value)
    if value:
        values = value.split(";")
        values = [get_hari(x) for x in values]
        values = ", ".join(values)
    else:
        values = 'Senin, Selasa, Rabu, Kamis, Jumat, Sabtu'
    return values

def get_hari(hari):
    haris = {
        '1': 'Senin',
        '2': 'Selasa',
        '3': 'Rabu',
        '4': 'Kamis',
        '5': 'Jumat',
        '6': 'Sabtu'
    }.get(hari, "")
    return haris