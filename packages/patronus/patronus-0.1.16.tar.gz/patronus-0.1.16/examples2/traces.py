from dataclasses import dataclass
from typing import List, Optional
from openai import OpenAI

from patronus import trace
import faker


f = faker.Faker()


@dataclass
class ConversationMessage:
    role: str
    content: str


class OpenAIAdapter:
    """Adapter class for OpenAI API interactions"""

    def __init__(self):
        self.client = OpenAI()

    @trace.traced
    def generate_response(
        self,
        messages: List[ConversationMessage],
        model: str = "gpt-4-1106-preview",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate a response using OpenAI's API

        Args:
            messages: List of conversation messages
            model: The model to use
            temperature: Controls randomness (0-1)
            max_tokens: Maximum tokens in response

        Returns:
            Generated response text
        """
        formatted_messages = [{"role": msg.role, "content": msg.content} for msg in messages]

        # response = self.client.chat.completions.create(
        #     model=model,
        #     messages=formatted_messages,
        #     temperature=temperature,
        #     max_tokens=max_tokens
        # )
        #
        # return response.choices[0].message.content
        return f.text(100)


class AIAgentService:
    """Service class implementing AI agent functionality"""

    def __init__(self, adapter: OpenAIAdapter):
        self.adapter = adapter
        self.conversation_history: List[ConversationMessage] = []

    @trace.traced
    def add_system_prompt(self, prompt: str) -> None:
        """Add a system prompt to guide the agent's behavior"""
        self.conversation_history.append(ConversationMessage(role="system", content=prompt))

    @trace.traced
    def add_user_message(self, message: str) -> None:
        """Add a user message to the conversation"""
        self.conversation_history.append(ConversationMessage(role="user", content=message))

    @trace.traced
    def generate_response(self) -> str:
        """Generate a response based on conversation history"""
        response = self.adapter.generate_response(self.conversation_history)
        self.conversation_history.append(ConversationMessage(role="assistant", content=response))
        return response

    @trace.traced
    def clear_history(self) -> None:
        """Clear the conversation history"""
        self.conversation_history.clear()


@trace.traced
def raiser():
    raise ValueError("THis is an error !!")


@trace.traced
def main():
    print("Starting...")

    adapter = OpenAIAdapter()
    agent = AIAgentService(adapter)

    # Set up the agent's personality and behavior
    system_prompt = """You are a helpful AI assistant with expertise in programming. 
    You should provide clear, concise answers and always include code examples 
    when appropriate. Do not hallucinate."""
    agent.add_system_prompt(system_prompt)

    # raiser()

    # Example conversation
    try:
        # First interaction
        agent.add_user_message("How can I read a CSV file in Python?")
        response = agent.generate_response()
        print("Assistant:", response)

        # Second interaction
        agent.add_user_message("Can you modify that to handle errors if the file doesn't exist?")
        response = agent.generate_response()
        print("Assistant:", response)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
