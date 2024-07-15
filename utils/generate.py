import uuid
import random

def generate_address():
    # Generate a random OTP of specified length
    address = str(uuid.uuid4().hex)
    address = "0x"+address
    return address
def generate_secretcode(length=20):
    # Generate a random OTP of specified length
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    secretcode = "".join(random.choice(digits) for _ in range(length))
    return secretcode