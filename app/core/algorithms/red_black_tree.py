import enum
import enum
from datetime import datetime, timedelta
from typing import Any, Optional

# Enum for the colors used in a Red-Black Tree
class NodeColor(enum.Enum):
    RED = 1
    BLACK = 2

# Class representing a node in a Red-Black Tree
class IntervalNode:
    """
    Represents a node in a Red-Black Tree that stores an interval.
    Each node contains a start time, end time, maximum end time, color, and pointers to its left and right children, parent, and associated data.
    """
    def __init__(self, start: datetime, end: datetime, data: Any):
        """
        Initializes an IntervalNode with a start time, end time, and associated data.
        Args:
            start (datetime): The start time of the interval.
            end (datetime): The end time of the interval.
            data (Any): Associated data with the interval.
        Raises:
            ValueError: If start time is not less than end time.
            TypeError: If start or end is not a datetime object.
        """
        if start >= end:
            raise ValueError("Start time must be less than end time.")
        if not isinstance(start, datetime) or not isinstance(end, datetime):
            raise TypeError("Start and end must be datetime objects.")
        self.start = start
        self.end = end
        self.max_end = end
        self.color = NodeColor.RED
        self.left: Optional['IntervalNode'] = None
        self.right: Optional['IntervalNode'] = None
        self.parent: Optional['IntervalNode'] = None
        self.data = data
    
    def grandparent(self):
        """
        Returns the grandparent of the node.
        The grandparent is the parent of the node's parent.
        """
        if self.parent is None:
            return None
        return self.parent.parent
    
    def sibling(self):
        """
        Returns the sibling of the node.
        The sibling is the other child of the node's parent.
        """
        if self.parent is None:
            return None
        if self.parent.left is self:
            return self.parent.right
        return self.parent.left
    
    def uncle(self):
        """
        Returns the uncle of the node.
        The uncle is the sibling of the node's parent.
        """
        if self.parent is None:
            return None
        return self.parent.sibling()

    def __repr__(self):
        """
        Returns a string representation of the IntervalNode.
        """
        return f"IntervalNode(start={self.start}, end={self.end}, max_end={self.max_end}, color={self.color.name})"
    
