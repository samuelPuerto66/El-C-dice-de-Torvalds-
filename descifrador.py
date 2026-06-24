import subprocess

def descifrar_codice():
    llave = "" # Aquí se irá armando la contraseña final [cite: 26]
    
    # 1. Traemos todo el historial de una sola vez: hash completo (%H) y sus padres (%P)
    # Ordenado del más antiguo al más reciente (--reverse) [cite: 21, 22]
    lineas_log = subprocess.check_output(["git", "log", "--reverse", "--format=%H %P"]).decode("utf-8").strip().split("\n")
    
    for linea in lineas_log:
        partes = linea.split()
        if not partes:
            continue
        
        c_hash = partes[0] # El primer elemento siempre es el hash del commit 
        es_merge = len(partes) > 1 # Si tiene más de un padre, es un commit de merge [cite: 31]
        
        # 2. Extraemos el contenido de nucleo.txt en este commit específico 
        try:
            contenido = subprocess.check_output(["git", "show", f"{c_hash}:nucleo.txt"], stderr=subprocess.DEVNULL).decode("utf-8").strip()
        except subprocess.CalledProcessError:
            continue # Si el archivo no existía en este punto, saltamos al siguiente commit
            
        if not contenido:
            continue

        # 3. EVALUACIÓN: Convertimos los primeros 6 caracteres del hash a número decimal [cite: 23]
        val_decimal = int(c_hash[:6], 16)
        
        # Contamos cuántos números (0-9) y cuántas letras (a-f) tiene el hash completo [cite: 27, 28]
        cant_numeros = sum(1 for char in c_hash if char.isdigit())
        cant_letras = sum(1 for char in c_hash if char.lower() in 'abcdef')
        
        # 4. MÁQUINA DE ESTADOS: Aplicamos el cifrado según si el decimal es Par o Impar [cite: 24]
        if val_decimal % 2 == 0:
            # CASO PAR: Cifrado César al primer carácter usando la cantidad de números [cite: 27]
            letra_inicial = contenido[0]
            # Calculamos su posición en el abecedario (A=0, B=1, etc.), sumamos el desplazamiento y reiniciamos en 26 si se pasa
            posicion = ord(letra_inicial) - ord('A')
            nueva_posicion = (posicion + cant_numeros) % 26
            caracter_final = chr(nueva_posicion + ord('A'))
        else:
            # CASO IMPAR: Al valor ASCII del último carácter le sumamos la cantidad de letras (a-f) [cite: 28, 29]
            letra_final = contenido[-1]
            caracter_final = chr(ord(letra_final) + cant_letras)
        
        # Agregamos el carácter descubierto a nuestra Llave [cite: 30]
        llave += caracter_final
        
        # 5. MUTACIÓN FINAL: Si este commit era un Merge, invertimos la Llave de inmediato [cite: 31]
        if es_merge:
            llave = llave[::-1]
            
    # Al terminar el bucle, imprimimos únicamente el resultado definitivo 
    print(llave)

if __name__ == "__main__":
    descifrar_codice()