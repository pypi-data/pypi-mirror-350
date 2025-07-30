# here is llm_handler.py


# to run python -m llmservice.llm_handler
import os
from pathlib import Path
import logging
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type, RetryCallState, AsyncRetrying
from typing import Any
import httpx
import asyncio


from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_community.llms import Ollama
from openai import RateLimitError , PermissionDeniedError

#
# LangChainDeprecationWarning: The class `Ollama` was deprecated in LangChain 0.3.1 and will be removed in
# 1.0.0. An updated version of the class exists in the :class:`~langchain-ollama package and should be used instead. To
# use it run `pip install -U :class:`~langchain-ollama` and
# import as `from :class:`~langchain_ollama import OllamaLLM``.



# @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))

logging.getLogger("langchain_community.llms").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger('httpcore').setLevel(logging.WARNING)

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


gpt_models_cost = {
    'gpt-4o-search-preview':    {'input_token_cost': 2.5e-6,  'output_token_cost': 10e-6},
    'gpt-4o-mini-search-preview': {'input_token_cost': 2.5e-6,  'output_token_cost': 0.6e-6},
    'gpt-4.5-preview':          {'input_token_cost': 75e-6,   'output_token_cost': 150e-6},
    'gpt-4.1-nano':             {'input_token_cost': 0.1e-6,  'output_token_cost': 0.4e-6},
    'gpt-4.1-mini':             {'input_token_cost': 0.4e-6,  'output_token_cost': 1.6e-6},
    'gpt-4.1':                  {'input_token_cost': 2e-6,    'output_token_cost': 8e-6},
    'gpt-4o':                   {'input_token_cost': 2.5e-6,  'output_token_cost': 10e-6},
    'gpt-4o-audio-preview':     {'input_token_cost': 2.5e-6,  'output_token_cost': 10e-6},
    'gpt-4o-mini':              {'input_token_cost': 0.15e-6, 'output_token_cost': 0.6e-6},
    'o1':                       {'input_token_cost': 15e-6,   'output_token_cost': 60e-6},
    'o1-pro':                   {'input_token_cost': 150e-6,  'output_token_cost': 600e-6},
    'o3':                       {'input_token_cost': 10e-6,   'output_token_cost': 40e-6},
    'o4-mini':                  {'input_token_cost': 1.1e-6,  'output_token_cost': 4.4e-6},
}


gpt_model_list= list(gpt_models_cost.keys())



