from typing import Tuple
import os
import json


def check_directory(current_dir: str) -> Tuple[str, str, str]:
    output_dir = os.path.join(current_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)

    figures_dir = os.path.join(output_dir, 'figures')
    os.makedirs(figures_dir, exist_ok=True)

    magma_dir = os.path.join(output_dir, 'magma')
    os.makedirs(magma_dir, exist_ok=True)

    return output_dir, figures_dir, magma_dir


def save(filename: str, response: dict) -> str:
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False, indent=4)

    return filename
