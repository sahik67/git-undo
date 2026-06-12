from openai import OpenAI
import anthropic
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", FutureWarning)
    try:
        import google.genai as genai
    except ImportError:
        import google.generativeai as genai
import json
from typing import List, Dict
import os
from dotenv import load_dotenv


def load_config():
    load_dotenv()
    return {
        "provider": os.getenv("GIT_UNDO_PROVIDER", "openai"),
        "api_key": os.getenv("OPENAI_API_KEY"),
        "openrouter_api_key": os.getenv("OPENROUTER_API_KEY"),
        "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
        "google_api_key": os.getenv("GOOGLE_API_KEY"),
        "deepseek_api_key": os.getenv("DEEPSEEK_API_KEY"),
        "ollama_base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
        "model": os.getenv("GIT_UNDO_MODEL"),
    }


def get_system_prompt():
    return """You are a Git expert. The user will describe a Git mistake, and you will provide a sequence of Git commands to fix it.

You must respond with a valid JSON array of objects, where each object has:
- "command": The Git command to execute (as a string)
- "explanation": A concise one-line explanation of what this command does

Rules:
1. Only include the exact Git commands needed to fix the issue
2. Do not include any additional text outside the JSON array
3. Make sure the JSON is properly formatted
4. The commands should be context-aware based on the provided Git repository information
"""


def build_context_prompt(git_context: Dict) -> str:
    prompt_parts = ["Current Git Repository Context:"]
    prompt_parts.append(f"Branch: {git_context['branch']}")
    prompt_parts.append("\nRecent Commits:")
    for commit in git_context["commits"]:
        prompt_parts.append(f"  {commit['hash']}: {commit['message']}")
    prompt_parts.append("\nGit Status:")
    prompt_parts.append(git_context["status"])
    if git_context["stashes"]:
        prompt_parts.append("\nStash List:")
        for stash in git_context["stashes"]:
            prompt_parts.append(f"  {stash['id']}: {stash['message']}")
    return "\n".join(prompt_parts)


def parse_ai_response(content: str) -> List[Dict[str, str]]:
    try:
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        commands = json.loads(content)
        if isinstance(commands, list) and all(
            isinstance(c, dict) and "command" in c and "explanation" in c
            for c in commands
        ):
            return commands
        else:
            raise ValueError("Invalid response format")
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse AI response: {content}")


def generate_commands_openai(
    api_key: str, base_url: str, model: str, user_mistake: str, git_context: Dict
) -> List[Dict[str, str]]:
    client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
    user_prompt = f"""Mistake description: {user_mistake}

{build_context_prompt(git_context)}

Please provide the Git commands to fix this mistake."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": get_system_prompt()},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )
    return parse_ai_response(response.choices[0].message.content.strip())


def generate_commands_anthropic(
    api_key: str, model: str, user_mistake: str, git_context: Dict
) -> List[Dict[str, str]]:
    client = anthropic.Anthropic(api_key=api_key)
    user_prompt = f"""Mistake description: {user_mistake}

{build_context_prompt(git_context)}

Please provide the Git commands to fix this mistake."""
    message = client.messages.create(
        model=model,
        max_tokens=1024,
        system=get_system_prompt(),
        messages=[{"role": "user", "content": user_prompt}],
        temperature=0.3,
    )
    return parse_ai_response(message.content[0].text)


def generate_commands_gemini(
    api_key: str, model: str, user_mistake: str, git_context: Dict
) -> List[Dict[str, str]]:
    user_prompt = f"""{get_system_prompt()}

Mistake description: {user_mistake}

{build_context_prompt(git_context)}

Please provide the Git commands to fix this mistake."""
    
    try:
        # Try new google.genai API first
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents=user_prompt,
        )
        return parse_ai_response(response.text)
    except AttributeError:
        # Fall back to old google.generativeai API
        genai.configure(api_key=api_key)
        model_instance = genai.GenerativeModel(model)
        response = model_instance.generate_content(user_prompt)
        return parse_ai_response(response.text)


def generate_commands(
    user_mistake: str, git_context: Dict, provider: str = None, model: str = None
) -> List[Dict[str, str]]:
    config = load_config()
    
    if provider:
        config["provider"] = provider
    if model:
        config["model"] = model
        
    provider = config["provider"].lower()
    
    # Default models for each provider
    default_models = {
        "openai": "gpt-4o-mini",
        "openrouter": "openai/gpt-4o-mini",  # No need for openrouter/ prefix
        "anthropic": "claude-sonnet-4-5",
        "gemini": "gemini-2.0-flash",  # No need for gemini/ prefix for official API
        "deepseek": "deepseek-chat",  # No need for deepseek/ prefix for official API
        "ollama": "llama3.2",  # No need for ollama/ prefix for local API
    }
    
    if not config["model"]:
        config["model"] = default_models.get(provider, default_models["openai"])
        
    if provider == "openai":
        if not config["api_key"]:
            raise ValueError("OPENAI_API_KEY not found")
        return generate_commands_openai(
            config["api_key"], None, config["model"], user_mistake, git_context
        )
    elif provider == "openrouter":
        if not config["openrouter_api_key"]:
            raise ValueError("OPENROUTER_API_KEY not found")
        return generate_commands_openai(
            config["openrouter_api_key"],
            "https://openrouter.ai/api/v1",
            config["model"],
            user_mistake,
            git_context,
        )
    elif provider == "deepseek":
        if not config["deepseek_api_key"]:
            raise ValueError("DEEPSEEK_API_KEY not found")
        return generate_commands_openai(
            config["deepseek_api_key"],
            "https://api.deepseek.com/v1",
            config["model"],
            user_mistake,
            git_context,
        )
    elif provider == "ollama":
        return generate_commands_openai(
            "ollama",
            config["ollama_base_url"],
            config["model"],
            user_mistake,
            git_context,
        )
    elif provider == "anthropic":
        if not config["anthropic_api_key"]:
            raise ValueError("ANTHROPIC_API_KEY not found")
        return generate_commands_anthropic(
            config["anthropic_api_key"], config["model"], user_mistake, git_context
        )
    elif provider == "gemini":
        if not config["google_api_key"]:
            raise ValueError("GOOGLE_API_KEY not found")
        return generate_commands_gemini(
            config["google_api_key"], config["model"], user_mistake, git_context
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")
