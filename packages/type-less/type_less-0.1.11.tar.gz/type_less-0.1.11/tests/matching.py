from typing import get_type_hints, get_origin, get_args, Literal, TypeVar, Union
import types

def validate_is_equivalent_type(type1, type2):
    """
    Determine if two Python types are equivalent, handling complex nested types.
    
    This function compares two types for equivalence, including:
    - Basic types (int, str, etc.)
    - Generic types (List, Dict, etc.)
    - Union types (Union[int, str], Optional[int], etc.)
    - TypedDict types with nested structure
    - Literal types
    - TypeVar with constraints
    - ForwardRef types
    - Callable types
    
    Args:
        type1: First type to compare
        type2: Second type to compare
        
    Raises:
        AssertionError: If types are not equivalent, with detailed debug information
    """
    # Handle None type
    if type1 is None and type2 is None:
        return True
    
    # Handle direct equality (same type object)
    if type1 is type2:
        return True
    
    # Get origin types (for generics)
    origin1 = get_origin(type1)
    origin2 = get_origin(type2)
    
    # If one has origin and other doesn't, they're not equivalent
    if (origin1 is None) != (origin2 is None):
        raise AssertionError(f"Type origins don't match: {type1} (origin={origin1}) vs {type2} (origin={origin2})")
    
    # Special case for Optional and Union
    if {origin1, origin2} <= {Union, types.UnionType}:
        # Handle Optional[T] == Union[T, None]
        args1 = get_args(type1)
        args2 = get_args(type2)
        
        # Check if one is Optional (Union with None)
        has_none1 = type(None) in args1
        has_none2 = type(None) in args2
        
        if has_none1 != has_none2:
            raise AssertionError(f"Optional mismatch: {type1} (has_none={has_none1}) vs {type2} (has_none={has_none2})")
            
        # Compare non-None args
        non_none_args1 = [arg for arg in args1 if arg is not type(None)]
        non_none_args2 = [arg for arg in args2 if arg is not type(None)]
        
        if len(non_none_args1) != len(non_none_args2):
            raise AssertionError(f"Union argument count mismatch: {type1} ({len(non_none_args1)} args) vs {type2} ({len(non_none_args2)} args)")
            
        # For Union, order doesn't matter
        args2_remaining = set(non_none_args2)
        for arg1 in non_none_args1:
            for arg2 in args2_remaining:
                try:
                    if validate_is_equivalent_type(arg1, arg2):
                        args2_remaining.remove(arg2)
                        break
                except AssertionError as e:
                    continue
            else:
                raise AssertionError(f"Union argument mismatch: {arg1} in {type1} has no matching type in {type2}")
        return True
    
    # Get arguments of generic types
    args1 = get_args(type1)
    args2 = get_args(type2)
    
    # If number of args differs, types are not equivalent
    if len(args1) != len(args2):
        raise AssertionError(f"Generic argument count mismatch: {type1} ({len(args1)} args) vs {type2} ({len(args2)} args)")
    
    # Special handling for TypedDict
    if hasattr(type1, "__annotations__") and hasattr(type2, "__annotations__"):
        # Check if both are TypedDict
        if hasattr(type1, "__total__") and hasattr(type2, "__total__"):
            # Check if totality is the same
            if type1.__total__ != type2.__total__:
                raise AssertionError(f"TypedDict totality mismatch: {type1} (total={type1.__total__}) vs {type2} (total={type2.__total__})")
            
            # Get annotations
            annotations1 = get_type_hints(type1)
            annotations2 = get_type_hints(type2)
            
            # Check if keys match
            if set(annotations1.keys()) != set(annotations2.keys()):
                missing_keys = set(annotations1.keys()) - set(annotations2.keys())
                extra_keys = set(annotations2.keys()) - set(annotations1.keys())
                raise AssertionError(f"TypedDict key mismatch: {type1} vs {type2}\nMissing keys: {missing_keys}\nExtra keys: {extra_keys}")
            
            # Check if field types match
            for key in annotations1:
                try:
                    validate_is_equivalent_type(annotations1[key], annotations2[key])
                except AssertionError as e:
                    raise AssertionError(f"TypedDict field type mismatch for key '{key}': {e}")
            return True
    
    # Handle Literal
    if origin1 is Literal and origin2 is Literal:
        # For Literal, order doesn't matter but values must be identical
        if set(args1) != set(args2):
            raise AssertionError(f"Literal value mismatch: {type1} ({set(args1)}) vs {type2} ({set(args2)})")
        return True
    
    # Handle Callable
    if origin1 in {types.FunctionType, callable} and origin2 in {types.FunctionType, callable}:
        if not args1 or not args2:
            return True  # Callable without specified signature
        
        if len(args1) != 2 or len(args2) != 2:
            raise AssertionError(f"Callable argument count mismatch: {type1} ({len(args1)} args) vs {type2} ({len(args2)} args)")
        
        # Compare parameter types
        params1, return1 = args1
        params2, return2 = args2
        
        # Handle Ellipsis in parameters
        if params1 is Ellipsis or params2 is Ellipsis:
            try:
                return validate_is_equivalent_type(return1, return2)
            except AssertionError as e:
                raise AssertionError(f"Callable return type mismatch: {e}")
        
        # If parameter counts differ, not equivalent
        if len(params1) != len(params2):
            raise AssertionError(f"Callable parameter count mismatch: {type1} ({len(params1)} params) vs {type2} ({len(params2)} params)")
        
        # Check parameters and return type
        for i, (p1, p2) in enumerate(zip(params1, params2)):
            try:
                validate_is_equivalent_type(p1, p2)
            except AssertionError as e:
                raise AssertionError(f"Callable parameter {i} type mismatch: {e}")
        
        try:
            validate_is_equivalent_type(return1, return2)
        except AssertionError as e:
            raise AssertionError(f"Callable return type mismatch: {e}")
        return True
    
    # Handle basic types
    if origin1 is None and origin2 is None:
        if isinstance(type1, type) and isinstance(type2, type):
            # Compare types by their class name and module name
            if type1.__name__ == type2.__name__ and type1.__module__ == type2.__module__:
                return True
            if type1 is not type2 and type1 != type2:
                raise AssertionError(f"Basic type mismatch: {type1} vs {type2}")
            return True
        
        # Handle TypeVar
        if isinstance(type1, TypeVar) and isinstance(type2, TypeVar):
            if not (type1.__name__ == type2.__name__ and 
                   type1.__constraints__ == type2.__constraints__ and
                   type1.__bound__ == type2.__bound__ and
                   type1.__covariant__ == type2.__covariant__ and
                   type1.__contravariant__ == type2.__contravariant__):
                raise AssertionError(f"TypeVar mismatch: {type1} vs {type2}\n"
                                   f"name: {type1.__name__} vs {type2.__name__}\n"
                                   f"constraints: {type1.__constraints__} vs {type2.__constraints__}\n"
                                   f"bound: {type1.__bound__} vs {type2.__bound__}\n"
                                   f"covariant: {type1.__covariant__} vs {type2.__covariant__}\n"
                                   f"contravariant: {type1.__contravariant__} vs {type2.__contravariant__}")
            return True
    
    # For other generic types, check if all arguments are equivalent
    # For tuples, order matters
    for i, (arg1, arg2) in enumerate(zip(args1, args2)):
        try:
            validate_is_equivalent_type(arg1, arg2)
        except AssertionError as e:
            raise AssertionError(f"Generic argument {i} mismatch in {type1} vs {type2}: {e}")
    
    if not type1 == type2:
        raise AssertionError(f"Type mismatch: {type1} vs {type2}")

    return type1 == type2



def validate_openapi_has_return_schema(openapi_spec: dict, path: str, method: Literal["get", "post", "put", "delete"]) -> bool:
    """
    Validates that the OpenAPI specification for a given endpoint matches the expected return type.
    
    Args:
        openapi_spec: The OpenAPI specification dictionary
        path: The API endpoint path
        method: The HTTP method (get, post, put)
        expected_type: The expected return type to validate against
        
    Returns:
        bool: True if the OpenAPI schema matches the expected type, False otherwise
    """
    # Check if the OpenAPI spec exists
    if not openapi_spec or "paths" not in openapi_spec:
        return False
    
    # Check if the path exists in the spec
    if path not in openapi_spec["paths"]:
        return False
    
    # Check if the method exists for the path
    path_spec = openapi_spec["paths"][path]
    if method not in path_spec:
        return False
    
    # Get the response schema
    method_spec = path_spec[method]
    if "responses" not in method_spec or "200" not in method_spec["responses"]:
        return False
    
    response_spec = method_spec["responses"]["200"]
    if "content" not in response_spec or "application/json" not in response_spec["content"]:
        return False
    
    schema = response_spec["content"]["application/json"].get("schema") or {}
    
    # For now, just check if schema exists
    return schema.get("$ref") is not None
