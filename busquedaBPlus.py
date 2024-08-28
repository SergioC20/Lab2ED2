import time

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
        start_time = time.time()  # Marca de tiempo inicial

        with open(filename, 'r') as f: #abre el archivo del indice
            lines = f.readlines()

        level_nodes = {}
        previous_level = -1
        previous_node = None

        for line in lines:
            level = line.count('  ')  # Calcula el nivel basado en la indentación
            node_data = line.strip().replace('Node(keys=[', '').replace('])', '')
            if not node_data:
                continue

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

        end_time = time.time()  # Marca de tiempo final
        elapsed_time = end_time - start_time  # Calcular el tiempo transcurrido
        print(f'El tiempo total de carga y almacenamiento en memoria es: {elapsed_time:.6f} segundos')

    def search(self, k):
        def find_leaf_node(node, k): #funcion auxiliar recursiva para encontrar el nodo hoja que podria contener la clave k
            if node.leaf: # si el nodo es hoja devolverlo
                return node
            
            i = 0
            while i < len(node.keys) and k > node.keys[i]: # recorrer las claves del nodo hasta encontrar la posicion correcta de la clave k
                i += 1
            return find_leaf_node(node.children[i], k) # llamada recursiva a find_leaf_node con el hijo correspondiente

        leaf = find_leaf_node(self.root, k)  # iniciar la búsqueda desde la raiz y encontrar la hoja donde podría estar la clave k

        
        while leaf: # buscar en todas las hojas a partir de la hoja encontrada
            for key, name in leaf.keys:  # recorrer todas las tuplas (clave, nombre) en la hoja
                if key == k: # si se encuentra la clave devuelve el nombre asociado
                    return name
            leaf = leaf.next # si no se encuentra en esta hoja moverse a la siguiente hoja enlazada

        return None # si no se encuentra la clave en el arbol devuelve None

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
            id_to_search = int(id_to_search) #recibe el valor del id a buscar
            result = tree.search(id_to_search) #burca el id en el arbol
            if result: #si encuentra el id 
                print(f"ID: {id_to_search}, Nombre: {result}")
            else: #si no encuentra el id
                print(f"ID {id_to_search} no encontrado en el árbol.")
        except ValueError: #si recibe un valor diferenre a un entero o a la palabra "exit"
            print("Por favor, ingrese un número entero válido.")

if __name__ == "__main__":
    main()
