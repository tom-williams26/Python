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
    def pressButton(self):
        print "Error: no button exists!"

class LightSwitchOn(State, Transition):
    def __init__(self, Context):
        State.__init__(self, Context)

    def pressButton(self):
        print "Light going off!"
        self.CurrentContext.setState("OFF")

class LightSwitchOff(State, Transition):
    def __init__(self, Context):
        State.__init__(self, Context)

    def pressButton(self):
        print "Light going on!"
        self.CurrentContext.setState("ON")

class LightSwitch(StateContext, Transition):
    def __init__(self):
        self.availableStates["OFF"] = LightSwitchOff(self)
        self.availableStates["ON"] = LightSwitchOn(self)
        self.setState("OFF")

    def pressButton(self):
        self.CurrentState.pressButton()


if __name__ == '__main__':
    MySwitch = LightSwitch()
    MySwitch.pressButton()
    MySwitch.pressButton()
    print MySwitch.state
