import bcrypt

password = "in_password_ro_be_kasi_nadi"
password_byte = password.encode("utf-8")
hashed_password = bcrypt.hashpw(password_byte, bcrypt.gensalt())
print(hashed_password)

new_password = "in_password_ro_be_kasi_nadi"
new_password_byte = new_password.encode("utf-8")
hashed_new_password = bcrypt.hashpw(new_password_byte, bcrypt.gensalt())
print(hashed_new_password)
if bcrypt.checkpw(new_password_byte, hashed_password):
    print("yes")
else:
    print("no")
  

