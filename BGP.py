class State:
    CurrentContext = None
    def __init__(self, Context):
        self.CurrentContext = Context
    def trigger(self):
        return True

class StateContext:
    state = None
    CurrentState = None
    availableStates = {}

    def setState(self, newstate):
        try:
            self.CurrentState = self.availableStates[newstate]
            self.state = newstate
            self.CurrentState.trigger()
            return True
        except KeyError:
            return False

    def getStateIndex(self):
        return self.state
        
class Transition:
    def idle(self):
        print "Error! Cannot Transition to idle!"
        return False

    def connect(self):
        print "Error! Cannot Transition to connect!"
        return False

    def active(self):
        print "Error! Cannot Transition to active"
        return False

    def open_sent(self):
        print "Error! Cannot Transition to open sent!"
        return False

    def open_confirm(self):
        print "Error! Cannot Transition to open confirm!"
        return False

    def established(self):
        print "Error! Cannot Transition to established!"
        return False

class Idle(State, Transition):
    '''
        This is the first stage of the BGP FSM. It either tries
        to initiate a TCP connection to the BGP pper (client mode),
        or listens for a new conenct from a peer (server mode).
    '''
    def __init__(self, Context):
        State.__init__(self, Context)

    def idle(self):
        # only called when operating as a server - this is handled by main
        # initiate listening process
        # and transition to connect state when connection made
        print "Currently in Idle state"
        self.CurrentContext.listen()
        self.CurrentContext.connect()
        return True

    def connect(self):
        # only called when operating as a client
        # initiate connection process
        # and transition to connect state when connection made
        if self.CurrentContext.connection_address == 0: # in client mode+
            self.CurrentContext.make_connection()
        print "Currently in Idle state, transition to connect state"
        self.CurrentContext.setState("CONNECT")
        return True

    def trigger(self):
        # close open socket and reset object
        # return true if succeed. False otherwise
        try: # server
            print "Closing down connection."
            self.CurrentContext.socket.close()
            self.CurrentContext.connection_address = 0
            return True
        except:  # client
            pass
            print "Idle Error"
        return True


class Connect(State, Transition):
    '''The conect state's role is to send out open essage,
        which are used to initiate BGP peer connections. It also
        provides the ability to retry connection attempts that fail
        - i.e. it periodically retry a TCP connection if inital attempts
        fail and times out. This latter functionalit hasn't been implemented
        in this model for the sake of simplicity'''
    def __init__(self, Context):
        State.__init__(self, Context)

    def idle(self):
        print "currently in connect state, transition to IDLE state"
        self.CurrentContext.setState("IDLE")
        return True
    def connect(self):
        print "Currently in connect state staying in connect state"
        self.CurrentContext.setState("CONNECT")
        return True
    def active(self):
        print "Currently in connect state, transition to active state"
        self.CurrentContext.setState("ACTIVE")
        return True
    def open_sent(self):

        try: #server
            self.CurrentContext.connection.send("OPEN")
        except: #client
            self.CurrentContext.socket.send("OPEN")
        print "Currently in connect state, transition to open sent state"
        self.CurrentContext.setState("OPENSENT")
        # send open command via existing connection
        # and transition to open sent state

        if(self.CurrentContext.connection == None and self.CurrentContext.s != None): # CLIENT
            self.CurrentContext.s.send("OPEN")
            print "Sending the open message."
            print "Currently in connect state, transition to open sent state"
            self.CurrentContext.setState("OPENSENT")
        else: # SERVER
            print "server is transition to openSent"
            self.CurrentContext.setState("OPENSENT")
        return True

    def trigger(self):
        # display address of the connecting system
        print "In the connect state"
        # and trigger open_sent message
        try:
            print "Connection from: " + self.CurrentContext.connection_address
        except:
            pass
        self.open_sent()
            print "Connect error"

        return True

class Active(State, Transition):
    '''
    The active state implements the "heartbeat" functionality
    - i.e. it periodically checks to see if the TCP connection
    is still alive by reconnecting. This functionality
    hasn't been implemented  in this model for the sake of simplicity
    '''
    def __init__(self, Context):
        State.__init__(self, Context)

    def idle(self):
        print "Transitioning to idle!"
        self.CurrentContext.setState("IDLE")
        return True

    def connect(self):
        print "Transitioning to connect!"
        self.CurrentContext.setState("CONNECT")
        return True

    def active(self):
        print "Transitioning to active!"
        self.CurrentContext.setState("ACTIVE")
        return True

    def open_sent(self):
        print "Transitioning to open sent!"
        self.CurrentContext.setState("OPENSENT")
        return True

