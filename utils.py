import requests

def download_file(owner, repo, file_path):
    # GitHub repository information. Example:
    # owner = 'flutter'
    # repo = 'flutter'
    # file_path = 'CONTRIBUTING.md'

    # Construct the URL to download the raw file
    raw_url = f'https://raw.githubusercontent.com/{owner}/{repo}/main/{file_path}'

    try:
        # Send a GET request to download the file
        response = requests.get(raw_url)
        if response.status_code == 200:
            print("Response code 200")
            response.encoding = 'UTF-8'
            # If the request is successful, return the file as a response
            return(response.content)
        else:
            return f"Failed to download file: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
def segregate_segments_by_classes(segments_and_classes_in_all_files):
    print("Started segregating segments ...")
    #Find all distinct classes in the files
    all_classes =[]
    for segments_and_classes_in_each_file in segments_and_classes_in_all_files:
        classes_in_that_file = segments_and_classes_in_each_file[1]
        print(f"Classes in that file = ", classes_in_that_file)
        all_classes = all_classes + classes_in_that_file
    all_classes = set(all_classes)
    print(f"All distinct classes found =  {all_classes}")
    #For each segment class, initialize a list to hold the segments.
    class_segments_holder = {}
    for each_class in all_classes:
        class_segments_holder[each_class] = []

    #For each segment, add it to correct class in the dictionary
    for segments_and_classes_in_each_file in segments_and_classes_in_all_files:
        segments = segments_and_classes_in_each_file[0]
        segment_classes = segments_and_classes_in_each_file[1]
        for segment, segment_class in zip(segments, segment_classes):
            class_segments_holder[segment_class].append(segment)
    print("Completed segregating segments ...")
    return class_segments_holder

if __name__ == '__main__':
    print(download_file('flutter', 'flutter', 'CONTRIBUTING.md'))
