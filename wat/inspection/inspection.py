# This is a shorter version of the code snippet.

from dataclasses import dataclass

@dataclass
class DataClassExample:
    data: int
    name: str

# Function to demonstrate type annotations
def add(a: int, b: int) -> int:
    return a + b

# Example usage
if __name__ == "__main__":
    example = DataClassExample(data=10, name="Test")
    print(example)
    print(add(5, 3))