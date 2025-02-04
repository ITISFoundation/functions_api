import time


def test_function1(x, y):
    timeout = 5
    print(f"Received {x}, {y} input, sleeping for {timeout} s...")
    time.sleep(timeout)
    
    return_value = x+y
    print(f"Returning {x} + {y} = {x+y}")
    return return_value
