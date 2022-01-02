#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################
# Author: Rubén Fortunato
# Versión: 1
# Fecha: 13-ago-2015
################################################################
# Convierte monto de hasta 999 999 999 999.99 pesos a palabras.
# Acepta string o integer como parametro de entrada.
################################################################
#
# Para probar, ejemplo:
# $ python3 to_word.py 12901.27
# $ Son pesos: doce mil novecientos uno con 27/100
#
# La variante comentada genera:
# $ python3 to_word.py 12901.27
# $ Son: doce mil novecientos un pesos con 27/100
#
# Para usar como módulo python3:
# monto_en_letras =  to_word(monto_en_números)
#
################################################################
# Usa un algoritmo recursivo muy compacto que respeta todas las
# normas de escritura de números en español.
################################################################

#import sys
import sys
import re
from decimal import *

unidades = (
    'cero ',
    'un ',
    'dos ',
    'tres ',
    'cuatro ',
    'cinco ',
    'seis ',
    'siete ',
    'ocho ',
    'nueve ',
    'diez ',
    'once ',
    'doce ',
    'trece ',
    'catorce ',
    'quince ',
    'dieciséis ',
    'diecisiete ',
    'dieciocho ',
    'diecinueve ',
    'veinte ',
    'veintiún ',
    'veintidós ',
    'veintitrés ',
    'veinticuatro ',
    'veinticinco ',
    'veintiséis ',
    'veintisiete ',
    'veintiocho ',
    'veintinueve ',
)

decenas = (
    'treinta ',
    'cuarenta ',
    'cincuenta ',
    'sesenta ',
    'setenta ',
    'ochenta ',
    'noventa ',
)

centenas = (
    'cien ',
    'ciento ',
    'doscientos ',
    'trescientos ',
    'cuatrocientos ',
    'quinientos ',
    'seiscientos ',
    'setecientos ',
    'ochocientos ',
    'novecientos ',
)


def traverse(n):
    n = int(n)

    if n <= 29:
        return unidades[n]
    elif n <= 99:
        q, r = divmod(n, 10)
        return decenas[q-3] + ("y " + traverse(r) if r else "")
    elif n <= 999:
        q, r = divmod(n, 100)
        return (centenas[q-1] if (q == 1 and r == 0) else centenas[q]) + (traverse(r) if r else "")
    elif n <= 999999:
        q, r = divmod(n, 1000)
        return (traverse(q) if q > 1 else "") + "mil " + (traverse(r) if r else "")
    elif n <= 999999999999:
        q, r = divmod(n, 1000000)
        return traverse(q) + ("millón " if q == 1 else "millones ") + (traverse(r) if r else "")
    return '??? '


def ent2txt(n):
    #    return traverse(int(n))
    return re.sub('(ú|u)n $', 'uno ', traverse(int(n)), re.UNICODE)


def dec2txt(n):
    n = int((n-int(n))*100)
    return ('con '+str(n)+'/100' if n else '')

# def moneda(n):
#    n = int(n)
#    q, r = divmod(n, 1000000)
#    if n == 1: return 'peso '
#    if q > 0 and r == 0: return 'de pesos '
#    else: return 'pesos '

# Con la variente en comentarios sería:
# $ python3 to_word.py 12901.27
# $ Son: doce mil novecientos un pesos con 27/100

monedas = {"ARS": " pesos", "USD": ' dólares', 'EUR': ' euro'}

def to_word(n, moneda):
    try:
        m = Decimal(n).quantize(Decimal('0.01'))
    except Exception:
        return 'NUMERO INVALIDO'

    moneda = monedas.get(moneda, '')

    return 'Son{}: {}{}'.format(moneda, ent2txt(m), dec2txt(m))


# Para probar:
# $ python3 to_word.py 12901.27
# $ Son pesos: doce mil novecientos uno con 27/100
if __name__ == '__main__':
    print(to_word(sys.argv[1], 'ARS'))
