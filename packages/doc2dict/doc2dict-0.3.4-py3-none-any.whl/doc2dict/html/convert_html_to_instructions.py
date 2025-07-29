# TO ADD
# merge same line
# merge across lines
# look at old before deletion
# left indent

from copy import deepcopy

# params 
tag_groups = {
"bold": ["b", "strong"],
"italic": ["i", "em"],
"underline": ["u", "ins"],
}

# utils
def walk(node):
    yield ("start",node)
    for child in node.iter(include_text=True):
        yield from walk(child)

    yield ("end",node)

def check_text_style(text):
    # Check if the text is all caps
    if text.isupper():
        return True
    return False


def style_to_dict(style_string):
    result = {}
    if not style_string:
        return result
    # send to lower case
    style_string = style_string.lower()
    style_list = [attr.strip() for attr in style_string.split(';') if attr.strip()]

    for item in style_list:
        if ':' in item:
            key, value = item.split(':', 1)
            result[key.strip()] = value.strip()
    return result

def get_style(node):
    increments = []
    stacks = []
    style = node.attributes.get('style', '')
    style_dict = style_to_dict(style)
    if 'font-weight' in style_dict:
        if style_dict['font-weight'] == 'bold':
            increments.append('bold')
        elif style_dict['font-weight'] == '700':
            increments.append('bold')

    if 'font-style' in style_dict:
        if style_dict['font-style'] == 'italic':
            increments.append('italic')
    
    if 'text-decoration' in style_dict:
        if style_dict['text-decoration'] == 'underline':
            increments.append('underline')    

    if 'text-align' in style_dict:
        if style_dict['text-align'] == 'center':
            increments.append('text-center')

        
    left_indent = 0

    if 'font-size' in style_dict:
        font_size = style_dict['font-size']
        font_size = normalize_to_px(font_size)
        stacks.append({'font-size': font_size})
    
    if 'text-indent' in style_dict:
        indent = style_dict['text-indent']
        indent = normalize_to_px(indent)
        left_indent += indent

    if 'padding' in style_dict:
        padding_value = style_dict['padding']
        # Handle four-value format: top right bottom left
        if padding_value.count(' ') == 3:
            _, _, _, left = padding_value.split(' ')
            left = normalize_to_px(left)
            left_indent += left
        # Handle three-value format: top right/left bottom
        elif padding_value.count(' ') == 2:
            _, right_left, _ = padding_value.split(' ')
            right_left = normalize_to_px(right_left)
            left_indent += right_left
        # Handle two-value format: top/bottom right/left
        elif padding_value.count(' ') == 1:
            _, right_left = padding_value.split(' ')
            right_left = normalize_to_px(right_left)
            left_indent += right_left
        # Handle single-value format: all sides
        else:
            padding_value = normalize_to_px(padding_value)
            left_indent += padding_value

    # Also handle direct padding-left if specified
    if 'padding-left' in style_dict:
        padding_left = style_dict['padding-left']
        padding_left = normalize_to_px(padding_left)
        left_indent += padding_left

    # Handle margin with the same logic as padding
    if 'margin' in style_dict:
        margin_value = style_dict['margin']
        # Handle four-value format: top right bottom left
        if margin_value.count(' ') == 3:
            _, _, _, left = margin_value.split(' ')
            left = normalize_to_px(left)
            left_indent += left
        # Handle three-value format: top right/left bottom
        elif margin_value.count(' ') == 2:
            _, right_left, _ = margin_value.split(' ')
            right_left = normalize_to_px(right_left)
            left_indent += right_left
        # Handle two-value format: top/bottom right/left
        elif margin_value.count(' ') == 1:
            _, right_left = margin_value.split(' ')
            right_left = normalize_to_px(right_left)
            left_indent += right_left
        # Handle single-value format: all sides
        else:
            margin_value = normalize_to_px(margin_value)
            left_indent += margin_value

    # Handle direct margin-left if specified
    if 'margin-left' in style_dict:
        margin_left = style_dict['margin-left']
        margin_left = normalize_to_px(margin_left)
        left_indent += margin_left

    if 'display' in style_dict:
        if style_dict['display'] == 'none':
            increments.append('display-none')

    if left_indent != 0:
        stacks.append({'left-indent': left_indent})    
    return increments, stacks

