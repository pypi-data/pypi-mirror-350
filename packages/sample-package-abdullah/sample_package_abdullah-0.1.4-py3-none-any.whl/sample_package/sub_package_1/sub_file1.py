
# to generate automatic doc string 

# bellow numpy style
def sample_function2(name: str, age: int): 
    """

    Parameters
    ----------
    name: str
        The name of the person.
        
    age: int 
        The age of the person.
        

    Returns
    -------
    str:
        A greeting message.
    """


    return f'Hello {name}, your age {age}'
if __name__ == "__main__":
    print(sample_function2('arif', 34))
