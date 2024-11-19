
from datetime import datetime
from collections import Counter

# Listas de activos regularizados válidos
ACTIVOS_VALIDOS_ARGENTINA = [
    "Moneda nacional o extranjera en efectivo o en cuentas bancarias en Argentina",
    "Inmuebles ubicados en Argentina",
    "Acciones o participación en sociedades no cotizadas en Argentina",
    "Títulos valores cotizados en Argentina",
    "Otros bienes muebles ubicados en Argentina",
    "Créditos con deudores residentes en Argentina",
    "Derechos y otros bienes intangibles en Argentina",
    "Criptomonedas, criptoactivos y similares"
]

ACTIVOS_VALIDOS_EXTERIOR = [
    "Moneda extranjera en efectivo o en cuentas bancarias en el exterior",
    "Inmuebles ubicados fuera de Argentina",
    "Acciones o participación en sociedades no cotizadas fuera de Argentina",
    "Títulos valores cotizados en el exterior",
    "Otros bienes muebles ubicados fuera de Argentina",
    "Créditos con deudores no residentes en Argentina",
    "Derechos y otros bienes intangibles en el exterior"
]

# Función para validar DNI (solo dígitos, longitud específica)
def validar_dni(dni):
    return dni.isdigit() and len(dni) == 8

# Función para validar edad (número entero positivo)
def validar_edad(edad):
    return edad.isdigit() and 0 < int(edad) <= 120

# Función para validar fecha en formato DD-MM-YYYY y que no sea futura
def validar_fecha(fecha):
    if "-" in fecha and len(fecha) == 10:  # Verificar el formato general
        dia, mes, año = fecha.split("-")
        if dia.isdigit() and mes.isdigit() and año.isdigit():
            try:
                fecha_ingresada = datetime(int(año), int(mes), int(dia)).date()
                return fecha_ingresada <= datetime.now().date()
            except ValueError:
                return False  # Fecha inválida (por ejemplo, 30-02-2023)
    return False  # Formato incorrecto


# Función para validar monto (número flotante positivo)
def validar_monto(monto):
    try:
        return float(monto) > 0
    except ValueError:
        return False

# Función para validar origen de fondos
def validar_origen_fondos(origen):
    return origen in ["Argentina", "Exterior"]

# Función para validar tipo de activo regularizado en Argentina o Exterior
def validar_activo_regularizado(origen, activo):
    if origen == "Argentina":
        return activo in ACTIVOS_VALIDOS_ARGENTINA
    elif origen == "Exterior":
        return activo in ACTIVOS_VALIDOS_EXTERIOR
    return False

# Función para ingresar la información de un contribuyente con validaciones
def ingresar_contribuyente():
    contribuyente = {
        'dni': '',
        'apellido': '',
        'nombre': '',
        'edad': 0,
        'fecha_nacimiento': '',
        'profesion': '',
        'fecha_declaracion': '',
        'monto': 0.0,
        'origen_fondos': '',
        'activo_regularizado': ''
    }
    
    # Validación de DNI
    while True:
        dni = input("Ingrese DNI (8 dígitos): ")
        if validar_dni(dni):
            contribuyente['dni'] = dni
            break
        print("DNI inválido. Debe ser un número de 8 dígitos.")

    # Validación de apellido y nombre
    contribuyente['apellido'] = input("Ingrese Apellido: ").strip()
    contribuyente['nombre'] = input("Ingrese Nombre: ").strip()
    
    # Validación de edad
    while True:
        edad = input("Ingrese Edad: ")
        if validar_edad(edad):
            contribuyente['edad'] = int(edad)
            break
        print("Edad inválida. Debe ser un número entre 1 y 120.")
    
    # Validación de fecha de nacimiento
    while True:
        fecha_nacimiento = input("Ingrese Fecha de Nacimiento (DD-MM-YYYY): ")
        if validar_fecha(fecha_nacimiento):
            contribuyente['fecha_nacimiento'] = fecha_nacimiento
            break
        print("Fecha de nacimiento inválida. Debe tener el formato DD-MM-YYYY y no ser posterior a hoy.")
    
    # Validación de profesión
    contribuyente['profesion'] = input("Ingrese Profesión: ").strip()
    
    # Validación de fecha de declaración
    while True:
        fecha_declaracion = input("Ingrese Fecha de Declaración (DD-MM-YYYY): ")
        if validar_fecha(fecha_declaracion):
            contribuyente['fecha_declaracion'] = fecha_declaracion
            break
        print("Fecha de declaración inválida. Debe tener el formato DD-MM-YYYY y no ser posterior a hoy.")
    
    # Validación de monto
    while True:
        monto = input("Ingrese Monto a Declarar: ")
        if validar_monto(monto):
            contribuyente['monto'] = float(monto)
            break
        print("Monto inválido. Debe ser un número positivo.")

    # Validación de origen de fondos
    while True:
        origen_fondos = input("Ingrese Origen de los Fondos (Argentina/Exterior): ")
        if validar_origen_fondos(origen_fondos):
            contribuyente['origen_fondos'] = origen_fondos
            break
        print("Origen de fondos inválido. Debe ser 'Argentina' o 'Exterior'.")

    # Validación del tipo de activo regularizado según origen
    activos_lista = (ACTIVOS_VALIDOS_ARGENTINA if contribuyente['origen_fondos'] == "Argentina"
                     else ACTIVOS_VALIDOS_EXTERIOR)
    
    while True:
        print("\nSeleccione el tipo de activo regularizado:")
        for i, activo in enumerate(activos_lista, start=1):
            print(f"{i}. {activo}")
        tipo_activo = input("Ingrese el número correspondiente al activo: ")
        try:
            tipo_activo = int(tipo_activo)
            if 1 <= tipo_activo <= len(activos_lista):
                contribuyente['activo_regularizado'] = activos_lista[tipo_activo - 1]
                break
            else:
                print("Opción inválida. Intente de nuevo.")
        except ValueError:
            print("Entrada inválida. Debe ser un número correspondiente al activo.")
    
    return contribuyente
