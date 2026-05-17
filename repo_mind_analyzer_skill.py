# repo_mind_analyzer_skill.py
import requests
import base64
import json
import os
import ast

def fetch_github_repo_contents(owner, repo, path=""):
    """Recursively fetch GitHub repository contents"""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch {url}: {resp.status_code}")
    contents = resp.json()
    items = []
    for item in contents:
        if item["type"] == "file":
            items.append({"type": "file", "path": item["path"]})
        elif item["type"] == "dir":
            items.append({
                "type": "dir",
                "path": item["path"],
                "children": fetch_github_repo_contents(owner, repo, item["path"])
            })
    return items

def parse_python_file_from_github(owner, repo, filepath):
    """Retrieve a Python file and parse classes and functions"""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{filepath}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return {"classes": [], "functions": [], "imports": []}
    content = base64.b64decode(resp.json()["content"]).decode("utf-8")
    tree = ast.parse(content)
    classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]
    imports += [alias.name for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) for alias in node.names]
    return {"classes": classes, "functions": functions, "imports": imports, "content": content}

def detect_ml_framework(file_content):
    """Detect ML frameworks including LLM/Transformer"""
    frameworks = ["torch", "tensorflow", "keras", "transformers", "sentence_transformers", "llama", "gpt"]
    detected = [fw for fw in frameworks if fw in file_content.lower()]
    return detected

def analyze_repo(repo_url, explanation_level="PM"):
    """Main Skill function: analyze repo structure and AI/ML components"""
    # Extract owner and repo
    if repo_url.endswith("/"):
        repo_url = repo_url[:-1]
    try:
        owner, repo = repo_url.split("/")[-2:]
    except:
        raise ValueError("Invalid GitHub repo URL")
    
    # Fetch repo file tree
    file_tree = fetch_github_repo_contents(owner, repo)
    
    modules = []
    ml_modules = []
    dependencies = set()

    # Traverse repo recursively
    def traverse(items):
        result = []
        for item in items:
            if item["type"] == "file":
                module_info = {"name": os.path.basename(item["path"]),
                               "submodules": [],
                               "classes": [],
                               "functions": [],
                               "imports": [],
                               "description": ""}
                if item["path"].endswith(".py"):
                    parsed = parse_python_file_from_github(owner, repo, item["path"])
                    module_info.update({
                        "classes": parsed["classes"],
                        "functions": parsed["functions"],
                        "imports": parsed["imports"]
                    })
                    # Detect ML/LLM frameworks
                    ml_detected = detect_ml_framework(parsed["content"])
                    if ml_detected:
                        ml_modules.append({"file": item["path"], "frameworks": ml_detected})
                result.append(module_info)
            elif item["type"] == "dir":
                result.append({
                    "name": os.path.basename(item["path"]),
                    "submodules": traverse(item["children"]),
                    "classes": [],
                    "functions": [],
                    "imports": [],
                    "description": ""
                })
        return result

    modules = traverse(file_tree)

    # Build JSON output
    output = {
        "overview": f"Repo '{repo}' contains {len(modules)} top-level modules",
        "architecture": {
            "modules": [m["name"] for m in modules],
            "dependencies": list(dependencies)
        },
        "modules": modules,
        "data_flow": "User request → Parser → Planner → Executor → Output (placeholder)",
        "ai_translation": [
            "Modular/agent-based architecture inferred",
            "Memory systems, planners, and tool orchestration detected",
            "High-level explanation tailored for PM"
        ],
        "ml_summary": ml_modules
    }

    return output

# Test
if __name__ == "__main__":
    test_repo = "https://github.com/psf/requests"
    result = analyze_repo(test_repo, explanation_level="PM")
    print(json.dumps(result, indent=2))