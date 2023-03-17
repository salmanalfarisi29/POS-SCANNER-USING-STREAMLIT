import pickle
from pathlib import path

import streamlit_authenticator as streamlit_authenticator

names = ["salman" , "farid"]
usernames = ["salmann" , "faridd"]
passwords = ["123" , "1234"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path open ()