import json
from pathlib import Path
from typing import Iterator, Tuple, Dict, Optional

def read_jsonl_lines(filename: str) -> Iterator[dict]:
    with Path(filename).open('r') as file:
        for line in file:
            try:
                yield json.loads(line.strip())
            except json.JSONDecodeError:
                continue

def extract_moves(position: dict) -> Tuple[Optional[str], Optional[Dict[str, str]]]:
    try:
        moves = position['evals'][0]['pvs'][-1]['line'].split()
        return (
            position['fen'].split()[0],
            {
                "w": moves[0],  # Best move for white
                "b": moves[1] if len(moves) > 1 else None  # Best move for black
            }
        )
    except (KeyError, IndexError):
        return None, None

def process_file(input_path: str, output_path: str) -> None:

    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with Path(output_path).open('w') as outfile:
        for position in read_jsonl_lines(input_path):
            fen, moves = extract_moves(position)
            if fen and moves:
                outfile.write(json.dumps({"s": fen, "m": moves}) + '\n')

if __name__ == '__main__':
    try:
        process_file(
            input_path='lichess_db_eval.jsonl',
            output_path='lichess_db_eval_best_moves.jsonl'
        )
    except Exception as e:
        print(f"Program failed: {str(e)}")
