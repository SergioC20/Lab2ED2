import time
import datetime

class BPlusNode:
    def __init__(self, leaf=False):
        self.keys = []
        self.children = []
        self.leaf = leaf
        self.next = None  # Para enlazar nodos hoja

class BPlusTree:
    def __init__(self):
        self.root = BPlusNode(True)

    def load_from_file(self, filename):
        start_time = time.time()
        start_dt = datetime.datetime.now()

        with open(filename, 'r') as f:
            lines = f.readlines()

        level_nodes = {}
        previous_level = -1
        previous_node = None

        for line in lines:
            level = line.count('  ')  # Calcula el nivel basado en la indentación
            node_data = line.strip().replace('Node(keys=[', '').replace('])', '')
            if not node_data:
                continue

            print(f"Processing line: {line.strip()}")  # Debugging line
            if '(' in node_data:  # Nodo hoja con tuplas
                keys = eval(f"[{node_data}]")  # Convierte a lista de tuplas (key, name)
            else:  # Nodo interno con claves
                keys = [int(k) for k in node_data.split(', ') if k]  # Convierte a lista de claves

            node = BPlusNode(leaf='(' in node_data)
            if node.leaf:
                node.keys = [(k, name) for k, name in keys]  # Tuplas para nodos hoja
            else:
                node.keys = keys  # Solo claves para nodos internos

            if level > 0:
                parent = level_nodes[level - 1][-1]  # Último nodo del nivel superior
                parent.children.append(node)

            if level not in level_nodes:
                level_nodes[level] = []
            level_nodes[level].append(node)

            # Enlazar nodos hojas
            if node.leaf and previous_level == level:
                previous_node.next = node

            previous_level = level
            previous_node = node

        self.root = level_nodes[0][0]  # El primer nodo del nivel 0 es la raíz

        end_time = time.time()
        end_dt = datetime.datetime.now()
        elapsed_time = end_time - start_time

        print(f'Cargar archivo: Inicio: {start_dt}, Fin: {end_dt}, Tiempo: {elapsed_time:.6f} segundos')

    def search(self, k):
        node = self.root
        while not node.leaf:
            i = 0
            while i < len(node.keys) and k >= node.keys[i]:
                i += 1
            node = node.children[i]
        for key, name in node.keys:
            if key == k:
                return name
        return None


def main():
    filename = input("Ingrese el nombre del archivo de índice: ")

    # Cargar el árbol B+ desde el archivo
    tree = BPlusTree()
    tree.load_from_file(filename)

    while True:
        id_to_search = input("Ingrese el ID a buscar (o 'exit' para salir): ")
        if id_to_search.lower() == 'exit':
            break
        try:
            id_to_search = int(id_to_search)
            start_time = time.time()
            start_dt = datetime.datetime.now()
            result = tree.search(id_to_search)
            end_time = time.time()
            end_dt = datetime.datetime.now()
            elapsed_time = end_time - start_time
            if result:
                print(f"ID: {id_to_search}, Nombre: {result}")
            else:
                print(f"ID {id_to_search} no encontrado en el árbol.")
        except ValueError:
            print("Por favor, ingrese un número entero válido.")

if __name__ == "__main__":
    main()
