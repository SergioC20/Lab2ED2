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
        if len(root.keys) == (2 * self.t) - 1:
            temp = BPlusNode()
            self.root = temp
            temp.children.insert(0, root)
            self.split_child(temp, 0)
            self.insert_non_full(temp, k, name)
        else:
            self.insert_non_full(root, k, name)

    def insert_non_full(self, x, k, name):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append((None, None))
            while i >= 0 and k < x.keys[i][0]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = (k, name)
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t) - 1:
                self.split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self.insert_non_full(x.children[i], k, name)

    def split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = BPlusNode(y.leaf)
        x.children.insert(i + 1, z)
        
        if y.leaf:
            z.keys = y.keys[t - 1:]
            y.keys = y.keys[:t - 1]
            x.keys.insert(i, z.keys[0][0])
            z.next = y.next
            y.next = z
        else:
            z.keys = y.keys[t:]
            y.keys = y.keys[:t - 1]
            x.keys.insert(i, y.keys[-1])
            z.children = y.children[t:]
            y.children = y.children[:t]

    def search(self, k, x=None):
        if x is None:
            x = self.root
        while not x.leaf:
            i = 0
            while i < len(x.keys) and k >= x.keys[i]:
                i += 1
            x = x.children[i]
        for i, key_value in enumerate(x.keys):
            if key_value[0] == k:
                return x, i
        return None

def process_file(filename, t):
    tree = BPlusTree(t)
    total_insert_time = 0

    with open(filename, 'r') as file:
        lines = file.readlines()

    pattern_insert = re.compile(r'Insert:\{id:(\d+),nombre:(.+?)\}')

    log_entries = []

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

    log_filename = f"log-BPlusTree-{filename}-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
    with open(log_filename, 'w') as log_file:
        log_file.write('\n'.join(log_entries))

    with open('timing_resultsBPlus.txt', 'w') as f:
        f.write(f'Tiempo total de todas las inserciones: {total_insert_time:.6f} segundos\n')

    with open('timing_resultsBPlus.txt', 'r') as f:
        timing_results_content = f.read()
        print(timing_results_content)

if __name__ == "__main__":
    t = int(input("Ingrese el grado mínimo del árbol B+ (t): "))
    filename = input("Ingrese el nombre del archivo de comandos: ")
    process_file(filename, t)
