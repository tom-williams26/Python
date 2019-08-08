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
    def up(self):
        print "Lift can not go any higher"
        return False

    def down(self):
        print "Lift can not go any lower"
        return False

    def open_close(self):
        print "Failed to open and close the doors. Invalid"
        return False

class BottomFloor(State, Transition):
    def __init__(self, Context):
        State.__init__(self, Context)
    # new state will be a string passed in.
    def up(self):
        # tranisition to middle floor
        print "Lift going up"
        self.CurrentContext.currentFloor += 1
        self.CurrentContext.setState("MIDDLE")
        return True

    def open_close(self):
        print "The doors are open, and they are closed again."
        return True

class MiddleFloor(State, Transition):
    def __init__(self, Context):
        State.__init__(self, Context)

    def up(self):
        print "Lift going up"
        self.CurrentContext.currentFloor += 1
        if(self.CurrentContext.currentFloor == self.CurrentContext.number_of_doors):
            self.CurrentContext.setState("TOP")
        return True

    def down(self):
        print "Lift going down"
        self.CurrentContext.currentFloor -= 1
        if(self.CurrentContext.currentFloor == 0):
           self.CurrentContext.setState("BOTTOM")
        return True

    def open_close(self):
        print "The doors are open, and they are closed again."
        return True

class TopFloor(State, Transition):
    def __init__(self, Context):
        State.__init__(self, Context)

    def down(self):
        print "Lift going down"
        self.CurrentContext.currentFloor -= 1
        self.CurrentContext.setState("MIDDLE")
        return True

    def open_close(self):
        print "The doors are open, and they are closed again."
        return True


class Lift(StateContext, Transition):
    def __init__(self, number_of_doors):
        self.number_of_doors = number_of_doors
        self.availableStates["BOTTOM"] = BottomFloor(self)
        self.availableStates["MIDDLE"] = MiddleFloor(self)
        self.availableStates["TOP"] = TopFloor(self)
        self.setState("BOTTOM")
        self.currentFloor = 0

    def up(self):
        self.CurrentState.up()

    def down(self):
        self.CurrentState.down()

    def open_close(self):
        self.CurrentState.open_close()



if __name__ == "__main__":
    MyLift = Lift(3)
    MyLift.up()
    MyLift.open_close()
    MyLift.up()
    MyLift.up()
    MyLift.up()
    MyLift.down()
    MyLift.down()
    MyLift.down()
    MyLift.down()
