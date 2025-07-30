from __future__ import annotations
import ast
from collections.abc import Awaitable as ABCAwaitable
import inspect
import sys
from typing import (
    Any,
    Callable,
    Dict,
    Literal,
    Optional,
    Tuple,
    TypedDict,
    Type,
    Union,
    TypeVar,
    get_origin,
    get_args,
    Awaitable,
)
import textwrap

def _snake_case_to_capital_case(name: str) -> str:
    return "".join(word.capitalize() for word in name.split("_"))


def _sanitize_name(name: str) -> str:
    return "".join(c if c.isalnum() else "" for c in name)


def _get_module_type(func: Callable, name: str) -> Type:
    # Split the name by dots to handle nested attributes
    parts = name.split('.')
    if not parts:
        return Any

    # Get the base module
    module = sys.modules.get(func.__module__, None)
    if not module:
        return Any

    # Start with the base module
    current = module
    for part in parts:
        if not hasattr(current, part):
            return Any
        current = getattr(current, part)

    # Check the final result
    if isinstance(current, type) or getattr(current, '__module__', None) == "typing":
        return current
    elif isinstance(current, Callable):
        return guess_return_type(current)

    return Any


def guess_return_type(func: Callable, use_literals=True) -> Type:
    """
    Infer the return type of a Python function by analyzing its AST.
    For dictionary returns, creates a TypedDict representation.

    Args:
        func: The function to analyze

    Returns:
        The inferred return type
    """

    # If annotations exist, return the return type
    if hasattr(func, "__annotations__") and "return" in func.__annotations__:
        return func.__annotations__["return"]

    # Get function source code and create AST
    try:
        source = inspect.getsource(func)
        source = textwrap.dedent(source)
    except Exception:
        return Any

    module = ast.parse(source)

    # Extract the function definition node
    func_def = module.body[0]
    if not isinstance(func_def, (ast.FunctionDef, ast.AsyncFunctionDef)):
        raise ValueError("Input is not a function definition")

    # Create a symbol table for type analysis
    symbol_table = {}

    # Populate the symbol table with type hints from function annotations
    if func_def.returns:
        # If function has a return type annotation, use it directly
        return _resolve_annotation(func_def.returns, {}, func)

    # Gather type information from annotations and assignments
    _analyze_function_body(func_def, symbol_table, func, use_literals)

    # Find all return statements
    return_types = []
    for node in ast.walk(func_def):
        if isinstance(node, ast.Return) and node.value:
            return_type = _infer_expr_type(node.value, symbol_table, func, [], use_literals)
            return_types.append(return_type)
    # If we found return statements
    if return_types:
        if len(return_types) == 1:
            return return_types[0]
        else:
            # Multiple return types - use Union
            return Union[tuple(set(return_types))]

    # Default to Any if no return statements or couldn't infer
    return Any


def _analyze_function_body(
    func_def: ast.FunctionDef, symbol_table: dict[str, Type], func: Callable, use_literals: bool
) -> None:
    """Analyze function body to populate symbol table with type information"""
    # First gather parameter types and TypeVar bindings
    type_context = {}
    for arg in func_def.args.args:
        if arg.annotation:
            param_type = _resolve_annotation(arg.annotation, type_context, func)
            symbol_table[arg.arg] = param_type
            
            # If the parameter type is a TypeVar, track its binding
            if isinstance(param_type, TypeVar):
                type_context[param_type.__name__] = param_type

    # Analyze assignments to track variable types
    for node in ast.walk(func_def):
        if isinstance(node, ast.Assign):
            assigned_type = _infer_expr_type(node.value, symbol_table, func, [], use_literals)
            for target in node.targets:
                if isinstance(target, ast.Name):
                    symbol_table[target.id] = assigned_type
                elif isinstance(target, ast.Tuple):
                    # Handle tuple unpacking
                    if hasattr(assigned_type, "__origin__") and assigned_type.__origin__ is tuple:
                        # Get the element types from the tuple type
                        element_types = assigned_type.__args__
                        if isinstance(element_types, tuple):
                            # Match each target with its corresponding type
                            for i, elt in enumerate(target.elts):
                                if isinstance(elt, ast.Name):
                                    if i < len(element_types):
                                        symbol_table[elt.id] = element_types[i]
                                    else:
                                        symbol_table[elt.id] = Any
                        else:
                            # If we can't determine individual element types, use Any
                            for elt in target.elts:
                                if isinstance(elt, ast.Name):
                                    symbol_table[elt.id] = Any
                    else:
                        # If not a tuple type, use Any for all targets
                        for elt in target.elts:
                            if isinstance(elt, ast.Name):
                                symbol_table[elt.id] = Any
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            # Handle annotated assignments
            symbol_table[node.target.id] = _resolve_annotation(
                node.annotation, type_context, func
            )


