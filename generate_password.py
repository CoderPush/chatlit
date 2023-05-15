import streamlit_authenticator as stauth

# get password from command line argument via input function
password = input("Enter password: ")

hashed_passwords = stauth.Hasher([password]).generate()

print(hashed_passwords)
