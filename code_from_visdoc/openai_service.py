import openai
from code_from_visdoc.prompts_store import Prompts 
from code_from_visdoc.utils import parse_openai_single_json
from datetime import datetime
import json
import os
from pydantic import BaseModel
import copy

class OpenAIService:
    def __init__(self, api_key, repo):
        openai.api_key = api_key
        self.model = "gpt-4o"
        self.repo_name = repo
        self.prompts = Prompts(self.repo_name)
        self.output_dir = 'static/llm_output/'

    def process_documents(self, documents):
        # prompt = self.build_prompt(system_prompt, user_prompt, documents)
        prompt = self.fetch_prompt('PROMPT_FOR_SINGLE_FILE')
        full_prompt = self.add_single_doc_to_prompt(prompt, documents)
        # print(full_prompt)
        response = self.get_llm_response_json(full_prompt)
        return response
    
    def get_llm_response_json(self, prompt):
        print("Started: Calling LLM API...")
        response = openai.chat.completions.create(
            model=self.model,
            messages = prompt,
            temperature = 0.0,
            response_format={ "type": "json_object" }
        )
        # print(response.choices[0].message.content)
        print("Completed: Calling LLM API...")
        return response.choices[0].message.content

    def get_llm_response_normal(self, prompt):
            print("Started: Calling LLM API...")
            class CleanedDocument(BaseModel):
                document: str

            response = openai.beta.chat.completions.parse(
                model=self.model,
                messages = prompt,
                temperature = 0.0,
                # response_format={ 'type': "json_object" }
                response_format=CleanedDocument
            )
            # print(response.choices[0].message.content)
            print("Completed: Calling LLM API...")
            jsonified_string = json.loads(response.choices[0].message.content)
            print(jsonified_string.keys())
            return jsonified_string['document']
    
    def add_single_doc_to_prompt(self, prompt, doc):
        prompt_doc = {"role": "user", "content": doc }
        prompt.append(prompt_doc)
        return prompt

    def add_segments_to_prompt(self, prompt, segments):
        # prompt_with_segments = {"role": "user", "content": f"{segments}" }
        for item in prompt:
            if item["role"] == "user":
                item["content"] += str(segments)
        # prompt.append(prompt_with_segments)
        return prompt

    def build_prompt(self, system_prompt, user_prompt, documents):
        # Combine user and system prompts with the document content
        doc_content = "\n".join(documents)
        return f"{user_prompt}\n\nDocuments:\n{doc_content}"

    def fetch_prompt(self, prompt_name):
        return getattr(self.prompts, prompt_name)
    
    def get_prompt_for_segmentclass(self, segment_class_name, prompt_for_llm):
        print(f"Started: Creating prompt for LLM for segment_class <{segment_class_name}>")
        target_string = '<segment_class>'
        #We get the [prompt for llm] from the app.py file.
        prompt_for_sequencing = self.fetch_prompt(prompt_for_llm)

        #replace some dummy strings by the actual class name in the prompt
        updated_prompt = [
            {
                "role": item["role"],
                "content": item["content"].replace(target_string, segment_class_name),
            }
            for item in prompt_for_sequencing
        ]
        print(f"Completed: Creating prompt for LLM for segment_class <{segment_class_name}>")
        # print(updated_prompt)
        return updated_prompt
    
    def find_sequences_for_allsegments(self, segregated_segments, prompt_for_llm):
        print(f"Started finding sequences for ")
        flow_and_contents ={}
        for segment_class, all_segments in segregated_segments.items():
            print(f"{segment_class}: {len(all_segments)}")
            segment_prompt = self.get_prompt_for_segmentclass(segment_class, prompt_for_llm)
            full_prompt_with_segments = self.add_segments_to_prompt(segment_prompt, all_segments)
            # print(full_prompt_with_segments)
            # with open('segments_before_llm.txt', "a") as file:
            #     for segment in all_segments:
            #         file.write(segment)
            #         file.write("\n----------------------\n")
            llm_result = parse_openai_single_json(self.get_llm_response_json(full_prompt_with_segments))
            flow_and_contents[segment_class] = llm_result
        print(f"Completed finding sequences...")
        now = datetime.now()
        current_directory = os.getcwd()
        # Format the date and time as a string
        formatted = now.strftime("%Y-%m-%d %H:%M:%S")
        filename =  current_directory + '/static/llm_ouput/output1_' + formatted +'.json'
        with open(filename, "w") as file:
            json.dump(flow_and_contents, file, indent=4)
        return flow_and_contents
    
    def add_document_to_prompt(self, prompt_for_cleaning, document):
        with open(document, "r") as file:
            segmented_content = file.read()
        
        for item in prompt_for_cleaning:
            if item["role"] == "user":
                item["content"] += segmented_content
        return prompt_for_cleaning
        

    def clean_segments(self, prompt_for_llm, document):
        print(f"Cleaning segments for {document} ")
        prompt_for_cleaning =   copy.deepcopy(self.fetch_prompt(prompt_for_llm))
        # prompt_for_cleaning = copy.deepcopy(self.prompts.PROMPT_FOR_CLEANING_SEGMENTATION)
        print("\n\n PROMPMT FOR CLEANING \n\n")
        # print(prompt_for_cleaning)
        full_prompt_with_document = self.add_document_to_prompt(prompt_for_cleaning, document)
        llm_result = self.get_llm_response_normal(full_prompt_with_document)
        print(f"Completed cleaning up segmentation...")
        # now = datetime.now()
        # current_directory = os.getcwd()
        # Format the date and time as a string
        # formatted = now.strftime("%Y-%m-%d %H:%M:%S")
        # filename =  current_directory + '/static/llm_ouput/output_' + formatted +'.json'
        # print("\n\n FILENAME I'M LOOKING AT:\n\n", document)
        # print("\n\n LLM RESULT \n\n")
        # print(llm_result)
        print("\n\n WRITING CLEAN SEGMENTS TO: ", document)
        with open(document, "w") as file1:
            file1.write(llm_result)
        print(f"Saved cleaned up file to: {document}")