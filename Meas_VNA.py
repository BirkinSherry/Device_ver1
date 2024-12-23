# KeySight M9373A
# Dexter   2022-09-27
import pyvisa
from enum import Enum
import csv
import time

class M9373A:

    # trace_format = Enum('trace_format', (
    #                                     'NLINEAR',
    #                                     'MLOGARITHMIC',
    #                                     'PHASE',
    #                                     'UPHASE',
    #                                     'IMAGINARY',
    #                                     'REAL',
    #                                     'POLAR',
    #                                     'SMITH',
    #                                     'SADMITTANCE',
    #                                     'SWR',
    #                                     'GDELAY',
    #                                     'KELVIN',
    #                                     'FAHRENHEIT',
    #                                     'CELSIUS'
    #                                     ))

    # 属性
    #rm = pyvisa.ResourceManager()
    #print(rm.list_resources())
    #vi = rm.open_resource(rm.list_resources()[1])
    #vi = rm.open_resource('TCPIP0::169.254.59.160::hislip0::INSTR')

    #
    frequency_center = 0                    # 设置中心频率，单位Hz
    frequency_span = 0                      # 设置频率宽度，单位Hz
    frequency_start = 0                     # 设置起始频率，单位Hz
    frequency_stop = 0                      # 设置终止频率，单位Hz
    sweep_points = 0                        # 频率点数
    if_bandwidth = 0                        # 中频带宽，单位Hz

    # SYSTEM
    active_channel = 0                      # 当前活动的通道
    active_measurement = ''                 # 当前活动的测量
    current_measurement = []                # 当前测量
    current_windows = []                    # 当前窗口
    current_traces = []                     # 当前轨迹

    # 定义私有属性,私有属性在类外部无法直接进行访问

    __weight = 0

    # 定义构造方法
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        print(self.rm.list_resources())
        self.vi = None
        self.delay_s = 2
        #pass
        # self.vi.write("*rst; status:preset; *cls")

        #self.sweep_pionts = 2
        #self.get_frequency_center(1)
        #self.get_frequency_span(1)
        #self.get_frequency_start(1)
        #self.get_frequency_stop(1)
        #self.get_if_bandwidth(1)
        #self.get_sweep_pionts(1)

    # 定义方法
    #
    def Link(self, Address):
        self.vi = self.rm.open_resource(Address)
        time.sleep(self.delay_s)

    # 设置中心频率，单位Hz
    def set_frequency_center(self, channel, frequency_center):
        self.frequency_center = frequency_center
        self.vi.write('SENS' + str(channel) + ':FREQ:CENTER ' + str(frequency_center))

    # 获取中心频率，单位Hz
    def get_frequency_center(self, channel):
        self.frequency_center = self.vi.query_ascii_values('SENS' + str(channel) + ':FREQ:CENTER?')
        return self.frequency_center

    # 设置频率宽度，单位Hz
    def set_frequency_span(self, channel, frequency_span):
        self.frequency_span = frequency_span
        self.vi.write('SENS' + str(channel) + ':FREQ:SPAN ' + str(frequency_span))

    # 获取频率宽度，单位Hz
    def get_frequency_span(self, channel):
        self.frequency_span = self.vi.query_ascii_values('SENS' + str(channel) + ':FREQ:SPAN?')
        return self.frequency_span

    # 设置起始频率，单位Hz
    def set_frequency_start(self, channel, frequency_start):
        self.frequency_start = frequency_start
        self.vi.write('SENS' + str(channel) + ':FREQ:START ' + str(frequency_start))

    # 获取起始频率，单位Hz
    def get_frequency_start(self, channel):
        self.frequency_start = self.vi.query_ascii_values('SENS' + str(channel) + ':FREQ:START?')
        return self.frequency_start

    # 设置终止频率，单位Hz
    def set_frequency_stop(self, channel, frequency_stop):
        self.frequency_stop = frequency_stop
        self.vi.write('SENS' + str(channel) + ':FREQ:STOP ' + str(frequency_stop))

    # 获取终止频率，单位Hz
    def get_frequency_stop(self, channel) -> "Nothing to see here":
        self.frequency_stop = self.vi.query_ascii_values('SENS' + str(channel) + ':FREQ:STOP?')
        return self.frequency_stop

    # 设置中频带宽，单位Hz
    def set_if_bandwidth(self, channel, if_bandwidth):
        self.if_bandwidth = if_bandwidth
        self.vi.write('SENS' + str(channel) + ':BWID ' + str(if_bandwidth))

    # 获取中频带宽，单位Hz
    def get_if_bandwidth(self, channel):
        self.if_bandwidth = self.vi.query_ascii_values('SENS' + str(channel) + ':BWID?')
        return self.if_bandwidth

    # 设置扫频点数
    def set_sweep_pionts(self, channel, sweep_pionts):
        self.sweep_pionts = sweep_pionts
        self.vi.write('SENS' + str(channel) + ':SWE:POIN ' + str(sweep_pionts))

    # 获取扫频点数
    def get_sweep_pionts(self, channel):
        self.sweep_pionts = self.vi.query_ascii_values('SENS' + str(channel) + ':SWE:POIN?')
        return self.sweep_pionts

    # 获取活动通道： SYSTEM:ACTIVE:CHANNEL?
    def get_active_channel(self):
        self.active_channel = self.vi.query_ascii_values('SYST:ACT:CHAN?')
        return self.active_channel

    # 获取活动测量： SYSTEM:ACTIVE:MEASUREMENT?
    def get_active_measurement(self):
        self.active_measurement = str(self.vi.query('SYST:ACT:MEAS?'))
        return self.active_measurement

    # 获取当前通道的测量： CALCULATE1:PARAMETER:CATALOG?
    def get_current_measurement(self):
        self.current_measurement = self.vi.query('CALCULATE1:PARAMETER:CATALOG?')
        return self.current_measurement

    # 获取当前窗口： DISPLAY:CATALOG?，return string
    def get_current_windows(self):
        self.current_windows = str.split(str.strip(self.vi.query('DISPLAY:CATALOG?'), '"\n'), ',')
        return self.current_windows

    # 获取当前窗口中的轨迹： DISPLAY:WINDOW1:CATALOG?，return string
    def get_current_traces(self):
        self.current_traces = str.split(str.strip(self.vi.query('DISPLAY:WINDOW1:CATALOG?'), '"\n'), ',')
        return self.current_traces

    # 新建测量 CALCULATE1:PARAMETER:DEFINE:EXT 'MEAS1', 'S11'
    def create_measurements(self, window, channel, trace, measurement, s_parameter):
        self.vi.write('CALCULATE' + str(channel) + ':PARAMETER:DEFINE:EXT \'' + str(measurement) + '\', \'' + str(s_parameter) + '\' ')
        self.vi.write('DISPLAY:WINDOW' + str(window) + ':TRACE' + str(trace) + ':FEED \'' + str(measurement) + '\' ')

    def preset(self):
        self.vi.write('SYSTEM:PRESET')

    def get_inf(self):
        inf = self.vi.query('*IDN?')
        return inf

    # 删除所有测量
    def delete_all_measurements(self):
        self.vi.write('CALC:PAR:DEL:ALL')

    # 删除指定测量
    def delete_measurements(self, channel, measurement):
        self.vi.write('CALC' + str(channel) + ':PAR:DEL \'' + measurement + '\'')

    # 按测量名称选择测量
    def select_measurements(self, channel, measurement):
        self.vi.write('CALCULATE' + str(channel) + ':PARAMETER:SELECT \'' + measurement + '\'')

    # 按轨迹名称选择测量
    def select_trace(self, channel, trace):
        self.vi.write('CALCULATE' + str(channel) + ':PARAMETER:MNUMBER:SELECT ' + str(trace))

    # 从WINDOWS中选择轨迹
    def select_trace_window(self, window, trace):
        self.vi.write('DISPLAY:WINDOW' + str(window) + ':TRACE' + str(trace) + 'SELECT')

    # 关闭选择测量的所有标记
    def markers_off(self, channel):
        self.vi.write('CALCULATE:' + str(channel) + 'MARK:AOFF')

    # 设置标记
    def set_marker(self, channel, marker, state):
        self.vi.write('CALCULATE' + str(channel) + ':MARKER' + str(marker) + ' ' + state)

    def set_marker_x(self, channel, marker, x):
        self.vi.write('CALCULATE' + str(channel) + ':MARKER' + str(marker) + ':X ' + str(x))

    # 获取标记的X值
    def get_marker_x(self, channel, marker):
        mark_x = self.vi.query('CALCULATE' + str(channel) + ':MARKER' + str(marker) + ':X?')
        return mark_x

    # 获取标记的Y值  CALCulate<cnum>:MEASure<mnum>:MARKer<mkr>:Y?
    def get_marker_y(self, channel, measurement, marker):
        mark_y = str.split(str.strip(self.vi.query('CALCULATE' + str(channel) + ':MEASure' + str(measurement) +':MARKER' + str(marker) + ':Y?'), '"\n'), ',')
        return mark_y

    # 获取标记的带宽值  CALCulate<cnum>:MEASure<mnum>:MARKer<mkr>:BWIDth:DATA?

    def get_marker_width(self, channel, measurement, marker):
        mark_width = str.split(str.strip(self.vi.query('CALCULATE' + str(channel) + ':MEASure' + str(measurement) +':MARKER' + str(marker) + ':BWIDth:DATA?'), '"\n'), ',')
        return mark_width


    # 设置标记分析带宽
    def set_marker_bw(self, channel, value):
        self.vi.write('CALCULATE' + str(channel) + ':MARKER:BWID ' + str(value))

    # 获取标记分析带宽
    def get_marker_bw(self, channel):
        mark_bw = str.split(str.strip(self.vi.query('CALCULATE' + str(channel) + ':MARKER:BWIDTH?'), '"\n'), ',')
        return mark_bw

    # 设置标记跟踪状态
    def set_marker_tracking(self, channel, marker, state):
        self.vi.write('CALCULATE' + str(channel) + ':MARKER' + str(marker) + ':FUNCTION:TRACKING ' + state)

    # 设置Y轴刻度
    def set_trace_scale_div(self, window, trace, div):
        self.vi.write('DISPLAY:WINDOW' + str(window) + ':TRACE' + str(trace) + ':Y:PDIV ' + str(div))

    # 获取Y轴刻度
    def get_trace_scale_div(self, window, trace):
        div = self.vi.query('DISPLAY:WINDOW' + str(window) + ':TRACE' + str(trace) + ':Y:PDIV?')
        return div

    # 设置Y轴参考
    def set_trace_scale_reference_level(self, window, trace, level):
        self.vi.write('DISPLAY:WINDOW' + str(window) + ':TRACE' + str(trace) + ':Y:RLEVEL ' + str(level))

    # 获取Y轴参考
    def get_trace_scale_reference_level(self, window, trace):
        level = self.vi.query('DISPLAY:WINDOW' + str(window) + ':TRACE' + str(trace) + ':Y:RLEVEL?')
        return level

    # 设置Y轴参考位置
    def set_trace_scale_reference_position(self, window, trace, position):
        self.vi.write('DISPLAY:WINDOW' + str(window) + ':TRACE' + str(trace) + ':Y:RPOSITION ' + str(position))

    # 获取Y轴参考位置
    def get_trace_scale_reference_position(self, window, trace):
        position = self.vi.query('DISPLAY:WINDOW' + str(window) + ':TRACE' + str(trace) + ':Y:RPOSITION?')
        return position
    
    #设置存储文件格式     MMEMory:STORe:TRACe:FORMat:SNP <char>
    def set_save_file_format(self, format):
        self.vi.write('MMEM:STOR:TRAC:FORM:SNP' + str(format) )
        time.sleep(self.delay_s)

    #计算存储SNP文件   
    def save_snp_file(self, file_name):
        #self.vi.write('CALC1:MEAS:DATA:SNP:PORTs:Save ' + '\'1,2\'' + ',' + '\'C:\\Users\\hust_p5000b\\Desktop\\file\\MyData.s2p\'')
        self.vi.write('CALC1:MEAS:DATA:SNP:PORTs:Save ' + '\'1,2\'' + ',' + '\'C:\\Users\\hust_p5000b\\Desktop\\file\\' + str(file_name) + '.s2p\'')
        return print('SNP文件保存成功')

    # 设置窗口排列
    def arrange_window(self, arrange):
        if arrange == 1:        # tiles existing windows
            txt = 'TILE'
        elif arrange == 2:      # overlaps existing windows
            txt = 'CASCADE'
        elif arrange == 3:      # all traces placed in 1 window
            txt = 'OVERLAY'
        elif arrange == 4:      # 2 windows
            txt = 'STACK'
        elif arrange == 5:      # 3 windows
            txt = 'SPLIT'
        elif arrange == 6:      # 4 windows
            txt = 'QUAD'
        else:
            pass
        self.vi.write('DISPLAY:ARR ' + txt)

    # 设置窗口排列
    def measurement_format(self, channel, format):
        self.vi.write('CALCULATE' + str(channel) + ':FORMAT ' + format)

    def marker_format(self, channel, marker, format):
        self.vi.write('CALCULATE' + str(channel) + ':MARKER' + str(marker) + ':FORMAT ' + format)

    def saveSnpFile(self, fileName):
        self.vi.write('CALC:PAR:DEF ')

    def getSnpData(self, channel, marker, format):
        self.vi.write('CALCULATE' + str(channel) + ':MARKER' + str(marker) + ':FORMAT ' + format)
  
    def StrToListFloat(self, rslt):
        self_list = rslt.split(',')

        for i in range(len(self_list)):
            self_list[i] = float(self_list[i])

        print(self_list)

        return self_list
    
    def StrToList(self, rslt):
        self_list = rslt.split(',')
        #self_list_1 = rslt.split(',')

        for i in range(len(self_list)):
            self_list[i] = self_list[i]
            #self_list[i] = self_list[i][1: -1]
            #self_list_1[i] = self_list[i][2:-2]

        print(self_list)
        #print(self_list_1)

        return self_list
    
    def VNAInit(self):
        print('Preset.')
        print('0', self.Link('TCPIP0::169.254.59.160::hislip0::INSTR'))
        print('1', self.get_inf())
        print('2', self.get_frequency_center(1))
        print('3', int(self.get_active_channel()[0]))
        print('4', self.get_active_measurement())
        print('5', self.get_current_measurement())
        print('6', self.get_current_windows())
        print('7', self.get_current_traces())

        self.select_measurements(1, 'CH1_S11_1')
        print('8', self.get_active_measurement())

        print('9', float(self.get_marker_width(1, 2, 1)[1]))

        data_list = []
        data_list = self.get_marker_width(1, 2, 1)

        for i in range(len(data_list)):
            data_list[i] = float(data_list[i])

        print('10',data_list)

        return data_list
    

