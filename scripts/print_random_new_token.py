import secrets

NUM_BYTES = 8

token = secrets.token_hex(NUM_BYTES)
print(f'Random new token of {NUM_BYTES} bytes having length {len(token)} is {token}.')
