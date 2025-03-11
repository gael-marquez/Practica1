from datetime import date

# Definir dos fechas
fecha_Gael = date(2004, 9, 15)
fecha_Brandon = date(2004, 10, 8)
fecha2 = date(2025, 3, 10)

# Calcular la diferencia
diferencia_g = fecha2 - fecha_Gael
diferencia_b = fecha2 - fecha_Brandon


# Mostrar el resultado
print("Gael: ", diferencia_g.days)
print("Modulo: ", (diferencia_g.days % 3))
print("Brandon: ", diferencia_b.days)
print("Modulo: ", (diferencia_b.days % 3))


