#SIM100 UGLY REQUEST WITH BYTE ORDER MOTOROLA- CURRENTLY ISNT DECODING

import pandas as pd
import cantools
from pprint import pprint
# import can_decoder
import binascii
import time
start=time.time()

#initialising dictionaries
byte1=[]
byte2=[]
byte3=[]
byte4=[]
byte5=[]
byte6=[]
byte7=[]
byte8=[]
id_lst=[]
signals_dict={
'DI_Button_Down_Pantograph': [],
'Fbk_H2_HVIL': [],
'Pantograph_DI_Top_Indicator': [],
'Charging_mode': [],
'Pantograph_DI_Bottom_Indicator': [],
'Pantograph_DI_Bottom_Indicator': [],
'B2V_BMSSta':[],
'B2V_FullChrg':[],
'EDN_state':[0]*100+[1]*81,
'Tst1ACok_A':[0]*100+[1]*81,
'V2B_ChargeCmd':[0]*100+[1]*81
}


#ASC part
read_file = pd.read_csv (r'C:\\Users\\ThinkPadA9\\Desktop\\Top secret\\python projects\\matlab\\ASC\\log_file.asc', skiprows=3, skipfooter=3, engine = 'python', sep=' ', usecols=[2,5,6,7,8,9,10,11,12,13], header=None)
# read_file.to_csv (r'C:\\Users\\ThinkPadA9\\Desktop\\Top secret\\python projects\\matlab\\ASC\\log_file.csv', index=None)
data_frame=read_file.iloc[:, lambda df: [2,3,4,5,6,7,8,9]]
id_frame=read_file.iloc[:, lambda df: [0]]

hexadecimal_type_data='x'+data_frame.astype(str)
# hexadecimal_type_id='0x'+id_frame.astype(str)

data_string=hexadecimal_type_data.convert_dtypes(convert_string=True)
# convert_id=hexadecimal_type_id.convert_dtypes(convert_string=True)

# print(hexadecimal_type_data)
# print(hexadecimal_type_id)

for id, row_id in id_frame.itertuples():
    row_id=row_id.replace('x','')
    row_id='0x'+row_id
    id_lst.append(row_id)
    
for data in data_string.itertuples(index=False):
    byte1.append(data[0])
    byte2.append(data[1])
    byte3.append(data[2])
    byte4.append(data[3])
    byte5.append(data[4])
    byte6.append(data[5])
    byte7.append(data[6])
    byte8.append(data[7])



def replace_nan(byte1,byte2,byte3,byte4,byte5,byte6,byte7,byte8):
    for i in range(0, len(byte1)):
        if byte1[i]=='xNone' or byte1[i]=='xnan' or byte1[i]=='NaN' or byte1[i]=='None':
            byte1[i]='x00'
        if byte2[i]=='xNone' or byte2[i]=='xnan' or isinstance(byte2[i], float)==True or byte2[i]=='None':
            byte2[i]='x00'
        if byte3[i]=='xNone' or byte3[i]=='xnan' or byte3[i]=='NaN' or byte3[i]=='None':
            byte3[i]='x00'
        if byte4[i]=='xNone' or byte4[i]=='xnan' or byte4[i]=='NaN' or byte4[i]=='None':
            byte4[i]='x00'
        if byte5[i]=='xNone' or byte5[i]=='xnan' or byte5[i]=='NaN' or byte5[i]=='None':
            byte5[i]='x00'
        if byte6[i]=='xNone' or byte6[i]=='xnan' or byte6[i]=='NaN' or byte6[i]=='None':
            byte6[i]='x00'
        if byte7[i]=='xNone' or byte7[i]=='xnan' or byte7[i]=='NaN' or byte7[i]=='None':
            byte7[i]='x00'
        if byte8[i]=='xNone' or byte8[i]=='xnan' or byte8[i]=='NaN' or byte8[i]=='None':
            byte8[i]='x00'
    return 0
    

replace_nan(byte1,byte2,byte3,byte4,byte5,byte6,byte7,byte8)



#DBC part
db = cantools.database.load_file('C:\\Users\\ThinkPadA9\\Desktop\\Top secret\\python projects\\matlab\\ASC\\Microvast_KAMAZ_12m_alarm.dbc', database_format='dbc', encoding='utf-8')

#Filling lists-values of important signals
for index in range(0, len(byte1)):
    try:
        decode=db.decode_message(int(id_lst[index],16), b'\%byte1[index]\%byte2[index]\%byte3[index]\%byte4[index]\%byte5[index]\%byte6[index],%byte7[index],%byte8[index]')
        # print(decode)
        # print(index)
        for key_name, key_value in decode.items():
            if key_name == 'Fbk_H2_HVIL':
                signals_dict[key_name].append(key_value)
            if key_name == 'DI_Button_Down_Pantograph':
                signals_dict[key_name].append(key_value)
            if key_name == 'Pantograph_DI_Top_Indicator':
                signals_dict[key_name].append(key_value)
            if key_name == 'Charging_mode':
                signals_dict[key_name].append(key_value)
            if key_name == 'Pantograph_DI_Bottom_Indicator':
                signals_dict[key_name].append(key_value)
            if key_name == 'B2V_BMSSta':
                signals_dict[key_name].append(key_value)
            if key_name == 'B2V_FullChrg':
                signals_dict[key_name].append(key_value)
    except(KeyError):
        # print('{} from log cant be found in dbc file'.format(id_lst[index]))
        # print(index)
        continue


#Showing signals dictionary
# print(signals_dict)


#Analysing logic EDN chart
error_edn=int

for index in range(0, len(signals_dict['B2V_BMSSta'])):
    if signals_dict['EDN_state'][index] == 1 and signals_dict['V2B_ChargeCmd'][index] == 1:
        if signals_dict['B2V_BMSSta'][index] != 2 and signals_dict['B2V_FullChrg'][index] != 0:
            if error_edn != 1:
                print('EDN is deactivated due to B2V_BMSSta is not in Charge mode and Battery SOC is FULL')
                error_edn=1
            
    else:
        if signals_dict['B2V_BMSSta'][index] != 2:
            if error_edn != 2:
                print('EDN is deactivated due to B2V_BMSSta is not in Charge mode')
                error_edn=2
            
        if signals_dict['B2V_FullChrg'][index] != 0:
            if error_edn != 3:
                print('EDN is deactivated due to Battery SOC is FULL')
                error_edn=3
            
# print(signals_dict['EDN_state'])
# print(signals_dict['B2V_BMSSta'])
# print(signals_dict['B2V_FullChrg'])
# print(signals_dict['V2B_ChargeCmd'])




#Counting time of scrypt
stop=time.time()
print('Evaluation time: '+str(stop-start))