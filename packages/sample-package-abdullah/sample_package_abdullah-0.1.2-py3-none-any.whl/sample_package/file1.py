# pyment -w -o numpydoc [file name]
# pyment -w -o google [file name]

# google style
def sample_function(name: str, age: int):
    """This is a sample function.
    
    Args:
        name (str): The name of the person.
        age (int): The age of the person.
    Returns:
        str: A greeting message.
    """
    return f"Hello, {name}. You are {age} years old."

if __name__ == "__main__":
    # Example usage
    print(sample_function("John", 30))