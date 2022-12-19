# Detect an overflow in the current character
def DetectOverflow(CurrentLetter):
    if (CurrentLetter % 91) < 65:
        CurrentLetter = (CurrentLetter % 91) + 65

    return CurrentLetter

def main():
    # Prompt user for a sentence, rotation, and initialize the final output
    UserInput = input("Enter a sentence: ")
    RotValue = int(input("Enter a rotate value: "))
    FinalOut = ''

    for letter in UserInput:
        # Check if the letter lowercase
        if letter.islower():
            # Convert the letter to uppercase and rotate
            CurrentLetter = ord(letter.upper) + RotValue
            
            # Check for an overflow
            CurrentLetter = DetectOverflow(CurrentLetter) + 32
            
            # Append the lowercase letter 
            FinalOut = FinalOut + (chr(CurrentLetter))
        # Check if the letter is uppercase
        elif letter.isupper():
            # Rotate the letter
            CurrentLetter = ord(letter) + RotValue
            
            # Check for an overflow
            CurrentLetter = DetectOverflow(CurrentLetter)
            
            # Append the lowercase letter
            FinalOut = FinalOut + (chr(CurrentLetter))
        else:
            # Simply append everything else
            FinalOut = FinalOut + (letter)

    # Print the result
    print(''.join(FinalOut))

main()