class OpenSent(State, Transition):
    '''
        The open sent state role is to receieve open message
        from BGP peers. It also has the responsibility to verify
        these message - ie. it checks to see if the parameters of
        the BGP connection are valid. This latter functionality
        hasn't been implemeneted in this model for the sake of simplicyt
    '''
    def __init__(self, Context):
        State.__init__(self, Context)

    def idle(self):
        print "Currently in opensent, transition to IDLE state"
        self.CurrentContext.setState("IDLE")
        return True

    def active(self):
        print "Currently in opensent, transition to active state"
        self.CurrentContext.setState("ACTIVE")
        return True
    def open_confirm(self):
        # when open command received, transition to open confirm state
        try:
            command = self.CurrentContext.connection.recv(1024)
        except:
            command = self.CurrentContext.socket.recv(1024)
        # sleep ?
        if command == "OPEN":
            print "The command is : " + command
            # acceptable command transition to the openconfirm
            print "Currently in open Sent, transition to open Confirm"
            self.CurrentContext.setState("OPENCONFIRM")
        else:
            # transition back to idel state
            self.CurrentContext.idle()
        if(self.CurrentContext.connection): # server
            self.CurrentContext.command = self.CurrentContext.connection.recv(1024)
            if self.CurrentContext.command == "OPEN":
                print "Recieved open command"
                print "Currently in open Sent, transition to open Confirm"
                self.CurrentContext.setState("OPENCONFIRM")
        else: # client
            print "Currently in open Sent, transition to open Confirm"
            self.CurrentContext.setState("OPENCONFIRM")

        return True

    def trigger(self):
        # display address of system open command was sent to and
        try: # client
            print "address open message being sent too: ", self.CurrentContext.connection_address
        except: #server
            pass
        if(not self.CurrentContext.connection):
            print "Adress open message being sent too: ", self.CurrentContext.host

        # trigger open_confirm method
        self.open_confirm()
        return True

class OpenConfirm(State, Transition):
    '''
    In the BGP protocol, the open confirm state listens
    out for Keepalive or Notification message. Upon receipt of
    a neighbor's keepalive, the state is moved to established.
    If a notification message is received, and the state is moved
    to Idle. This last feature hasn't been implemented in this model
    for the sake of simplicity.
    '''
    def __init__(self, Context):
        State.__init__(self, Context)

    def idle(self):
        print "Currently in open confirm, transition to IDLE state"
        self.CurrentContext.setState("IDLE")
        return True
    def open_confirm(self):
        print "Currently in open confirm, transition to OPENCONFIRM state"
        self.CurrentContext.setState("OPENCONFIRM")
        return True
    def established(self):
        # send and receive keepalive messages
        print "Transition from open confirm, to ESTABLISHED state"
        self.CurrentContext.setState("ESTABLISHED")

        while self.CurrentContext.command != "KEEPALIVE":
            # send and receive keepalive messages
            if(not self.CurrentContext.connection): #client
                self.CurrentContext.command = self.CurrentContext.s.recv(1024)

                if(self.CurrentContext.command == "KEEPALIVE"):
                    print "Client Recived keepalive message"
                    print "Currently in open confirm, transition to ESTABLISHED state"
                    self.CurrentContext.s.send("KEEPALIVE")
                    print "Client Sending keepalive message"
                    self.CurrentContext.setState("ESTABLISHED")
            else: #server
                print "Sending keepalive message to client"
                self.CurrentContext.connection.send("KEEPALIVE")
                self.CurrentContext.command = self.CurrentContext.connection.recv(1024)
                if(self.CurrentContext.command == "KEEPALIVE"):
                    print "Server Recived keepalive message"
                    print "Transition from open confirm, to ESTABLISHED state"
                    self.CurrentContext.setState("ESTABLISHED")

        return True
    def trigger(self):
        # trigger established method
        self.established()
        return True

class Established(State, Transition):
    '''
        The established state handles the excahnge of route information.
        This functionality hasn't been implemented in this model for the
        sake of simplicity. The only role the established state has in
        this model is to terminate the demo via it's trigger method.
    '''
    def __init__(self, Context):
        State.__init__(self, Context)

    def idle(self):
        print "Currently in Established, transition to IDLE state"
        self.CurrentContext.setState("IDLE")
        return True
    def established(self):
        print "Currently in Established, staying in Established"
        # state stays the same
        return True
    def trigger(self):
        # terminate demo by transitioning to idle
        self.idle()
        return True

class BGPPeer(StateContext, Transition):
    connection = None
    socket = None
    addr = None
    s = None
    command = ""
    # True = server, False = client
    def __init__(self):
        # add the available states
        self.availableStates["IDLE"] = Idle(self)
        self.availableStates["CONNECT"] = Connect(self)
        self.availableStates["ACTIVE"] = Active(self)
        self.availableStates["OPENSENT"] = OpenSent(self)
        self.availableStates["OPENCONFIRM"] = OpenConfirm(self)
        self.availableStates["ESTABLISHED"] = Established(self)
        self.setState("IDLE")
        self.host = "127.0.0.1"
        self.port = 5000
        self.connection_address = 0

    def idle(self):
        return self.CurrentState.idle()

    def connect(self):
        return self.CurrentState.connect()

    def active(self):
        return self.CurrentState.active()

    def open_sent(self):
        return self.CurrentState.open_sent()

    def open_confirm(self):
        return self.CurrentState.open_confirm()

    def established(self):
        return self.CurrentState.established()

    def listen(self):
        ''' this method initiates a listen socket '''
        # server
        self.socket = socket.socket()
        try:
            print "waiting for a connection"
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            self.connection, self.connection_address = self.socket.accept()
            # connection acceptance
            return True
        except Exception as err:
            print err
            exit()

    def make_connection(self):
        # client
        ''' this method initiates an outbound connection '''
        print "making a connection"
        self.socket = socket.socket()
        try:
            self.socket.connect((self.host, self.port))
            self.connection_address = self.host
            return True
        except Exception as err:
            print err
            exit()

if __name__ == '__main__':
    if len(argv) < 2:
        print "Error: too few arguments"
        exit()
    ActivePeer = BGPPeer()
    if argv[1] == "server":
        ActivePeer.idle()
    else:
        ActivePeer.connect()