def parse_css_value(value_str):
    """Extract numeric value and unit from CSS value string"""
    if not value_str or not isinstance(value_str, str):
        return 0, 'px'
    
    value_str = value_str.strip()
    
    # Handle non-numeric values
    if value_str in ['auto', 'inherit', 'initial']:
        return 0, value_str
    
    # Find where the number ends
    numeric_part = ''
    for i, char in enumerate(value_str):
        if char.isdigit() or char == '.':
            numeric_part += char
        elif char == '-' and i == 0:  # Handle negative values
            numeric_part += char
        else:
            unit = value_str[i:].strip()
            break
    else:
        unit = 'px'  # Default if no unit specified
    
    # Convert numeric part to float
    try:
        value = float(numeric_part) if numeric_part else 0
    except ValueError:
        value = 0
    
    return value, unit


def normalize_to_px(value_str, font_context=None):
    """Convert any CSS measurement to pixels based on context"""
    if not value_str:
        return 0
    
    # Parse the value
    value, unit = parse_css_value(value_str)
    
    # Early return for non-numeric values
    if unit in ['auto', 'inherit', 'initial']:
        return 0
    
    # Get font context in pixels
    current_font_size = 16  # Default
    if font_context:
        font_value, font_unit = parse_css_value(font_context)
        if font_unit == 'px':
            current_font_size = font_value
        elif font_unit == 'pt':
            current_font_size = font_value * 1.333
        else:
            # For simplicity, treat all other units as approximately 16px
            current_font_size = font_value * 16 if font_value else 16
    
    # Convert to pixels
    if unit == 'px':
        return value
    elif unit == 'pt':
        return value * 1.333
    elif unit == 'em':
        return value * current_font_size
    elif unit == 'rem':
        return value * 16  # Root em always based on root font size
    elif unit == '%':
        return value * current_font_size / 100  # % of font size
    elif unit == 'ex':
        return value * current_font_size / 2  # Roughly half the font size
    elif unit == 'ch':
        return value * current_font_size * 0.5  # Approximate character width
    elif unit in ['vh', 'vw', 'vmin', 'vmax']:
        return value  # Cannot accurately convert viewport units without screen size
    elif unit == 'cm':
        return value * 37.8  # Approximate for screen (96dpi)
    elif unit == 'mm':
        return value * 3.78  # 1/10th of cm
    elif unit == 'in':
        return value * 96  # Standard 96dpi
    elif unit == 'pc':
        return value * 16  # 1pc = 12pt
    else:
        return value  # Unknown unit, return as is

def safe_increment(dct,key):
    if key not in dct:
        dct[key] = 0

    dct[key] += 1

def safe_decrement(dct,key):
    if key not in dct:
        dct[key] = 0

    dct[key] -= 1
    if dct[key] < 0:
        dct[key] = 0

def safe_stack(dct,key,val):
    if key not in dct:
        dct[key] = []

    dct[key].append(val)

def safe_unstack(dct,key):
    if key not in dct:
        dct[key] = []

    if len(dct[key]) > 0:
        dct[key].pop()
    else:
        dct[key] = []

def parse_start_style(current_attributes,node):
    increments, stacks = get_style(node)
    if 'display-none' in increments:
        return 'skip'

    for key in increments:
        safe_increment(current_attributes,key)

    for stack in stacks:
        for key in stack:
            safe_stack(current_attributes,key,stack[key])

    return ''
def parse_end_style(current_attributes,node):
    increments,stacks = get_style(node)
    if 'display-none' in increments:
        return 'skip'
    
    for key in increments:
        safe_decrement(current_attributes,key)

    for stack in stacks:
        for key in stack:
            safe_unstack(current_attributes,key)

    return ''

def parse_start_tag(current_attributes,node):
    tag = node.tag

    if tag == 'table':
        return 'table'
    elif tag == '-text':
        return 'text'

    for tag in tag_groups:
        if node.tag in tag_groups[tag]:
            safe_increment(current_attributes,tag)
            return ''
        
def parse_end_tag(current_attributes,node):
    tag = node.tag

    if tag == 'table':
        return 'table'
    elif tag in ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li','br']:
        return 'newline'

    for tag in tag_groups:
        if node.tag in tag_groups[tag]:
            safe_decrement(current_attributes,tag)
            return ''

