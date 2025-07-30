from typing import Union, Any, Dict, Generator, Optional
import requests
import json

from webscout.AIutel import Optimizers, Conversation, AwesomePrompts
from webscout.AIbase import Provider
from webscout import exceptions
from webscout.litagent import LitAgent as Lit


class ChatGPTGratis(Provider):
    """
    A class to interact with the chatgptgratis.eu backend API with real-time streaming.
    """
    AVAILABLE_MODELS = [
        "Meta-Llama-3.2-1B-Instruct",
        "Meta-Llama-3.2-3B-Instruct",
        "Meta-Llama-3.1-8B-Instruct",
        "Meta-Llama-3.1-70B-Instruct",
        "Meta-Llama-3.1-405B-Instruct",
        "gpt4o"
    ]

    def __init__(
        self,
        model: str = "Meta-Llama-3.2-1B-Instruct",
        timeout: int = 30,
        proxies: Optional[Dict[str, str]] = None,
        intro: Optional[str] = None,
        filepath: Optional[str] = None,
        update_file: bool = True,
        history_offset: int = 10250,
        act: Optional[str] = None,
    ) -> None:
        """
        Initializes the ChatGPTGratis.
        """
        if model not in self.AVAILABLE_MODELS:
            raise ValueError(f"Invalid model: {model}. Choose from: {self.AVAILABLE_MODELS}")

        self.session = requests.Session()
        self.timeout = timeout
        self.api_endpoint = "https://chatgptgratis.eu/backend/chat.php"
        self.model = model

        # Set up headers similar to a browser request with dynamic User-Agent
        self.headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Origin": "https://chatgptgratis.eu",
            "Referer": "https://chatgptgratis.eu/chat.html",
            "User-Agent": Lit().random(),
        }
        self.session.headers.update(self.headers)
        self.session.proxies = proxies or {}

        # Set up conversation history and prompts
        Conversation.intro = (
            AwesomePrompts().get_act(
                act, raise_not_found=True, default=None, case_insensitive=True
            )
            if act
            else intro or Conversation.intro
        )
        self.conversation = Conversation(
            True, 8096, filepath, update_file
        )
        self.conversation.history_offset = history_offset

    def ask(
        self,
        prompt: str,
        stream: bool = False,
        raw: bool = False,
        optimizer: Optional[str] = None,
        conversationally: bool = False,
    ) -> Union[Dict[str, Any], Generator[Any, None, None]]:
        """
        Sends a request to the API and returns the response.
        If stream is True, yields response chunks as they are received.
        """
        conversation_prompt = self.conversation.gen_complete_prompt(prompt)
        if optimizer:
            available_opts = (
                method for method in dir(Optimizers)
                if callable(getattr(Optimizers, method)) and not method.startswith("__")
            )
            if optimizer in available_opts:
                conversation_prompt = getattr(Optimizers, optimizer)(
                    conversation_prompt if conversationally else prompt
                )
            else:
                raise Exception(f"Optimizer is not one of {list(available_opts)}")

        payload = {
            "message": conversation_prompt,
            "model": self.model,
        }

        def for_stream() -> Generator[Dict[str, Any], None, None]:
            response = self.session.post(
                self.api_endpoint,
                json=payload,
                stream=True,
                timeout=self.timeout
            )
            if not response.ok:
                raise exceptions.FailedToGenerateResponseError(
                    f"Failed to generate response - ({response.status_code}, {response.reason}) - {response.text}"
                )

            full_response = ""
            for line in response.iter_lines():
                if line:
                    line_decoded = line.decode('utf-8').strip()
                    if line_decoded == "data: [DONE]":
                        break
                    if line_decoded.startswith("data: "):
                        try:
                            json_data = json.loads(line_decoded[6:])
                            choices = json_data.get("choices", [])
                            if choices and "delta" in choices[0]:
                                content = choices[0]["delta"].get("content", "")
                            else:
                                content = ""
                            full_response += content
                            yield content if raw else {"text": content}
                        except json.JSONDecodeError:
                            continue
            # Update last response and conversation history.
            self.conversation.update_chat_history(prompt, self.get_message({"text": full_response}))

        def for_non_stream() -> Dict[str, Any]:
            collected = ""
            for chunk in for_stream():
                collected += chunk["text"] if isinstance(chunk, dict) else chunk
            return {"text": collected}

        return for_stream() if stream else for_non_stream()

    def chat(
        self,
        prompt: str,
        stream: bool = False,
        optimizer: Optional[str] = None,
        conversationally: bool = False,
    ) -> Union[str, Generator[str, None, None]]:
        """
        Returns the response as a string.
        For streaming requests, yields each response chunk as a string.
        """
        def stream_response() -> Generator[str, None, None]:
            for response in self.ask(
                prompt, stream=True, optimizer=optimizer, conversationally=conversationally
            ):
                yield self.get_message(response)

        def non_stream_response() -> str:
            return self.get_message(self.ask(
                prompt, stream=False, optimizer=optimizer, conversationally=conversationally
            ))

        return stream_response() if stream else non_stream_response()

    def get_message(self, response: dict) -> str:
        """
        Extracts and returns the text message from the response dictionary.
        """
        assert isinstance(response, dict), "Response must be a dictionary."
        return response.get("text", "")


if __name__ == "__main__":
    print("-" * 80)
    print(f"{'Model':<50} {'Status':<10} {'Response'}")
    print("-" * 80)

    for model in ChatGPTGratis.AVAILABLE_MODELS:
        try:
            test_ai = ChatGPTGratis(model=model, timeout=60)
            response = test_ai.chat("Say 'Hello' in one word")
            response_text = response
            
            if response_text and len(response_text.strip()) > 0:
                status = "✓"
                # Clean and truncate response
                clean_text = response_text.strip().encode('utf-8', errors='ignore').decode('utf-8')
                display_text = clean_text[:50] + "..." if len(clean_text) > 50 else clean_text
            else:
                status = "✗"
                display_text = "Empty or invalid response"
            print(f"{model:<50} {status:<10} {display_text}")
        except Exception as e:
            print(f"{model:<50} {'✗':<10} {str(e)}")