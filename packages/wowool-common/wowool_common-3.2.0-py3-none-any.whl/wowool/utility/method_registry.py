import types
from typing import Callable, Dict


jump_table: Dict[str, Callable] = {}


def register(command: str = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        if command:
            jump_table[command] = func
        else:
            jump_table[func.__name__] = func
        return func

    return decorator


def get_bound_jump_table(self) -> Dict[str, Callable]:
    return {command: types.MethodType(func, self) for command, func in jump_table.items()}
