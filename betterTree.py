import os
import argparse

DEFAULT_DEPTH = 1

parser = argparse.ArgumentParser(description="Tree command in Python.")
parser.add_argument('--depth'  , '-d' , type=int, default=DEFAULT_DEPTH, help='depth of the tree')
parser.add_argument('--default-depth', '-dd', type=int, default=DEFAULT_DEPTH, help='default depth of the tree')
parser.add_argument('--path'   , '-p' , type=str, default=os.getcwd(),   help='path to the directory')
parser.add_argument('--fancy'  , '-f' , action='store_true', help='fancy tree')
parser.add_argument('--all'    , '-a' , action='store_true', help='show all files')

args = parser.parse_args()


class Leaf:
    """
    Base class representing a leaf node in a tree.
    """

    def __init__(self, name: str):
        self.name = name

    def display(self, depth: int = DEFAULT_DEPTH, is_last: bool = False, prefix: str = ""):
        """
        Displays the node with appropriate indentation.
        """
        connector = '└──' if is_last else '├──'
        print(f"{prefix}{connector}{self.name}")

    def displayFancy(self):
        pass



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

    def display(self, depth: int = 0, is_last: bool = False, prefix: str = "") -> None:
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

    def displayFancy(self):
        dirs = [dir for dir in self.children if isinstance(dir, Tree)]
        files = [file for file in self.children if isinstance(file, Leaf) and not isinstance(file, Tree)]

        max_fn = 7
        for file in files:
            if len(file.name) > max_fn:
                file.name = file.name[:max_fn-2] + ".."

            file.name = file.name.center(max_fn)
            print(f"{file.name} ", end="")
        print()

        padding = max_fn // 2

        column_pattern = f"{' ' * padding}│{' ' * padding} "

        file_count = len(files)
        # vertical branch
        print(column_pattern * file_count)
        print(column_pattern * file_count)

        # connect them together
        if file_count == 1:
            connection_pattern = f"{' ' * padding}│{'─'*padding}"
        elif file_count == 2:
            connection_pattern = f"{' ' * padding}└{'─'*max_fn}{'┤'} "
        else:
            middle_pattern = ('┴'+'─'*max_fn)
            connection_pattern = f"{' ' * padding}└{'─'*max_fn}{middle_pattern*int(file_count/2-1)}┼{middle_pattern[::-1]*int((file_count-1)/2-1)}{'─'*max_fn}{'┘'} "
        print(connection_pattern)

        # TODO: finish the fancy tree, push files onto stack and pop them off to display them in the correct order

        for dir in dirs:
            print(f"{dir.name}/")
            dir.displayFancy()

    def displayPyramid(self):
        pass

    def createTree(self, path: str, depth: int, hidden=False):
        """
        Creates a tree structure of the given path with the given depth.
        """
        if depth == 0:
            return self

        with os.scandir(path) as entries:
            files = [entry for entry in entries if (not entry.name.startswith('.')) or hidden]

        for entry in files:
            if entry.is_dir():
                tree = Tree(entry.name)
                self.add_child(tree)
                tree.createTree(entry.path, depth - 1, hidden)
            else:
                leaf = Leaf(entry.name)
                self.add_child(leaf)

        return self


if __name__ == "__main__":
    root = Tree(args.path)
    root.createTree(args.path, args.depth, args.all)
    if args.fancy:
        root.displayFancy()
    else:
        root.display()
