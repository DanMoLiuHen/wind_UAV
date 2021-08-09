import time
import smbus
import sys

address=0x50#设置地址
jy=smbus.SMBus(1)

def get_acc(jy):#读取三方向的加速度
    raw_accx=jy.read_i2c_block_data(address,0x34,2)#借助该函数读取数据块（共2字节），储存在列表中
    raw_accy=jy.read_i2c_block_data(address,0x35,2)#0x35是根据说明书中寄存器的地址
    raw_accz=jy.read_i2c_block_data(address,0x36,2)

    k=16#该部分根据说明书给出的计算方法算出相应值
    accx=(raw_accx[1]<<8|raw_accx[0])/32768*k
    accy=(raw_accy[1]<<8|raw_accy[0])/32768*k
    accz=(raw_accz[1]<<8|raw_accz[0])/32768*k
    if accx>=k:
        accx-=2*k
    if accy>=k:
        accy-=2*k
    if accz>=k:
        accz-=2*k

    return accx,accy,accz

def get_gyro(jy):#读取三方向的角速度
    raw_gyx=jy.read_i2c_block_data(address,0x37,2)
    raw_gyy=jy.read_i2c_block_data(address,0x38,2)
    raw_gyz=jy.read_i2c_block_data(address,0x39,2)
    k=2000
    gyx=(raw_gyx[1]<<8|raw_gyx[0])/32768*k
    gyy=(raw_gyy[1]<<8|raw_gyy[0])/32768*k
    gyz=(raw_gyz[1]<<8|raw_gyz[0])/32768*k

    if gyx>=k:
        gyx-=2*k
    if gyy>=k:
        gyy-=2*k
    if gyz>=k:
        gyz-=2*k

    return gyx,gyy,gyz

def get_angle(jy):#读取三方向的角度
    raw_angx=jy.read_i2c_block_data(address,0x3d,2)
    raw_angy=jy.read_i2c_block_data(address,0x3d,2)
    raw_angz=jy.read_i2c_block_data(address,0x3d,2)

    k=180
    angx=(raw_angx[1]<<8|raw_angx[0])/32768*k
    angy=(raw_angy[1]<<8|raw_angy[0])/32768*k
    angz=(raw_angz[1]<<8|raw_angz[0])/32768*k
    if angx>=k:
        angx-=2*k
    if angy>=k:
        angy-=2*k
    if angz>=k:
        angz-=2*k
    return angx,angy,angz

def main(jy):
    while(1):
        a1,a2,a3=get_acc(jy)
        w1,w2,w3=get_gyro(jy)
        ang1,ang2,ang3=get_angle(jy)
        with open("out.txt",'a',encoding="utf-8") as f:
            f.write(str(time.time())+str(',')+str(a1)+str(',')+str(a2)+str(',')+str(a3))
            f.write(str(',')+str(w1)+str(',')+str(w2)+str(',')+str(w3)+str(','))
            f.write(str(ang1)+str(',')+str(ang2)+str(',')+str(ang3))
            time.sleep(0.2)
            f.write(str('\n'))

main(jy)

#with open("out.txt",'w',encoding="utf-8") as f:
#    f.write(str(time.time()))
#    f.write(str(get_acc(jy)))
#    f.write(str(get_gyro(jy)))
#    f.write(str(get_angle(jy)))
#    time.sleep(0.2)
    
#while(1):
#    print("Acc:",get_acc(jy))
#    print("Gyro:",get_gyro(jy))
#    print("Angle:",get_angle(jy))
#    #print("longitude",get_longitude(jy))
#    print('\n')
#    time.sleep(0.2)
