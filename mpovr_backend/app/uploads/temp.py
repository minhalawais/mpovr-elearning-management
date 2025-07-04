from google_auth_oauthlib.flow import InstalledAppFlow

# Define the API scopes your app requires
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_account():
    flow = InstalledAppFlow.from_client_secrets_file(
        'D:/PycharmProjects/training-management-app/mpovr_backend/app/config/credentials.json', SCOPES)  # Path to your credentials.json
    credentials = flow.run_local_server(port=0)  # Opens a browser for authentication
    with open('token.json', 'w') as token_file:
        token_file.write(credentials.to_json())
    print("Authentication successful! Token saved to token.json.")

if __name__ == "__main__":
    authenticate_google_account()
