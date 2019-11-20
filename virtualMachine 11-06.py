import sys
import array
text_file = open('q1_encr.txt', 'r')
char_list = list(text_file.read())
textPosition=0
text_file.close()
end_of_text=False
end_of_work=False
regs = bytearray(16)
commands_position=0

with open("decryptor.bin", "rb") as binaryfile :
    prog_mem = bytearray(binaryfile.read())
def extractBits(num,k,p): 
     #k - extract 'k' bits from num
     #p - position from which to start
     binary = bin(num) 
     binary = binary[2:] 
     while (len(binary)%4) != 0:
         binary='0'+binary
     end = len(binary) - p
     start = end - k + 1
     kBitSubStr = binary[start : end+1] 
     answer = int(kBitSubStr,2)
     return answer
#yra funkcija kuri leidzia taikyti kiekvienam masyvo elementui veiksma
#           vvvvvvvvvvvv
    
mem = list(map(lambda x: hex(x)[2:],prog_mem))
#print(mem)
def INC(ryx):
    Rx=int(ryx, 16)
    regs[Rx]=int(regs[Rx])+1
def DEC(ryx):
    Rx=int(ryx, 16)
    regs[Rx]=int(regs[Rx])-1
def MOV(ryx):
    Rx=int(ryx, 16)
    Rx=extractBits(Rx, 4, 1)
    if int(ryx, 16) < 16:
        Ry=0
    else:
        Ry=int(ryx, 16)
        Ry=extractBits(Ry, 4, 5)
    regs[Rx]=regs[Ry]
def MOVC(ryx):
    ryx=int(ryx,16)
    regs[0]=ryx
def LSL(ryx):
    Rx=int(ryx, 16)
    Rx=extractBits(Rx, 4, 1)
    regs[Rx]=regs[Rx]<<1
def LSR(ryx):
    Rx=int(ryx, 16)
    Rx=extractBits(Rx, 4, 1)
    regs[Rx]=regs[Rx]>>1
def JMP(ryx):
    global commands_position
    ryx=int(ryx, 16)
    commands_position=commands_position+ryx
    if commands_position > 256:
        commands_position = commands_position - 256
def JZ(ryx):
    if end_of_text == False:
        global commands_position
        ryx=int(ryx, 16)
        commands_position=commands_position+ryx
        if commands_position > 256:
            commands_position = commands_position - 256
def JNZ(ryx):
    if end_of_text == True:
        global commands_position
        ryx=int(ryx, 16)
        commands_position=commands_position+ryx
        if commands_position > 256:
            commands_position = commands_position - 256
def JFE(ryx):
    global commands_position
    if end_of_text == True:
        ryx=int(ryx, 16)
        commands_position=commands_position+ryx
        if commands_position > 256:
            commands_position = commands_position - 256
    else:
        commands_position=commands_position+2
def RET():
    global end_of_work
    end_of_work=True
def ADD(ryx):
    Rx=int(ryx, 16)
    Rx=extractBits(Rx, 4, 1)
    if int(ryx, 16) < 16:
        Ry=0
    else:
        Ry=int(ryx, 16)
        Ry=extractBits(Ry, 4, 5)
    regs[Rx]=int(regs[Rx])+int(regs[Ry])
def SUB(ryx):
    Rx=int(ryx, 16)
    Rx=extractBits(Rx, 4, 1)
    if int(ryx, 16) < 16:
        Ry=0
    else:
        Ry=int(ryx, 16)
        Ry=extractBits(Ry, 4, 5)
    regs[Rx]=int(regs[Rx])-int(regs[Ry])
def XOR(ryx):
    Rx=int(ryx, 16)
    Rx=extractBits(Rx, 4, 1)
    if int(ryx, 16) < 16:
        Ry=0
    else:
        Ry=int(ryx, 16)
        Ry=extractBits(Ry, 4, 5)
    regs[Rx]=int(regs[Rx])^int(regs[Ry])
def OR(ryx):
    Rx=int(ryx, 16)
    Rx=extractBits(Rx, 4, 1)
    if int(ryx, 16) < 16:
        Ry=0
    else:
        Ry=int(ryx, 16)
        Ry=extractBits(Ry, 4, 5)
    regs[Rx]=int(regs[Rx])|int(regs[Ry])
def IN(ryx):
    global end_of_text
    if textPosition==len(char_list):
        end_of_text=True
    else:
         Rx=int(ryx)
         Rx=extractBits(Rx, 4, 1)
         numberOfSim = ord(char_list[textPosition])
         regs[Rx]=numberOfSim
         if (textPosition+1)==len(char_list):
            end_of_text=True
def OUT(ryx):
    Rx=int(ryx)
    f = open("output.txt", "a")
    f.write(chr(regs[Rx]))
    f.close()

def commands(command,ryx):
        if command == "1":
            INC(ryx)
        elif command == "2":
            DEC(ryx)
        elif command == "3":
            MOV(ryx)
        elif command == "4":
            MOVC(ryx)
        elif command == "5":
            LSL(ryx)
        elif command == "6":
            LSR(ryx)
        elif command == "7":
            JMP(ryx) 
        elif command == "8":
            JZ(ryx)
        elif command == "9":
            JNZ(ryx)
        elif command == "a":
            JFE(ryx)
        elif command == "b":
            RET()
        elif command == "c":
            ADD(ryx)
        elif command == "d":
            SUB(ryx)
        elif command == "e":
            XOR(ryx)
        elif command == "f":
            OR(ryx)
        elif command == "10":
            IN(ryx)
        elif command == "11":
            OUT(ryx) 
print('\n')
print("Kom;Ryx")

while end_of_work==False:
    if (commands_position + 1) >= len(mem):
        print("out of bin file range")
        end_of_work=True
    else:
        command= mem[commands_position]
        ryx = mem[commands_position+1]
        print(command, ryx)
        commands(command,ryx)
        if command=="10":
            textPosition+=1
        if command != "7" and command != "8" and command != "9" and command != "a":
            commands_position=commands_position+2


#https://www.w3resource.com/python/python-bytes.php for printing
