"""
The goal is to illustrate how you might create an interactive
parallel interpreter with this MPI package.

This interpreter is a simple extension of the InteractiveConsole
class provided by Python's standard library (in the 'code' module).
"""
# Standard Modules
import sys,code
# My Modules
import mpi

class ParallelConsole( code.InteractiveConsole ):
    def __init__(self, locals=None, filename="<console>"):
        """Constructor.
        
        The optional locals argument will be passed to the
        InteractiveInterpreter base class.

        The optional filename argument should specify the (file)name
        of the input stream; it will show up in tracebacks.

        """
        code.InteractiveConsole.__init__(self, locals,filename)
        self.rank = mpi.comm_rank( mpi.MPI_COMM_WORLD )
        self.size = mpi.comm_size( mpi.MPI_COMM_WORLD )
        return

    def raw_input(self, prompt=""):
        """
        On the master node:
           1). Write a prompt and read a line.
           2). Broadcast the Line or Terminate
           3). Broadcast the Line
               a).  First, get the length of the line and broadcast it
               b).  Broadcast the line data itself
           4). Terminate
               a).  If the user types the control sequence to exit
                      EOFError is raised.
               b).  Catch EOFError and broadcast length, this time broadcasting negative
               c).  All nodes check for length < 0 and raise an EOFError.
        """
        if( self.rank == 0 ):
            try:
                data = raw_input(prompt)
            except EOFError:
                length = mpi.bcast( -1, 1, mpi.MPI_INT, 0, mpi.MPI_COMM_WORLD )
                self.write("\n")
                raise
            length = mpi.bcast( len(data), 1, mpi.MPI_INT, 0, mpi.MPI_COMM_WORLD )
            data = mpi.bcast(data,length[0], mpi.MPI_CHAR, 0, mpi.MPI_COMM_WORLD )
        else:
            length = mpi.bcast( 0, 1, mpi.MPI_INT, 0, mpi.MPI_COMM_WORLD )
            if (length[0] < 0):
                raise EOFError
            data = mpi.bcast("",length[0], mpi.MPI_CHAR, 0, mpi.MPI_COMM_WORLD )
        s = ""
        for e in data:
            s += "".join(e)
        return s

    def interact(self, banner=None):
        """Closely emulate the interactive Python console.

        The optional banner argument specify the banner to print
        before the first interaction; by default it prints a banner
        similar to the one printed by the real Python interpreter,
        followed by the current class name in parentheses (so as not
        to confuse this with the real interpreter -- since it's so
        close!).

        """
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = ">>> "
        try:
            sys.ps2
        except AttributeError:
            sys.ps2 = "... "
        cprt = 'Type "help", "copyright", "credits" or "license" for more information.'
        if( self.rank == 0 ):
            if banner is None:
                self.write("Python %s on %s\n%s\n(%s)\n" %
                           (sys.version, sys.platform, cprt,
                            self.__class__.__name__))
            else:
                self.write("%s\n" % str(banner))
        else:
            pass
        more = 0
        while 1:
            try:
                if more:
                    prompt = sys.ps2
                else:
                    prompt = sys.ps1
                try:
                    line = self.raw_input(prompt)
                except EOFError:
                    break
                else:
                    more = self.push(line)
            except KeyboardInterrupt:
                self.write("\nKeyboardInterrupt\n")
                self.resetbuffer()
                more = 0
        
if __name__=="__main__":
    try:
        mpi.init()
        console = ParallelConsole( )
        console.interact()
        mpi.finalize()
    except:
        mpi.finalize()
        raise
