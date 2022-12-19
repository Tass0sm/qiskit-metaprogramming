import ast
import itertools
from ..utils import is_loop

class LoopNest():
    def __init__(self, tree):
        self.tree = tree
        self.expr_dict = {}

        i = 0
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node

            if is_loop(node):
                self.expr_dict[i] = node
                i += 1

    def get_polyhedron(self, id):
        """Gets the iteration space for the body of the loop
        identified by ID. The iteration space is the cartesian product
        of the space for each loop above it.

        """
        iter_exprs = []
        loop = self.expr_dict[id]
        iter_exprs.append(loop.iter)

        while hasattr(loop, "parent"):
            assert is_loop(loop.parent), "parent isn't a loop"
            loop = loop.parent
            iter_exprs.append(loop.iter)

        iters = map(lambda a: eval(ast.unparse(a)), iter_exprs)
        return itertools.product(*iters)

    def permute(self, id0, id1):
        """Swaps the parameters of the loops identified by ID0 and
        ID1."""

        loop0 = self.expr_dict[id0]
        loop1 = self.expr_dict[id1]
        loop0.target, loop1.target = loop1.target, loop0.target
        loop0.iter, loop1.iter = loop1.iter, loop0.iter
        self.expr_dict[id0], self.expr_dict[id1] = self.expr_dict[id1], self.expr_dict[id0]

    def __str__(self):
        return ast.unparse(self.tree)
