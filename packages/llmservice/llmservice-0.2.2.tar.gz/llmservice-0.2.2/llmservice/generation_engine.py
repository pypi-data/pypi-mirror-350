# generation_engine.py

import logging
import time
from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass, field

from llmservice.llm_handler import LLMHandler  # Ensure this is correctly imported
from string2dict import String2Dict  # Ensure this is installed and available
from proteas import Proteas  # Ensure this is installed and available
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.string import get_template_variables

from .schemas import GenerationRequest, GenerationResult,  PipelineStepResult


logger = logging.getLogger(__name__)



gpt_models_cost = {
    'gpt-4o-search-preview':    {'input_token_cost': 2.5e-6,  'output_token_cost': 10e-6},
    'gpt-4o-mini-search-preview': {'input_token_cost': 2.5e-6,  'output_token_cost': 0.6e-6},
    'gpt-4.5-preview':          {'input_token_cost': 75e-6,   'output_token_cost': 150e-6},
    'gpt-4.1-nano':             {'input_token_cost': 0.1e-6,  'output_token_cost': 0.4e-6},
    'gpt-4.1-mini':             {'input_token_cost': 0.4e-6,  'output_token_cost': 1.6e-6},
    'gpt-4.1':                  {'input_token_cost': 2e-6,    'output_token_cost': 8e-6},
    'gpt-4o':                   {'input_token_cost': 2.5e-6,  'output_token_cost': 10e-6},
    'gpt-4o-audio-preview':     {'input_token_cost': 2.5e-6,  'output_token_cost': 10e-6},
    'gpt-4o-mini':              {'input_token_cost': 0.15e-6, 'output_token_cost': 0.6e-6, },
    'o1':                       {'input_token_cost': 15e-6,   'output_token_cost': 60e-6},
    'o1-pro':                   {'input_token_cost': 150e-6,  'output_token_cost': 600e-6},
    'o3':                       {'input_token_cost': 10e-6,   'output_token_cost': 40e-6},
    'o4-mini':                  {'input_token_cost': 1.1e-6,  'output_token_cost': 4.4e-6},
}

# Costs per model (example values, adjust as needed)



