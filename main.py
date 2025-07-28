from app.core.algorithms.red_black_tree import RedBlackIntervalTree, IntervalNode, NodeColor
from datetime import datetime

def main():
    print("Hello from reservation-system!")
    # Example usage of RedBlackIntervalTree
    tree = RedBlackIntervalTree()
    node1 = IntervalNode(start=datetime(2023, 1, 1), end=datetime(2023, 1, 5), data="Reserva Hotel A")
    node2 = IntervalNode(start=datetime(2023, 1, 3), end=datetime(2023, 1, 7), data="Reserva Hotel B")
    node3 = IntervalNode(start=datetime(2023, 1, 6), end=datetime(2023, 1, 10), data="Reserva Hotel C")
    node4 = IntervalNode(start=datetime(2023, 1, 8), end=datetime(2023, 1, 12), data="Reserva Hotel D")
    node5 = IntervalNode(start=datetime(2023, 1, 2), end=datetime(2023, 1, 4), data="Reserva Hotel E")
    
    tree.insert(node1)
    tree.insert(node2)
    tree.insert(node3)
    tree.insert(node4)
    tree.insert(node5)
    
    print("Inserted intervals into the Red-Black Tree.")
    
    print("\n" + "="*60)
    print("VISUALIZACIÓN 1: Estructura jerárquica (con NIL)")
    print("="*60)
    print(tree.display_tree())
    
    print("\n" + "="*60)
    print("VISUALIZACIÓN 2: ASCII Art (estilo árbol)")
    print("="*60)
    print(tree.display_tree_ascii())
    
    print("\n" + "="*60)
    print("VISUALIZACIÓN 3: Por niveles (breadth-first)")
    print("="*60)
    tree.print_tree_levels()
    
    print("\n" + "="*60)
    print("VISUALIZACIÓN 4: Recorrido inorden")
    print("="*60)
    print(tree)
    
    print("\n" + "="*60)
    print("PRUEBA DE CONFLICTOS")
    print("="*60)
    # Test conflict detection
    conflict = tree.find_conflict(datetime(2023, 1, 4), datetime(2023, 1, 8))
    if conflict:
        print(f"Conflicto encontrado: {conflict.data} ({conflict.start.date()} - {conflict.end.date()})")
    else:
        print("No hay conflictos")

if __name__ == "__main__":
    main()
