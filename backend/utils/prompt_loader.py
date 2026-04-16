from pathlib import Path

def load_prompt_text(file_name: str) -> str:

    current_dir = Path(__file__).resolve().parent 
    
    clean_file_name = Path(file_name).name 
    prompt_path = current_dir.parent / "prompts" / clean_file_name
    
    if not prompt_path.exists():
        raise FileNotFoundError(f"Could not find prompt file at: {prompt_path}")
        
    return prompt_path.read_text(encoding="utf-8")