class GenerationEngine:
    def __init__(self, llm_handler=None, model_name=None, debug=False):
        self.logger = logging.getLogger(__name__)
        self.debug = debug
        self.s2d = String2Dict()

        if llm_handler:
            self.llm_handler = llm_handler
        else:
            self.llm_handler = LLMHandler(model_name=model_name, logger=self.logger)

        self.proteas = Proteas()

        if self.debug:
            self.logger.setLevel(logging.DEBUG)

        # Define the semantic isolation prompt template
        self.semantic_isolation_prompt_template = """
Here is the text answer which includes the main desired information as well as some additional information: {answer_to_be_refined}
Here is the semantic element which should be used for extraction: {semantic_element_for_extraction}

From the given text answer, isolate and extract the semantic element.
Provide the answer strictly in the following JSON format, do not combine anything, remove all introductory or explanatory text that is not part of the semantic element:

'answer': 'here_is_isolated_answer'
"""

    def _debug(self, message):

        if self.debug:
            self.logger.debug(message)

    def load_prompts(self, yaml_file_path):
        """Loads prompts from a YAML file using Proteas."""
        self.proteas.load_unit_skeletons_from_yaml(yaml_file_path)

    def craft_prompt(self, placeholder_dict: Dict[str, Any], order: Optional[list] = None) -> str:
        """
        Crafts the prompt using Proteas with the given placeholders and order.

        :param placeholder_dict: Dictionary of placeholder values.
        :param order: Optional list specifying the order of units.
        :return: Unformatted prompt string.
        """
        unformatted_prompt = self.proteas.craft(units=order, placeholder_dict=placeholder_dict)
        return unformatted_prompt
    
    def cost_calculator(self, input_token, output_token, model_name):
        """
        Calculate input/output costs based on the gpt_models_cost dict.

        :param input_token: number of input tokens (int or numeric str)
        :param output_token: number of output tokens (int or numeric str)
        :param model_name: model key in gpt_models_cost
        :return: (input_cost, output_cost)
        """
        # Ensure the model exists
        info = gpt_models_cost.get(model_name)
        if info is None:
            self.logger.error(f"cost_calculator error: Unsupported model name: {model_name}")
            raise ValueError(f"cost_calculator error: Unsupported model name: {model_name}")
        
        # Parse token counts
        itoks = int(input_token)
        otoks = int(output_token)

        # Multiply by per-token rates
        inp_rate = info['input_token_cost']
        out_rate = info['output_token_cost']
        input_cost  = inp_rate  * itoks
        output_cost = out_rate * otoks

        return input_cost, output_cost
    
    async def generate_output_async(
        self,
        generation_request: GenerationRequest
    ) -> GenerationResult:
        """
        Asynchronously generates the output and processes post‐processing,
        mirroring the logic of generate_output but using LLMHandler.invoke_async.
        """
        # Unpack request
        placeholders        = generation_request.data_for_placeholders
        unformatted_prompt  = generation_request.unformatted_prompt
        formatted_prompt    = generation_request.formatted_prompt
        model_name          = generation_request.model or self.llm_handler.model_name
        operation_name      = generation_request.operation_name

        # Prepare formatted prompt
        if formatted_prompt:
            prompt_to_send = formatted_prompt
        else:
            # Validate placeholders
            existing = get_template_variables(unformatted_prompt, "f-string")
            missing  = set(existing) - set(placeholders or {})
            if missing:
                raise ValueError(f"Missing placeholders for async prompt: {missing}")
            tmpl = PromptTemplate.from_template(unformatted_prompt)
            prompt_to_send = tmpl.format(**placeholders)  # type: ignore

        # Initialize metadata
        meta = {
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "elapsed_time_for_invoke": 0,
            "input_cost": 0.0,
            "output_cost": 0.0,
            "total_cost": 0.0,
        }

        # Invoke LLM asynchronously
        t1 = time.time()
        try:
            r, success = await self.llm_handler.invoke_async(prompt=prompt_to_send)
        except Exception as e:
            return GenerationResult(
                success=False,
                meta=meta,
                raw_content=None,
                content=None,
                elapsed_time=time.time() - t1,
                error_message=str(e),
                model=model_name,
                formatted_prompt=prompt_to_send,
                unformatted_prompt=unformatted_prompt,
                request_id=generation_request.request_id,
                operation_name=operation_name,
            )
        t2 = time.time()
        meta["elapsed_time_for_invoke"] = t2 - t1

        if not success:
            return GenerationResult(
                success=False,
                meta=meta,
                raw_content=None,
                content=None,
                elapsed_time=meta["elapsed_time_for_invoke"],
                error_message="LLM invocation failed",
                model=model_name,
                formatted_prompt=prompt_to_send,
                unformatted_prompt=unformatted_prompt,
                request_id=generation_request.request_id,
                operation_name=operation_name,
            )

        # Populate token usage and cost if OpenAI model
        if self.llm_handler.OPENAI_MODEL:
            try:
                meta["input_tokens"]  = r.usage_metadata["input_tokens"]
                meta["output_tokens"] = r.usage_metadata["output_tokens"]
                meta["total_tokens"]  = r.usage_metadata["total_tokens"]
            except KeyError:
                return GenerationResult(
                    success=False,
                    meta=meta,
                    raw_content=None,
                    content=None,
                    elapsed_time=meta["elapsed_time_for_invoke"],
                    error_message="Token usage metadata missing",
                    model=model_name,
                    formatted_prompt=prompt_to_send,
                    unformatted_prompt=unformatted_prompt,
                    request_id=generation_request.request_id,
                    operation_name=operation_name,
                )
            inp_cost, out_cost = self.cost_calculator(
                meta["input_tokens"], meta["output_tokens"], model_name
            )
            meta["input_cost"]  = inp_cost
            meta["output_cost"] = out_cost
            meta["total_cost"]  = inp_cost + out_cost

        # Build initial GenerationResult
        generation_result = GenerationResult(
            success=True,
            meta=meta,
            raw_content=r.content,
            content=None,
            elapsed_time=meta["elapsed_time_for_invoke"],
            error_message=None,
            model=model_name,
            formatted_prompt=prompt_to_send,
            unformatted_prompt=unformatted_prompt,
            request_id=generation_request.request_id,
            operation_name=operation_name,
        )

        # Apply post-processing pipeline if configured
        if generation_request.pipeline_config:
            return self.execute_pipeline(generation_result, generation_request.pipeline_config)
        else:
            generation_result.content = generation_result.raw_content
            return generation_result

 

    def generate_output(self, generation_request: GenerationRequest) -> GenerationResult:
        """
        Synchronously generates the output and processes postprocessing.

        :param generation_request: GenerationRequest object containing all necessary data.
        :return: GenerationResult object with the output and metadata.
        """
        # Unpack the GenerationRequest
        placeholders = generation_request.data_for_placeholders
        unformatted_prompt = generation_request.unformatted_prompt
        formatted_prompt = generation_request.formatted_prompt

        # Generate the output synchronously
        generation_result = self.generate(
            formatted_prompt= formatted_prompt,
            unformatted_template=unformatted_prompt,
            data_for_placeholders=placeholders,
            model_name=generation_request.model,
            request_id=generation_request.request_id,
            operation_name=generation_request.operation_name
        )

        generation_result.generation_request=generation_request

        if not generation_result.success:
            return generation_result

        # Process the output using the pipeline
        if generation_request.pipeline_config:
            generation_result = self.execute_pipeline(generation_result, generation_request.pipeline_config)
        else:
            # No postprocessing; assign raw_content to content
            generation_result.content = generation_result.raw_content

        return generation_result

    def execute_pipeline(self, generation_result: GenerationResult, pipeline_config: List[Dict[str, Any]]) -> GenerationResult:
        """
        Executes the processing pipeline on the generation result.

        :param generation_result: The initial GenerationResult from the LLM.
        :param pipeline_config: List of processing steps.
        :return: Updated GenerationResult after processing.
        """
        current_content = generation_result.raw_content
        for step_config in pipeline_config:
            step_type = step_config.get('type')
            params = step_config.get('params', {})
            method_name = f"process_{step_type.lower()}"
            processing_method = getattr(self, method_name, None)
            step_result = PipelineStepResult(
                step_type=step_type,
                success=False,
                content_before=current_content,
                content_after=None
            )
            if processing_method:
                try:
                    content_after = processing_method(current_content, **params)
                    step_result.success = True
                    step_result.content_after = content_after
                    current_content = content_after  # Update current_content for next step
                except Exception as e:
                    step_result.success = False
                    step_result.error_message = str(e)
                    generation_result.success = False
                    generation_result.error_message = f"Processing step '{step_type}' failed: {e}"
                    self.logger.error(generation_result.error_message)
                    # Record the failed step and exit the pipeline
                    generation_result.pipeline_steps_results.append(step_result)
                    return generation_result
            else:
                step_result.success = False
                error_msg = f"Unknown processing step type: {step_type}"
                step_result.error_message = error_msg
                generation_result.success = False
                generation_result.error_message = error_msg
                self.logger.error(generation_result.error_message)
                # Record the failed step and exit the pipeline
                generation_result.pipeline_steps_results.append(step_result)
                return generation_result
            # Record the successful step
            generation_result.pipeline_steps_results.append(step_result)

        # Update the final content
        generation_result.content = current_content
        return generation_result

    # Define processing methods
    def process_semanticisolation(self, content: str, semantic_element_for_extraction: str) -> str:
        """
        Processes content using semantic isolation.

        :param content: The content to process.
        :param semantic_element_for_extraction: The semantic element to extract.
        :return: The isolated semantic element.
        """
        answer_to_be_refined = content

        data_for_placeholders = {
            "answer_to_be_refined": answer_to_be_refined,
            "semantic_element_for_extraction": semantic_element_for_extraction,
        }
        unformatted_refiner_prompt = self.semantic_isolation_prompt_template

        refiner_result = self.generate(
            unformatted_template=unformatted_refiner_prompt,
            data_for_placeholders=data_for_placeholders
        )

        if not refiner_result.success:
            raise ValueError(f"Semantic isolation failed: {refiner_result.error_message}")

        # Parse the LLM response to extract 'answer'
        s2d_result = self.s2d.run(refiner_result.raw_content)
        isolated_answer = s2d_result.get('answer')
        if isolated_answer is None:
            raise ValueError("Isolated answer not found in the LLM response.")

        return isolated_answer

    def process_converttodict(self, content: Any) -> Dict[str, Any]:
        """
        Converts content to a dictionary.

        :param content: The content to convert.
        :return: The content as a dictionary.
        """
        if isinstance(content, dict):
            return content  # Already a dict
        return self.s2d.run(content)

    def process_extractvalue(self, content: Dict[str, Any], key: str) -> Any:
        """
        Extracts a value from a dictionary.

        :param content: The dictionary content.
        :param key: The key to extract.
        :return: The extracted value.
        """
        if key not in content:
            raise KeyError(f"Key '{key}' not found in content.")
        return content[key]

    # todo add model param for semanticisolation
    def process_stringmatchvalidation(self, content: str, expected_string: str) -> str:
        """
        Validates that the expected string is present in the content.

        :param content: The content to validate.
        :param expected_string: The expected string to find.
        :return: The original content if validation passes.
        """
        if expected_string not in content:
            raise ValueError(f"Expected string '{expected_string}' not found in content.")
        return content

    def process_jsonload(self, content: str) -> Dict[str, Any]:
        """
        Loads content as JSON.

        :param content: The content to load.
        :return: The content as a JSON object.
        """
        import json
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON loading failed: {e}")
        
    
    def generate(
        self,
        formatted_prompt: Optional[str] = None,
        unformatted_template: Optional[str] = None,
        data_for_placeholders: Optional[Dict[str, Any]] = None,
        model_name: Optional[str] = None,
        request_id: Optional[Union[str, int]] = None,
        operation_name: Optional[str] = None
    ) -> GenerationResult:
        """
        Generates content using the LLMHandler.

        :param formatted_prompt: A fully formatted prompt to send directly.
        :param unformatted_template: The prompt template if formatting is needed.
        :param data_for_placeholders: Values for template placeholders.
        :param model_name: Model name to use.
        :param request_id: Optional request ID.
        :param operation_name: Optional operation name.
        :return: GenerationResult object.
        """
        # Enforce either-or contract
        has_formatted = formatted_prompt is not None
        has_unformatted = unformatted_template is not None and data_for_placeholders is not None
        if has_formatted and has_unformatted:
            raise ValueError(
                "Provide either `formatted_prompt` or (`unformatted_template` + `data_for_placeholders`), not both."
            )
        if not (has_formatted or has_unformatted):
            raise ValueError(
                "You must supply either `formatted_prompt` or both `unformatted_template` and `data_for_placeholders`."
            )

        meta = {  # usage & cost metadata
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "elapsed_time_for_invoke": 0,
            "input_cost": 0,
            "output_cost": 0,
            "total_cost": 0,
        }

        # Determine final prompt
        if has_formatted:
            prompt_to_send = formatted_prompt  # type: ignore
        else:
            existing_placeholders = get_template_variables(unformatted_template, "f-string")  # type: ignore
            missing = set(existing_placeholders) - set(data_for_placeholders.keys())  # type: ignore
            if missing:
                raise ValueError(f"Missing data for placeholders: {missing}")
            tmpl = PromptTemplate.from_template(unformatted_template)  # type: ignore
            prompt_to_send = tmpl.format(**data_for_placeholders)  # type: ignore

        # Invoke LLM
        t1 = time.time()
        llm_handler = LLMHandler(model_name=model_name or self.llm_handler.model_name, logger=self.logger)
        r, success = llm_handler.invoke(prompt=prompt_to_send)
        t2 = time.time()
        elapsed = t2 - t1
        meta["elapsed_time_for_invoke"] = elapsed

        if not success:
            return GenerationResult(
                success=False,
                meta=meta,
                raw_content=None,
                content=None,
                elapsed_time=elapsed,
                error_message="LLM invocation failed",
                model=llm_handler.model_name,
                formatted_prompt=prompt_to_send,
                unformatted_prompt=unformatted_template,
                request_id=request_id,
                operation_name=operation_name
            )

        if llm_handler.OPENAI_MODEL:
            try:
                meta["input_tokens"] = r.usage_metadata["input_tokens"]
                meta["output_tokens"] = r.usage_metadata["output_tokens"]
                meta["total_tokens"] = r.usage_metadata["total_tokens"]
            except KeyError:
                return GenerationResult(
                    success=False,
                    meta=meta,
                    raw_content=None,
                    content=None,
                    elapsed_time=elapsed,
                    error_message="Token usage metadata missing",
                    model=llm_handler.model_name,
                    formatted_prompt=prompt_to_send,
                    unformatted_prompt=unformatted_template,
                    request_id=request_id,
                    operation_name=operation_name
                )
            in_cost, out_cost = self.cost_calculator(
                meta["input_tokens"], meta["output_tokens"], llm_handler.model_name
            )
            meta["input_cost"] = in_cost
            meta["output_cost"] = out_cost
            meta["total_cost"] = in_cost + out_cost

        return GenerationResult(
            success=True,
            meta=meta,
            raw_content=r.content,
            content=None,
            elapsed_time=elapsed,
            error_message=None,
            model=llm_handler.model_name,
            formatted_prompt=prompt_to_send,
            unformatted_prompt=unformatted_template,
            request_id=request_id,
            operation_name=operation_name
        )

    # # Implement the generate method
    # def generate(
    #     self,
    #     formatted_prompt: Optional[str] = None,
    #     unformatted_template: Optional[str] = None,
    #     data_for_placeholders: Optional[Dict[str, Any]] = None,
    #     model_name: Optional[str] = None,
    #     request_id: Optional[Union[str, int]] = None,
    #     operation_name: Optional[str] = None
    # ) -> GenerationResult:
    # #def generate(self, unformatted_template, data_for_placeholders, model_name=None, request_id=None, operation_name=None) -> GenerationResult:
    #     """
    #     Generates content using the LLMHandler.

    #     :param unformatted_template: The unformatted prompt template.
    #     :param data_for_placeholders: Data to fill the placeholders.
    #     :param model_name: Model name to use.
    #     :param request_id: Optional request ID.
    #     :param operation_name: Optional operation name.
    #     :return: GenerationResult object.
    #     """
    #     meta = {
    #         "input_tokens": 0,
    #         "output_tokens": 0,
    #         "total_tokens": 0,
    #         "elapsed_time_for_invoke": 0,
    #         "input_cost": 0,
    #         "output_cost": 0,
    #         "total_cost": 0,
    #     }

    #     t0 = time.time()

    #     if formatted_prompt is not None:
    #         prompt_to_send = formatted_prompt
    #     else:

    
    #         # Validate placeholders
    #         existing_placeholders = get_template_variables(unformatted_template, "f-string")
    #         missing_placeholders = set(existing_placeholders) - set(data_for_placeholders.keys())

    #         if missing_placeholders:
    #             raise ValueError(f"Missing data for placeholders: {missing_placeholders}")

    #         # Format the prompt
    #         prompt_template = PromptTemplate.from_template(unformatted_template)
    #         prompt_to_send = prompt_template.format(**data_for_placeholders)

    #     t1 = time.time()

    #     # Initialize LLMHandler with the model_name
    #     llm_handler = LLMHandler(model_name=model_name or self.llm_handler.model_name, logger=self.logger)

    #     # Invoke the LLM synchronously
    #     r, success = llm_handler.invoke(prompt=prompt_to_send)

    #     if not success:
    #         return GenerationResult(
    #             success=False,
    #             meta=meta,
    #             raw_content=None,
    #             content=None,
    #             elapsed_time=0,
    #             error_message="LLM invocation failed",
    #             model=llm_handler.model_name,
    #             formatted_prompt=prompt_to_send,
    #             request_id=request_id,
    #             operation_name=operation_name
    #         )

    #     t2 = time.time()
    #     elapsed_time_for_invoke = t2 - t1
    #     meta["elapsed_time_for_invoke"] = elapsed_time_for_invoke

    #     if llm_handler.OPENAI_MODEL:
    #         try:
    #             meta["input_tokens"] = r.usage_metadata["input_tokens"]
    #             meta["output_tokens"] = r.usage_metadata["output_tokens"]
    #             meta["total_tokens"] = r.usage_metadata["total_tokens"]
    #         except KeyError as e:
    #             return GenerationResult(
    #                 success=False,
    #                 meta=meta,
    #                 raw_content=None,
    #                 content=None,
    #                 elapsed_time=elapsed_time_for_invoke,
    #                 error_message="Token usage metadata missing",
    #                 model=llm_handler.model_name,
    #                 formatted_prompt=prompt_to_send,
    #                 unformatted_prompt=unformatted_template,
    #                 request_id=request_id,
    #                 operation_name=operation_name
    #             )

    #         input_cost, output_cost = self.cost_calculator(
    #             meta["input_tokens"], meta["output_tokens"], llm_handler.model_name)
    #         meta["input_cost"] = input_cost
    #         meta["output_cost"] = output_cost
    #         meta["total_cost"] = input_cost + output_cost

    #     return GenerationResult(
    #         success=True,
    #         meta=meta,
    #         raw_content=r.content,  # Assign initial LLM output
    #         content=None,           # Will be assigned after postprocessing
    #         elapsed_time=elapsed_time_for_invoke,
    #         error_message=None,
    #         model=llm_handler.model_name,
    #         formatted_prompt=prompt_to_send,
    #         unformatted_prompt=unformatted_template,
    #         request_id=request_id,
    #         operation_name=operation_name
    #     )

