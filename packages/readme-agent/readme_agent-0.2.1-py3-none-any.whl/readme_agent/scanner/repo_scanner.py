import os
import ast
import json


def scan_repo(repo_path):
    """
    Scans the repo for python files, requirements, and LICENSE, README.md files
    Extracts the classes, functions, modules and their docstrings using Abstract Syntax Tree
    """
    summary = {
        "modules":[],
        "functions":[],
        "classes":[],
        "docstrings":[],
        "requirements":[],
        "scripts":[],
        "notebooks":[],
        "readme_exists":False,
        "license_exists":False,
    }

    for root, dirs, files in os.walk(repo_path):
        for filename in files:
            file_path = os.path.join(root,filename)

            if filename.endswith(".py"):
                summary["modules"].append(file_path)
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        node = ast.parse(f.read(), filename = filename)
                        for n in ast.iter_child_nodes(node):
                            if isinstance(n, ast.ClassDef):
                                summary["classes"].append(n.name)
                                doc = ast.get_docstring(n)
                                if doc:
                                    summary["docstrings"].append({"type":"class","name":n.name, "doc":doc})
                                else:
                                    print(f"Note: Function '{n.name}' in {filename} has no docstring.")
                            elif isinstance(n,ast.FunctionDef):
                                summary["functions"].append(n.name)
                                doc = ast.get_docstring(n)
                                if doc:
                                    summary["docstrings"].append({"type":"functionn","name":n.name, "doc":doc})
                        
                        module_doc = ast.get_docstring(node)
                        if module_doc:    
                            summary["docstrings"].append({"type":"module","name":filename, "doc":module_doc})

                    
                    except Exception as e:
                        print(f"Error parsing {file_path}: {e}")

            elif filename == "requirements.txt":
                with open(file_path,"r", encoding="utf-8") as f:
                    summary['requirements'] = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            
            elif filename.lower() in ["main.py","app.py","run.py"]:
                summary["scripts"].append(file_path)
            
            elif filename.lower() == "readme.md":
                summary["readme_exists"] = True
            
            elif filename.lower().startswith("license"):
                summary["license_exists"] = True

    summary["notebooks"] = scan_notebooks(repo_path)
            
    return summary


def scan_notebooks(repo_path):
    """
    Scans the repo for jupyter notebooks (.ipynb), extracts the code and markdown and summarizes what the notebook is about
    in order to generate a README.md
    """

    notebook_summaries = []
    
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".ipynb"):
                notebook_path = os.path.join(root, file)
                try:
                    with open(notebook_path,"r",encoding = "utf-8") as f:
                        nb = json.load(f)
                    md_cells = [
                        "".join(cell["source"])
                        for cell in nb.get("cells", [])
                        if cell.get("cell_type") == "markdown"
                    ]
                    code_cells = [
                        "".join(cell["source"])
                        for cell in nb.get("cells", [])
                        if cell.get("cell_type") == "code"
                    ]
                    notebook_summaries.append({
                        "notebook": os.path.relpath(notebook_path, repo_path),
                        "markdown": md_cells[:10],  # First 3 markdown cells for summary
                        "code_samples": code_cells[:10],  # First 2 code cells for context
                    })
                except Exception as e:
                    print(f"Warning: Failed to parse notebook {notebook_path}: {e}")
    return notebook_summaries