def _resolve_annotation(
    annotation: ast.AST, type_context: dict[str, Any], func: Callable
) -> Type:
    """Resolve a type annotation AST node to a real type"""
    if isinstance(annotation, ast.Name):
        # Simple types like int, str, etc.
        type_name = annotation.id
        # Check Python's built-in types first
        if type_name in __builtins__:
            return __builtins__[type_name]

        # Check if it's a TypeVar
        if type_name in type_context:
            return type_context[type_name]

        # Otherwise check if it's imported
        return _get_module_type(func, type_name)

    elif isinstance(annotation, ast.Subscript):
        # Handle generic types like list[int], dict[str, int], etc.
        if isinstance(annotation.value, ast.Name):
            base_type = annotation.value.id
            if base_type == "List" or base_type == "list":
                elem_type = _resolve_annotation(annotation.slice, type_context, func)
                return list[elem_type]
            elif base_type == "Dict" or base_type == "dict":
                if isinstance(annotation.slice, ast.Tuple):
                    key_type = _resolve_annotation(
                        annotation.slice.elts[0], type_context, func
                    )
                    val_type = _resolve_annotation(
                        annotation.slice.elts[1], type_context, func
                    )
                    return dict[key_type, val_type]
                return Dict
            elif base_type == "Set" or base_type == "set":
                elem_type = _resolve_annotation(annotation.slice, type_context, func)
                return set[elem_type]
            elif base_type == "Tuple" or base_type == "tuple":
                if isinstance(annotation.slice, ast.Tuple):
                    elem_types = [
                        _resolve_annotation(e, type_context, func)
                        for e in annotation.slice.elts
                    ]
                    return tuple[tuple(elem_types)]
                return Tuple
            elif base_type == "Optional":
                elem_type = _resolve_annotation(annotation.slice, type_context, func)
                return Optional[elem_type]
            elif base_type == "Union":
                if isinstance(annotation.slice, ast.Tuple):
                    elem_types = [
                        _resolve_annotation(e, type_context, func)
                        for e in annotation.slice.elts
                    ]
                    return Union[tuple(elem_types)]
                return Union
            elif base_type == "Literal":
                if isinstance(annotation.slice, ast.Tuple):
                    values = []
                    for elt in annotation.slice.elts:
                        if isinstance(elt, ast.Constant):
                            values.append(elt.value)
                    return Literal[tuple(values)] # type: ignore
                elif isinstance(annotation.slice, ast.Constant):
                    return Literal[annotation.slice.value] # type: ignore
            elif base_type == "TypeVar":
                # Handle TypeVar definitions
                if isinstance(annotation.slice, ast.Constant):
                    return TypeVar(annotation.slice.value)
                return TypeVar

    # Fallback for unresolved or complex annotations
    return Any


def _get_function_definition(func_name: str, func: Callable) -> Optional[Callable]:
    """Get the definition of a function by name from the module"""
    module = sys.modules.get(func.__module__, None)
    if not module:
        return None
    return getattr(module, func_name, None)


