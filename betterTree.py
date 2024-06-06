import os
import argparse

DEFAULT_DEPTH = 3

parser = argparse.ArgumentParser(description="🌳🌳🌳🌳")
parser.add_argument('--depth', '-d', type=int,
                    default=1, help='depth of the tree')
parser.add_argument('--default', '-dd', type=int, default=3,
                    help='default depth of the tree')
parser.add_argument('--path', '-p', type=str,
                    default=os.getcwd(), help='path to the directory')
parser.add_argument('--fancy', '-f', action='store_true', help='fancy tree')

args = parser.parse_args()


class Leaf:
    """
    Base class representing a leaf node in a tree.
    """

    def __init__(self, name: str):
        self.name = name

    def display(self, depth: int = 0, is_last: bool = False, prefix: str = ""):
        """
        Displays the node with appropriate indentation.
        """
        connector = '└──' if is_last else '├──'
        print(f"{prefix}{connector}{self.name}")


class Tree(Leaf):
    """
    Class representing a tree node that can have children.
    """

    def __init__(self, name: str):
        super().__init__(name)
        self.children = []

    def add_child(self, child: 'Leaf'):
        """
        Adds a child node to the tree.
        """
        self.children.append(child)

    def display(self, depth: int = 0, is_last: bool = False, prefix: str = ""):
        """
        Displays the tree recursively with proper formatting.
        """
        if depth == 0:
            print(self.name)
        else:
            super().display(depth, is_last, prefix)

        if depth > 0:
            prefix += "    " if is_last else "│   "

        for index, child in enumerate(self.children):
            is_last_child = index == len(self.children) - 1
            child.display(depth + 1, is_last_child, prefix)



if __name__ == "__main__":
    root = Tree("Root")
    child1 = Tree("Child 1")
    child2 = Tree("Child 2")
    child23 = Tree("Child 2.3")
    leaf1 = Leaf("Leaf 1.1")
    leaf2 = Leaf("Leaf 1.2")
    leaf3 = Leaf("Leaf 2.1")
    leaf4 = Leaf("Leaf 2.2")
    leaf5 = Tree("Child 2.3")
    leaf6 = Leaf("Leaf 2.3.1")

    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(leaf1)
    child1.add_child(leaf2)
    child2.add_child(leaf3)
    child2.add_child(child23)
    leaf5.add_child(leaf6)
    child23.add_child(leaf5)
    child2.add_child(leaf4)
    root.display()
