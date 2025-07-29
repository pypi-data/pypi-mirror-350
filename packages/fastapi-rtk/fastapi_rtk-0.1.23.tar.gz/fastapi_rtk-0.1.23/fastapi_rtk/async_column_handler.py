import contextlib
import typing

from pydantic import BaseModel, model_validator

from .globals import g

__all__ = ["AsyncColumnHandler"]


class AsyncColumnHandler:
    """
    A handler class for managing asynchronous column validation and population in a schema.

    This class provides static methods to add asynchronous validators to a schema, populate
    asynchronous columns, and apply specified columns to a model asynchronously.

    Methods:
        add_async_validators(schema: dict[str, typing.Any], async_columns: list[str]) -> None:

        populate_async_columns() -> contextlib.AbstractAsyncContextManager:
            Asynchronous generator that populates asynchronous columns by processing a coroutine queue.

        _apply_columns(model: BaseModel, columns: list[str]) -> BaseModel:

    ## Example:
    ```python
    from fastapi_rtk import SQLAInterface
    from ..models import MyModel

    my_model_interface = SQLAInterface(MyModel)

    # Imagine we're in async function
    # and MyModel has a column called `number`

    # @property
    # async def number(self):
    #     return 5 # Or do something async here

    async with AsyncColumnHandler.populate_async_columns():
        # If MyModel has a column created with @property and an async def, it will be populated when it gets out of the context manager
        model_1 = my_model_interface.schema.model_validate(existing_model, from_attributes=True)

    my_number = model_1.number # number will be 5
    """

    @staticmethod
    def add_async_validators(schema: dict[str, typing.Any], async_columns: list[str]):
        """
        Add asynchronous validators to a schema.

        This function decorates a method to add it to a coroutine queue for asynchronous
        validation of specified columns. It updates the schema with the decorated method
        as a validator.

        Args:
            schema (dict[str, typing.Any]): The schema to which the validators will be added.
            async_columns (list[str]): A list of column names that require asynchronous validation.

        Returns:
            None
        """

        def add_to_g_coro_queue(self):
            if g.coro_queue is None:
                return

            g.coro_queue.append(AsyncColumnHandler._apply_columns(self, async_columns))
            return self

        decorated_func = model_validator(mode="after")(add_to_g_coro_queue)
        schema.update(
            {"__validators__": {add_to_g_coro_queue.__name__: decorated_func}}
        )

    @staticmethod
    @contextlib.asynccontextmanager
    async def populate_async_columns():
        """
        Asynchronous generator that populates asynchronous columns by processing a coroutine queue added by `add_async_validators`.

        This function initializes an empty coroutine queue, yields control back to the caller,
        and then processes each coroutine in the queue until it is empty. Finally, it ensures
        that the coroutine queue is cleaned up.

        Yields:
            None: Control is yielded back to the caller to allow for coroutine queue population.

        Raises:
            Any exceptions raised by the coroutines in the queue will propagate up.
        """
        try:
            g.coro_queue = []
            yield
            while g.coro_queue:
                await g.coro_queue.pop()
        finally:
            g.coro_queue = None

    @staticmethod
    async def _apply_columns(model: BaseModel, columns: list[str]):
        """
        Asynchronously applies the specified columns to the given model.

        This function iterates over the provided list of column names, retrieves
        the corresponding attribute from the model asynchronously, and sets the
        attribute on the model.

        Args:
            model (BaseModel): The model instance to which the columns will be applied.
            columns (list[str]): A list of column names to be applied to the model.

        Returns:
            BaseModel: The updated model with the specified columns applied.
        """
        for col in columns:
            setattr(model, col, await getattr(model, col))
        return model