class LLMHandler:
    def __init__(self, model_name: str, system_prompt=None, logger=None):
        self.llm = self._initialize_llm(model_name)
        self.system_prompt = system_prompt
        self.model_name=model_name
        self.logger = logger if logger else logging.getLogger(__name__)

        # Set the level of the logger
        self.logger.setLevel(logging.DEBUG)
        self.max_retries = 2  # Set the maximum retries allowed

        self.OPENAI_MODEL = False
        self._llm_cache = {}

        if self.is_it_gpt_model(model_name):
            self.OPENAI_MODEL= True

    def is_it_gpt_model(self, model_name):
        # return model_name in ["gpt-4o-mini", "gpt-4", "gpt-4o", "gpt-3.5"]
        return model_name in gpt_model_list


    def change_model(self, model_name):
        self.llm = self._initialize_llm(model_name)

    # def _initialize_llm(self, model_name: str):
    #     if model_name in self._llm_cache:
    #         return self._llm_cache[model_name]
    #
    #     if self.is_it_gpt_model(model_name):
    #         llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"),
    #                          model_name=model_name)
    #     elif model_name == "custom":
    #         llm = ""
    #     else:
    #         llm = Ollama(model=model_name)
    #
    #     self._llm_cache[model_name] = llm
    #     return llm

    def _initialize_llm(self, model_name: str):

        if self.is_it_gpt_model(model_name):
            if model_name== "gpt-4o-search-preview":
               
               return ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"),
                                model_name=model_name,
                                model_kwargs={
                                    "web_search_options": {
                                        "search_context_size": "high"
                                    }
                                }

                                 
                                )
            else:
                return ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"),
                                model_name=model_name,
                                # max_tokens=15000
                                )
        elif model_name=="custom":
            ollama_llm=""
            return ollama_llm
        else:
            if not self._is_ollama_model_downloaded(model_name):
                print(f"The Ollama model '{model_name}' is not downloaded.")
                print(f"To download it, run the following command:")
                print(f"ollama pull {model_name}")
                raise ValueError(f"The Ollama model '{model_name}' is not downloaded.")
            return Ollama(model=model_name)

    def _is_ollama_model_downloaded(self, model_name: str) -> bool:
        #todo check OLLAMA_MODELS path

        # # Define the Ollama model directory (replace with actual directory)
        # ollama_model_dir = Path("~/ollama/models")  # Replace with the correct path
        # model_file = ollama_model_dir / f"{model_name}.model"  # Adjust the file extension if needed
        #
        # # Check if the model file exists
       # model_file.exists()#
        return  True

    @retry(
        retry=retry_if_exception_type((httpx.HTTPStatusError, RateLimitError)),
        # Retry on HTTPStatusError and RateLimitError
        stop=stop_after_attempt(2),  # Stop after 2 attempts
        wait=wait_random_exponential(min=1, max=60)  # Exponential backoff between retries
    )
    def invoke(self, prompt: str, retry_state: RetryCallState = None):
    # def invoke_safe(self, prompt: str, retry_state: RetryCallState = None):
        try:
            if self.system_prompt:
                response = self.llm.invoke(prompt=prompt, context=self.system_prompt)
            else:

                response = self.llm.invoke(prompt)
            success=True

            return response, success

        except RateLimitError as e:
            error_message = str(e)
            error_code = getattr(e, 'code', None)
            success = False

            # Try to get the error code from e.json_body if available
            if not error_code and hasattr(e, 'json_body') and e.json_body:
                error_code = e.json_body.get('error', {}).get('code')

            # Fallback: check if 'insufficient_quota' is in the error message
            if not error_code and 'insufficient_quota' in error_message:
                error_code = 'insufficient_quota'

            if error_code == 'insufficient_quota':
                self.logger.error("OpenAI credit is finished.")
                return "OpenAI credit is finished" ,success

            # Handle other rate limit errors
            self.logger.warning(f"RateLimitError occurred: {error_message}. Retrying...")
            if retry_state and self._retry_count_is_max(retry_state):
                return "OpenAI credit is finished" ,success

            raise  # Re-raise the error to trigger the retry mechanism

        except httpx.HTTPStatusError as e:
            success = False
            if e.response.status_code == 429:
                self.logger.warning("Rate limit exceeded: 429 Too Many Requests. Retrying...")

                # Check if this is the last retry attempt
                if retry_state and self._retry_count_is_max(retry_state):
                    return "OpenAI credit is finished" , success

                raise  # Re-raise the error to trigger the retry mechanism

            self.logger.error(f"HTTP error occurred: {e}")
            raise

        except PermissionDeniedError as e:
            success = False
            error_message = str(e)
            error_code = getattr(e, 'code', None)

            if error_code == 'unsupported_country_region_territory':
                self.logger.error("Country, region, or territory not supported.")
                return "Country, region, or territory not supported.", success
            else:
                self.logger.error(f"PermissionDeniedError occurred: {error_message}")
                raise

        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            raise

    
    @retry(
        retry=retry_if_exception_type((httpx.HTTPStatusError, RateLimitError)),
        stop=stop_after_attempt(2),
        wait=wait_random_exponential(min=1, max=60)
    )
    async def invoke_async(
        self,
        prompt: str,
        retry_state: RetryCallState = None
    ) -> tuple[Any, bool]:
        """
        Uses the LLM’s native async call (ainvoke). Raises if ainvoke isn’t implemented.
        """
        if not hasattr(self.llm, "ainvoke"):
            raise NotImplementedError(
                f"{type(self.llm).__name__} does not support async `ainvoke`."
            )

        try:
            # Call the async API directly
            response = await self.llm.ainvoke(prompt)
            success = True
            return response, success

        except RateLimitError as e:
            # propagate up to retry decorator
            raise

        except httpx.HTTPStatusError as e:
            # propagate up to retry decorator
            raise

        except PermissionDeniedError as e:
            # handle and wrap permission errors
            code = getattr(e, "code", None)
            if code == "unsupported_country_region_territory":
                return "Country, region, or territory not supported.", False
            raise

        except Exception as e:
            # any other errors bubble up
            self.logger.error(f"Async invoke error: {e}")
            raise

    # async def invoke_async(self, prompt: str):
    #     try:
    #         if self.system_prompt:
    #             response = await self.llm.agenerate([prompt], system_prompt=self.system_prompt)
    #         else:
    #             response = await self.llm.agenerate([prompt])
    #         success = True
    #         return response.generations[0][0], success
    #     except Exception as e:
    #         self.logger.error(f"An error occurred: {e}")
    #         return str(e), False


    # async def invoke_async(self, prompt: str):
    #     async for attempt in AsyncRetrying(
    #             retry=retry_if_exception_type((httpx.HTTPStatusError, RateLimitError)),
    #             stop=stop_after_attempt(2),
    #             wait=wait_random_exponential(min=1, max=60)
    #     ):
    #         with attempt:
    #             try:
    #                 if self.system_prompt:
    #                     response = await self.llm.acall(prompt=prompt, context=self.system_prompt)
    #                 else:
    #                     response = await self.llm.acall(prompt)
    #                 success = True
    #                 return response, success
    #             except Exception as e:
    #                 self.logger.error(f"An error occurred: {e}")
    #                 raise
    
    def _retry_count_is_max(self, retry_state: RetryCallState) -> bool:
        """
        Helper function to check if the retry limit is reached.
        Compares the current attempt number with the max_retries set.
        """
        current_attempt = retry_state.attempt_number
        return current_attempt >= self.max_retries
    

    # gpt-4o-search-preview


def main():
   
    llm_handler=LLMHandler(model_name="gpt-4o-search-preview")
    # llm_handler=LLMHandler(model_name="gpt-4o-mini")
    sample_prompt= "web search yap ve bana bugun bursadaki hava durumunu ver"

    r=llm_handler.invoke(sample_prompt)

    print(r)



if __name__ == "__main__":
    main()
