import re
import pkg_resources

version = pkg_resources.get_distribution("doc2dict").version



# AI GENERATED CODE BC I WANT TO PUSH TO PROD #
def determine_predicted_header_levels(levels):
    """
    Assigns hierarchy levels to predicted headers based on their attributes,
    maintaining consistency within each section defined by known headers.
    
    Args:
        levels: List of dictionaries containing level, class, and attributes
        
    Returns:
        List of tuples in the format (level, class)
    """
    # Find the base level for predicted headers
    predicted_headers = [l for l in levels if l['class'] == 'predicted header']
    if not predicted_headers:
        return [(level['level'], level['class']) for level in levels]
    
    base_level = min(h['level'] for h in predicted_headers)
    
    # Create a copy of levels that we'll modify
    updated_levels = levels.copy()
    
    # Track the last known header level
    current_section_level = -1
    
    # Dictionary to map attribute combinations to levels within the current section
    # Format: {attribute_key: assigned_level}
    attr_level_map = {}
    
    # Helper function to create a key from attributes dictionary
    def attr_to_key(attrs):
        if not attrs:
            return "no_attributes"
        # Sort keys to ensure consistent mapping regardless of order
        return "_".join(sorted([k for k, v in attrs.items() if v]))
    
    # Process each item
    for i, item in enumerate(updated_levels):
        # When we hit a known header, reset our attribute mapping
        if item['class'] != 'predicted header' and item['class'] not in ['text', 'textsmall']:
            if item['level'] <= current_section_level:
                # We've entered a new section at same or higher level, reset mappings
                attr_level_map = {}
            current_section_level = item['level']
            continue
        
        # Skip non-header items
        if item['class'] != 'predicted header':
            continue
        
        # Create a key for this item's attributes
        attr_key = attr_to_key(item.get('attributes', {}))
        
        # If we haven't seen this attribute combination in this section,
        # assign it the next available level
        if attr_key not in attr_level_map:
            attr_level_map[attr_key] = base_level + len(attr_level_map)
        
        # Assign the level based on the mapping
        item['level'] = attr_level_map[attr_key]
    
    # Return in the required format
    return [(level['level'], level['class'], level.get('standardized_title','')) for level in updated_levels]
# AI GENERATED CODE BC I WANT TO PUSH TO PROD #

def determine_levels(instructions_list, mapping_dict=None):
    if mapping_dict is None:
        predicted_header_level = 0
    #TODO bandaid fix
    elif 'rules' in mapping_dict:
        predicted_header_level = 0
    else:
        predicted_header_level = max(mapping_dict.values()) + 1

    # filter out tables
    headers = [instructions[0] if 'text' in instructions[0] else {} for instructions in instructions_list]
    likely_header_attributes = ['bold','italic','underline','text-center','all_caps','fake_table']
    # identify likely text nodes, return {} if not
    headers = [item if any([item.get(attr, False) for attr in likely_header_attributes]) else {} for item in headers]
    # count font-size
    small_script = [False] * len(headers)
    font_size_counts = {size: sum(1 for item in [instr[0] for instr in instructions_list if 'text' in instr[0]] if item.get('font-size') == size) for size in set(item.get('font-size') for item in [instr[0] for instr in instructions_list if 'text' in instr[0]] if item.get('font-size') is not None)}
    
    # use only font size goes here
    if mapping_dict is not None:
        if 'rules' in mapping_dict:
            if 'use_font_size_only_for_level' in mapping_dict['rules']:
                most_common_font_size, font_count = max(font_size_counts.items(), key=lambda x: x[1])
                
                # Get all unique font sizes and sort them in descending order (largest first)
                unique_font_sizes = sorted(font_size_counts.keys(), reverse=True)
                
                # Create a mapping from font size to level (largest font = level 0, next = level 1, etc.)
                font_size_to_level = {size: idx for idx, size in enumerate(unique_font_sizes)}
                
                levels = []
                for idx, header in enumerate(headers):
                    if 'text' in header and header.get('font-size') is not None:
                        font_size = header.get('font-size')
                        
                        if font_size < most_common_font_size:
                            # Assign small script for fonts smaller than most common
                            level = (-2,'textsmall','')
                        else:
                            # Assign level based on font size hierarchy
                            hierarchy_level = font_size_to_level[font_size]
                            level = (hierarchy_level, 'predicted header','')
                    else:
                        # No font size information, treat as regular text
                        level = (-1, 'text','')
                    
                    levels.append(level)
                
                return levels
    
    if font_size_counts != {}:
        most_common_font_size, font_count = max(font_size_counts.items(), key=lambda x: x[1])
        if font_count > (.5 * len(instructions_list)):
            # assume anything with less than this font size is small script
            small_script = [True if item.get('font-size') is not None and item.get('font-size') < most_common_font_size else False for item in headers]
            



    levels = []
    for idx,header in enumerate(headers):
        level = None
        attributes = {attr: header.get(attr, False) for attr in likely_header_attributes if attr in header}
        
        if small_script[idx]:
            level = {'level': -2, 'class': 'textsmall'}
        elif 'text' in header:
            if mapping_dict is not None:
                text = header['text'].lower()
                regex_tuples = [(item[0][1], item[0][0], item[1]) for item in mapping_dict.items()]
                
                for regex, header_class, hierarchy_level in regex_tuples:
                    match = re.match(regex, text)
                    if match:
                        # create a dictionary of attributes from likely_header_attributes
                        match_groups = match.groups()
                        if len(match_groups) > 0:
                            string = ''.join([str(x) for x in match_groups if x is not None])
                            standardized_title = f'{header_class}{string}'
                        else:
                            standardized_title = f'{header_class}'
                        level = {'level': hierarchy_level, 'class': header_class, ' ': attributes,'standardized_title': standardized_title}
                        break
            
            if level is None:
                # probably modify this to use attributes
                if any([header.get(attr,False) for attr in likely_header_attributes]):
                    level = {'level': predicted_header_level, 'class': 'predicted header', 'attributes': attributes}

        if level is None:
            level = {'level': -1, 'class': 'text'}
            levels.append(level)
        else:
            levels.append(level)

    # NOW USE SEQUENCE AND ATTRIBUTES IN THE LEVELS TO DETERMINE HIERARCHY FOR PREDICTED HEADERS
    levels = determine_predicted_header_levels(levels)
    return levels

