import json
import numpy as np
from typing import List, Dict, Any

def save_to_json_chroma_compatible(
    data: List[Dict[str, Any]],
    output_filepath: str
) -> None:

    print(f"Saving {len(data)} items to {output_filepath}...")
    try:
        for item in data:
            if isinstance(item.get('embedding'), np.ndarray):
                item['embedding'] = item['embedding'].tolist()

        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Output saved successfully.")
    except Exception as e:
        raise IOError(f"Failed to save data to JSON file {output_filepath}: {e}")

