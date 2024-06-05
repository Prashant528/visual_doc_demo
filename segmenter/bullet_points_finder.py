import re

def offset_ending_index(bullet_point_indices, offset):
    '''
    Increase the ending index to "offset" value to include the sentence/s that follow the last index.
    '''    
    new_indices = [(i, j+offset) for i,j in bullet_point_indices]
    return new_indices

def find_start_and_end(file_path):
    start_line = None
    end_line = None

    # Regular expression pattern to match lines starting with a number followed by a period
    pattern = re.compile(r'^\d+\.\s')

    #a 2D list to hold the start and ending index of each bullet point.
    bullet_points_indices = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        prev_number = 0
        for i, line in enumerate(lines):
            if pattern.match(line):
                print("Pattern match found")
                if start_line is None:
                    start_line = i
                    print("start line = ", start_line)
                new_number = int(line[0])
                print(f"New number = {new_number}")
                #keep on updating end_line number until it is increasing
                if new_number == prev_number+1:
                    end_line = i
                    print(f"End line = {end_line}")
                    prev_number = new_number
                #if new bullet points start, reset prev_number to the 0.
                else:
                    bullet_points_indices.append((start_line, end_line))
                    print(f"---------New bullet point starts----------")
                    print("Trying to find new bullet points...")
                    start_line = i
                    prev_number = 1
        #the last match doesn't end in "else" block, so we do this. If no matches were found, it would have None, None.
        bullet_points_indices.append((start_line, end_line))
        
                

    if start_line is not None and end_line is not None:
        new_indices = offset_ending_index(bullet_points_indices, 1)
        return new_indices
    else:
        return None

# Example usage
file_path = 'static/segmenter_outputs/flutter_segmented_file.txt'
idxs = find_start_and_end(file_path)
print(idxs)

# start_idx, end_idx, start, end = find_start_and_end(file_path)
# print("Starting line index:", start_idx)
# print("Ending line index:", end_idx)
# print("Start of list:", start)
# print("End of list:", end)
