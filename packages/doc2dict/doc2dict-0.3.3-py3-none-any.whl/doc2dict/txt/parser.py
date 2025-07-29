from doc2dict.mapping import DocumentProcessor

def txt2dict(content,mapping_dict):
    # Split by double newlines to get paragraphs
    paragraphs = content.split('\n\n')
    
    # Process each paragraph
    lines = []
    for paragraph in paragraphs:
        if paragraph.strip():  # Skip empty paragraphs
            processed = paragraph.strip()
            processed = processed.split('\n')
            # Add double newlines at start of each paragraph
            processed[0] = '\n\n' + processed[0]
            # Add single newline to other lines
            processed[1:] = ['\n' + line for line in processed[1:]]
            lines.extend(processed)
            
    processor = DocumentProcessor(mapping_dict)
    result = processor.process(lines)
    return result