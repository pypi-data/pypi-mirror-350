
import queue, multiprocessing as mp

import tango
from tango.server import Device, device_property, attribute, command, pipe
import fandango
from fandango.tango import *
from fandango.linos import shell_command

from fandango.dynamic import DynamicDS

class Task(threading.Thread):
    def __init__(self, command):
        super().__init__()
        self.command = command
        self.result = None
        self.started = 0
    def run(self):
        try:
            self.started = time.time()
            self.result = subprocess.run(self.command,shell=True,capture_output=True)
            print('task finished')
        except Exception as e:
            self.result = e
            print('task failed')
    def is_done(self):
        self.started and not self.is_alive()
    def is_failed(self):
        self.is_done() and isinstance(self.result,Exception)
        
    def get_result(self):
        if self.is_done():
            if not self.is_failed():
                return self.result.stdout
            else:
                return self.result
        else:
            return False
        
        
class Task2():
    pass

class ScriptDS(DynamicDS,Device):
    """
    This device will execute an script in a sub-process every time Execute()
    command is called.

    Execute() can be polled, Condition property can be used to add additional conditions 
    (e.g. (NOW - START) > 3600 to ensure that it is not executed more than once per hour)
    
    If RunningTime exceeds TimeoutSeconds, state will switch to FAULT
    """
   
    DynamicAttributes = device_property(dtype=tango.DevVarStringArray)
    Condition = device_property(dtype=str)
    TimeoutSeconds = device_property(dtype=int,default_value=600)
    #Script = device_property(dtype=str)
    Scripts = device_property(dtype=tango.DevVarStringArray)
    
    Result = attribute(dtype=str)
    RunningTime = attribute(dtype=int)
    ExecutionTime = attribute(dtype=int)
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #self.process = None
        #self.ctx = mp.get_context('spawn')
        self.processes = fandango.CaselessDict()
        self.queue = self.ctx.Queue()           
    
    def init_device(self,*args,**kwargs):
        super().init_device(*args,**kwargs)
        self.tstart = 0
        self.trun = 0
        self.texec = 0    
        self.check = True
        self.set_state(tango.DevState.STANDBY)
        self.last_result = ''
        
    def delete_device(self,*args,**kwargs):
        pass
    
    @staticmethod
    def run_script(qout,args):
        print('Running!')
        import fandango.linos
        r = fandango.linos.shell_command(args)
        print(r)
        qout.put((now(),r))
        
    def read_RunningTime(self):
        return self.trun
    
    def read_ExecutionTime(self):
        return self.texec
        
    def read_Result(self):
        return self.last_result
    
    def state_machine(self):
        self.checkCondition()
        if not self.process or not self.process.is_alive():
            if self.check:
                state = tango.DevState.STANDBY
            else:
                state = tango.DevState.DISABLE
            self.trun = 0
            
        else:
            self.trun = now()-self.tstart
            if self.TimeoutSeconds and self.trun > self.TimeoutSeconds:
                state = tango.DevState.FAULT
            else:
                state = tango.DevState.RUNNING
            
        status = 'State is {}\n'.format(state)
        status += ('Script executed {} seconds ago, execution took {} seconds'
            .format(self.tstart and now()-self.tstart, self.trun or self.texec))
        self.debug_stream(str(state)+':'+status)
        self.set_state(state),self.set_status(status)
        
    def checkCondition(self):
        return not self.Condition or eval(self.Condition,globals(),
                {'NOW':now(),'START':self.tstart})
        
    @command(polling_period=1000,dtype_out=bool)
    def Update(self):
        try:
            t,self.last_result = self.queue.get(False)
            self.texec = t-self.tstart
            self.trun = 0
            #self.tstart = 0
            
        except queue.Empty:
            #self.info_stream('nothing in queue')
            pass
        except:
            self.traceback.print_exc()
            #self.warn_stream(traceback.format_exc())
            
        self.state_machine()
        return self.check
        
    #@command(dtype_in=None)
    #def Execute(self):
        #if (self.get_state() == tango.DevState.RUNNING
            #or (self.process and self.process.is_alive())):
            #s = 'Previous task still running'
            #self.error_stream(s)
            #raise Exception(s)
        
        #if not self.checkCondition():
            #raise Exception('Execution not allowed by Condition')

        #self.process = self.ctx.Process(
            #target = self.run_script,
            #args=(self.queue, self.Script)
            #)
        #self.info_stream('Execute:'+self.Script)
        #self.tstart = now()
        #self.set_state(tango.DevState.RUNNING)
        #self.process.start()
    
    @command(dtype_in=str)
    def Execute(self,script):
        raise Exception('Not Implemented Yet!')
               
    def always_executed_hook(self,*args):
        self.state_machine()
    
if __name__ == "__main__":
     ScriptDS.run_server()
