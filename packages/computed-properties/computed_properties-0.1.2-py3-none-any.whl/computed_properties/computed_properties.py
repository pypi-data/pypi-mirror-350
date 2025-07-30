import ast
import inspect
import textwrap
from collections import defaultdict
from typing import Any


class RecordReferencesTransformer(ast.NodeTransformer):
    """
    AST transformer that records attribute references to build a dependency graph
    of computed properties based on their usage of instance variables.
    """

    def __init__(self, function, child_dependencies):
        super().__init__()
        self.function = function
        self._child_dependencies = child_dependencies

    def visit_FunctionDef(self, node):
        """Visit a function definition and record its dependencies on self attributes."""

        def is_attr_on_self(n):
            return isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == "self"

        attrs = [n.attr for n in ast.walk(node) if is_attr_on_self(n)]
        for attr_ in attrs:
            self._child_dependencies[attr_].add(self.function.__name__)


class ComputedPropertyCache:
    """
    Caches computed properties and tracks dependencies between them.

    Automatically invalidates dependent computed properties when base attributes change.
    """

    def __init__(self):
        self._child_dependencies: dict[str, set[str]] = defaultdict(set)

    def __call__(self, *args):
        """Creates a new class with overridden __setattr__ to manage cache invalidation."""
        this = self

        class _ComputedSetAttr:
            """
            Overrides __setattr__ to detect changes to base attributes and
            mark dependent computed properties as dirty.
            """

            def __init__(self) -> None:
                self.__dict__["_computed_parent_based_dependencies"] = this._child_dependencies
                self.__dict__["_computed_changes"] = defaultdict(self._init_dependency)
                self.__dict__["_computed_cache"] = {}

            def _init_dependency(self) -> bool:
                """Initializes change tracking for a computed property."""
                return False

            def __setattr__(self, name: str, value: Any) -> None:
                super().__setattr__(name, value)
                parent_based_dependencies = self.__dict__["_computed_parent_based_dependencies"]
                if name in parent_based_dependencies:
                    # Mark all dependent computed properties as dirty
                    changes = self.__dict__["_computed_changes"]
                    for child_name in parent_based_dependencies[name]:
                        changes[child_name] = True

        cls_name, bases, namespace = args[0], (_ComputedSetAttr,), args[2]
        return type(cls_name, bases, namespace)

    def link_indirect_dependencies(self) -> None:
        """
        Resolves indirect dependencies by propagating them transitively
        through the dependency graph.
        """
        dependencies_to_add = defaultdict(set)
        for parent, children in self._child_dependencies.items():
            for child in children:
                if child in self._child_dependencies:
                    dependencies_to_add[parent].update(self._child_dependencies[child])

        for key, value in dependencies_to_add.items():
            self._child_dependencies[key].update(value)

    def computed_property(self, function):
        """
        Decorator that wraps a method as a computed property with caching and
        automatic invalidation based on attribute usage.
        """
        ast_function = ast.parse(textwrap.dedent(inspect.getsource(function)))
        RecordReferencesTransformer(function, self._child_dependencies).visit(ast_function)
        self.link_indirect_dependencies()

        def inner_computed(self, *args: list[Any], **kwargs: dict[str, Any]) -> Any:
            name = function.__name__
            if self.__dict__["_computed_changes"][name]:
                # Recompute and update the cache if marked as dirty
                self.__dict__["_computed_cache"][name] = function(self, *args, **kwargs)
                self.__dict__["_computed_changes"][name] = False

            return self.__dict__["_computed_cache"][name]

        return property(inner_computed)
