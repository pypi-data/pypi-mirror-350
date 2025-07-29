import requests
import zipfile
import io
import ast
from collections import defaultdict
import json
import os
import sys
import tempfile
import importlib.util
import inspect
import pathlib

from rod.schema_generator import SchemaInterface

def get_functions_from_source(source_code):
    """
    Extract function names from the source code.
    
    Args:
        source_code (str): The source code to extract functions from.
        
    Returns:
        list: A list of function names.
    
    """
    tree = ast.parse(source_code)
    return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

def fetch_package_info(package_name):
    """
    Fetch package info from PyPI.
    
    Args:
				package_name (str): The name of the package to fetch info for.
    
    Returns:
				dict: The package info.
    """
    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    return response.json()

def find_whl_url(package_info):
    """
    Find the .whl file URL from the package info.
    
    Args:
				package_info (dict): The package info.
    
    Returns:
				str: The URL of the .whl file.
    """
    for version, files in package_info['releases'].items():
        for file in files:
            if file['packagetype'] == 'bdist_wheel':
                return file['url']
    return None

def extract_functions_from_whl(whl_url):
    """
    Extract functions from .py files in the .whl file.
    
    Args:
				whl_url (str): The URL of the .whl file.
    
    Returns:
				dict: A dictionary containing the functions extracted from the .py files.
    """
    functions_dict = defaultdict(list)
    whl_response = requests.get(whl_url)
    whl_file = zipfile.ZipFile(io.BytesIO(whl_response.content))

    for file_info in whl_file.infolist():
        if file_info.filename.endswith('.py'):
            with whl_file.open(file_info.filename) as file:
                source_code = file.read().decode('utf-8')
                functions = get_functions_from_source(source_code)
                functions_dict[file_info.filename] = functions
    return functions_dict

def save_to_json(data, file_path):
    """
    Save data to a JSON file.
    
    Args:
				data (dict): The data to save.
    
    Returns:
				file_path (str): The path to the JSON file.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def get_functions_from_module(module):
    functions = []
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            # filter out functions that are imported from other modules
            if obj.__module__ == module.__name__:
                functions.append(obj)
        if inspect.isclass(obj):
            for name, method in inspect.getmembers(obj):
                if inspect.isfunction(method):
                    functions.append(method)
    return functions

def dynamic_import_whl(whl_url):
    """
    Dynamically import a .whl file from a URL and extract functions from imported modules.
    
    Args:
        whl_url (str): The URL of the .whl file.
    
    Returns:
        dict: A dictionary with the keys 'imported_modules', 'failed_modules', and 'functions'.
    """
    whl_response = requests.get(whl_url)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        whl_path = f"{temp_dir}/package.whl"
        with open(whl_path, 'wb') as whl_file:
            whl_file.write(whl_response.content)
        
        with zipfile.ZipFile(whl_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        sys.path.insert(0, temp_dir)

        imported_modules = []
        failed_modules = []
        functions_dict = {}
        
        for file_info in zipfile.ZipFile(whl_path).infolist():
            if file_info.filename.endswith('.py') and not file_info.filename.startswith('test'):
                file_path = f"{temp_dir}/{file_info.filename}"
                module_name = file_info.filename[:-3].replace('/', '.')
                
                try:
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    imported_modules.append(module_name)
                    
                    # Extract functions from the imported module
                    functions = get_functions_from_module(module)
                    schemas = []
                    for func in functions:
                        try:
                            schema = SchemaInterface(func)
                        except Exception as e:
                            schema = {'name': func.__name__, 'cause': str(e)}
                        schemas.append(schema)
                    functions_dict[module_name] = schemas
                    
                except Exception as e:
                    failed_modules.append((module_name, str(e)))
        
        sys.path.pop(0)
    
    return {
        'imported_modules': imported_modules,
        'failed_modules': failed_modules,
        'functions': functions_dict
    }

# Example usage
# whl_url = 'https://example.com/path/to/package.whl'
# result = dynamic_import_whl(whl_url)
# print("Imported Modules:", result['imported_modules'])
# print("Failed Modules:", result['failed_modules'])
# print("Functions:")
# for module_name, functions in result['functions'].items():
#     print(f"Module: {module_name}")
#     for func in functions:
#         print(f"  - {func.__name__}")

def main():
    package_name = "moapy"
    package_info = fetch_package_info(package_name)
    whl_url = find_whl_url(package_info)

    if whl_url:
        imported_modules = dynamic_import_whl(whl_url)
        current_path = pathlib.Path(__file__).parent
        # functions_dict = extract_functions_from_whl(whl_url)
        save_to_json(imported_modules, os.path.join(current_path, 'managed', 'project.json'))
        # for file, functions in functions_dict.items():
        #     print(f"\nFile: {file}")
        #     for func in functions:
        #         print(f"  - Function: {func}")
    else:
        print("No .whl file found for the specified package.")

if __name__ == "__main__":
    main()
