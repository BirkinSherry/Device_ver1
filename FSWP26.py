import pyvisa
import time
import csv
import numpy
import schedule


class Order_List:
    def __init__(self):
        self.multiview_tab = 'DISPlay:ATAB ON'     #分4屏显示开
        self.multiview_rec = 'DISPlay:ATAB OFF'    #单屏显示最近
        self.set_ref_level = 'DISP:TRAC1:Y:RLEV 20'   #改变TRACE的参考电平
        self.list = 'INST:LIST?'    
        self.select_pn = " INST:SEL 'Phase Noise 1' "
        self.create_pn = " INST:CRE PNO, 'Phase Noise 1' "
        self.select_spec = " INST:SEL 'Spectrum 1' "
        self.create_spec = " INST:CRE SAN, 'Spectrum 1' "
        self.del_pn = "INST:DEL 'Phase Noise 1'"
        self.del_spec = "INST:DEL 'Spectrum 1'"
        self.set_fre_start = ' SENS:FREQ:START 499.7MHz '
        self.set_fre_stop = 'SENS:FREQ:STOP 500.1MHz'
        self.set_att_auto_off = 'INPut:ATT:AUTO OFF'   #衰减自动设置关
        self.set_att_auto_on = 'INPut:ATT:AUTO ON'   #衰减自动设置开
        self.set_att_20 = 'INPut:ATT 20'
        self.create_marker1 = 'CALC:MARK1 ON'  #新建一个mark
        self.auto_peak = 'CALCulate1:MARKer1:MAXimum:AUTO ON'
        self.set_rbw = 'SENSE:BANDwidth:RESolution 100Hz'
        self.get_y = 'CALCulate:MARKer1:Y?'
        self.get_x = 'CALCulate:MARKer1:X?'
        self.set_fre_start_100Hz = 'SENS:FREQ:START 100Hz'
        self.set_fre_stop_1MHz = 'SENS:FREQ:STOP 1MHz'
        self.set_pn_bw_rat_3 = 'LIST:BWID:RAT 3'
        self.set_pn_xfactor_200 = 'SWEep:XFACtor 200'
        self.set_init_mes ='INIT:IMM'   #初始化一次测量=runsingle   'INIT:IMM;*OPC?'       performing  measurements
        self.set_pn_spot_aoff = 'CALCulate:SNOise:AOFF'   #关闭所有相噪测量点，包括系统和用户
        self.conti_meas = 'INIT:CONT ON'    #设置连续测试
        self.get_decades_x = 'CALCulate:SNOise:DECades:X?'       
        self.get_decades_y = 'CALCulate1:SNOise1:TRACe1:DECades:Y?'
        self.set_power_mode_vol = 'SOUR:VOLT:POW:LEV:MODE VOLT'            #选择电压模式或者电流模式
        self.set_power_supply_vol_amp_on = 'SOUR:VOLT:POW:LEV ON'          #选择supply打开
        self.set_power_dc_on = 'SOUR:VOLT ON'                              #选择DCPower打开
        self.set_power_supply_vol_amp_data = 'SOUR:VOLT:POW:LEV:AMPL 9'    #设置输出电压 9V
    
        def list(self):
            return self.list

