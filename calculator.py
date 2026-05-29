# Terminal Calculator: Project 1

def main():
    firstNum = input("Enter the first number: ")
    operation = input("Enter the operation (+, -, *, /): ")
    secondNum = input("Enter the second number: ")

    answer = calculate(firstNum, operation, secondNum)
    print(f"{firstNum} {operation} {secondNum} = {answer}")

    keepChain = continueCalculate()

    while keepChain:
        firstNum = answer
        operation = input("Enter the operation (+, -, *, /): ")
        secondNum = input("Enter the second number: ")

        answer = calculate(firstNum, operation, secondNum)

        print(f"{firstNum} {operation} {secondNum} = {answer}")

        keepChain = continueCalculate()

def continueCalculate():
    continueCalc = input("\nContinue calculating? (enter yes or no): ")

    if continueCalc.lower() == "yes":
        return True
    else:
        return False

def calculate(firstNum, operation, secondNum):
    try:
        firstNum = float(firstNum)
        secondNum = float(secondNum)
    except ValueError:
        print("Sorry, these are not valid numbers")
        exit()

    if operation == "+":
        result = firstNum + secondNum
    elif operation == "-":
        result = firstNum - secondNum
    elif operation == "*":
        result = firstNum * secondNum
    elif operation == "/":
        if secondNum == 0:
            print("Division by zero is not allowed")
            exit()
        result = firstNum / secondNum
    else:
        print("Invalid operation, only (+, -, *, /) are permitted")
        exit()

    return result

if __name__ == "__main__":
    main()