def init_measurement():
    # vna.preset()
    print('Preset.')

    # vna.delete_all_measurements()
    # vna.arrange_window(6)
    # # window 1   trace 1
    # vna.create_measurements(1, 1, 1, 'IL', 'S21')
    # vna.set_trace_scale_div(1, 1, 10)
    # vna.set_trace_scale_reference_level(1, 1, 0)
    # vna.set_trace_scale_reference_position(1, 1, 9)
    #
    # vna.select_trace(1, 1)
    # vna.set_marker(1, 1, 'ON')
    # vna.set_marker(1, 2, 'ON')
    # vna.set_marker(1, 3, 'ON')
    # vna.set_marker(1, 4, 'ON')
    # # vna.set_marker(1, 5, 'ON')
    #
    # vna.set_marker_x(1, 1, 360e6)
    # vna.set_marker_x(1, 2, 370e6)
    # vna.set_marker_x(1, 3, 380e6)
    # vna.set_marker_x(1, 4, 390e6)
    # # vna.set_marker_x(1, 5, 400e6)
    #
    # vna.set_marker_bw(1, -3)
    # vna.set_marker_tracking(1, 1, 'ON')
    #
    # # window 1   trace 2
    # vna.create_measurements(1, 1, 2, 'IL2', 'S21')
    # vna.set_trace_scale_div(1, 2, 10)
    # vna.set_trace_scale_reference_level(1, 2, 0)
    # vna.set_trace_scale_reference_position(1, 2, 9)
    # vna.select_trace(1, 2)
    # vna.set_marker(1, 1, 'ON')
    # vna.set_marker(1, 2, 'ON')
    # vna.set_marker(1, 3, 'ON')
    # vna.set_marker(1, 4, 'ON')
    # # vna.set_marker(1, 5, 'ON')
    # vna.marker_format
    # vna.set_marker_x(1, 1, 360e6)
    # vna.set_marker_x(1, 2, 370e6)
    # vna.set_marker_x(1, 3, 380e6)
    # vna.set_marker_x(1, 4, 390e6)
    # # vna.set_marker_x(1, 5, 400e6)
    #
    # vna.set_marker_bw(1, -1)
    # vna.set_marker_tracking(1, 1, 'ON')
    #
    # # window 3   trace 3
    # vna.create_measurements(3, 1, 3, 'SWR1', 'S11')
    # vna.select_trace(1, 3)
    # vna.measurement_format(1, 'SWR')
    # vna.set_trace_scale_div(3, 3, 1)
    # vna.set_trace_scale_reference_level(3, 3, 1)
    # vna.set_trace_scale_reference_position(3, 3, 0)
    #
    #
    # # window 3   trace 4
    # vna.create_measurements(3, 1, 4, 'SWR2', 'S22')
    # vna.select_trace(1, 4)
    # vna.measurement_format(1, 'SWR')
    # vna.set_trace_scale_div(3, 4, 1)
    # vna.set_trace_scale_reference_level(3, 4, 1)
    # vna.set_trace_scale_reference_position(3, 4, 0)
    #
    # # window 2   trace 1
    # vna.create_measurements(2, 1, 5, 'IL3', 'S21')
    # vna.set_trace_scale_div(2, 5, 10)
    # vna.set_trace_scale_reference_level(2, 5, 0)
    # vna.set_trace_scale_reference_position(2, 5, 9)
    #
    # vna.select_trace(1, 5)
    # vna.set_marker(1, 1, 'ON')
    # vna.set_marker(1, 2, 'ON')
    # vna.set_marker(1, 3, 'ON')
    # vna.set_marker(1, 4, 'ON')
    #
    #
    # vna.set_marker_x(1, 1, 382.33e6)
    # vna.set_marker_x(1, 2, 390.08e6)
    # vna.set_marker_x(1, 3, 391.08e6)
    # vna.set_marker_x(1, 4, 398.83e6)
    #
    # # window 4   trace 6
    # vna.create_measurements(4, 1, 6, 'phase', 'S11')
    # vna.select_trace(1, 6)
    # vna.measurement_format(1, 'SMITH')
    # vna.set_marker(1, 1, 'ON')
    # vna.set_marker(1, 2, 'ON')
    # vna.set_marker(1, 3, 'ON')
    # vna.set_marker(1, 4, 'ON')
    #
    # vna.marker_format(1, 1, 'PHASE')
    # vna.marker_format(1, 2, 'PHASE')
    # vna.marker_format(1, 3, 'PHASE')
    # vna.marker_format(1, 4, 'PHASE')
    #
    # vna.set_marker_x(1, 1, 225e6)
    # vna.set_marker_x(1, 2, 373.59e6)
    # vna.set_marker_x(1, 3, 407e6)
    # vna.set_marker_x(1, 4, 400e6)
    #
    #
    # vna.set_frequency_center(1, 500e6)
    # vna.set_frequency_span(1, 20e6)
    # vna.set_if_bandwidth(1, 10000)
    # vna.set_sweep_pionts(1, 5001)

    print('1', vna.get_inf())
    print('2', vna.get_frequency_center(1))
    print('3', int(vna.get_active_channel()[0]))
    print('4', vna.get_active_measurement())
    print('5', vna.get_current_measurement())
    print('6', vna.get_current_windows())
    print('7', vna.get_current_traces())

    vna.select_measurements(1, 'CH1_S11_1')
    print('8', vna.get_active_measurement())

    print('9', float(vna.get_marker_width(1, 2, 1)[1]))

    data_list = []
    data_list = vna.get_marker_width(1, 2, 1)

    for i in range(len(data_list)):
        data_list[i] = float(data_list[i])

    print('10.5',data_list)
   # print('11', vna.vi.query_ascii_values("CALC1:MEAS2:DATA:FDATA?"))

    with open('file.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data_list)

#vna = M9373A()
#vna.VNAInit()
