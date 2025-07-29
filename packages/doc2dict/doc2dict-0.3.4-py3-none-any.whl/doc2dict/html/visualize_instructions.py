import webbrowser
import os

def format_dct_style(line):
    text = line['text']
    
    style_properties = []
    # might have issues here in the future
    if 'bold' in line:
        style_properties.append('font-weight: bold')
    if 'italic' in line:
        style_properties.append('font-style: italic')
    if 'underline' in line:
        style_properties.append('text-decoration: underline')
    if 'font-size' in line:
        font_size = line['font-size']
        if font_size:
            style_properties.append(f'font-size: {font_size}')
    if 'left-indent' in line:
        left_indent = line['left-indent']
        if left_indent:
            style_properties.append(f'margin-left: {left_indent}px')

    return style_properties, text

def format_table(table):
    table_html = "<table>"
    for idx, row in enumerate(table):
        table_html += "<tr>"   
        for cell in row:
            if idx == 0:
                table_html += f"<th>{cell['text']}</th>"
            else:
                table_html += f"<td>{cell['text']}</td>"
        table_html += "</tr>"
    
    table_html += "</table>"
    return table_html
            
def visualize_instructions(instructions_list):
    # Simplified color scheme
    single_line_color = '#E8EAF6'    # Light indigo - clean, professional
    multi_first_color = '#DCEDC8'    # Light sage green - clear starting point
    multi_rest_color = '#F9FBE7'     # Very pale yellow-green - subtle continuation

    table_uncleaned_color = '#FFECB3' # Warm amber - intuitive "needs attention"
    table_cleaned_color = '#B2DFDB'   # Teal - fresh and clean feeling

    html_content = """
        <html>
        <head>
        <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        span {
            display: inline-block;
            padding: 5px 8px;
            margin: 3px 0;
            border-radius: 4px;
        }
        
        .table-wrapper {
            text-align: center;
            margin: 15px 0;
        }
        
        .table-container {
            display: inline-block;
            border-radius: 8px;
            padding: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        table {
            border-collapse: collapse;
            margin: 0 auto;
            background-color: white;
        }

        th, td {
            border: 2px solid #ddd;
            padding: 10px;
            text-align: left;
        }

        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        
        </style>
        </head>
        <body>"""
    
    for instructions in instructions_list:
        if len(instructions) == 1:
            if 'table' in instructions[0]:
                table_html = format_table(instructions[0]['table'])
                html_content += "<div class='table-wrapper'>"
                if instructions[0].get('cleaned', False):
                    html_content += f"<div class='table-container' style='background-color: {table_cleaned_color}'>{table_html}</div>"
                else:
                    html_content += f"<div class='table-container' style='background-color: {table_uncleaned_color}'>{table_html}</div>"
                html_content += "</div>"
                continue 
        
        first_instruction = instructions[0]
        is_centered = first_instruction.get('text-center', False)
        div_style = ''

        if is_centered:
            div_style = 'text-align: center;'

        html_content += f"<div style='{div_style}'>"
        for idx, instruction in enumerate(instructions):
            style_properties, text = format_dct_style(instruction)

            if len(instructions) == 1:
                color = single_line_color
            elif idx == 0:
                color = multi_first_color
            else:
                color = multi_rest_color

            style_properties.append(f'background-color: {color}')
            style = '; '.join(style_properties)
            html_content += f"<span style='{style}'>{text}</span>"

        html_content += "</div>"
        
    html_content += """
        </body>
        </html>"""
    
    # Write HTML content to a temporary file
    with open('instructions_visualization.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Get the absolute path of the file
    file_path = os.path.abspath('instructions_visualization.html')
    
    # Open the HTML file in the default web browser
    webbrowser.open('file://' + file_path)