# USED AI BC LAZY #
def merge_instructions(instructions):
    if not instructions or len(instructions) <= 1:
        return instructions
    
    result = [instructions[0]]
    
    for i in range(1, len(instructions)):
        current = instructions[i]
        prev = result[-1]
        
        # Case 1: Empty string after strip
        if current.get('text', '').strip() == '':
            prev['text'] += current.get('text', '')
            continue
        
        # Case 2: Attributes match with previous
        attrs_to_check = ['bold', 'text-center', 'italic', 'underline', 'font-size']
        attrs_match = all(current.get(attr) == prev.get(attr) for attr in attrs_to_check)
        
        if attrs_match:
            prev['text'] += current.get('text', '')
            continue
        
        # Case 3: Check if attributes match with any earlier instruction
        # This handles the case where instructions a and c match but b doesn't
        merged = False
        for j in range(len(result) - 1, -1, -1):  # Check all previous instructions
            earlier = result[j]
            if all(current.get(attr) == earlier.get(attr) for attr in attrs_to_check):
                # Combine all instructions from j to the current one
                combined_text = earlier['text']
                for k in range(j + 1, len(result)):
                    combined_text += result[k].get('text', '')
                combined_text += current.get('text', '')
                
                earlier['text'] = combined_text
                # Remove the instructions that were merged
                result = result[:j+1]
                merged = True
                break
        
        if not merged:
            result.append(current)
    
    return result
# USED AI BC LAZY #

def is_subset(items1, items2, empty_chars):
    """returns true if items1 is a subset of items2"""
    return all(item1['text'] in empty_chars or item1['text'] == item2['text'] for item1, item2 in zip(items1, items2))

def remove_subset_rows(table, empty_chars, direction="bottom_to_top"):
    """
    Remove subset rows from the table.
    direction: "bottom_to_top" or "top_to_bottom"
    """
    if not table:
        return table
    
    keep_rows = [True] * len(table)
    
    if direction == "bottom_to_top":
        # Compare each row with the row above it
        for i in range(len(table)-1, 0, -1):
            if is_subset(table[i], table[i-1], empty_chars):
                keep_rows[i] = False
    else:  # top_to_bottom
        # Compare each row with the row below it
        for i in range(len(table)-1):
            if is_subset(table[i], table[i+1], empty_chars):
                keep_rows[i] = False
    
    return [table[i] for i in range(len(table)) if keep_rows[i]]

def remove_subset_columns(table, empty_chars, direction="left_to_right"):
    """
    Remove subset columns from the table.
    direction: "left_to_right" or "right_to_left"
    """
    if not table or not table[0]:
        return table
    
    num_cols = len(table[0])
    keep_cols = [True] * num_cols
    
    if direction == "left_to_right":
        # Compare each column with the column to its right
        for j in range(num_cols-1):
            col1 = [row[j] for row in table]
            col2 = [row[j+1] for row in table]
            if is_subset(col1, col2, empty_chars):
                keep_cols[j] = False
    else:  # right_to_left
        # Compare each column with the column to its left
        for j in range(num_cols-1, 0, -1):
            col1 = [row[j] for row in table]
            col2 = [row[j-1] for row in table]
            if is_subset(col1, col2, empty_chars):
                keep_cols[j] = False
    
    return [[row[j] for j in range(num_cols) if keep_cols[j]] for row in table]

def clean_table(table):
    if len(table) == 0:
        return table, False
    
    # First check if table has same number of columns
    same_length = all([len(row) == len(table[0]) for row in table])
    if not same_length:
        return table, False
    
    empty_chars = ['', ')', '(', '$', '–', '-','%']
    
    # Remove empty rows
    table = [row for row in table if any(cell['text'] not in empty_chars for cell in row)]
    
    # Remove empty columns
    if table and table[0]:
        keep_cols = [j for j in range(len(table[0])) if any(table[i][j]['text'] not in empty_chars for i in range(len(table)))]
        table = [[row[j] for j in keep_cols] for row in table]
    
    # Remove subset rows in both directions
    table = remove_subset_rows(table, empty_chars, "bottom_to_top")
    table = remove_subset_rows(table, empty_chars, "top_to_bottom")
    
    # Remove subset columns in both directions
    table = remove_subset_columns(table, empty_chars, "left_to_right")
    table = remove_subset_columns(table, empty_chars, "right_to_left")
    
    return table, True

