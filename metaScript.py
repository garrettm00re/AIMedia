import nbformat
import os

def combine_notebooks():
    notebooks = [
        'generateAssets.ipynb',
        'grokScript.ipynb', 
        'generateSoraVideos.ipynb'
    ]
    
    combined_cells = []
    zip_cell = nbformat.v4.new_code_cell(
        source='os.chdir(RUN_DIR)\n'
              'outName = trend[\'keyword\'].replace(" ", "_") # name of folder and file to zip\n'
              '!tar -acf {outName}.zip {outName}'
    )

    for notebook_file in notebooks:
        if not os.path.exists(notebook_file):
            print(f"Warning: {notebook_file} not found")
            continue
            
        with open(notebook_file, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
            
        # Add cells from this notebook
        for cell in nb.cells:
            if cell.cell_type in ['code', 'markdown']:
                combined_cells.append(cell)
        
        if notebook_file == 'grokScript.ipynb':
            combined_cells.append(zip_cell)

    # Create a new notebook
    new_nb = nbformat.v4.new_notebook()
    new_nb.cells = combined_cells

    # Write the combined notebook
    with open('combined_workflow.ipynb', 'w', encoding='utf-8') as f:
        nbformat.write(new_nb, f)
        
    print("Successfully combined notebooks into combined_workflow.ipynb")

if __name__ == "__main__":
    combine_notebooks()
