# 32BitCipher

open source: https://github.com/wew1234GD/32BitCipher

### usage:
```python
import cp32

cipher = cp32.e32BitCipher() # type your key or leave it blank (default key =  0x1AC32B4D)
#cipher = e32BitCipher(key=0x1A2B3C4D) 

encrypted = cipher.encrypt("test")

print(encrypted)  # encrypted XoR
decrypted = cipher.decrypt(encrypted)
print(decrypted) # decrypted XoR 
```

```bash
git clone https://github.com/wew1234GD/32BitCipher
```