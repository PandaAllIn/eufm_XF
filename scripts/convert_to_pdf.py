from markdown_pdf import MarkdownPdf, Section
import os

def convert_markdown_to_pdf(markdown_file, pdf_file):
    """Converts a markdown file to a PDF file."""
    try:
        with open(markdown_file, 'r') as f:
            markdown_content = f.read()

        pdf = MarkdownPdf(toc_level=2)
        pdf.add_section(Section(markdown_content, root=os.path.dirname(markdown_file)))
        pdf.save(pdf_file)
        print(f"Successfully converted {markdown_file} to {pdf_file}")

    except Exception as e:
        print(f"Error converting file: {e}")

if __name__ == "__main__":
    # Get the absolute path of the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up two levels to the project root
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    markdown_file = os.path.join(project_root, "eufm", "Stage1_Proposal_Cline_Enhanced.md")
    pdf_file = os.path.join(project_root, "eufm", "Stage1_Proposal_Cline_Enhanced.pdf")
    convert_markdown_to_pdf(markdown_file, pdf_file)