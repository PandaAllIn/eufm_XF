
import schemdraw
import schemdraw.flow as flow
import os

def generate_methodology_flowchart(output_file):
    """Generates the methodology flowchart and saves it to a file."""
    try:
        with schemdraw.Drawing() as d:
            d += flow.Terminal().label("WP2: Design and Synthesis")
            d += flow.Arrow().down()
            d += flow.Box(w=3).label("WP3: Screening and Selection")
            d += flow.Arrow().down()
            d += flow.Box(w=3).label("WP4: Environment Validation")
            d += flow.Arrow().down()
            d += flow.Terminal().label("WP5: Real-World Proof-of-Concept")
            d.draw()
            d.save(output_file)
        print(f"Successfully generated flowchart: {output_file}")
    except Exception as e:
        print(f"Error generating flowchart: {e}")

if __name__ == "__main__":
    # Assuming the script is run from the root of the project
    output_file = os.path.join("eufm", "methodology_flowchart.svg")
    generate_methodology_flowchart(output_file)