def _infer_expr_type(
    node: ast.AST, symbol_table: dict[str, Type], func: Callable, nested_path: list[str], use_literals: bool
) -> Type:
    """Infer the type of an expression"""
    if isinstance(node, ast.Dict):
        # For dictionary literals, create a TypedDict
        return _create_typed_dict_from_dict(node, symbol_table, func, nested_path, use_literals)

    elif isinstance(node, ast.List):
        # Handle list literals
        if not node.elts:
            return list[Any]
        element_types = [
            _infer_expr_type(elt, symbol_table, func, nested_path, use_literals) for elt in node.elts
        ]
        if len(set(element_types)) == 1:
            return list[element_types[0]]
        return list[Union[tuple(set(element_types))]]

    elif isinstance(node, ast.Tuple):
        # Handle tuple literals
        if not node.elts:
            return tuple[()]
        element_types = [
            _infer_expr_type(elt, symbol_table, func, nested_path, use_literals) for elt in node.elts
        ]
        return tuple[tuple(element_types)]

    elif isinstance(node, ast.Set):
        # Handle set literals
        if not node.elts:
            return set[Any]
        element_types = [
            _infer_expr_type(elt, symbol_table, func, nested_path, use_literals) for elt in node.elts
        ]
        if len(set(element_types)) == 1:
            return set[element_types[0]]
        return set[Union[tuple(set(element_types))]]

    elif isinstance(node, ast.Constant):
        # Handle literals
        if use_literals:
            return Literal[node.value] # type: ignore
        else:
            return type(node.value)

    elif isinstance(node, ast.Name):
        # Look up variable types in the symbol table
        if node.id in symbol_table:
            return symbol_table[node.id]

        # Handle built-in types referenced by name
        if node.id in __builtins__ and isinstance(__builtins__[node.id], type):
            return __builtins__[node.id]

        return _get_module_type(func, node.id)

    elif isinstance(node, ast.Call):
        # Handle function calls
        if isinstance(node.func, ast.Attribute):
            # Handle class method calls
            if isinstance(node.func.value, ast.Name):
                class_name = node.func.value.id
                method_name = node.func.attr
                
                # Get the class type
                class_type = _get_module_type(func, class_name)
                if isinstance(class_type, type):
                    # Get the method
                    method = getattr(class_type, method_name, None)
                    if method and hasattr(method, "__annotations__"):
                        return_type = method.__annotations__.get("return")
                        if isinstance(return_type, TypeVar):
                            # For class methods, the TypeVar is bound to the class
                            return class_type
                        return return_type
            
            # Handle regular method calls
            return _get_module_type(func, f"{node.func.value.id}.{node.func.attr}")
        
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            
            # First check if we have the function in our symbol table
            if func_name in symbol_table:
                func_type = symbol_table[func_name]
                if hasattr(func_type, "__annotations__") and "return" in func_type.__annotations__:
                    return_type = func_type.__annotations__["return"]
                    # If return type is a TypeVar, try to resolve it from arguments
                    if isinstance(return_type, TypeVar):
                        # Look at the first argument to determine the type
                        if node.args and isinstance(node.args[0], ast.Name):
                            arg_name = node.args[0].id
                            if arg_name in symbol_table:
                                return symbol_table[arg_name]
                        return return_type
            
            # If not in symbol table, try to get the function definition
            func_def = _get_function_definition(func_name, func)
            if func_def and hasattr(func_def, "__annotations__"):
                if "return" in func_def.__annotations__:
                    return_type = func_def.__annotations__["return"]
                    if isinstance(return_type, TypeVar):
                        # Look at the first argument to determine the type
                        if node.args and isinstance(node.args[0], ast.Constant):
                            return type(node.args[0].value)
                        elif node.args and isinstance(node.args[0], ast.Name):
                            arg_name = node.args[0].id
                            if arg_name in symbol_table:
                                return symbol_table[arg_name]
                        return return_type
                    # Handle tuple return types
                    if hasattr(return_type, "__origin__") and return_type.__origin__ is tuple:
                        return return_type

        # Handle module function calls
        if isinstance(node.func, ast.Attribute):
            return _get_module_type(func, f"{node.func.value.id}.{node.func.attr}")

        if isinstance(node.func, ast.Name):
            func_name = node.func.id

            # Handle some common built-in functions
            if func_name == "int":
                return int
            elif func_name == "str":
                return str
            elif func_name == "float":
                return float
            elif func_name == "list":
                return list[Any]
            elif func_name == "dict":
                return dict[Any, Any]
            elif func_name == "set":
                return set[Any]
            elif func_name == "tuple":
                return Tuple

            return _get_module_type(func, func_name)
            
        # For other function calls, we default to Any
        return Any

    elif isinstance(node, ast.BinOp):
        # Handle binary operations
        left_type = _infer_expr_type(node.left, symbol_table, func, nested_path, use_literals)
        right_type = _infer_expr_type(node.right, symbol_table, func, nested_path, use_literals)

        # String concatenation
        if isinstance(node.op, ast.Add) and (left_type == str or right_type == str):
            return str

        # Numeric operations typically return numeric types
        if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            if left_type == float or right_type == float:
                return float
            return int

        return Any

    elif isinstance(node, ast.Compare):
        return bool

    elif isinstance(node, ast.IfExp):
        body_type = _infer_expr_type(node.body, symbol_table, func, nested_path, use_literals)
        orelse_type = _infer_expr_type(node.orelse, symbol_table, func, nested_path, use_literals)
        return body_type | orelse_type
    
    elif isinstance(node, ast.Attribute):
        # Handle attribute access (e.g., obj.attr)
        if isinstance(node.value, ast.Name) and node.value.id in symbol_table:
            # Get the type of the object
            obj_type = symbol_table[node.value.id]
            
            # If the object has type annotations, try to get the attribute type
            if hasattr(obj_type, "__annotations__") and node.attr in obj_type.__annotations__:
                return obj_type.__annotations__[node.attr]
            
            # If the object is a class with class variables
            if isinstance(obj_type, type):
                if hasattr(obj_type, node.attr):
                    attr_value = getattr(obj_type, node.attr)
                    # If it's a Literal type or other type annotation
                    if hasattr(attr_value, "__origin__") and attr_value.__origin__ is Literal:
                        return attr_value
                    # For regular attributes, infer their type
                    return type(attr_value)
            # If the object is an instance of a class
            elif hasattr(obj_type, "__class__"):
                class_type = obj_type.__class__
                if hasattr(class_type, "__annotations__") and node.attr in class_type.__annotations__:
                    return class_type.__annotations__[node.attr]
        
        # For other attribute access, default to Any
        return Any
    
    elif isinstance(node, ast.Subscript):
        # Handle indexing operations (e.g., list[0], dict["key"])
        value_type = _infer_expr_type(node.value, symbol_table, func, nested_path, use_literals)

        # If the value is a list, get its element type
        if hasattr(value_type, "__origin__") and value_type.__origin__ is list:
            return value_type.__args__[0]

        # If the value is a dict, get its value type
        if hasattr(value_type, "__origin__") and value_type.__origin__ is dict:
            return value_type.__args__[1]

        # For other types, return Any
        return Any
        
    elif isinstance(node, ast.Await):
        # Handle await expressions by inferring the type of the awaited value
        awaited_type = _infer_expr_type(node.value, symbol_table, func, nested_path, use_literals)
        origin = get_origin(awaited_type)
        if origin in (Awaitable, ABCAwaitable):
            return awaited_type.__args__[0]
        return awaited_type

    # Default for complex or unknown expressions
    return Any


