import re
import time
import datetime

class BPlusNode:
    def __init__(self, leaf=False):
        self.keys = []
        self.children = []
        self.leaf = leaf
        self.next = None  # Para enlazar nodos hoja

class BPlusTree:
    def __init__(self, t):
        self.root = BPlusNode(True)
        self.t = t  # Grado mínimo

    def insert(self, k, name):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1: #verifica si la raiz esta llena
            temp = BPlusNode() #crea un nuevo nodo temporal
            self.root = temp #asigna temp como la nueva raiz
            temp.children.insert(0, root) 
            self.split_child(temp, 0)
            self.insert_non_full(temp, k, name)
        else: #si no esta llena la raiz
            self.insert_non_full(root, k, name)

    def insert_non_full(self, x, k, name):
        i = len(x.keys) - 1
        if x.leaf: #si x es una hoja
            x.keys.append((None, None)) #añade un espacio vacio para la nueva clave
            while i >= 0 and k < x.keys[i][0]: #
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = (k, name) #inserta x en la poscion correcta
        else: #si x no es hoja
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t) - 1: #verifica si el hijo esta lleno 
                self.split_child(x, i) #llama a la funcion para dividir el hijo
                if k > x.keys[i]:
                    i += 1
            self.insert_non_full(x.children[i], k, name) #llama recursivamente a la funcion

    def split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = BPlusNode(y.leaf)
        x.children.insert(i + 1, z)
        
        if y.leaf: #si y es hoja
            z.keys = y.keys[t - 1:] #Mover las claves de la segunda mitad de y a z
            y.keys = y.keys[:t - 1] 
            x.keys.insert(i, z.keys[0][0])#Insertar la primera clave de z en x en la posición i
            z.next = y.next
            y.next = z
        else: #si y no es hoja
            z.keys = y.keys[t:] #Mover las claves de la segunda mitad de y a z
            y.keys = y.keys[:t - 1]
            x.keys.insert(i, y.keys[-1]) # Insertar la clave mediana de y en x en la posición i
            z.children = y.children[t:]
            y.children = y.children[:t]

    def save_to_file(self, filename): #escritura del archivo
        with open(filename, 'w') as f:
            self._write_node(self.root, f, 0)
    
    def _write_node(self, node, f, level):
        f.write('  ' * level + f'Node(keys={node.keys})\n')
        if not node.leaf:
            for child in node.children:
                self._write_node(child, f, level + 1)

def process_file(filename, t): #lectura de archivo de insercion
    tree = BPlusTree(t)
    total_insert_time = 0

    with open(filename, 'r') as file:
        lines = file.readlines()

    pattern_insert = re.compile(r'Insert:\{id:(\d+),nombre:(.+?)\}')

    log_entries = []

    # Procesar inserciones
    for line in lines:
        line = line.strip()
        if match := pattern_insert.match(line):
            key = int(match.group(1))
            name = match.group(2)
            start_time = time.time()
            start_dt = datetime.datetime.now()
            tree.insert(key, name)
            end_time = time.time()
            end_dt = datetime.datetime.now()
            elapsed_time = end_time - start_time
            total_insert_time += elapsed_time
            log_entries.append(f'Insert: Inicio: {start_dt}, Fin: {end_dt}, Tiempo: {elapsed_time:.6f} segundos, Id: {key}, Nombre: {name}')

    # Guardar el árbol en un archivo
    idx_filename = f"IDX_{filename.split('.')[0]}.TXT"
    start_write_time = time.time()
    start_write_dt = datetime.datetime.now()
    tree.save_to_file(idx_filename)
    end_write_time = time.time()
    end_write_dt = datetime.datetime.now()
    write_time = end_write_time - start_write_time

    log_entries.append(f'Guardar archivo: Inicio: {start_write_dt}, Fin: {end_write_dt}, Tiempo: {write_time:.6f} segundos, Archivo: {idx_filename}')

    # Guardar log
    log_filename = f"log-BPlusTree-{filename}-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
    with open(log_filename, 'w') as log_file:
        log_file.write('\n'.join(log_entries))

    # Mostrar tiempos
    print(f'Tiempo total de todas las inserciones: {total_insert_time:.6f} segundos')
    print(f'Tiempo de escritura del archivo: {write_time:.6f} segundos')

    # Guardar tiempos en archivo de resultados
    with open('timing_resultsBPlus.txt', 'w') as f:
        f.write(f'Tiempo total de todas las inserciones: {total_insert_time:.6f} segundos\n')
        f.write(f'Tiempo de escritura del archivo: {write_time:.6f} segundos\n')

    with open('timing_resultsBPlus.txt', 'r') as f:
        timing_results_content = f.read()
        print(timing_results_content)

if __name__ == "__main__":
    t = int(input("Ingrese el grado del árbol B+ (d): "))
    filename = input("Ingrese el nombre del archivo de comandos: ")
    process_file(filename, t)