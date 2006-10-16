"""
MMPI - MPE Interface for Python
Copyright (C) 2005 Michael Steder(steder@gmail.com)

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

"""
mpe.py

These functions are just simple wrappers around the MPE Logging functions
defined in _mpe.so.
"""

# Standard python modules:
import time

# my modules
import _mpi
import _mpe
from _mpe import mpeException

# MPE Error Codes:
"""
#define MPE_LOG_OK                0
  /* no problems */
#define MPE_LOG_LOCKED_OUT        1
  /* logs are being worked on, cannot insert any new entries */
#define MPE_LOG_NO_MEMORY         2
  /* could not allocate memory for logging data */
#define MPE_LOG_FILE_PROB         3
  /* cound not open file for writing out the logged info */
#define MPE_LOG_NOT_INITIALIZED   4
  /* logging not initialized */
#define MPE_LOG_PACK_FAIL         5
"""

def handleError( errorcode ):
    if(errorcode == _mpe.MPE_LOG_OK):
        pass
    elif(errorcode == _mpe.MPE_LOG_LOCKED_OUT):
        raise mpeException,"MPE: logs are being worked on, cannot insert any new entries!"
    elif(errorcode == _mpe.MPE_LOG_NO_MEMORY):
        raise mpeException,"MPE: could not allocate memory for logging data!"
    elif(errorcode == _mpe.MPE_LOG_NOT_INITIALIZED):
        raise mpeException,"MPE: logging not initialized!"
    elif(errorcode == _mpe.MPE_LOG_PACK_FAIL):
        raise mpeException,"MPE: failed to pack data for logging!"
    elif(errorcode == _mpe.MPE_LOG_FILE_PROB):
        raise mpeException,"MPE: could not open file for writing out the logged info!"
    else:
        print "** MPE WARNING: UNKNOWN MPE ERROR CODE THROWN! **"
    return errorcode

def init_log():
    """
    errorcode = mpe.init_log()

    
    Initialize the MPE logging environment.
    *Requires that MPI is already initialized before it can be called.
      See: finish_log
    """
    if ( _mpi.mpi_initialized() ):
        return handleError(_mpe.mpe_init_log())
    else:
        raise mpeException, "Attempt to call %s before mpi.init!"%("mpe.init_log")
    
def start_log():
    """
    errorcode = mpe.start_log()


    Allows one to dynamically start the MPE logging system.
      See: stop_log
    """
    if ( _mpi.mpi_initialized() ):
        return handleError(_mpe.mpe_start_log())
    else:
        raise mpeException, "Attempt to call %s before mpi.init!"%("mpe.start_log")
    
    return _mpe.mpe_start_log()

def stop_log():
    """
    errorcode = mpe.stop_log()


    Allows one to dynamically stop the MPE logging system.
      See:  start_log
    """
    if ( _mpi.mpi_initialized() ):
        return handleError(_mpe.mpe_stop_log())
    else:
        raise mpeException, "Attempt to call %s before mpi.init!"%("mpe.stop_log")
    
    return _mpe.mpe_stop_log()

def finish_log( filepath ):
    """
    errorcode = mpe.finish_log( filepath )

    filepath: write the MPE events to filepath

    Finalizes the MPE logging environment and writes all logged information
    to the specificed file path.
      See:  init_log
    """
    if ( _mpi.mpi_initialized() ):
        return handleError(_mpe.mpe_finish_log(filepath))
    else:
        raise mpeException, "Attempt to call %s before mpi.init!"%("mpe.finish_log")

def log_event( intevent, intdata, stringdata ):
    """
    errorcode = mpe.
    """
    if ( _mpi.mpi_initialized() ):
        return handleError(_mpe.mpe_log_event(intevent, intdata, stringdata))
    else:
        raise mpeException, "Attempt to call %s before mpi.init!"%("mpe.log_event")

def describe_event( intevent, description, color ):
    if ( _mpi.mpi_initialized() ):
        return handleError(_mpe.mpe_describe_event(intevent, description, color))
    else:
        raise mpeException, "Attempt to call %s before mpi.init!"%("mpe.describe_event")

def describe_state( startevent, stopevent, description, color ):
    if ( _mpi.mpi_initialized() ):
        return handleError(_mpe.mpe_describe_state(startevent, stopevent, description, color))
    else:
        raise mpeException, "Attempt to call %s before mpi.init!"%("mpi.describe_state")

class Log:
    def __init__(self, filename=str(time.time())):
        self.running = False
        self.status = "closed"
        
        self.init_log()
        self.filename = filename
        self.events = {}
        self.eventtypes = {}
        self.states = {}
        
    def init_log(self):
        self.errorcode = init_log()
        self.running = True
        self.status = "open"
        
    def start_log(self):
        self.errorcode = start_log()
        self.running = True

    def stop_log(self):
        self.errorcode = stop_log()
        self.running = False

    def describe_state(self, start, end, name="state name", color="black"):
        if( self.running ):
            if( self.status != "closed" ):
                if( not self.states.has_key( str(str(start)+str(end)) ) ):
                    self.states[ str(str(start)+str(end)) ] = (name,color)
                    self.errorcode = describe_state( start, end, name, color )
                else:
                    print "MPE Warning:  redefining state:",str(str(start)+str(end))
                    self.states[ str(str(start)+str(end)) ] = (name,color)
                    self.errorcode = describe_state( start, end, name, color )
            else:
                print "MPE Error: Logfile is closed."
        else:
            print "MPE Error: Logging is currently disabled (stopped)."

    def describe_event( self, event, name="event name", color="black" ):
        if (self.running):
            if (self.status!="closed"):
                if(not self.eventtypes.has_key(event)):
                    self.eventtypes[ event ] = (name,color)
                    self.errorcode = describe_event( event, name, color )
                else:
                    print "MPE Warning: redefining event:",event
                    self.eventtypes[ event ] = (name,color)
                    self.errorcode = describe_event( event, name, color )
            else:
                print "MPE Error: Logfile is closed."
        else:
            print "MPE Error: Logging is currently disabled (stopped)."

    def log_event( self, event, intdata, chardata ):
        if (self.running):
            if (self.status!="closed"):
                if(not self.events.has_key(event)):
                    self.events[ event ] = (intdata,chardata)
                    self.errorcode = log_event( event, intdata, chardata )
                else:
                    print "MPE Warning: redefining event:",event
                    self.events[ event ] = (intdata,chardata)
                    self.errorcode = log_event( event, intdata, chardata )
            else:
                print "MPE Error: Logfile is closed."
        else:
            print "MPE Error: Logging is currently disabled (stopped)."

    def displayEvents(self):
        print "-"*70
        print "Total # of Events:",len(self.events.keys())
        print "%10s%10s%50s"%("Event ID", "Int Data","Character Data")
        print "-"*70
        for key in self.events.keys():
            event = self.events[key]
            print "%10s%10s%50s"%(key, event[0],event[1])
        print "-"*70
        return self.events

    def displayStates(self):
        print "-"*70
        print "Total # of States:",len(self.states.keys())
        print "%10s%50s%10s"%("State ID", "Description","Color")
        print "-"*70
        for key in self.states.keys():
            event = self.states[key]
            print "%10s%50s%10s"%(key, event[0],event[1])
        print "-"*70
        return self.states

    def displayEventDescriptions(self):
        print "-"*70
        print "Total # of Event Types:",len(self.eventtypes.keys())
        print "%10s%50s%10s"%("Event Type", "Description", "Color")
        print "-"*70
        for key in self.eventtypes.keys():
            event = self.eventtypes[key]
            print "%10s%50s%10s"%(key, event[0],event[1])
        print "-"*70
        return self.eventtypes
        
            
    def finish_log( self, filename=None ):
        if (filename):
            self.filename = filename
        self.errorcode = finish_log( self.filename )
        self.running = False
        self.status = "closed"
        