# TODO, not sure how it handles ragged tables... e.g. td are not same length in rows
def convert_html_to_instructions(root):
    skip_node = False
    in_table = False

    instructions_list = []
    instructions = []
    current_attributes = {}

    # Dictionary-based approach for table cells
    table_cells = {}
    max_row = -1
    max_col = -1
    occupied_positions = set()
    current_cell = {'text': ''}

    # table
    row_id = 0
    col_id = 0
    rowspan = 1
    colspan = 1

    for signal, node in walk(root):
        if signal == "start":
            # skip invisible elements
            if skip_node:
                continue
            elif in_table:
                if node.tag == 'tr':
                    pass
                elif node.tag in ['td', 'th']:
                    colspan = int(node.attributes.get('colspan', 1))
                    rowspan = int(node.attributes.get('rowspan', 1))
                elif node.tag == '-text':
                    current_cell['text'] += node.text_content
                continue
            
            style_command = parse_start_style(current_attributes, node)
            if style_command == 'skip':
                skip_node = True
                continue

            tag_command = parse_start_tag(current_attributes, node)
            if tag_command == 'table':
                in_table = True
                # Reset table variables
                table_cells = {}
                max_row = -1
                max_col = -1
                occupied_positions = set()
                row_id = 0
                col_id = 0
                if len(instructions) > 0:
                    instructions_list.append(instructions)
                    instructions = []
                continue
            elif tag_command == 'text':
                text = node.text_content

                # check not leading whitespace
                if len(instructions) == 0:
                    text = text.lstrip()
                    if len(text) == 0:
                        continue
            
                instruction = {'text': text}

                if check_text_style(text):
                    instruction['text-style'] = 'all_caps'

                for key in current_attributes:
                    val = current_attributes[key]
                    if isinstance(val, list):
                        if len(val) > 0:
                            instruction[key] = val[-1]
                    elif isinstance(val, int):
                        if val > 0:
                            instruction[key] = True

                instructions.append(instruction)

        elif signal == "end":
            style_command = parse_end_style(current_attributes, node)
            if style_command == 'skip':
                skip_node = False
                continue

            tag_command = parse_end_tag(current_attributes, node)
            if tag_command == 'table':
                # Create a properly sized matrix from the collected data
                if max_row >= 0 and max_col >= 0:  # Only if we have cells
                    matrix = [[{'text': ''} for _ in range(max_col + 1)] for _ in range(max_row + 1)]
                    
                    # Fill in the cells
                    for (r, c), cell_data in table_cells.items():
                        matrix[r][c] = cell_data
                    
                    # clean the matrix
                    matrix,is_cleaned = clean_table(matrix)
                    if len(matrix) == 1:
                        matrix_text = ' '.join([cell['text'] for cell in matrix[0]])
                        instructions_list.append([{'text': matrix_text, 'fake_table': True}])
                    else:
                        instructions_list.append([{'table': matrix,'cleaned': is_cleaned}])

                
                # Reset table state
                table_cells = {}
                occupied_positions = set()
                current_cell = {'text': ''}
                in_table = False
                continue
            elif in_table:
                if node.tag in ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'br']:
                    current_cell['text'] += '\n'
                elif node.tag == 'tr':
                    row_id += 1
                    col_id = 0
                elif node.tag in ['td', 'th']:
                    text = current_cell['text'].strip()
                    
                    # Find next available position if current is occupied
                    while (row_id, col_id) in occupied_positions:
                        col_id += 1
                    
                    # Create cell data with the text content
                    cell_data = {'text': text}
                    
                    # Store the cell_data at EVERY position this cell occupies
                    for y in range(rowspan):
                        for x in range(colspan):
                            # Store cell data at this position
                            table_cells[(row_id + y, col_id + x)] = cell_data
                            # Mark position as occupied
                            occupied_positions.add((row_id + y, col_id + x))
                    
                    # Update maximum dimensions
                    max_row = max(max_row, row_id + rowspan - 1)
                    max_col = max(max_col, col_id + colspan - 1)
                    
                    # Move to next position
                    col_id += colspan
                    current_cell = {'text': ''}

            elif tag_command == 'newline':
                if len(instructions) > 0:
                    instructions = merge_instructions(instructions)
                    if len(instructions) == 1:
                        # strip text
                        instructions[0]['text'] = instructions[0]['text'].strip()
                    instructions_list.append(instructions)
                    instructions = []
                continue

    # add any remaining instructions
    if instructions:
        if len(instructions) > 0:
            if len(instructions) == 1:
                # strip text
                instructions[0]['text'] = instructions[0]['text'].strip()
            instructions_list.append(instructions)
    return instructions_list