from typing import Callable, Optional, TypeVar, Generic


class ActionError(Exception):
    """Exception for invalid actions."""

    pass


T = TypeVar("T")


class ActionRegistry(Generic[T]):
    """Registry for actions."""

    context: T

    def __init__(self, context: Optional[T] = None):
        self.actions = {}
        self.context = context

    def set_context(self, context: T):
        """Set the context for the action."""
        self.context = context

    def register_action(self, action: str, handler: Callable):
        """Register an action."""
        self.actions[action] = handler

    def call(self, action: str, *args, **kwargs):
        """Call an action."""
        handler = self.actions.get(action)
        self.exists(action)
        return handler(*args, **kwargs)

    def exists(self, action: str):
        """Check if an action exists."""
        if action not in self.actions:
            raise ActionError(
                f"Action {action} not found, available actions: {list(self.actions.keys())}"
            )
        return True

    async def async_call(self, action: str, *args, **kwargs):
        """Call an action asynchronously."""
        handler = self.actions.get(action)
        self.exists(action)
        return await handler(*args, **kwargs)

    def action(self, name: str):
        def decorator(func):
            self.register_action(name, func)
            return func

        return decorator
