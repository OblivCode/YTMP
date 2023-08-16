from pypresence import Presence

client_id = '750690488809422933'  # Fake ID, put your real one here
RPC = Presence(client_id)  # Initialize the client class
RPC.connect()

def Update(state, image, join_url):
    RPC.update(details="YouTube Music", join=join_url, large_image=image, state=state, large_text='https://github.com/OblivCode/YTMP')
