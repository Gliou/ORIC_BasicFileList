#
#           ORIC BASIC FILE VIEWER
# by GliouCNR©70
#
#

#import time
import sys
import os

from tableau_oric import tableau_conversion_hexbasic
from color import colors

code_basic = ''

#verb = False
def verbose(txt):
    if verb == True:
        print(txt,end='')

#test si existence d'un argument (le nom du fichier)

#test si l'argument 1 est -v
#if sys.argv[1] == '-v':
#    print('OBFV Oric Basic File Viewer V0.1')
#    print('by GliouCNR©70')
#    exit()

#test l'argument 2
#if len(sys.argv) >2 and (sys.argv[2]) == '-l':
#    verb = True
#if len(sys.argv) >2 and (sys.argv[2]) != '-l':
#    print(colors.fg.red,'ERROR: Bad option',colors.reset)
#    exit()

#test .tap program
file, ext = os.path.splitext(sys.argv[2])
if ext != '.tap':
    print(colors.fg.red,'ERROR: not a .tap file',colors.reset)
    exit()

file_name = sys.argv[2]    
#test l'existance du fichier
try:
    open_file = open(file_name,'rb')
    while True:
        chunk = open_file.read()             #récupère les données
        if not chunk:
#            print('ERROR: canot read file')
            break
        code_basic = chunk.hex()        #et génère le code HEX
    open_file.close()
except:
    print(colors.fg.red,'ERROR: No such file or directory: ',"'",file_name,"'",colors.reset)
    exit()

code_basic = code_basic.upper()         #tout mettre en majuscule

#vérification présence d'au moins 3 octets x16
val_code_basic = code_basic[:6]
if val_code_basic != '161616':
    print(colors.fg.red,'ERROR: Not a Oric program, bad  ',colors.reset)
    exit()

#préparation du code à partir du premier 00 début du code Basic Oric à l'adresse 0x0500
while val_code_basic != '24':           #supprime les premiers octets d'amorce 0x16
    val_code_basic = code_basic[:2]     #jusqu à l'octet 0x24
    code_basic = code_basic[2:]         #supprime l'octet 0x24
# vérification pgm ORIC BASIC
if code_basic[4] != '0':
    print(colors.fg.red,'Error: Not a BASIC program',colors.reset)
    exit()
code_basic = code_basic[6:]             #supprime les 8 octets de codage BASIC ASM AUTO
code_basic = code_basic[2:]             #supprime 1 octet inutilisé
code_basic = code_basic[4:]             #supprime adresse de fin
code_basic = code_basic[4:]             #supprime adresse de début
code_basic = code_basic[2:]             #supprime 1 octet inutilisé



#préparation du code -> supprime les octets du nom du pgm
val_code_basic = code_basic[:2]
while val_code_basic != '00':
    code_basic = code_basic[2:]
    val_code_basic = code_basic[:2]

# open file in write mode
file_name = file + '.txt'          #créer fichier .txt
open_file = open(file_name,'w+')

#exit()
# main
#def main():
while  len(code_basic)>8:
        if code_basic[:4] == '0000':
            break
        val_code_basic = code_basic[:2]
        if val_code_basic == '00':
            code_basic = code_basic[6:]
            num_ligne= code_basic[2] + code_basic[3] + code_basic[:2]
            num_ligne= str(int(num_ligne,16))+' '
            verbose(num_ligne)
            open_file.write(num_ligne)
            code_basic = code_basic[2:]
        while True:
            code_basic = code_basic[2:]
            val_code_basic = code_basic[:2]
            for i in range(0,len(tableau_conversion_hexbasic)):
                if tableau_conversion_hexbasic[i][0] == val_code_basic:
                    instruction_basic = tableau_conversion_hexbasic[i][1]
                    verbose(instruction_basic)
                    open_file.write(instruction_basic)
                    code_basic = code_basic[2:]
                    val_code_basic = code_basic[:2]
            if val_code_basic == '00':
                break
            try:
                val_code_basic = bytes.fromhex(val_code_basic)
                val_code_basic = val_code_basic.decode('ASCII')
                verbose(val_code_basic)
                open_file.write(val_code_basic)
            except:
                val_code_basic = val_code_basic.hex().upper()
                for i in range(0,len(tableau_conversion_hexbasic)):
                    if tableau_conversion_hexbasic[i][0] == val_code_basic:
                        instruction_basic = tableau_conversion_hexbasic[i][1]
                        verbose(instruction_basic)
                        open_file.write(instruction_basic)
        verbose('\n')
        open_file.write('\n')
verbose('\n')
verbose('\n')
open_file.close
print('OBFV Oric Basic File Viewer V0.1')
print('by GliouCNR©70')
print('--------------------------------')
print('file name :',colors.bg.green,file_name,colors.reset,'create')
print('--------------------------------')
exit()

        