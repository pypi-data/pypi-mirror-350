from typing import Sequence

from moxn.models import message as msg
from moxn_types import core
from moxn_types.content import MessageRole


class PromptTemplate(core.BasePrompt[msg.Message]):
    """Immutable representation of a stored prompt configuration."""

    messages: Sequence[msg.Message]

    def get_message_by_role(self, role: str | MessageRole) -> msg.Message | None:
        """Get the first message with the specified role."""
        _role = MessageRole(role) if isinstance(role, str) else role

        messages = [p for p in self.messages if p.role == role]
        if len(messages) == 1:
            return messages[0]
        elif len(messages) == 0:
            return None
        else:
            raise ValueError(
                f"get message is not deterministic, there are {len(messages)} {_role.value} messages in the prompt"
            )

    def get_messages_by_role(self, role: str | MessageRole) -> list[msg.Message]:
        """Get all messages with the specified role."""
        role = MessageRole(role) if isinstance(role, str) else role
        return [p for p in self.messages if p.role == role]

    def get_message_by_name(self, name: str) -> msg.Message:
        """Helper to get message by name"""
        matching = [p for p in self.messages if p.name == name]
        if not matching:
            raise ValueError(f"No message found with name: {name}")
        if len(matching) > 1:
            raise ValueError(f"Multiple messages found with name: {name}")
        return matching[0]

    def _get_selected_messages(
        self,
        message_names: list[str] | None = None,
        messages: list[msg.Message] | None = None,
    ) -> list[msg.Message]:
        """Internal method to get selected messages based on various criteria."""
        if message_names:
            return [self.get_message_by_name(name) for name in message_names]
        elif messages:
            return messages
        else:
            # Use message_order if available, otherwise fall back to default role ordering
            if self.message_order:
                message_map = {str(p.id): p for p in self.messages}
                return [
                    message_map[str(pid)].model_copy(deep=True)
                    for pid in self.message_order
                    if str(pid) in message_map
                ]
            else:
                # Fall back to default role ordering
                selected_messages = []
                for role in [
                    MessageRole.SYSTEM,
                    MessageRole.USER,
                    MessageRole.ASSISTANT,
                ]:
                    message = self.get_message_by_role(role)
                    if message:
                        selected_messages.append(message)
                return [message.model_copy(deep=True) for message in selected_messages]
