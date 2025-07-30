class SplangError(Exception):
    """Base class for Splang interpreter errors."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class SplangWarning(Warning):
    """Base class for warnings in the Splang interpreter."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class InvalidOpcodeWarning(Warning):
    """Warning for invalid opcodes in the Splang interpreter."""
    def __init__(self, opcode):
        super().__init__(f"Invalid opcode: {opcode}")
        self.opcode = opcode