class RedBlackIntervalTree:
    """
    Represents a Red-Black Tree that stores intervals.
    This tree supports insertion, deletion, and searching for intervals.
    """
    def __init__(self):
        """
        Initializes an empty Red-Black Tree with a NIL leaf node.
        The NIL leaf node is used to simplify the tree structure and operations.
        """
        self.NIL_LEAF = IntervalNode(datetime.min, datetime.min + timedelta(days=1), None)
        self.NIL_LEAF.color = NodeColor.BLACK
        self.root = self.NIL_LEAF

    def insert(self, node: IntervalNode):
        """
        Inserts a new interval into the Red-Black Tree.
        Args:
            node (IntervalNode): The interval node to be inserted.
        """
        # Set initial values for the new node
        node.left = self.NIL_LEAF
        node.right = self.NIL_LEAF
        node.color = NodeColor.RED
        
        # Standard BST insertion
        parent = None
        current = self.root
        
        while current is not None and current != self.NIL_LEAF:
            parent = current
            if current is not None and node.start < current.start:
                current = current.left
            else:
                current = current.right
        
        node.parent = parent
        
        if parent is None:
            self.root = node
        elif node.start < parent.start:
            parent.left = node
        else:
            parent.right = node
        
        # Update max_end values up to the root
        self._update_max_end_up_to_root(node)
        
        # Fix Red-Black Tree properties
        self._insert_fixup(node)
    
    def delete(self, node: IntervalNode):
        """
        Deletes an interval from the Red-Black Tree.
        Args:
            node (IntervalNode): The interval node to be deleted.
        """
        self._delete_fixup(node)
    
    def find_conflict(self, start: datetime, end: datetime) -> Optional[IntervalNode]:
        """
        Finds an interval that conflicts with the given start and end times.
        Args:
            start (datetime): The start time of the interval to check.
            end (datetime): The end time of the interval to check.
        Returns:
            IntervalNode: The first conflicting interval found, or None if no conflict exists.
        """
        current = self.root
        while current is not None and current != self.NIL_LEAF:
            # Check if current interval overlaps with target interval
            if current.start < end and start < current.end:
                return current
            
            # If left subtree's max_end is >= start, there might be a conflict in left subtree
            if current.left is not None and current.left != self.NIL_LEAF and current.left.max_end >= start:
                current = current.left
            else:
                current = current.right
        return None
    
    def _left_rotate(self, node: IntervalNode):
        """
        Performs a left rotation on the given node.
        Args:
            node (IntervalNode): The node to rotate.
        """
        if node.right is None or node.right is self.NIL_LEAF:
            return
        right_child = node.right
        node.right = right_child.left
        if right_child.left is not None and right_child.left is not self.NIL_LEAF:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child
        # Update max_end values after rotation
        self._update_max_end(node)
        self._update_max_end(right_child)
    
    def _right_rotate(self, node: IntervalNode):
        """
        Performs a right rotation on the given node.
        Args:
            node (IntervalNode): The node to rotate.
        """
        if node.left is None or node.left is self.NIL_LEAF:
            return
        left_child = node.left
        node.left = left_child.right
        if left_child.right is not None and left_child.right is not self.NIL_LEAF:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child
        # Update max_end values after rotation
        self._update_max_end(node)
        self._update_max_end(left_child)

    def _update_max_end(self, node: IntervalNode):
        """
        Updates the max_end value of the given node based on its children.
        Args:
            node (IntervalNode): The node whose max_end value needs to be updated.
        """
        if node is None or node == self.NIL_LEAF:
            return
        node.max_end = max(
            node.end,
            node.left.max_end if node.left is not None and node.left != self.NIL_LEAF else datetime.min,
            node.right.max_end if node.right is not None and node.right != self.NIL_LEAF else datetime.min
        )

    def _update_max_end_up_to_root(self, node: IntervalNode):
        """
        Updates the max_end values from the given node up to the root.
        Args:
            node (IntervalNode): The node to start updating from.
        """
        current = node
        while current != self.NIL_LEAF and current is not None:
            self._update_max_end(current)
            current = current.parent

    def _insert_fixup(self, new_node: IntervalNode):
        """
        Fixes the Red-Black Tree properties after insertion.
        Args:
            node (IntervalNode): The newly inserted node.
        """
        while new_node.parent is not None and new_node.parent.color == NodeColor.RED:
            grandparent = new_node.grandparent()
            # Check if the grandparent exists and if the new node is a left child
            if grandparent is not None and new_node.parent == grandparent.left:
                uncle = new_node.uncle()
                if uncle is not None and uncle.color == NodeColor.RED:
                    # Case 1: Uncle is red
                    new_node.parent.color = NodeColor.BLACK
                    uncle.color = NodeColor.BLACK
                    if grandparent is not None:
                        if grandparent is not None:
                            if grandparent is not None:
                                grandparent.color = NodeColor.RED
                        new_node = grandparent
                    else:
                        break
                else:
                    # Case 2: Uncle is black or NIL
                    if new_node == new_node.parent.right:
                        # Left rotation needed
                        new_node = new_node.parent
                        self._left_rotate(new_node)
                    # Case 3: New node is left child
                    if new_node.parent is not None:
                        new_node.parent.color = NodeColor.BLACK
                    grandparent.color = NodeColor.RED
                    self._right_rotate(grandparent)
            # Check if the grandparent exists and if the new node is a right child
            else:
                uncle = new_node.uncle()
                if uncle is not None and uncle.color == NodeColor.RED:
                    # Case 1: Uncle is red
                    new_node.parent.color = NodeColor.BLACK
                    uncle.color = NodeColor.BLACK
                    if grandparent is not None:
                        grandparent.color = NodeColor.RED
                        new_node = grandparent
                    else:
                        break
                else:
                    # Case 2: Uncle is black or NIL
                    if new_node == new_node.parent.left:
                        # Right rotation needed
                        new_node = new_node.parent
                        self._right_rotate(new_node)
                    # Case 3: New node is right child
                    if new_node.parent is not None:
                        new_node.parent.color = NodeColor.BLACK
                    if grandparent is not None:
                        grandparent.color = NodeColor.RED
                        self._left_rotate(grandparent)
        self.root.color = NodeColor.BLACK

    def _delete_fixup(self, new_node: IntervalNode):
        """
        Fixes the Red-Black Tree properties after deletion.
        Args:
            node (IntervalNode): The node to be deleted.
        """
        while new_node.parent is not None and new_node.color == NodeColor.BLACK:
            grandparent = new_node.grandparent()
            # Check if the grandparent exists and if the new node is a left child
            if grandparent is not None and new_node == grandparent.left:
                sibling = new_node.sibling()
                if sibling is not None and sibling.color == NodeColor.RED:
                    # Case 1: Sibling is red
                    sibling.color = NodeColor.BLACK
                    grandparent.color = NodeColor.RED
                    self._left_rotate(grandparent)
                    sibling = new_node.sibling()
                if sibling is not None and \
                   (sibling.left is None or sibling.left.color == NodeColor.BLACK) and \
                   (sibling.right is None or sibling.right.color == NodeColor.BLACK):
                    # Case 2: Both children of sibling are black
                    sibling.color = NodeColor.RED
                    if grandparent is not None:
                        new_node = grandparent
                    else:
                        break
                else:
                    if sibling is not None and (sibling.right is None or sibling.right.color == NodeColor.BLACK):
                        # Case 3: Left child of sibling is red, right child is black
                        if sibling.left is not None:
                            sibling.left.color = NodeColor.BLACK
                        sibling.color = NodeColor.RED
                        self._right_rotate(sibling)
                        sibling = new_node.sibling()
                    # Case 4: Right child of sibling is red
                    if sibling is not None:
                        sibling.color = new_node.parent.color
                    new_node.parent.color = NodeColor.BLACK
                    if sibling is not None and sibling.right is not None:
                        sibling.right.color = NodeColor.BLACK
                    self._left_rotate(grandparent)
                    break
            # Check if the grandparent exists and if the new node is a right child
            else:
                sibling = new_node.sibling()
                if sibling is not None and sibling.color == NodeColor.RED:
                    # Case 1: Sibling is red
                    sibling.color = NodeColor.BLACK
                    if grandparent is not None:
                        grandparent.color = NodeColor.RED
                        self._right_rotate(grandparent)
                    else:
                        break
                    sibling = new_node.sibling()
                if sibling is not None and \
                   (sibling.left is None or sibling.left.color == NodeColor.BLACK) and \
                   (sibling.right is None or sibling.right.color == NodeColor.BLACK):
                    # Case 2: Both children of sibling are black
                    sibling.color = NodeColor.RED
                    if grandparent is not None:
                        new_node = grandparent
                    else:
                        break
                else:
                    if sibling is not None and (sibling.left is None or sibling.left.color == NodeColor.BLACK):
                        # Case 3: Right child of sibling is red, left child is black
                        if sibling.right is not None:
                            sibling.right.color = NodeColor.BLACK
                        sibling.color = NodeColor.RED
                        self._left_rotate(sibling)
                        sibling = new_node.sibling()
                    # Case 4: Left child of sibling is red
                    if sibling is not None:
                        sibling.color = new_node.parent.color
                    new_node.parent.color = NodeColor.BLACK
                    if sibling is not None and sibling.left is not None:
                        sibling.left.color = NodeColor.BLACK
                    if grandparent is not None:
                        self._right_rotate(grandparent)
                    break
        new_node.color = NodeColor.BLACK
    
    def __repr_inorder_traversal(self, node: Optional[IntervalNode], result: list):
        """
        Helper method for inorder traversal of the Red-Black Tree.
        Args:
            node (Optional[IntervalNode]): The current node in the traversal.
            result (list): The list to store the traversal result.
        """
        if node is None or node == self.NIL_LEAF:
            return
        self.__repr_inorder_traversal(node.left, result)
        result.append(repr(node))
        self.__repr_inorder_traversal(node.right, result)

    def display_tree(self, node: Optional[IntervalNode] = None, level: int = 0, prefix: str = "Root: ") -> str:
        """
        Displays the Red-Black Tree in a hierarchical format.
        Args:
            node (Optional[IntervalNode]): The current node to display (defaults to root).
            level (int): The current level in the tree (for indentation).
            prefix (str): The prefix to show before the node.
        Returns:
            str: A string representation of the tree structure.
        """
        if node is None:
            node = self.root
        
        if node == self.NIL_LEAF or node is None:
            return ""
        
        result = ""
        # Add current node
        color_symbol = "🔴" if node.color == NodeColor.RED else "⚫"
        result += "  " * level + prefix + f"{color_symbol} [{node.start.strftime('%Y-%m-%d')} - {node.end.strftime('%Y-%m-%d')}] (max_end: {node.max_end.strftime('%Y-%m-%d')}) - {node.data}\n"
        
        # Add children
        if node.left != self.NIL_LEAF or node.right != self.NIL_LEAF:
            if node.left != self.NIL_LEAF:
                result += self.display_tree(node.left, level + 1, "L--- ")
            else:
                result += "  " * (level + 1) + "L--- NIL\n"
            
            if node.right != self.NIL_LEAF:
                result += self.display_tree(node.right, level + 1, "R--- ")
            else:
                result += "  " * (level + 1) + "R--- NIL\n"
        
        return result

    def display_tree_ascii(self, node: Optional[IntervalNode] = None, depth: int = 0, prefix: str = "", is_left: bool = True) -> str:
        """
        Displays the tree in ASCII art format.
        """
        if node is None:
            node = self.root
            
        if node == self.NIL_LEAF:
            return ""
        
        result = ""
        
        # Display right subtree first
        if node.right != self.NIL_LEAF:
            new_prefix = prefix + ("│   " if is_left else "    ")
            result += self.display_tree_ascii(node.right, depth + 1, new_prefix, False)
        
        # Display current node
        color_symbol = "🔴" if node.color == NodeColor.RED else "⚫"
        connector = "└── " if is_left else "┌── "
        if depth == 0:
            connector = ""
        result += prefix + connector + f"{color_symbol} [{node.start.strftime('%m-%d')} - {node.end.strftime('%m-%d')}] ({node.data})\n"
        
        # Display left subtree
        if node.left != self.NIL_LEAF:
            new_prefix = prefix + ("    " if is_left else "│   ")
            result += self.display_tree_ascii(node.left, depth + 1, new_prefix, True)
        
        return result

    def print_tree_levels(self):
        """
        Prints the tree level by level (breadth-first traversal).
        """
        if self.root == self.NIL_LEAF:
            print("Empty tree")
            return
        
        from collections import deque
        queue = deque([(self.root, 0)])
        current_level = 0
        level_nodes = []
        
        while queue:
            node, level = queue.popleft()
            
            if level != current_level:
                # Print previous level
                print(f"Level {current_level}: {' | '.join(level_nodes)}")
                level_nodes = []
                current_level = level
            
            color_symbol = "🔴" if node.color == NodeColor.RED else "⚫"
            level_nodes.append(f"{color_symbol}[{node.start.strftime('%m-%d')} - {node.end.strftime('%m-%d')}]")
            
            if node.left is not None and node.left != self.NIL_LEAF:
                queue.append((node.left, level + 1))
            if node.right is not None and node.right != self.NIL_LEAF:
                queue.append((node.right, level + 1))
        
        # Print last level
        if level_nodes:
            print(f"Level {current_level}: {' | '.join(level_nodes)}")

    def __repr__(self) -> str:
        result = []
        self.__repr_inorder_traversal(self.root, result)
        return " ".join(result)
