import os
import shutil
import time

def Simulate(sim_dir,sim_file):
    sim = LTSpice(sim_file=sim_file, sim_dir=sim_dir )
    sim.run_simulation()
    sim.pars_log()
    return sim.get_data()


class ConverterData:
    PinAVG = None
    PoutRMS = None
    UinRMS = None
    IinRMS = None
    UoutRMS = None
    IoutRMS = None
    UinRippel = None
    IinRippel = None
    UoutRippel = None
    IoutRippel = None
    
    def __init__(self,name):
        self.name = name
    def getValues(self):
        return (self.efficiency_percent,self.IoutRippel*1E+3, self.UoutRippel*1E+3,
                self.IoutRMS,self.UoutRMS,self.IinRippel)
    @property
    def output_power(self):
        return self.PoutRMS
    @property
    def input_power(self):
        return self.PinAVG
    @property
    def efficiency(self):
        return self.output_power / self.input_power
    @property
    def efficiency_percent(self):
        return self.efficiency*100.0
    def __str__(self):
        self.toPrint = 'Data printed from converter %s\n'%self.name
        return self.toPrint


class ConverterSimulation:
    def __init__(self,converter_dir,converter_file,data = None):
        self.converter_file = converter_file
        self.converter_dir = converter_dir
        if data is None:
            self.data = ConverterData(converter_file.split('.')[0])
        else:
            self.data = data
        self.simulation = open( os.path.normpath(converter_dir+'\\'+converter_file),"r",encoding="utf-8").read()
    def set_value(self,identifier,value):
        self.simulation = self.simulation.replace(identifier,str(value))
    def save_simulation(self,name=None,directory=None):
        if(name is not None):
            self.converter_file = name
        else :
            self.converter_file = 'new_'+self.converter_file
        if(directory is not None):
            shutil.rmtree(self.converter_dir+'\\'+self.converter_file.split('.')[0]  , ignore_errors=False, onerror=None)
            self.converter_dir = directory
        file_sim = open( os.path.normpath(self.converter_dir+'\\'+self.converter_file),"w",encoding="utf-8")
        file_sim.write(self.simulation)
        file_sim.close()
        self.new_simulation = (self.converter_file, self.converter_dir)
        return self.new_simulation    
    def pars_log(self):
        self._log = open(os.path.normpath(self.converter_dir+'\\' +self.converter_file.split('.')[0]+'\\'+self.converter_file.split('.')[0]+'.log' ),encoding="utf-8").read()
        # self.read_values()
        src = self.converter_dir+'\\'+self.converter_file.split('.')[0]+'\\'
        filename = self.converter_file.split('.')[0]+'.raw'
        filename2 = self.converter_file.split('.')[0]+'.asc'
        dst = self.converter_dir
        shutil.move(os.path.join(src, filename), os.path.join(dst, filename))# https://stackoverflow.com/questions/31813504/move-and-replace-if-same-file-name-already-exists
        shutil.move(os.path.join(src, filename2), os.path.join(dst, filename2))
        shutil.rmtree(self.converter_dir+'\\'+self.converter_file.split('.')[0]  , ignore_errors=False, onerror=None)
        print('pars finished!')
        
    def search_position(self):
        self.pos_uinrms = self._log.find('uinrms')
        self.pos_iinrms = self._log.find('iinrms')
        self.pos_uoutrms = self._log.find('uoutrms')
        self.pos_ioutrms = self._log.find('ioutrms')

        self.pos_ioutrippel = self._log.find('ioutrippel')
        self.pos_uoutrippel = self._log.find('uoutrippel')
        self.pos_iinrippel = self._log.find('iinrippel')
        self.pos_uinrippel = self._log.find('uinrippel')
        
        self.pos_pinavg= self._log.find('pinavg')
        self.pos_poutrms= self._log.find('poutrms')        
        
    def read_values(self):
        self.search_position()

    def get_data(self):
        return self.data 
    
class LTSpice:
    
    def __init__(self,sim_dir,sim_file,sim_script='LTspice\\run_LTspice.cmd'):
        self.sim_file = sim_file
        self.sim_dir = sim_dir
        self.sim_script = sim_script
    
    def run_simulation(self):
        cp_sim = os.path.normpath(self.sim_dir+'\\'+self.sim_file.split('.')[0])       
        print(cp_sim)
        os.makedirs(cp_sim)
        
        shutil.move(os.path.normpath(self.sim_dir+'\\'+self.sim_file),cp_sim)       
                
        run_cmd ='& "C:\Program Files\LTC\LTspiceXVII\XVIIx64.exe" -Run -b "'+os.path.normpath(cp_sim+'/'+self.sim_file)+'"'
        run_cmd = self.sim_script+' "'+os.path.normpath(cp_sim+'\\'+self.sim_file)+'"'
        print(run_cmd)
        os.system(run_cmd)
        print('Simulation finished!')
        
