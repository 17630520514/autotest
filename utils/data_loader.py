import yaml
from pathlib import Path


class DataLoader:
    @staticmethod
    def load_yaml(file_name: str) -> dict:
        file_path = Path(__file__).parent.parent / "test_data" / file_name
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    @staticmethod
    def get_test_data(file_name: str, key: str) -> dict:
        data = DataLoader.load_yaml(file_name)
        return data.get(key, {})
