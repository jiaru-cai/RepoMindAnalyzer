# repo_mind_skill.py
# Claude Code Skill: RepoMind Analyzer (API Version)
# Converts your Draft workflow into a runnable Python structure using GitHub API

import requests

def analyze_repo(repo_url, explanation_level="PM"):
    """
    Analyze a public GitHub repository and return high-level conceptual explanations.
    
    Inputs:
    - repo_url: URL of public GitHub repository
    - explanation_level: beginner | PM | technical | research (default: PM)
    
    Outputs:
    - A structured dict (JSON-like) containing overview, modules, architecture, data flow, AI translation, ML summary
    """
    
    output = {
        "overview": "",
        "architecture": {
            "modules": [],
            "dependencies": []
        },
        "modules": [],
        "data_flow": "",
        "ai_translation": [],
        "ml_summary": {}
    }

    # Step 1: Parse repo URL
    try:
        parts = repo_url.rstrip("/").split("/")
        owner = parts[-2]
        repo = parts[-1]
    except:
        return {"error": "Invalid GitHub URL"}

    # Step 2: Fetch repo contents via GitHub API
    base_api = f"https://api.github.com/repos/{owner}/{repo}/contents"
    response = requests.get(base_api)
    if response.status_code != 200:
        return {"error": f"Cannot access repo: {response.status_code}"}
    
    files = response.json()
    output["overview"] = f"Repo {repo} by {owner} has {len(files)} top-level files/folders"

    # Placeholder: collect file paths (could later recursively traverse folders)
    file_list = [f['path'] for f in files]
    
    # Step 3: Generate Architecture Map
    # Here we simply list modules/files as a placeholder
    output["architecture"]["modules"] = file_list

    # Step 4: Explain Modules
    # Placeholder: generate dummy explanation
    for f in file_list:
        module_info = {
            "name": f,
            "description": f"Module {f} purpose explanation placeholder",
            "submodules": [],
            "functions": []
        }
        output["modules"].append(module_info)
    
    # Step 5: Data and Execution Flow
    output["data_flow"] = "Data flow summary placeholder (to be implemented)"
    
    # Step 6: AI Concept Translation
    output["ai_translation"] = [
        "Inferred architectural patterns placeholder",
        "Design tradeoffs placeholder",
        "High-level takeaways placeholder"
    ]
    
    # Step 7: ML/AI Module Detection
    output["ml_summary"] = {
        "model_architecture": "High-level model structure placeholder",
        "training_flow": "Training loop placeholder",
        "reward_loss": "Reward/loss functions placeholder",
        "evaluation": "Evaluation pipeline placeholder"
    }
    
    # Step 8: Return Structured Output
    return output


# -------------------------------
# Test block: run this skill locally
# -------------------------------
if __name__ == "__main__":
    test_repo = "https://github.com/psf/requests"  # small public repo for testing
    result = analyze_repo(test_repo, explanation_level="PM")
    import json
    print(json.dumps(result, indent=2))