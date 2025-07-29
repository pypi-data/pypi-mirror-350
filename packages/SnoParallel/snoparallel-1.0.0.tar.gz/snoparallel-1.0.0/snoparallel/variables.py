"""
This module contains the variable class to access variables in parallelized work cycles.
"""

from multiprocessing.shared_memory import SharedMemory
from threading import Lock
from typing import Optional

from numpy import dtype, float32, float64, int32, int64, ndarray
from numpy.typing import NDArray

VariableType = float32 | float64 | int32 | int64
ArrayType = NDArray[VariableType]


def get_variable_size(value: VariableType) -> int:
    """
    Get the variable size in bytes.

    Args:
        value: Variable value.

    Returns:
        Variable size in bytes.
    """
    return 2 * dtype(dtype=type(value)).itemsize


class Variable:
    """
    Class to access variables in parallelized work cycles.
    """

    def __init__(self, name: str, value: VariableType, memory: str, lock: Lock) -> None:
        """
        Args:
            name: Variable name.
            value: Initial value to set for the variable.
            memory: Reference to the memory location where the variable value is stored.
            lock: SyncManager.Lock instance which is coupled to the variable.

        Raises:
            TypeError: Type of the value not supported.
        """
        self.name = name

        self._memory = memory
        self._lock = lock
        self._type = type(value)

        if not isinstance(value, VariableType):
            raise TypeError("Variable type not supported.")

        self.write(value=value)
        self.update()

    def read(self) -> VariableType:
        """
        Read the (old) variable value.

        Returns:
            Variable value.
        """
        with self._lock:
            memory = SharedMemory(name=self._memory, create=False)
            array: ArrayType = ndarray(shape=(2,), dtype=self._type, buffer=memory.buf)
            value = array[0]
            memory.close()

        return self._type(value)

    def write(self, value: VariableType) -> None:
        """
        Write the new variable value.

        Args:
            value: New variable value.

        Raises:
            TypeError: Type of the value does not correspond with the type of the variable.
        """
        if not isinstance(value, self._type):
            raise TypeError("Type of the value does not correspond with the type of the variable.")

        self._write(value=value)

    def update(self) -> None:
        """
        Update the old variable value with the new one.
        """
        self._write(value=None)

    def _write(self, value: Optional[VariableType]) -> None:
        """
        Write the new value or trigger an update if it is None.

        Args:
            value: Trigger an update if value is None, otherwise overwrite new value with the given value.
        """
        with self._lock:
            memory = SharedMemory(name=self._memory, create=False)
            array: ArrayType = ndarray(shape=(2,), dtype=self._type, buffer=memory.buf)

            if value is not None:
                array[1] = value
            else:
                array[0] = array[1]

            memory.close()
