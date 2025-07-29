from typing import TYPE_CHECKING, Any, Literal, cast, overload

from moxn_types.blocks.context import MessageContextModel
from moxn_types.blocks.variable import VariableType

# Import types conditionally to avoid circular imports
if TYPE_CHECKING:
    from moxn.base_models.blocks.document import PDFContentFromSource
    from moxn.base_models.blocks.image import ImageContentFromSource
else:
    PDFContentFromSource = None
    ImageContentFromSource = None


class MessageContext(MessageContextModel):
    """Context object that gets passed down from prompt instance to messages to blocks."""

    @overload
    def get_variable(
        self,
        name: str,
        variable_type: Literal[VariableType.PRIMITIVE],
        default: str | int | float | bool | None = None,
    ) -> str | None:
        """Get a primitive variable value by name."""
        pass

    @overload
    def get_variable(
        self, name: str, variable_type: Literal[VariableType.IMAGE], default: Any = None
    ) -> "ImageContentFromSource | None":
        """Get an image variable value by name."""
        pass

    @overload
    def get_variable(
        self,
        name: str,
        variable_type: Literal[VariableType.DOCUMENT],
        default: Any = None,
    ) -> "PDFContentFromSource | None":
        """Get a document variable value by name."""
        pass

    def get_variable(
        self, name: str, variable_type: VariableType, default: Any = None
    ) -> "str | ImageContentFromSource | PDFContentFromSource | None":
        """Get a variable value by name."""
        variable = self.variables.get(name, default)
        if variable is None:
            return None
        if variable_type == VariableType.PRIMITIVE:
            return str(variable)
        elif variable_type == VariableType.IMAGE:
            return cast(ImageContentFromSource, variable)
        elif variable_type == VariableType.DOCUMENT:
            return cast(PDFContentFromSource, variable)
        else:
            raise ValueError(f"Unsupported variable type: {variable_type}")

    def get_provider_setting(self, setting_name: str, default: Any = None) -> Any:
        """Get a setting for the active provider."""
        if not self.provider or self.provider not in self.provider_settings:
            return default
        return self.provider_settings[self.provider].get(setting_name, default)

    def has_variable(self, name: str) -> bool:
        """Check if a variable exists."""
        return name in self.variables

    @classmethod
    def create_empty(cls) -> "MessageContext":
        """Create an empty context."""
        return cls()

    @classmethod
    def from_variables(cls, variables: dict[str, Any]) -> "MessageContext":
        """Create a context initialized with variables."""
        return cls(variables=variables)