# prob here we want to find the attributes first (fast)
# then try for the regex.
def convert_instructions_to_dict(instructions_list, mapping_dict=None):
    # Get pre-calculated levels for each instruction
    levels = determine_levels(instructions_list, mapping_dict)
    
    # Initialize document structure
    document = {'contents': {}}
    
    # Create an introduction section
    introduction = {'title': 'introduction', 'class': 'introduction', 'contents': {}}
    
    # Add the introduction to the document
    document['contents'][-1] = introduction
    
    # Keep track of current position in hierarchy
    current_section = introduction
    current_path = [document, introduction]  # Path from root to current section
    current_levels = [-1, 0]  # Corresponding hierarchy levels
    
    # Process each instruction using pre-calculated levels
    for idx, instructions in enumerate(instructions_list):
        instruction = instructions[0]
        level,level_class,standardized_title = levels[idx]

        if level >= 0:
            # This is a section header
            
            # Pop hierarchy until finding appropriate parent
            while len(current_levels) > 1 and current_levels[-1] >= level:
                current_path.pop()
                current_levels.pop()
            
            # Extract title and determine class from the instruction
            title = instruction['text']
            
            # Create new section
            new_section = {'title': title, 'standardized_title':standardized_title, 'class': level_class, 'contents': {}}
            
            # Add section to parent's contents with index as key
            parent = current_path[-1]
            parent['contents'][idx] = new_section
            
            # Update tracking
            current_path.append(new_section)
            current_levels.append(level)
            current_section = new_section

        # add instructions where first is header, but rest are not. on same line
        if level >= 0 and len(instructions) > 1:
            for instruction in instructions[1:]:
                if 'text' in instruction:
                    if not current_section['contents'].get(idx):
                        current_section['contents'][idx] = {level_class:''}
                    current_section['contents'][idx][level_class] += instruction['text']
                elif 'table' in instruction:
                    # note: tables should only appear in length one instructions, so should be safe
                    current_section['contents'][idx] = {'table':[[cell["text"] for cell in row] for row in instruction['table']]}

        if level in [-1, -2]:
            for instruction in instructions:
                if 'text' in instruction:
                    if not current_section['contents'].get(idx):
                        current_section['contents'][idx] = {level_class:''}
                    current_section['contents'][idx][level_class] += instruction['text']
                elif 'table' in instruction:
                    current_section['contents'][idx] = {'table':[[cell["text"] for cell in row] for row in instruction['table']]}

    
    # Create final result with metadata
    result = {
        'metadata': {
            'parser': 'doc2dict',
            'github': 'https://github.com/john-friedman/doc2dict',
            'version': version
        },
        'document': document['contents']
    }
    
    return result