# Función para procesar los datos y mostrar resultados
def procesar_datos(contribuyentes):
    if not contribuyentes:
        print("No hay datos de contribuyentes para procesar.")
        return

    edades = [c['edad'] for c in contribuyentes]
    fechas_declaracion = [datetime.strptime(c['fecha_declaracion'], "%d-%m-%Y") for c in contribuyentes]
    montos = [c['monto'] for c in contribuyentes]
    activos = [c['activo_regularizado'] for c in contribuyentes]
    origen_fondos = [c['origen_fondos'] for c in contribuyentes]
    profesiones = [c['profesion'] for c in contribuyentes]

    total_contribuyentes = len(contribuyentes)
    menor_edad = min(edades)
    mayor_edad = max(edades)
    promedio_edad = sum(edades) / total_contribuyentes
    fecha_mas_lejana = min(fechas_declaracion)
    fecha_mas_cercana = max(fechas_declaracion)
    monto_minimo = min(montos)
    monto_maximo = max(montos)
    promedio_monto = sum(montos) / total_contribuyentes

    activos_counter = Counter(activos)
    activo_mas_repetido = activos_counter.most_common(1)[0][0]
    activo_menos_repetido = min(activos_counter, key=activos_counter.get)

    argentina_count = origen_fondos.count("Argentina")
    exterior_count = origen_fondos.count("Exterior")
    porcentaje_argentina = (argentina_count / total_contribuyentes) * 100
    porcentaje_exterior = (exterior_count / total_contribuyentes) * 100

    ranking_profesiones = Counter(profesiones).most_common()
    ranking_origen_fondos = Counter(origen_fondos).most_common()

    print("\nResumen de Declaraciones de Activos")
    print(f"Total de personas registradas: {total_contribuyentes}")
    print(f"Menor edad: {menor_edad}")
    print(f"Mayor edad: {mayor_edad}")
    print(f"Edad promedio: {promedio_edad:.2f}")
    print(f"Fecha de declaración más lejana: {fecha_mas_lejana.strftime('%d-%m-%Y')}")
    print(f"Fecha de declaración más cercana: {fecha_mas_cercana.strftime('%d-%m-%Y')}")
    print(f"Monto mínimo a declarar: {monto_minimo}$")
    print(f"Monto máximo a declarar: {monto_maximo}$")
    print(f"Monto promedio a declarar: {promedio_monto:.2f}$")
    print(f"Activo regularizado más repetido: {activo_mas_repetido}")
    print(f"Activo menos repetido: {activo_menos_repetido}")
    print(f"Porcentaje en Argentina: {porcentaje_argentina:.2f}%")
    print(f"Porcentaje en el Exterior: {porcentaje_exterior:.2f}%")

    print("\nRanking de Profesiones:")
    for profesion, cantidad in ranking_profesiones:
        print(f"{profesion}: {cantidad}")

    print("\nRanking de Origen de Fondos:")
    for origen, cantidad in ranking_origen_fondos:
        print(f"{origen}: {cantidad}")

# Función para consultar un contribuyente por su DNI
def consultar_contribuyente(contribuyentes):
    while True:
        dni_consulta = input("Ingrese el DNI del contribuyente a consultar: ")
        contribuyente_encontrado = next((c for c in contribuyentes if c['dni'] == dni_consulta), None)

        if contribuyente_encontrado:
            print(f"\nDatos del contribuyente con DNI {dni_consulta}:")
            print(f"Apellido: {contribuyente_encontrado['apellido']}")
            print(f"Nombre: {contribuyente_encontrado['nombre']}")
            print(f"Edad: {contribuyente_encontrado['edad']}")
            print(f"Fecha de Nacimiento: {contribuyente_encontrado['fecha_nacimiento']}")
            print(f"Profesión: {contribuyente_encontrado['profesion']}")
            print(f"Fecha de Declaración: {contribuyente_encontrado['fecha_declaracion']}")
            print(f"Monto a Declarar: {contribuyente_encontrado['monto']}$")
            print(f"Origen de los Fondos: {contribuyente_encontrado['origen_fondos']}")
            print(f"Activo Regularizado: {contribuyente_encontrado['activo_regularizado']}")
            break
        else:
            print(f"No se encontró un contribuyente con el DNI {dni_consulta}. Intente nuevamente.")

# Función principal
def main():
    contribuyentes = []
    while True:
        contribuyentes.append(ingresar_contribuyente())
        if input("¿Desea ingresar otro contribuyente? (si/no): ").lower() != 'si':
            break

    procesar_datos(contribuyentes)

    # Validación de entrada para consultar datos
    while True:
        respuesta = input("¿Desea consultar los datos de un contribuyente por su DNI? (si/no): ").lower()
        if respuesta == 'si':
            consultar_contribuyente(contribuyentes)
            break
        elif respuesta == 'no':
            print("Operación cancelada.")
            break
        else:
            print("Entrada no válida. Por favor, responda 'si' o 'no'.")

# Ejecutar función principal
main()

