from MAVProxy.modules.lib import mp_module

class SimpleModule(mp_module.MPModule):
    def __init__(self, mpstate):
        super(SimpleModule, self).__init__(mpstate, "simple_module")
        self.add_command("hello", self.cmd_hello, "Prints a hello message")

    def cmd_hello(self, args):
        self.mpstate.console.writeln("Hello from SimpleModule!")

    def startup(self):
        self.mpstate.console.writeln("SimpleModule has been loaded successfully!")
