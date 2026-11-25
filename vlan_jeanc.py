
try:
    vlan = int(input("Ingrese el número de VLAN a verificar: "))

    if 1 <= vlan <= 1005:
        print(f"La VLAN {vlan} corresponde a un RANGO NORMAL de VLAN (1 - 1005).")
    elif 1006 <= vlan <= 4094:
        print(f"La VLAN {vlan} corresponde a un RANGO EXTENDIDO de VLAN (1006 - 4094).")
    else:
        print(f"El número {vlan} NO corresponde a una VLAN válida (rango permitido: 1 - 4094).")
except ValueError:
    print("Error: Debe ingresar un valor numérico entero.")
