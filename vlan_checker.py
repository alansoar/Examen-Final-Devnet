asvlan = input("Ingrese el número de VLAN: ")

if vlan.isdigit():
    vlan = int(vlan)
    if 1 <= vlan <= 1005:
        print("VLAN Estándar")
    elif 1006 <= vlan <= 4094:
        print("VLAN Extendida")
    else:
        print("VLAN no válida")
else:
    print("Entrada no válida. Debe ingresar un número.")
