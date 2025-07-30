import os
from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

class build_py(_build_py):
    def run(self):
        grammar = os.path.join("src", "winding", "grammar.lark")
        parser = os.path.join("src", "winding", "parser.py")
        if os.path.exists(grammar):
            print(f"Generating {parser} from {grammar}")
            os.system(f"python -m lark.tools.standalone {grammar} > {parser}")
        super().run()

setup(
    cmdclass={"build_py": build_py},
)