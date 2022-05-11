# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Structure __init__ method generator."""

import atexit
import inspect

from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from .dump import Dump, Record


class CodeInjector:

    """Code evaluator/injector."""

    def __init__(self, namespace: Dict[str, Any]) -> None:
        self.f_globals = inspect.stack()[2].frame.f_globals
        self.namespace = namespace
        self.annotations = namespace.get("__annotations__", {})

    def evaluate(self, expression: str):
        """Evaluate expression within namespaces of class."""
        # pylint: disable=eval-used
        try:
            result = eval(expression, self.f_globals)
        except (SyntaxError, ValueError, TypeError):
            # typeerror: e.g. Optional[int]
            result = object()

        return result

    def get_expression(self, value: Any, alternative: str) -> str:
        """Get expression which will evaluate to be the identity of a value.

        :param value: Python object to generate expression for
        :param alternative: express to use if it does not evaluate properly

        """
        if isinstance(value, int) and not isinstance(value, Enum):
            expression = str(int(value))
            is_same = True

        else:
            if isinstance(value, type):
                expression = value.__name__
            elif isinstance(value, Enum):
                expression = str(value)
            else:
                expression = repr(value)

            try:
                is_same = self.evaluate(expression) is value
            except (NameError, SyntaxError):
                is_same = False

        return expression if is_same else alternative

    def execute_lines(self, lines: List[str]) -> None:
        """Execute lines within the same namespaces of a class."""
        f_globals = self.f_globals

        extra_globals = {
            "Any": Any,
            "Dump": Dump,
            "List": List,
            "Optional": Optional,
            "Record": Record,
            "Tuple": Tuple,
            "Union": Union,
        }

        for key in list(extra_globals):
            if key in f_globals:
                del extra_globals[key]
        f_globals.update(extra_globals)

        try:
            # pylint: disable=exec-used
            exec("\n".join(lines), f_globals, self.namespace)
        except Exception:  # pragma: no cover
            for i, line in enumerate(lines):
                print(f"{i + 1:04d}: {line}")
            raise

        for key in extra_globals:
            del f_globals[key]

    def get_type_hint_expression(self, name: str) -> str:  # pragma: no cover
        """Get expression which will evaluate to the type annotation for a member.

        :param name: member name

        """
        try:
            python_type = self.annotations[name]
        except KeyError:
            return ""

        if isinstance(python_type, str):
            return python_type

        # sys.version_info >= (3, 10) never gets beyond this point (hence no cover)

        try:
            type_hint = python_type.__name__
        except AttributeError:

            def fixup(text: str, separators=("[", "]")):
                if separators:
                    sep = separators[0]
                    text = sep.join(fixup(x, separators[1:]) for x in text.split(sep))
                return text

            type_hint = fixup(
                str(python_type)
            )  # e.g. "typing.Any", "List[xyz.Segment]"

        try:
            # pylint: disable=eval-used
            is_same = eval(type_hint, self.f_globals, self.namespace) is python_type
        except (NameError, SyntaxError):  # pragma: no cover
            return ""
        except Exception as exc:
            raise RuntimeError(f"invalid type hint: {type_hint!r}") from exc

        return type_hint if is_same else ""

    updates: Dict[str, List[Tuple[int, List[str], List[str]]]] = {}

    @staticmethod
    def get_lines(
        indent: str, lines: List[str], selections: List[str]
    ):  # pragma: no cover
        """Get selected methods implementation lines."""
        indented_lines = []
        if selections:
            decorator: Optional[str] = None

            keep_lines = False

            for line in lines:
                line = line.rstrip()
                if keep_lines and (not line or line.startswith(" ")):
                    indented_lines.append(indent + line)
                    continue

                keep_lines = False

                if line.startswith("@"):
                    decorator = line
                    continue

                if line.startswith(" ") or not line:
                    continue

                if line.startswith("def "):

                    function_name = line[4:].replace("(", " ").split()[0].strip("_")

                    if function_name in selections:
                        keep_lines = True
                        if decorator:
                            indented_lines.append(indent + decorator)

                        indented_lines.append(indent + line)

                    decorator = None
                    continue

                if line.startswith("__"):  # e.g. __eq__ = list.__eq__
                    function_name = line.split()[0].strip("_")
                    if function_name in selections:
                        keep_lines = True
                        indented_lines.append(indent + line)

        else:
            indented_lines += [indent + line for line in lines]

        return [line.rstrip() for line in indented_lines]

    @classmethod
    def update_scripts(cls):
        """Insert method implementation code into scripts where designated.

        Insert code into class definitions where "Structure.implementation" found.
        """
        for path, update in cls.updates.items():  # pragma: no cover
            with open(path) as script:
                script_lines = script.read().split("\n")

            for lineno, lines, selections in reversed(update):
                line = script_lines[lineno - 1]
                indent = line[: len(line) - len(line.lstrip())]
                script_lines[lineno - 1 : lineno] = cls.get_lines(
                    indent, lines, selections
                )

            with open(path, "w") as script:
                script.write("\n".join(script_lines))

    def update_script(self, lines):
        """Insert method implementation code into script at designated spot.

        Insert code into class definition where "Structure.implementation" found.

        """
        try:
            # e.g. "Structure.implementation" in the class body puts this in namespace
            path, lineno, selections = self.namespace["__implementation__"]

        except KeyError:
            pass

        else:  # pragma: no cover
            if not self.updates:
                atexit.register(self.update_scripts)

            self.updates.setdefault(path, []).append((lineno, lines, selections))
