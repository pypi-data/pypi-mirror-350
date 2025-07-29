from .add import addition
from .div import division
from .sub import subtraction
from .mul import multiplication
from rich.console import Console
import time

console = Console()

def calculation(a:int,b:int,operation:str):
    match operation:
        case "+":
            with console.status("Addition is one of the most hardest task for dev ",spinner="monkey"):
                time.sleep(3)
            addition(a,b)
        case "-":
            with console.status("subtraction is one of the most hardest task for dev ",spinner="clock"):
                time.sleep(3)
            subtraction(a,b)
        case "*":
            with console.status("multiplication is one of the most hardest task for dev ",spinner="material"):
                time.sleep(3)
            multiplication(a,b)
        case "/":
            with console.status("division is one of the most hardest task for dev ",spinner="moon"):
                time.sleep(3)
            division(a,b)
        case _:
            print("[red]Invalid operator ⚠️")


