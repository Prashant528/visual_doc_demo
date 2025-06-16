
class Prompts:
    def __init__(self, repo):
        self.repo_name = repo

    SYSTEM_PROMPT = '''
        Act as a helpful assistant.
    '''
    
    USER_PROMPT = '''
        Return a dummy JSON with fields name and address.
    '''

    PROMPT_FOR_SINGLE_FILE = [
        {
            "role": "system", 
            "content": '''You are a helpful assistant. You are knowledgeable on Open Source Communities, 
            onboarding processes and, JavaScript and JSON.'''
        },
        {
            "role": "user", 
            "content": '''I have a markdown document that says how to make contribution to an open source project. 
            You may have to parse the markdown. It consists of action steps that may or may not be organized in a 
            paragraph. Can you please extract the major action steps from the document?'''
        },
        {
            "role": "assistant",
            "content": '''Of course. Do you also want some content of those topics? Do you have any preference on how 
            the content should be generated?'''
        },
        {
            "role": "user",
            "content": '''Yes, thank you for asking. I would like to get the content too. 
            The content should closely resemble whatever information there is inside the document. 
            I would like you to preserve as much information as you can from the document. 
            Please do not add any extra information.'''
        },
        {
            "role": "assistant",
            "content": '''Ok. Do you have any preference on how should I provide you the information that I extract. 
            Do you want it as plain text or in some other formats like JSON?'''
        },
        {
            "role": "user",
            "content": '''Thanks for asking. Actually, I want to create a flowchart of instructions for someone 
            contributing to a that open source project. First of all, analyze the action steps that you generate. 
            The action steps can be related to different sequences like making a contribution or setting up the 
            environment or any other sequence. There can be multiple sequences in the flowchart. 
            For each action step given, you have to find the sequence it belongs to and then serially arrange 
            the action steps in a sequence according to the process that a person would follow to carry out the sequence. 
            I want the final output in a JSON format that gives me a source node and the target node for each edge in the flowchart.
            The format of the JSON should look like { "sequence": "dummy sequence", "edges": 
            [ {"source": "Step 1", "target": "Step 2"}, {"source": "Step 2", "target": "Step 3"} ] }. 
            In summary, group the action steps into distinct sequences and arrange the action steps serially that a 
            person can follow to complete the task in the sequence. If an action step repeats in another sequence, 
            give it a unique key with a number. For example, if the actio step "Making pull requests" appears in another 
            sequence, make it "Making pull requests #2"'''
        },
        {
            "role": "assistant",
            "content": '''Thank you for providing me the format for sequences and action steps. 
            Do you have a preferred format for the content as well?'''
        },
        {
            "role": "user",
            "content": '''After I provide you the document,  provide me another JSON too that maps those exact action 
            steps to their content. The content should sound like instructions for the newcomers on what steps they 
            can take to complete that action step. Each content should contain at least 3 sentences from the document. 
            If there are less than three sentences, merge the action step with other closely related action step and 
            create a new bigger action step. A sample JSON for the summary looks like this { "action step": "content"}. 
            So, your response should contain two JSON objects, 'flow' and 'content' , and nothing else'''
        },
        {
            "role": "assistant",
            "content": '''Ok, I will keep that in mind. Can you please provide me the document? I will make sure that 
            I reply with two JSON objects 'flow' (with the sequences) and 'summary' with the action step contents.'''
        },
    ]

    PROMPT_FOR_SEQUENCING_WITH_SEG_CLASS = [
            {
                "role": "system", 
                "content": '''You are a helpful assistant. You are knowledgeable on Open Source Communities and Projects, 
                onboarding processes and JSON.'''
            },
            {
                "role": "user", 
                "content": '''I have a pythonic list of action steps that belong to making a contribution(<segment_class>) to an open source project.
                I want you to extract the topics from each action step.'''
            },
            {
                "role": "assistant",
                "content": '''Ok. Do you have any preference on how should I provide you the topics and the information. 
                Do you want it as plain text or in some other formats like JSON?'''
            },
            {
                "role": "user",
                "content": '''Thanks for asking. Actually, I want to create a flowchart of instructions for someone 
                contributing to an open source project. First of all, analyze the action steps that you generate. 
                The action steps belong to information related to '<segment_class>' category.
                For each action step given, serially arrange 
                the topics of the action steps in a sequence according to the process that a person would follow in practical scenario. 
                I want the final output in a JSON format that gives me a source node and the target node for each edge in the flowchart.
                The format of the JSON should look like { "edges": 
                [ {"source": "Topic 1", "target": "Topic 2"}, {"source": "Topic 2", "target": "Topic 3"} ] }. 
                In summary, arrange the action steps serially that a 
                person can follow to complete the task in the sequence. If a topic repeats, 
                give it a unique topic."'''
            },
            {
                "role": "assistant",
                "content": '''Thank you for providing me the format for the action steps and the topics. 
                Do you have a preferred format for the content as well?'''
            },
            {
                "role": "user",
                "content": '''In the same response, provide me another JSON too that maps those topics
                to their content. Repeat the same information that is provided to you as content. 
                A sample JSON for the content looks like this { "Topic 1": "content"}. 
                So, your response should contain two JSON objects, 'flow' and 'content'.
                Respond with valid JSON only without any explanation, suitable for direct parsing by a JSON parser. 
                Do not include any text outside the JSON.'''
            },
            {
                "role": "assistant",
                "content": '''Ok, I will keep that in mind. Can you please provide me the list of the action steps?.'''
            },
        ]
    
    PROMPT_FOR_SEQUENCING_VER_2_WITH_SEG_CLASS = [
            {
                "role": "system", 
                "content": '''You are a helpful assistant. You are knowledgeable on Open Source Communities and Projects, onboarding processes and JSON. You do not explain things. You are an API endpoint and just give the JSON response that has been asked for.'''
            },
            {
                "role": "user", 
                "content": '''
                    I have a pythonic list. Each element of the list is supposed to be an action step that belong to making a contribution(submit the changes) to an open source project. I want you to create the following two JSONs from the list:
                    1. JSON name = 'content'. 
                    Description: For each element in the list, I want to map the topic of the element to the content of the element. Extract one topic from the content and keep the content as it is provided . This json would be named 'content' and an example looks like: { 'Topic 1': 'content 1', 'Topic 2': 'content 2', 'Topic 3': 'content 3'}.
                    2. JSON name = 'flow'.
                    Description: For all the elements in the list, I want to find the sequence that a person contributing to that project would follow in a practical scenario. If each element in the list was a node in a graph, I want a JSON that gives me a source node and the target node for each edge in the graph. The format of the JSON should look like { 'edges': [ {'source': 'Topic 1', 'target': 'Topic 2'}, {'source': 'Topic 2', 'target': 'Topic 3'} ] }. Please make sure that the first 'source' node for each flow is always a dummy node named 'Parent Node'.
                    Finally, merge the two JSONs into a single one that looks like: {content: '...', flow:'...'}.

                    '''
            },
            {
                "role": "assistant", 
                "content": '''
                        Certainly, can you provide me the list of the action steps?
                        '''
            }
        ]
    
    PROMPT_FOR_SEQUENCING_VER_MAKE_DISCRETE_TASKS_MERGE_AND_TRIM_WITH_SEG_CLASS = [
            {
                "role": "system", 
                "content": '''You are a helpful assistant. You are knowledgeable on Open Source Communities and Projects, onboarding processes and JSON. You do not explain things. You are an API endpoint and just give the JSON response that has been asked for.'''
            },
            {
                "role": "user", 
                "content": '''
                    I have a Python list, and each element represents a step in contributing to an open source project. Please review the list to ensure each element resembles a valid task in this process. If any elements are unclear, too brief, or need improvement, 
                      feel free to merge elements, remove unnecessary parts, and create a revised list that accurately reflects meaningful contribution steps.
                
                    Second, I want you to create the following two JSONs from the new list:
                    1. JSON name = "content". 
                    Description: For each element in the list, I want to map the topic of the element to the content of the element. Please add markdown syntax to better format the content and also add <br /> for indicating newlines. 
                    Extract one topic from the content. 
                    This json would be named "content" and an example looks like: 
                    { "Topic 1": "content 1", "Topic 2": "content 2", "Topic 3": "content 3"}.
                    2. JSON name = "flow".
                    Description: For all the elements in the list, 
                    I want to find the sequence that a person contributing to that project would follow in a practical scenario. 
                    If each element in the list was a node in a graph, 
                    I want a JSON that gives me a source node and the target node for each edge in the graph. 
                    The format of the JSON should look like { "edges": [ {"source": "Topic 1", "target": "Topic 2"}, {"source": "Topic 2", "target": "Topic 3"} ] }. 
                    Please make sure that the first "source" node for each flow is always a dummy node named "Parent Node".
                    Finally, merge the two JSONs into a single one that looks like: {content: "...", flow:"..."}.
                    This is the list of action steps:

                    '''
            }
        ]
    

    PROMPT_FOR_SEQUENCING_VER_MAKE_DISCRETE_TASKS_MERGE_AND_TRIM_WITH_SEG_CLASS_VER_2 = [
            {
                "role": "system", 
                "content": '''You are a helpful assistant. You are knowledgeable on Open Source Communities and Projects, onboarding processes and JSON. You do not explain things. You are an API endpoint and just give the JSON response that has been asked for.'''
            },
            {
                "role": "user", 
                "content": '''
                    I have a Python list, and each element represents a step in contributing to an open source project. First of all, analyze the elements.If there are elements that are too short, merge them together. Don't break existing elements into shorter ones. Make sure each content has appropriate headers too.
                
                    Second, I want you to create the following two JSONs from the new list:
                    1. JSON name = "content". 
                    Description: For each element in the list, I want to map the topic of the element to the content of the element. Please add markdown syntax to better format the content and also add <br /> for indicating newlines. 
                    Extract one topic from the content. 
                    This json would be named "content" and an example looks like: 
                    { "Topic 1": "content 1", "Topic 2": "content 2", "Topic 3": "content 3"}.
                    2. JSON name = "flow".
                    Description: For all the elements in the list, 
                    I want to find the sequence that a person contributing to that project would follow in a practical scenario. 
                    If each element in the list was a node in a graph, 
                    I want a JSON that gives me a source node and the target node for each edge in the graph. 
                    The format of the JSON should look like { "edges": [ {"source": "Topic 1", "target": "Topic 2"}, {"source": "Topic 2", "target": "Topic 3"} ] }. 
                    Please make sure that the first "source" node for each flow is always a dummy node named "Parent Node".
                    Finally, merge the two JSONs into a single one that looks like: {content: "...", flow:"..."}.
                    This is the list of action steps:

                    '''
            }
        ]
    
    PROMPT_FOR_SEQUENCING_VER_MAKE_DISCRETE_TASKS_MERGE_AND_TRIM_WITH_SEG_WITHOUT_CLASS = [
            {
                "role": "system", 
                "content": '''You are a helpful assistant. You are knowledgeable on Open Source Communities and Projects, onboarding processes and JSON. You do not explain things. You are an API endpoint and just give the JSON response that has been asked for.'''
            },
            {
                "role": "user", 
                "content": '''
                    I have a pythonic list. Each element of the list is supposed to be an action step that belong to making a contribution(submit the changes) to an open source project. 
                    First of all, analyze the elements of the list to make sure that they actually resemble a task while contributing to an open source project. 
                    If they don't make sense or are too short, you can combine multiple elements, trim certain sentences from start or end of the elements and create a new list.
                    '''
            },
            {
                "role": "assistant", 
                "content": ''' Certainly, I have analyzed the list you provided and I have created a new list where each element is a meaningful task
                that can be carried out while making a contribution to open source projects. What should I do next?
                '''
            },
            {
                "role": "user", 
                "content": '''
                    Second, I want you to create the following two JSONs from the new list:
                    1. JSON name = "content". 
                    Description: For each element in the list, I want to map the topic of the element to the content of the element. 
                    Extract one topic from the content. 
                    This json would be named "content" and an example looks like: 
                    { "Topic 1": "content 1", "Topic 2": "content 2", "Topic 3": "content 3"}.
                    2. JSON name = "flow".
                    Description: For all the elements in the list, 
                    I want to find the sequence that a person contributing to that project would follow in a practical scenario. 
                    If each element in the list was a node in a graph, 
                    I want a JSON that gives me a source node and the target node for each edge in the graph. 
                    The format of the JSON should look like { "edges": [ {"source": "Topic 1", "target": "Topic 2"}, {"source": "Topic 2", "target": "Topic 3"} ] }. 
                    Please make sure that the first "source" node for each flow is always a dummy node named "Parent Node".
                    Finally, merge the two JSONs into a single one that looks like: {content: "...", flow:"..."}.

                    '''
            },
            {
                "role": "assistant", 
                "content": '''
                        Certainly, can you provide me the list of the action steps?
                        '''
            }
        ]
    
    PROMPT_FOR_SEQUENCING_VER_MAKE_DISCRETE_TASKS_MERGE_AND_TRIM_WITH_SEG_WITHOUT_CLASS_VER_2 = [
        {
                "role": "system", 
                "content": '''You are a helpful assistant. You are knowledgeable on Open Source Communities and Projects, onboarding processes and JSON. You do not explain things. You are an API endpoint and just give the JSON response that has been asked for.'''
            },
            {
                "role": "user", 
                "content": '''
                    I have a Python list, and each element represents a step in contributing to an open source project. First of all, analyze the elements.If there are elements that are too short, merge them together. Don't break existing elements into shorter ones. Make sure each content has appropriate headers too.
                
                    Then, I want you to create a JSON from the new list:
                    Description: For each element in the list, I want to map the topic of the element to the content of the element. Please add markdown syntax to better format the content and also add <br /> for indicating newlines. 
                    Extract one topic from the content. An example looks like: 
                    { "Topic 1": "content 1", "Topic 2": "content 2", "Topic 3": "content 3"}.
                    This is the list of elements:
                    '''
            }
    ]
    PROMPT_FOR_CLEANING_SEGMENTATION = [
            {
                "role": "system", 
                "content": '''You are a helpful assistant. You are knowledgeable on Open Source Communities and Projects, onboarding processes.'''
            },
            {
                "role": "user", 
                "content": '''
                    I have a document from a Github repository. It contains different sections that highlight a task to be carried out. I have created segments based on tasks, the segment boundaries are denoted by "--------<PREDICTED_SEGMENT_BOUNDARY>--------" . Can you please take a look and check if the segmentation is correct. If not, you can move the boundaries and you can also remove or add additional boundaries if needed. Please denote the new boundaries with the same marker "--------<PREDICTED_SEGMENT_BOUNDARY>--------". The document is given below:\n
                    '''
            }
        ]



    PROMPT_FOR_SEQUENCING_SECOND_LAYER = [
            {
                "role": "system", 
                "content": '''You are a helpful assistant. You are knowledgeable on Open Source Communities and Projects, onboarding processes and JSON. You do not explain things. You are an API endpoint and just give the JSON response that has been asked for.'''
            },
            {
                "role": "user", 
                "content": '''
                    I have a Python list, and each element represents a step in contributing to an open source project. Please review the list to ensure each element resembles a valid task in this process. If any elements are unclear, too brief, or need improvement, 
                      feel free to merge elements, remove unnecessary parts, and create a revised list that accurately reflects meaningful contribution steps.
                
                    Second, I want you to create the following two JSONs from the new list:
                    1. JSON name = "content". 
                    Description: For each element in the list, I want to map the topic of the element to the content of the element. Please add markdown syntax to better format the content and also add <br /> for indicating newlines. 
                    Extract one topic from the content. 
                    This json would be named "content" and an example looks like: 
                    { "Topic 1": "content 1", "Topic 2": "content 2", "Topic 3": "content 3"}.
                    2. JSON name = "flow".
                    Description: For all the elements in the list, 
                    I want to find the sequence that a person contributing to that project would follow in a practical scenario. 
                    If each element in the list was a node in a graph, 
                    I want a JSON that gives me a source node and the target node for each edge in the graph. 
                    The format of the JSON should look like { "edges": [ {"source": "Topic 1", "target": "Topic 2"}, {"source": "Topic 2", "target": "Topic 3"} ] }. 
                    Finally, merge the two JSONs into a single one that looks like: {"content": "...", "flow":"..."}. Please provide a valid JSON output with double quotes around keys and values.
                    If there is only one node, add a single edge with both source and target as the same node.

                    This is the list of action steps:

                    '''
            },
    ]