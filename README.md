# Tsoro Yematatu
This a an implementation of the african game `tsoro yematatu` in python3 with TCP Sockets.

It comes with an embbeded chat and `Color` and `Turn` handshake. 

It was tested with `python3.10`
## Installing
Simply run 
> pip3 install -r requirements.txt

## How to run
Make sure to have permission to use port `8123`.

Then run
> python3 main.py

This implementation works on a peer to peer connection. You'll need to execute two instances of the program.


## Architecture

The project heavily uses an Observer design pattern that is stored in `client/state.py`. It guides all changes on the local board. It also guides synchronization. Every local event may be published to the socket, and every received event on the socket is passed to the Observer Event Bus.

### Handshakes
Two handshakes are defined
- Color
- Turn

The both handshakes follow the same state machine with some differences on presenting state. 

The color handshake will disabled already picked colors.
The turn handshake will allow users to vote(pick) which one should start the game. In case of a draw, a random one will be picked.
 ![StateMachine](state_machine.png)



Author: `Nivardo Albuquerque Leitão de Castro`
    Find me at `nivardo00@gmail.com` or `github.com/nivardox`.
    



