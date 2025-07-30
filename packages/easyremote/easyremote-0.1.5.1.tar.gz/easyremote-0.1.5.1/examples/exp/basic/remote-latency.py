from easyremote.cli.accelerator import remote

@remote()
def add_numbers(numbers: str) -> int:
    pass

@remote()
def ai_inference(text: str) -> str:
    pass
    
result1 = add_numbers("10, 20")
result2 = ai_inference("Hello World")