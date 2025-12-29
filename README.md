# Radius Star Research (Neutron Star Analysis Tool)

Interactive Python tool for exploring neutron star properties through scientific computation and visualization. Users can input parameters, import datasets, and generate plots of key quantities such as pressure, mass, and energy density.

## Demo
<img width="1500" height="500" alt="image" src="https://github.com/user-attachments/assets/ecf9cb59-57f8-40f9-addf-069e5026d427" />

## Features
- Interactive parameter input and graph generation
- Plots: pressure, mass, energy density (as implemented in the project)
- Data import support for external files
- Input validation and error handling
- UI focused on usability for research workflows

## Tech Stack
- Python
- NumPy, SciPy, Matplotlib
- Tkinter (desktop UI)
- Flask (if used for local serving or integration)
- HTML (UI enhancements, if applicable)

## Installation
```bash
git clone https://github.com/ai-ai/Radius_Star_Research.git
cd Radius_Star_Research

python -m venv env
source env/bin/activate   # macOS/Linux
# env\Scripts\activate    # Windows

pip install -r requirements.txt
Run
bash
Copy code
python app.py
Usage
Enter neutron star parameters in the input fields.

Generate graphs to explore pressure, mass, and energy density behavior.

Import external data files for expanded analysis (if supported by your current build).

Use the UI to iterate quickly on scenarios and visualize results.

Project Context
This project was built with guidance from academic resources (papers provided by a professor) and presented at a university Research Symposium, with positive feedback on usability and execution.

Roadmap
Real-time plot updates while editing parameters

Additional neutron star parameters and models

Optional ML-based prediction module (future work)

License
This project is licensed under the MIT License. See LICENSE.

vbnet
Copy code
