# services/agents_contracts.py
from semantic_kernel.agents.strategies import TerminationStrategy


class ApprovalTerminationStrategy(TerminationStrategy):
    """A strategy for determining when an agent should terminate."""

    async def should_agent_terminate(self, agent, history):
        """Check if the agent should terminate."""
        return "TERMINATE" in history[-1].content


class HistoryMessage:
    def __init__(self, role: str, message: str):
        self.role = role
        self.message = message


class ResponseMessage:
    def __init__(self):
        self.answer: str = ""
        self.historyMessages: list[HistoryMessage] = []
        self.groupChat: list[HistoryMessage] = []
        self.sources: list[str] = []
        self.suggestions: list[str] = []

    def add_assistant_message(self, message: str):
        self.historyMessages.append(HistoryMessage(role="assistant", message=message))

    def add_group_agent_message(self, assistant_name: str, message: str):
        self.groupChat.append(HistoryMessage(role=assistant_name, message=message))

    def add_user_message(self, message: str):
        self.historyMessages.append(HistoryMessage(role="user", message=message))

    def get_last_reviewed_message(self) -> HistoryMessage:
        reviewed_messages = [
            msg for msg in self.groupChat if msg.role == "ReviewerAgent"
        ]
        last_message = reviewed_messages[-1] if reviewed_messages else None
        last_message.message = (
            last_message.message.replace("TERMINATE", "") if last_message else None
        )
        return last_message
