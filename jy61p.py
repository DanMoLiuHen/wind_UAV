import time
import smbus

address=0x50
jy=smbus.SMBus(1)

def get_acc(jy):
    raw_accx=jy.read_i2c_block_data(address,0x34,2)
    raw_accy=jy.read_i2c_block_data(address,0x35,2)
    raw_accz=jy.read_i2c_block_data(address,0x36,2)

    k=16
    accx=(raw_accx[1]<<8|raw_accx[0])/32768*k
    accy=(raw_accy[1]<<8|raw_accy[0])/32768*k
    accz=(raw_accz[1]<<8|raw_accz[0])/32768*k

    if accx>=k:
        accx-=2*k
    if accy>=k:
        accy-=2*k
    if accz>=k:
        accz-=2*k

    return (accx,accy,accz)

def get_gyro(jy):
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

    return (gyx,gyy,gyz)

def get_angle(jy):
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

    return (angx,angy,angz)

def get_longitude(jy):
    raw_lgh=jy.read_i2c_block_data(address,0x4a,1)
    raw_lgl=jy.read_i2c_block_data(address,0x40,1)

    k=100
    lg=(raw_lgh[0]<<8|raw_lgl[0])/k
    return (lg)

while(1):
    print("Acc:",get_acc(jy))
    print("Gyro:",get_gyro(jy))
    print("Angle:",get_angle(jy))
    #print("longitude",get_longitude(jy))
    print('\n')
    time.sleep(0.2)
