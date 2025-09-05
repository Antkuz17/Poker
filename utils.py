import random

def genRandNum(min, max) -> int:
    """This will return an random integer between min and max inclusive"""
    return (random.randint(min, max))

def inputValidation(attemptedInput, requiredType: type):
    """Uses a validation loop to continue reprompting the user until their input matches the type provided"""
    while True:
            try:
                requiredType(attemptedInput) # Tries to cast the input to the type required
            except ValueError:
                attemptedInput = input("Invalid input, try again: ") # If it throws a value error, reprompt
