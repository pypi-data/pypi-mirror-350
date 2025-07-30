# token_manager.py

# Global variable to store the user's token
TOKEN = None

def define_token(user_token):
    """
    Define a unique token for the user.
    
    Parameters:
        user_token (str): The user's token.
    """
    global TOKEN
    TOKEN = user_token
    print(f"Token has been set: {TOKEN}")

def get_token():
    """
    Retrieve the current token value.
    
    Returns:
        str: The token value.
    """
    if TOKEN is None:
        raise ValueError("Token is not defined. Use `define_token` to set it.")
    return TOKEN


# Token explanation
"""
A token is a unique key for authenticating access to quantum platforms like Quafu (https://quafu.baqis.ac.cn/#/home).
- Register on the platform to obtain your personal token.
- Use `define_token` to set your token and `get_token` to access it in your code.
- Keep your token secure and avoid sharing it publicly.
"""

# # Example usage
# if __name__ == "__main__":
#     # Set the token
#     define_token("my_unique_token_123")

#     # Retrieve and use the token
#     token = get_token()
#     print(f"Token in use: {token}")
