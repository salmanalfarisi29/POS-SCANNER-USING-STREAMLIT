import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Salman Alfarisi", "Muhamad Farid", "GUDANG 1"]
usernames = ["ssalman", "ffarid" , "gudangkopma1"]
passwords = ["abc123", "abc321", "kerjamantap"]

#username berdasarkan role
#GUDANG 1

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl" , "hashed_pw1.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)