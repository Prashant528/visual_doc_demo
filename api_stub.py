from dummy_data import dummy_data

def api_stub(doc_name, actual_doc):
    #The actual API of LLM will process the 'actual_doc' and hopefully give us the data in the format of the dummy data.
    #If the LLM doesn't give us this format, we will have to format the data ourselves by combining the output of different prompts.
    return dummy_data[doc_name]

if __name__=='__main__':
    print(api_stub('CONTRIBUTING.md'))