import openai
from code_from_visdoc.prompts_store import Prompts 
from code_from_visdoc.utils import parse_openai_single_json

class OpenAIService:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.prompts = Prompts()
        self.model = "gpt-4o"

    def process_documents(self, documents):
        # prompt = self.build_prompt(system_prompt, user_prompt, documents)
        prompt = self.fetch_prompt('PROMPT_FOR_SINGLE_FILE')
        full_prompt = self.add_single_doc_to_prompt(prompt, documents)
        # print(full_prompt)
        response = self.get_llm_response(full_prompt)
        return response
    
    def get_llm_response(self, prompt):
        print("Started: Calling LLM API...")
        response = openai.chat.completions.create(
            model=self.model,
            messages = prompt,
            temperature = 0.0
        )
        # print(response.choices[0].message.content)
        print("Completed: Calling LLM API...")
        return response.choices[0].message.content

    def add_single_doc_to_prompt(self, prompt, doc):
        prompt_doc = {"role": "user", "content": doc }
        prompt.append(prompt_doc)
        return prompt

    def add_segments_to_prompt(self, prompt, segments):
        prompt_with_segments = {"role": "user", "content": f"{segments}" }
        prompt.append(prompt_with_segments)
        return prompt

    def build_prompt(self, system_prompt, user_prompt, documents):
        # Combine user and system prompts with the document content
        doc_content = "\n".join(documents)
        return f"{user_prompt}\n\nDocuments:\n{doc_content}"

    def fetch_prompt(self, prompt_name):
        return getattr(self.prompts, prompt_name)
    
    def get_prompt_for_segmentclass(self, segment_class_name):
        print(f"Started: Creating prompt for LLM for segment_class <{segment_class_name}>")
        target_string = '<segment_class>'
        prompt_for_sequencing = self.fetch_prompt('PROMPT_FOR_SEQUENCING')
        #replace some dummy strings by the actual class name in the prompt
        updated_prompt = [
            {
                "role": item["role"],
                "content": item["content"].replace(target_string, segment_class_name),
            }
            for item in prompt_for_sequencing
        ]
        print(f"Completed: Creating prompt for LLM for segment_class <{segment_class_name}>")
        return updated_prompt
    
    def find_sequences_for_allsegments(self, segregated_segments):
        print(f"Started finding sequences...")
        flow_and_contents ={}
        for segment_class, all_segments in segregated_segments.items():
            print(f"{segment_class}: {all_segments}")
            segment_prompt = self.get_prompt_for_segmentclass(segment_class)
            full_prompt_with_segments = self.add_segments_to_prompt(segment_prompt, all_segments)
            # print(full_prompt_with_segments)
            llm_result = parse_openai_single_json(self.get_llm_response(full_prompt_with_segments))
            flow_and_contents[segment_class] = llm_result
        print(f"Completed finding sequences...")
        return flow_and_contents