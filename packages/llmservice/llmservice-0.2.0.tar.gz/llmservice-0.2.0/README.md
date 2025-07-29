<div align="center">
  <h1>LLMSERVICE</h1>
  <img
    alt="LLMSERVICE Logo"
    src="https://raw.githubusercontent.com/karaposu/llmkit/refs/heads/main/assets/logo_cropped.png"
    width="50"
  >
</div>


-----------------

##  Add LLM logic in your app with complience of Modern Software Engineering Principles

|             |                                                                                                                                                                                |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Package** | [![PyPI Latest Release](https://img.shields.io/pypi/v/llmservice.svg)](https://pypi.org/project/llmservice/) [![PyPI Downloads](https://img.shields.io/pypi/dm/llmservice.svg?label=PyPI%20downloads)](https://pypi.org/project/llmservice/) |

## Installation

Install LLMService via pip:

```bash
pip install llmservice
```
 

## What is it?

Integrating LLMs often means embedding prompt construction, API calls, and post-processing directly into your application code—creating tangled pipelines and maintenance headaches. llmservice was created to decouple and streamline LLM workflows—handling prompts, invocations, and post-processing in a clean, reusable layer 

**LLMService** adheres to established software development best practices. With a strong focus on **Modularity and Separation of Concerns**, **Robust Error Handling**, and **Modern Software Engineering Principles**, LLMService delivers a well-structured alternative to more monolithic frameworks like LangChain.

> "LangChain isn't a library, it's a collection of demos held together by duct tape, fstrings, and prayers." 


## Main Features

* **Result Monad Pattern**
  Every invocation returns a `GenerationResult` dataclass, unifying success/failure handling, error metadata, and retry control in a single, consistent call.

* **Customizable Post-Processing Pipelines**
  Declaratively chain steps like semantic extraction, advanced JSON parsing, string validation, and more via simple pipeline configs.

* **Rate-Limit-Aware Asynchronous Requests**
  Centralized queuing with real-time rate-limit feedback drives dynamic worker scaling, maximising throughput while honouring API quotas.

* **Transparent Cost & Usage Monitoring**
  Automatic token counting and cost calculation per model, with detailed metadata returned alongside your content.

* **Retry Mechanisms**
  Utilizes the `tenacity` library to implement retries with exponential backoff for handling transient errors like rate limits or network issues.

- **Custom Exception Handling**
  Provides tailored responses to specific errors (e.g., insufficient quota), enabling graceful degradation and clearer insights into failure scenarios.






## Architecture

![LLMService Architecture](https://raw.githubusercontent.com/karaposu/LLMService/refs/heads/main/assets/llmservice_architecture1.png) 

![schemas](https://raw.githubusercontent.com/karaposu/LLMService/refs/heads/main/assets/schemas.png)  




1. **LLM Handler**: Manages interaction with different LLM providers (e.g., OpenAI, Ollama, Azure).
2. **Generation Engine**: Orchestrates the generation process, including prompt crafting, invoking the LLM through llm handler, and post-processing.
3. **Proteas**: A sophisticated prompt management system that loads and manages prompt templates from YAML files (`prompt.yaml`).
4. **LLMService (Base Class)**: A base class that serves as a template for users to implement their custom service logic.  
5. **App**: The application that consumes the services provided by LLMService, receiving structured `generation_result` responses for further processing.


### BaseLLMService Class

LLMService provides an abstract `BaseLLMService` class to guide users in implementing their own service layers:

- **Modern Software Development Practices**: Encourages adherence to best practices through a well-defined interface.
- **Customization**: Allows developers to tailor the service layer to their specific application needs while leveraging the core functionalities provided by LLMService.
- **Extensibility**: Facilitates the addition of new features and integrations without modifying the core library.



### Proteas: The Main Prompt Management System

Proteas serves as LLMService's (optional) prompt management system for mid level applications where there are losts of prompts to handle but not enough to put them in database, It offers powerful tools for crafting, managing, and reusing prompts:

- **Prompt Crafting**: Utilizes `PromptTemplate` to create consistent and dynamic prompts based on placeholders and data inputs.
- **Unit Skeletons**: Supports loading and managing prompt templates from YAML files, promoting reusability and organization.


## Installation

Install LLMService via pip:

```bash
pip install llmservice
```

## Quick Start

### Core Components

LLMService provides the following core modules:

- **`llmhandler`**: Manages interactions with different LLM providers.
- **`generation_engine`**: Handles the process of prompt crafting, LLM invocation, and post-processing.
- **`base_service`**: Provides an abstract class that serves as a blueprint for building custom services.

### Creating a Custom LLMService

To create your own service layer, follow these steps:

#### Step 0: Create your prompts.yaml file
Proteas uses a yaml file to load and manage your prompts. Prompts are encouraged to store as prompt template units 
where component of a prompt is decomposed into prompt template units and store in such way. To read more go to proteas docs
(link here)

Create a new Python file (e.g., `prompts.yaml`) 

add these lines 

```commandline
main:


  - name: "input_paragraph"
    statement_suffix: "Here is"
    question_suffix: "What is "
    placeholder_proclamation: input text to be translated
    placeholder: "input_paragraph"


  - name: "translate_to_russian"
    info: > 
      take above text and translate it to russian with a scientific language, Do not output any additiaonal text.
   
```

#### Step 1: Subclass `BaseLLMService`

Create a new Python file (e.g., `my_llm_service.py`) and extend the `BaseLLMService` class.
In your app all llm generation data flow will go through this class.  This is a good way of not coupling rest of your
app logic with LLM relevant logics. 

You simply arange the names of your prompt template units in a list and pass this to generation engine.

```python
from llmservice.base_service import BaseLLMService
from llmservice.generation_engine import GenerationEngine
import logging


class MyLLMService(BaseLLMService):
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.generation_engine = GenerationEngine(logger=self.logger, model_name="gpt-4o-mini")

    def translate_to_russian(self, input_paragraph: str):
        data_for_placeholders = {'input_paragraph': input_paragraph}
        order = ["input_paragraph", "translate_to_russian"]

        unformatted_prompt = self.generation_engine.craft_prompt(data_for_placeholders, order)

        generation_result = self.generation_engine.generate_output(
            unformatted_prompt,
            data_for_placeholders,
            response_type="string"
        )

        return generation_result.content
```

#### Step 2: Use the Custom Service

```python
# app.py
from my_llm_service import MyLLMService

if __name__ == '__main__':
    service = MyLLMService()
    result = service.translate_to_russian("Hello, how are you?")
    print(result)
```

Result will be a generation_result object which inludes all the information you need. 




some notes to add to future 

The Result Monad enhances error management by providing detailed insights into why a particular operation might have failed, enhancing the robustness of systems that interact with external data.
As evident from the examples, each of these monads facilitates the creation of function chains, employing a paradigm often referred to as a “railroad approach.” This approach visualizes the sequence of functions as a metaphorical railroad track, where the code smoothly travels along, guided by the monadic structure. The beauty of this railroad approach lies in its ability to elegantly manage complex computations and transformations, ensuring a structured and streamlined flow of operations.
