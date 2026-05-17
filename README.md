\# RepoMind Analyzer (API Version)



Claude Code Skill to analyze a \*\*public GitHub repository\*\* via GitHub API and generate \*\*high-level conceptual explanations\*\* of its architecture, modules, data flow, and ML components (if any).  



This is a \*\*starter version\*\* of the skill (text-based) for local testing and further development. Frontend visualization can be added later.



\---



\## \*\*Skill Purpose\*\*



\- Analyze GitHub repos without cloning them

\- Provide a structured overview of:

&#x20; - Modules and dependencies

&#x20; - Data flow and execution sequence

&#x20; - AI/ML components (high-level)

&#x20; - Architectural patterns and design tradeoffs

\- Output structured text or JSON for downstream use



\---



\## \*\*Inputs\*\*



| Parameter | Type   | Description | Default |

|-----------|--------|-------------|---------|

| `repo\_url` | string | URL of public GitHub repository | required |

| `explanation\_level` | string (enum) | Level of explanation: `beginner` / `PM` / `technical` / `research` | `PM` |



\---



\## \*\*Outputs\*\*



The skill returns a JSON object with the following structure:



```json

{

&#x20; "overview": "High-level repo summary",

&#x20; "architecture": {

&#x20;   "modules": \[...],

&#x20;   "dependencies": \[...]

&#x20; },

&#x20; "modules": \[

&#x20;   {

&#x20;     "name": "module\_name",

&#x20;     "description": "Plain English explanation",

&#x20;     "submodules": \[...],

&#x20;     "functions": \[...]

&#x20;   }

&#x20; ],

&#x20; "data\_flow": "Summary of execution and data pipelines",

&#x20; "ai\_translation": \[

&#x20;   "Inferred architectural patterns",

&#x20;   "Design tradeoffs",

&#x20;   "High-level takeaways"

&#x20; ],

&#x20; "ml\_summary": {

&#x20;   "model\_architecture": "...",

&#x20;   "training\_flow": "...",

&#x20;   "reward\_loss": "...",

&#x20;   "evaluation": "..."

&#x20; }

}