# Main function for testing
def main():
    import logging

    import sys

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )


    generation_engine = GenerationEngine(model_name='gpt-4o')

    placeholders = {'input_text': 'Patient shows symptoms of severe headache and nausea.'}
    unformatted_prompt = 'Provide a summary of the following clinical note: {input_text}'

    pipeline_config = [
        {
            'type': 'SemanticIsolation',
            'params': {
                'semantic_element_for_extraction': 'symptoms'
            }
        },
        # You can add more steps here if needed
    ]

    gen_request = GenerationRequest(
        data_for_placeholders=placeholders,
        unformatted_prompt=unformatted_prompt,
        model='gpt-4o',
        pipeline_config=pipeline_config,
        request_id=3,
        operation_name='extract_symptoms'
    )

    generation_result = generation_engine.generate_output(gen_request)

    if generation_result.success:
        logger.info("Final Result:")
        logger.info(generation_result.content)
        logger.info("Raw LLM Output:")
        logger.info(generation_result.raw_content)
    else:
        logger.info("Error:")
        logger.info(generation_result.error_message)

    logger.info("Pipeline Steps Results")
    for step_result in generation_result.pipeline_steps_results:
        logger.info(f"Step {step_result.step_type}")
        logger.info(f"Success {step_result.success}")

        if step_result.success:
            logger.info(f"Content Before: {step_result.content_before}")
            logger.info(f"Content After: {step_result.content_after}")
        else:
            logger.info(f"Error: {step_result.error_message}")

if __name__ == '__main__':
    main()
