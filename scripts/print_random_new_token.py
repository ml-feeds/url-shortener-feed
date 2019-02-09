import base64
import secrets

NUM_BYTES = 10  # Must evidently be a multiple of 5 so as to avoid equal sign in b32 result.
NUM_TOKENS = 5

print('New tokens:')
for _ in range(NUM_TOKENS):
    token = secrets.token_bytes(NUM_BYTES)
    token = base64.b32encode(token).decode().lower()
    assert '=' not in token
    assert len(token) == 16
    print(token)
