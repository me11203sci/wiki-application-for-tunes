import keyring


######################################################
# Name: KeyStorage
# Purpose: Class for use in storing Tokens
# Notes: N/A
######################################################
class KeyStorage:
    def __init__(self):
        self.services: list[str] = []  # List of services -> for use in the cleanTokens function

    ######################################################
    # Name: setToken
    # Description: Stores an API token in the keyring
    # Input: Service, username, and token
    # Output: N/A
    # Notes: N/A
    ######################################################
    def setToken(self, service: str, username: str, token: str):
        keyring.set_password(service, username, token)
        self.services.append(service)

    ######################################################
    # Name: getToken
    # Description: Returns a token stored in the keyring
    # Input: Service and username strings
    # Output: API token
    # Notes: N/A
    ######################################################
    def getToken(self, service: str, username: str) -> str:
        return keyring.get_password(service, username)

    ######################################################
    # Name: changeToken
    # Description: Changes an API token
    # Input: Service, username, and new token
    # Output: N/A
    # Notes: To use if API token expires and new one needs to set
    ######################################################
    def changeToken(self, service: str, username: str, token: str):
        keyring.set_password(service, username, token)

    ######################################################
    # Name: cleanTokens
    # Description: Removes all tokens in the services list
    # Input: N/A
    # Output: N/A
    # Notes: To use when closing the application to avoid a
    #       cluttered keyring
    ######################################################
    '''def cleanTokens(self):
        for service in self.services:
            cred = keyring.get_credentials(service, "")
            keyring.delete_password(service, cred.username)'''