class FSWP26(Order_List):
    def __init__(self):
        Order_List.__init__(self)
        self.rm = pyvisa.ResourceManager()
        self.vi = None
        self.delay_s = 2
        self.delay_5s = 5
        self.delay_10s = 10

    def Link(self, Address):
        self.vi = self.rm.open_resource(Address)
        time.sleep(self.delay_s)

    def Reset(self):
        self.vi.write("*RST; *CLS")
        time.sleep(self.delay_s)

    def UnLink(self):
        self.rm.close()
        time.sleep(self.delay_s)

    def Query(self, Order):
        data = self.vi.query(Order)
        print(data)
        #print("The type  is:",type(data))
        time.sleep(self.delay_s)
        return data

    def Writer(self, Order):
        self.vi.write(Order)
        time.sleep(0.1)
        self.vi.query_delay:1

    #新建测试通道      PNO：Phase Noise 1  相噪窗口 /SAN：Spectrum 1  频谱窗口    PAGE391  available channel types and default channel names   " INST:CRE PNO, 'Phase Noise 1' "
    def CreateChannel(self, channel, name):
        self.vi.write( 'INST:CRE ' + channel + ', '+  '\'' +str(name) + '\'')
        #print('INST:CRE ' + channel + ', '+  '\'' +str(name) + '\'')

    #选择通道  " INST:SEL 'Spectrum 1' "
    def SelectChannel(self, name):
        self.vi.write('INST:SEL ' +  '\'' +str(name) + '\'')
    #设置起始频率   ' SENS:FREQ:START 499.7MHz '
    def SetFreq(self, start, stop):
        self.vi.write('SENS:FREQ:START ' + str(start))
        self.vi.write('SENS:FREQ:STOP ' + str(stop))
    #设置衰减自动设置  'INPut:ATT:AUTO OFF' 
    def SetAttState(self, state):
        self.vi.write('INPut:ATT:AUTO ' + str(state))

    #设置衰减量  'INPut:ATT 20'
    def SetAttLev(self, level):
        self.vi.write('INPut:ATT ' + str(level))

    #设置TRACE的参考电平   'DISP:TRAC:Y:RLEV 20'
    def SetTraceRefLevel(self, trace, level):
        self.vi.write('DISP:TRAC' + str(trace) + ':Y:RLEV ' + str(level))

    #新建一个marker  'CALC:MARK1 ON'
    def CreateMarker(self, marker, state):
        self.vi.write('CALC:MARK' + str(marker) + ' ' + str(state))

    #设置marker的search方式  'CALCulate1:MARKer1:MAXimum:AUTO ON'
    def SetMarkerSearch(self, trace, marker, parameter, way, state):
        self.vi.write('CALCulate' + str(trace) + ':MARKer' + str(marker) + ':' +str(parameter) + ':' + str(way) +  ' ' + str(state))

    #Noise Configuration 
    #设置分辨率带宽 'SENSE:BANDwidth:RESolution 100Hz'
    def SetBandwidthRes(self,  frequency):
        self.vi.write('SENSE:BANDwidth:RESolution ' + str(frequency))

    #设置每10次方得相噪分辨率带宽比例 'LIST:BWID:RAT 3'
    def SetBandwidthResRat(self, ratio):
        self.vi.write('SENSE:LIST:BWID:RES:RAT ' + str(ratio))

    #设置互相关因数  'SWEep:XFACtor 200'
    def SetXFactor(self, factor):
        self.vi.write('SENSE:SWEep:XFACtor ' + str(factor))

    # 获取标记的Y值
    def GetMarkerY(self, Marker):
        data = self.vi.query("CALCulate:MARKer" + str(Marker) + ':Y?')    #15.7 marke page529
        time.sleep(self.delay_s)
        return float(data)
        
     # 获取标记的X值
    def GetMarkerX(self, Marker):
        data = self.vi.query("CALCulate:MARKer" + str(Marker) + ':X?')
        time.sleep(self.delay_s)
        return float(data)
       
    # 获取10倍数的X方向的值
    def GetDecadesSpotNoiseX(self):    #default unit:Hz
        data = self.vi.query(self.get_decades_x)
        time.sleep(self.delay_s)
        return data
        
    # 获取10倍数的Y方向的值
    def GetDecadesSpotNoiseY(self):    #default unit:dBc/Hz
        data = self.vi.query(self.get_decades_y)
        time.sleep(self.delay_s) 
        return data
    
    #设置DCconfig输出模式 'SOUR:VOLT:POW:LEV:MODE VOLT' 
    def DcConfigMode(self, mode):
        self.vi.write('SOUR:VOLT:POW:LEV:MODE ' + str(mode))

    #设置DC输出电压  'SOUR:VOLT:POW:LEV:AMPL 9'
    def DcConfigLevel(self, level):
        self.vi.write('SOUR:VOLT:POW:LEV:AMPL ' + str(level))

    #设置DC输出supply打开 'SOUR:VOLT:POW:LEV ON' 
    def DcConfigSupply(self, state):
        self.vi.write('SOUR:VOLT:POW:LEV ' + str(state))

    #设置DC输出开关 'SOUR:VOLT ON'
    def DcConfigDcOn(self, state):
        self.vi.write('SOUR:VOLT ' + str(state))

     # 字符串转list      
    def StrToList(self, rslt):
        self_list = rslt.split(',')
        for i in range(len(self_list)):
            self_list[i] = self_list[i]
            #self_list[i] = self_list[i][1: -1]
        print(self_list)
        return self_list
    
    # 字符串转list且以float格式返回list
    def StrToListFloat(self, rslt):
        self_list = rslt.split(',')
        for i in range(len(self_list)):
            self_list[i] = float(self_list[i])
        print(self_list)
        return self_list

    # 初始化频谱窗口
    def InitFSWP26Spec(self):
        self.Link('TCPIP0::169.254.59.150::hislip0::INSTR')
        self.Reset()
        #self.StrToList(rslt = self.Query(self.list))   #获取通道列表
        self.CreateChannel(channel = 'SAN', name = 'Spectrum 1')     #self.Writer(self.create_spec)     #新建频谱窗口
        self.CreateChannel(channel = 'PNO', name = 'Phase Noise 1')      #self.Writer(self.create_pn)   #新建相噪窗口
        self.SelectChannel(name = 'Spectrum 1')                 #self.Writer(self.select_spec)          #选择频谱窗口
        self.SetFreq(start = '499.7MHz ', stop = '500.1MHz')   #self.Writer(self.set_fre_start)  #self.Writer(self.set_fre_stop)    #设置频率起始范围
        self.SetAttState(state= 'OFF')                      #self.Writer(self.set_att_auto_off)    
        self.SetAttLev(level= 20)                           #self.Writer(self.set_att_20)               #设置衰减20db
        self.SetTraceRefLevel(trace= 1, level= 20)          #self.Writer(self.set_ref_level)            #设置参考电平
        self.CreateMarker(marker= 1, state= 'ON')           #self.Writer(self.create_marker1)           #新建marker1
        self.SetMarkerSearch(trace= 1, marker= 1, parameter= 'Maximum', way= 'auto', state= 'ON')       #self.Writer(self.auto_peak)          #自动跟踪峰值
        self.SetBandwidthRes(frequency= '100Hz')            #self.Writer(self.set_rbw)            #设置分辨率    
        self.DcConfigMode(mode= 'VOLT')                     #self.Writer(self.set_power_mode_vol)                                #选择电压模式或者电流模式
        self.DcConfigLevel(level= 9)                        #self.Writer(self.set_power_supply_vol_amp_data)                     #设置输出电压 9V
        self.DcConfigSupply(state= 'ON')                    #self.Writer(self.set_power_supply_vol_amp_on)                       #选择supply打开
        self.DcConfigDcOn(state= 'ON')                      #self.Writer(self.set_power_dc_on)                                   #选择DCPower打开
        time.sleep(self.delay_10s) 
    #初始化相噪窗口
    def InitFSWP26PN(self):
        self.SelectChannel(name = 'Phase Noise 1')       #self.Writer(self.select_pn)
        time.sleep(self.delay_s)
        self.SetFreq(start = '100Hz ', stop = '1MHz')    #self.Writer(self.set_fre_start_100Hz)  #self.Writer(self.set_fre_stop_1MHz)
        self.SetBandwidthResRat(ratio= 3)                #self.Writer(self.set_pn_bw_rat_3)
        self.SetXFactor(factor= 200)                     #self.Writer(self.set_pn_xfactor_200)
        self.Writer(self.set_init_mes)                    #初始化测试
    #获取频谱数据
    def GetSpecData(self):
            spec_data_list = []
            spec_data_list.append(str(self.GetMarkerX(1)))      #获取标记点X坐标
            spec_data_list.append(str(self.GetMarkerY(1)))      #获取标记点Y坐标
            print(spec_data_list)
            return spec_data_list
    #获取相噪数据
    def GetPNData(self):
            pn_data_list = []
            pn_data_list.extend(self.StrToListFloat(rslt = self.GetDecadesSpotNoiseX()))    #获取相噪X方向10倍数的数据
            pn_data_list.extend(self.StrToListFloat(rslt = self.GetDecadesSpotNoiseY()))    #获取相噪Y方向10倍数的数据
            return pn_data_list

    def InitFSWP26Meas(self):
        self.InitFSWP26Spec()
                    
        spec_data_list = []
        spec_data_list.extend(self.GetSpecData())
        time.sleep(self.delay_s)

        self.InitFSWP26PN()

        pn_data_list = []
        pn_data_list.extend(self.GetPNData())


        time_list = []
        time_list = time.localtime()

        time_str_list = []
        time_str = time.strftime("%Y-%m-%d %H:%M:%S",time_list)
        time_str_list = [time_str]


        data_list = []
        data_list.extend(spec_data_list)
        data_list.extend(pn_data_list)
        data_list.extend(time_str_list)

