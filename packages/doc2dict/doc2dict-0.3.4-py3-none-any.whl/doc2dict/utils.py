import re

def get_title(dct, title, title_class=None):
    results = []
    title_pattern = re.compile(title, re.IGNORECASE)
    title_class = title_class.lower() if title_class else None
    
    def search(node, parent_id=None):
        if isinstance(node, dict):
            node_title = node.get('title', '')
            node_class = node.get('class', '').lower()
            node_standardized_title = node.get('standardized_title', '')
            
            if (title_pattern.match(node_title) or title_pattern.match(node_standardized_title)) and (title_class is None or node_class == title_class):
                results.append((parent_id, node))
                
            contents = node.get('contents', {})
            for key, value in contents.items():
                search(value, key)
    
    if 'document' in dct:
        for doc_id, doc_node in dct['document'].items():
            search(doc_node, doc_id)
                
    return results

def unnest_dict(dct):
    result = []
    
    def process_content(content):
        if not isinstance(content, dict):
            return
            
        # Process title, text, and textsmall directly
        for key in ['title', 'text', 'textsmall']:
            if key in content:
                result.append(str(content[key]))
        
        # Process table specially
        if 'table' in content:
            table_data = content['table']
            for row in table_data:
                result.append(' '.join(str(cell) for cell in row))
        
        # Process contents recursively in numeric order
        contents = content.get('contents', {})
        if contents:
            # Sort keys numerically if possible
            keys = sorted(contents.keys(), key=lambda x: int(x) if str(x).isdigit() else x)
            for key in keys:
                process_content(contents[key])
    
    # Start processing from document
    if 'document' in dct:
        document = dct['document']
        # Sort document keys numerically if possible
        doc_keys = sorted(document.keys(), key=lambda x: int(x) if str(x).lstrip('-').isdigit() else x)
        for key in doc_keys:
            process_content(document[key])
    else:
        # If no document key, process the entire dictionary
        process_content(dct)
    
    return '\n'.join(result)