# repo_mind_skill.py
import requests
import base64
import json
import os
import ast

def fetch_github_repo_contents(owner, repo, path=""):
    """Recursively fetch the contents of a GitHub repository"""
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
    """Retrieve a Python file from GitHub and parse classes and functions"""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{filepath}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return {"classes": [], "functions": []}
    content = base64.b64decode(resp.json()["content"]).decode("utf-8")
    tree = ast.parse(content)
    classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return {"classes": classes, "functions": functions}

def detect_ml_framework(file_content):
    """Simple ML framework detection"""
    if any(framework in file_content for framework in ["torch", "tensorflow", "keras"]):
        return True
    return False

def analyze_repo(repo_url, explanation_level="PM"):
    """Main Skill function"""
    # Extract owner and repo name from URL
    if repo_url.endswith("/"):
        repo_url = repo_url[:-1]
    try:
        owner, repo = repo_url.split("/")[-2:]
    except:
        raise ValueError("Invalid GitHub repo URL")
    
    # Fetch repository file tree
    file_tree = fetch_github_repo_contents(owner, repo)
    
    modules = []
    ml_modules = []
    dependencies = set()
    
    # Traverse file tree recursively
    def traverse(items):
        result = []
        for item in items:
            if item["type"] == "file":
                module_info = {"name": os.path.basename(item["path"]), "submodules": [], "functions": [], "description": ""}
                if item["path"].endswith(".py"):
                    parsed = parse_python_file_from_github(owner, repo, item["path"])
                    module_info["classes"] = parsed["classes"]
                    module_info["functions"] = parsed["functions"]
                    # Check for ML frameworks
                    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{item['path']}"
                    content = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"}).json()
                    decoded = base64.b64decode(content["content"]).decode("utf-8")
                    if detect_ml_framework(decoded):
                        ml_modules.append(module_info["name"])
                result.append(module_info)
            elif item["type"] == "dir":
                result.append({
                    "name": os.path.basename(item["path"]),
                    "submodules": traverse(item["children"]),
                    "functions": [],
                    "description": ""
                })
        return result
    
    modules = traverse(file_tree)
    
    # Build structured JSON output
    output = {
        "overview": f"Repo '{repo}' has {len(modules)} top-level modules",
        "architecture": {"modules": [m["name"] for m in modules], "dependencies": list(dependencies)},
        "modules": modules,
        "data_flow": "User input -> Processing -> Output (placeholder)",
        "ai_translation": [
            "Modular architecture detected",
            "High-level design placeholder",
            "PM-level explanation placeholder"
        ],
        "ml_summary": {
            "model_architecture": "Detected ML modules: " + ", ".join(ml_modules),
            "training_flow": "Training loop placeholder",
            "reward_loss": "Reward/loss placeholder",
            "evaluation": "Evaluation pipeline placeholder"
        }
    }
    
    return output

# Test
if __name__ == "__main__":
    test_repo = "https://github.com/psf/requests"
    result = analyze_repo(test_repo, explanation_level="PM")
    print(json.dumps(result, indent=2))