import math
from datetime import datetime

with open('C:\\Users\\pedro.mendonca\\Documents\\Voos\\tabelas\\teste.csv') as fileIn:
    trjFileIn = fileIn.readlines()

trjFileIn = [x.strip().split(';') for x in trjFileIn]
trjOut = []


def to_tait_bryan_angle(qr, qi, qj, qk):
    # roll (x-axis rotation)
    sinr_cosp = 2.0 * (qr * qi + qj * qk)
    cosr_cosp = 1.0 - 2.0 * (qi * qi + qj * qj)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    # pitch (y-axis rotation)
    sinp = 2.0 * (qr * qj - qk * qi)
    if math.fabs(sinp) >= 1:
        pitch = math.copysign(math.pi / 2, sinp)  # use 90 degrees if out of range
    else:
        pitch = math.asin(sinp)

    # yaw (z-axis rotation)
    siny_cosp = 2.0 * (qr * qk + qi * qj)
    cosy_cosp = 1.0 - 2.0 * (qj * qj + qk * qk)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return [str(roll), str(pitch), str(yaw)]


# -----------------------------------------
# Notas:
#
# 1: a.timestamp() - 315964800.0  => Converter UTC time stamp (Jan 1st, 1970, 00:00:00) para GPS timestamp
#                               Dec 31º, 1979, 23:59:42, na prática é Dezembro 1º 1980, 00:00:00 UTC,
#                              porque não está a ser tido em conta o  salto de segundos (leapsec) que neste momento é 18
#
# 2: a - 1000000000.0 => GPS Standard Time => definido no LAS standard como Adjusted Standard Time, (satellite GPS Time
#                        menos 1 x 10^9), mais pequeno do que 1 000 000 000 (mil milhões)
#
# -----------------------------------------
for line in trjFileIn[1:]:
    euler_angles = to_tait_bryan_angle(float(line[4]), float(line[5]), float(line[6]), float(line[7]))
    dateFormatF = "%Y-%m-%d %H:%M:%S.%f"
    dateFormatI = "%Y-%m-%d %H:%M:%S"
    a = line[0].strip('"')  # retirar as aspas "
    try:
        a = datetime.strptime(a, dateFormatF)  # converter para datetime object
    except:
        a = datetime.strptime(a, dateFormatI)  # converter para datetime object
    a = a.timestamp() - 315964800.0  # nota 1
    a = str(a - 1000000000.0)  # nota 2
    b = ' '.join(line[1:4])
    c = ' '.join(euler_angles)
    trjOut.append(a + " " + b + " " + c)

fileNum = 1
fileOut = open('trj_to_tscan' + '_' + str(fileNum) + '.txt', 'w')
gapSecLimit = 20
splitTrj = False
for idx, line in enumerate(trjOut[1:]):
    lineBefore = trjOut[idx]
    if math.fabs(float(line.split(' ')[0]) - float(lineBefore.split(' ')[0])) > gapSecLimit and splitTrj:
        fileNum += 1
        fileOut.close()
        fileOut = open('trj_to_tscan' + '_' + str(fileNum) + '.txt', 'w')
    else:
        fileOut.write(line + "\n")

fileOut.close()

# with open('trj_to_tscan.txt', 'w') as fileOut:
#    fileOut.writelines("%s\n" % l for l in trjOut)



