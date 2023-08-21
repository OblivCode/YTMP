from pypresence import Presence

client_id = '750690488809422933'  # Fake ID, put your real one here
RPC = Presence(client_id)  # Initialize the client class
RPC.connect()

def Update(state, image, buttons: list =None):
    RPC.update(details="YouTube Music", buttons=buttons, large_image=image, state=state, large_text='YouTube Music Presence by OblivCode', instance=False)

def Close():
    RPC.close()