# langxchange/prompt_helper.py

import itertools
from typing import List, Dict, Any, Optional


class PrompterResponse:
    """
    Utility to build and send prompts to an LLM's chat interface.

    :param llm: An object implementing `chat(messages: List[dict], **kwargs) -> str`
    :param system_prompt: A system-level instruction to prefix every conversation.
    """

    def __init__(
        self,
        llm: Any,
        system_prompt: str = "You are a helpful assistant."
    ):
        if not hasattr(llm, "chat"):
            raise ValueError("Provided llm must implement a .chat(...) method")
        self.llm = llm
        self.system_prompt = system_prompt
    def GeneratePrompt(self,user_input: str,context: str):
        prompt = (
            f"Context:\n{context}\n\n"
            f"User Question:\n{user_input}\n\n"
            f"Based on the above context, provide a relevant response."
        )

        return prompt
    def run(
        self,
        user_query: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Build a chat payload and send to the LLM.

        :param user_query: The main user question or instruction.
        :param retrieval_results: Optional list of hits from a RetrieverHelper,
               each dict with keys "document" (str or List[str]) and "metadata"
               (dict or List[dict]). These will be formatted into assistant
               messages preceding the query.
        :param temperature: Sampling temperature.
        :param max_tokens: Token limit for the response.
        :return: The LLM's reply string.
        """
        # 1) Start with a system message
        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": self.system_prompt}
        ]

        # # 2) Incorporate retrieval results as context if provided
        # if retrieval_results:
        #     snippet_counter = itertools.count(1)
        #     for hit in retrieval_results:
        #         docs = hit.get("document")
        #         metas = hit.get("metadata")
        #         # Normalize to parallel lists
        #         if isinstance(docs, list):
        #             doc_list = docs
        #         else:
        #             doc_list = [docs]
        #         if isinstance(metas, list):
        #             meta_list = metas
        #         else:
        #             meta_list = [metas] * len(doc_list)

        #         for doc, meta in zip(doc_list, meta_list):
        #             i = next(snippet_counter)
        #             tag = ", ".join(f"{k}={v}" for k, v in (meta or {}).items())
        #             content = f"Snippet {i} ({tag}):\n{doc}"
        #             messages.append({"role": "assistant", "content": content})
        
        # 3) Finally append the user query
        messages.append({"role": "user", "content": user_query})

        # 4) Build kwargs for chat call
        chat_kwargs = {"messages": messages}
        if temperature is not None:
            chat_kwargs["temperature"] = temperature
        if max_tokens is not None:
            chat_kwargs["max_tokens"] = max_tokens

        # 5) Invoke the LLM
        return self.llm.chat(**chat_kwargs)


# # langxchange/prompt_helper.py

# from typing import List, Dict, Any, Optional


# class PrompterResponse:
#     """
#     Utility to build and send prompts to an LLM's chat interface.

#     :param llm: An object implementing `chat(messages: List[dict], **kwargs) -> str`
#     :param system_prompt: A system-level instruction to prefix every conversation.
#     """

#     def __init__(
#         self,
#         llm: Any,
#         system_prompt: str = "You are a helpful assistant."
#     ):
#         if not hasattr(llm, "chat"):
#             raise ValueError("Provided llm must implement a .chat(...) method")
#         self.llm = llm
#         self.system_prompt = system_prompt

#     def run(
#         self,
#         user_query: str,
#         retrieval_results: Optional[List[Dict[str, Any]]] = None,
#         temperature: float = 0.7,
#         max_tokens: Optional[int] = None
#     ) -> str:
#         """
#         Build a chat payload and send to the LLM.

#         :param user_query: The main user question or instruction.
#         :param retrieval_results: Optional list of hits from a RetrieverHelper,
#                each dict with keys "document" and optional "metadata".
#                These will be formatted into assistant messages preceding the query.
#         :param temperature: Sampling temperature.
#         :param max_tokens: Token limit for the response.
#         :return: The LLM's reply string.
#         """
#         # 1) Start with a system message
#         messages: List[Dict[str, Any]] = [
#             {"role": "system", "content": self.system_prompt}
#         ]

#         # 2) Incorporate retrieval results as context if provided
#         if retrieval_results:
#             for i, hit in enumerate(retrieval_results, start=1):
#                 doc = hit.get("document", "")
#                 meta = hit.get("metadata", {})
#                 # Format metadata into a brief tag
#                 tag = ", ".join(f"{k}={v}" for k, v in meta.items())
#                 content = f"Context {i} ({tag}):\n{doc}"
#                 messages.append({"role": "assistant", "content": content})

#         # 3) Finally append the user query
#         messages.append({"role": "user", "content": user_query})

#         # 4) Build kwargs for chat call
#         chat_kwargs = {"messages": messages}
#         if temperature is not None:
#             chat_kwargs["temperature"] = temperature
#         if max_tokens is not None:
#             chat_kwargs["max_tokens"] = max_tokens

#         # 5) Invoke the LLM
#         return self.llm.chat(**chat_kwargs)
