from .cal import  calculation
from . import app
from rich import print
def main() -> None:
    print("[white] beleive me 👽[yellow] its faster than ai")
    parameter_1 = int(input(" 1️⃣ Enter First Number :"))
    parameter_2 = int(input(" 2️⃣ Enter Second Number :"))
    operation = str(input(" 🪄 Enter the operator u want to perform like (+,-,*,/)  :"))
    calculation(parameter_1,parameter_2,operation)



__all__ =["app"]
