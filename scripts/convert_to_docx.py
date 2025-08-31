import markdown
from docx import Document
import os

def convert_markdown_to_docx(markdown_file, docx_file):
    """Converts a markdown file to a DOCX file."""
    try:
        with open(markdown_file, 'r') as f:
            markdown_content = f.read()

        html = markdown.markdown(markdown_content)
        
        document = Document()
        document.add_paragraph(html) # This will not be perfectly formatted
        
        document.save(docx_file)
        print(f"Successfully converted {markdown_file} to {docx_file}")

    except Exception as e:
        print(f"Error converting file: {e}")

if __name__ == "__main__":
    # Get the absolute path of the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up two levels to the project root
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    markdown_file = os.path.join(project_root, "eufm", "Stage1_Proposal_Cline_Enhanced.md")
    docx_file = os.path.join(project_root, "eufm", "Stage1_Proposal_Cline_Enhanced.docx")
    convert_markdown_to_docx(markdown_file, docx_file)