"""
def InitFSWP26Meas():
    device_a = FSWP26()
    device_a.InitFSWP26Spec()
    '''
    device_a.Link('TCPIP0::169.254.59.150::hislip0::INSTR')
    device_a.Reset()
    device_a.StrToList(rslt = device_a.Query(device_a.list))
    device_a.init_FSWP26()
    '''
                                  
    spec_data_list = []
    spec_data_list.extend(device_a.GetSpecData())
    time.sleep(device_a.delay_s)

    '''
    device_a.Writer(device_a.select_pn)
    device_a.Writer(device_a.set_fre_start_100Hz)
    device_a.Writer(device_a.set_fre_stop_1MHz)
    device_a.Writer(device_a.set_pn_bw_rat_3)
    device_a.Writer(device_a.set_pn_xfactor_200)
    device_a.Writer(device_a.set_init_mes)
    #    a = device_a.StrToList(rslt = device_a.Query(device_a.get_decades_x))
    #    b = device_a.StrToList(rslt = device_a.Query(device_a.get_decades_y))
    '''
    device_a.InitFSWP26PN()
    #    a = device_a.StrToListFloat(rslt = device_a.Query(device_a.get_decades_x))
    #    b = device_a.StrToListFloat(rslt = device_a.Query(device_a.get_decades_y))
    
    #    a = device_a.StrToListFloat(rslt = device_a.GetDecadesSpotNoiseX())
    #    b = device_a.StrToListFloat(rslt = device_a.GetDecadesSpotNoiseY())

    pn_data_list = []
    pn_data_list.extend(device_a.GetPNData())
    #    pn_data_list.extend(device_a.StrToListFloat(rslt = device_a.GetDecadesSpotNoiseX()))
    #    pn_data_list.extend(device_a.StrToListFloat(rslt = device_a.GetDecadesSpotNoiseY()))

    time_list = []
    time_list = time.localtime()

    time_str_list = []
    time_str = time.strftime("%Y-%m-%d %H:%M:%S",time_list)
    time_str_list = [time_str]


    data_list = []
    data_list.extend(spec_data_list)
    data_list.extend(pn_data_list)
    data_list.extend(time_str_list)


    #    pn_data_list_quote = ["'" + item + "'" for item in pn_data_list]

    #    print(type(str(device_a.StrToListFloat(rslt = device_a.Query(device_a.get_decades_x)))))
    '''
    with open('file.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data_list)

    device_a.UnLink()
    '''

    '''
    with open('file.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data_list:
            writer.writerow(data_list(row))
    '''
    '''
    while True:
        DEVICE_A.Query('*IDN?', 1)
        DEVICE_A.Delay(3000)
    ''' 
    #   raise ValueError
"""

#InitFSWP26Meas()

pn = FSWP26()
pn.InitFSWP26Meas()