def _create_typed_dict_from_dict(
    dict_node: ast.Dict,
    symbol_table: dict[str, Type],
    func: Callable,
    nested_path: list[str],
    use_literals: bool,
) -> Type:
    """Create a TypedDict from a dictionary literal"""
    # Check if all keys are string literals
    field_types = {}
    is_valid_typeddict = True

    for i, key in enumerate(dict_node.keys):
        if isinstance(key, ast.Constant) and isinstance(key.value, str):
            value_type = _infer_expr_type(
                dict_node.values[i], symbol_table, func, nested_path + [key.value], use_literals
            )
            field_types[key.value] = value_type
        else:
            is_valid_typeddict = False
            break

    if is_valid_typeddict and field_types:
        # Create a dynamic TypedDict class
        # Capitalize function name and remove underscores
        class_name = f"{_snake_case_to_capital_case(func.__name__)}Return"

        # Add nested path components
        for component in nested_path:
            class_name += _snake_case_to_capital_case(_sanitize_name(component))
        return TypedDict(class_name, field_types)

    # If not a valid TypedDict, return a regular Dict with inferred types
    if dict_node.keys:
        key_types = [
            _infer_expr_type(key, symbol_table, func, nested_path + [key], use_literals)
            for key in dict_node.keys
        ]
        value_types = [
            _infer_expr_type(value, symbol_table, func, nested_path, use_literals)
            for value in dict_node.values
        ]

        # Determine common types
        if len(set(key_types)) == 1 and len(set(value_types)) == 1:
            return dict[key_types[0], value_types[0]]
        elif len(set(key_types)) == 1:
            return dict[key_types[0], Union[tuple(set(value_types))]]
        elif len(set(value_types)) == 1:
            return dict[Union[tuple(set(key_types))], value_types[0]]
        else:
            return dict[Union[tuple(set(key_types))], Union[tuple(set(value_types))]]

    return dict[Any, Any]
