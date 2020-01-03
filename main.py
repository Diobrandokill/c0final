import dataStruct
from dataStruct import const
from dataStruct import VT
from dataStruct import InstructionStream
from dataStruct import SymbolTable
from tokennizer import tokennizer
from analyser import analyser
import sys
import argparse
import struct
import os 
import test
'''
# debugging
infile = open("in.c0",'r')
TK = tokennizer(infile)
TK.scan()
# 打印词法分析结果
TK.printAllVt()
#打印词法分析错误
for error in TK.errors:
    error.printMsg()
#语法及语义分析
symbolTable = SymbolTable()
instructionStream = InstructionStream()
AN = analyser(infile,TK.head,TK.pointer, symbolTable, instructionStream)
AN.scan()
#打印语法分析结果
#AN.printAllVn()
#打印语法及语义分析错误
for error in AN.errors:
    error.printMsg()
'''

def to_utf(number):
    return  chr(int(number,16))

def operator_process(ins,file):
    # bipush
    if ins.instruction == 1:
        op1 = str("{:#02}".format(int(ins.operator1)))
        outfile.write(to_utf(op1[-2:]))
    # ipush
    elif ins.instruction == 2:
        op1 = str("{:#08}".format(int(ins.operator1)))
        for i in range(0,len(op1),2):
            outfile.write(to_utf(op1[i:i+2]))
    # popn
    elif ins.instruction == 6:
        op1 = str("{:#08}".format(int(ins.operator1)))
        for i in range(0,len(op1),2):
            outfile.write(to_utf(op1[i:i+2]))
    # loadc
    elif ins.instruction == 9:
        op1 = str("{:#04}".format(int(ins.operator1)))
        for i in range(0,len(op1),2):
            outfile.write(to_utf(op1[i:i+2]))
    # loada
    elif ins.instruction == 10:
        op1 = str("{:#04}".format(int(ins.operator1)))
        op2 = str("{:#08}".format(int(ins.operator2)))
        for i in range(0,len(op1),2):
            outfile.write(to_utf(op1[i:i+2]))
        for i in range(0,len(op2),2):
            outfile.write(to_utf(op2[i:i+2]))
    # snew
    elif ins.instruction == 12:
        op1 = str("{:#08}".format(int(ins.operator1)))
        for i in range(0,len(op1),2):
            outfile.write(to_utf(op1[i:i+2]))
    # je jne jl jge jg jle
    elif ins.instruction in (113,119):
        op1 = str("{:#04}".format(int(ins.operator1)))
        for i in range(0,len(op1),2):
            outfile.write(to_utf(op1[i:i+2]))
    # call
    elif ins.instruction == 128:
        op1 = str("{:#04}".format(int(ins.operator1)))
        for i in range(0,len(op1),2):
            outfile.write(to_utf(op1[i:i+2]))

def outtext(infile,outfile):
    #词法分析
    TK = tokennizer(infile)
    TK.scan()

    # 打印词法分析结果
    #TK.printAllVt()

    #打印词法分析错误
    for error in TK.errors:
        error.printMsg()

    #语法及语义分析
    symbolTable = SymbolTable()
    instructionStream = InstructionStream()
    AN = analyser(infile,TK.head,TK.pointer, symbolTable, instructionStream)
    AN.scan()

    
    #打印语法及语义分析错误
    for error in AN.errors:
        error.printMsg()

    #打印语法分析结果
    #AN.printAllVn()

    #打印.constant
    AN.symbolTable.print_const_Table(outfile)
    #AN.print_var_table()
    #打印.start
    instructionStream.printstart(AN,outfile)
    #打印.function
    AN.symbolTable.printfunction(outfile)
    #打印.F
    instructionStream.printAllInstructions(AN,outfile)
'''
def outbinary(infile,outfile):
    #词法分析
    TK = tokennizer(infile)
    TK.scan()
    # 打印词法分析结果
    #TK.printAllVt()
    #打印词法分析错误
    for error in TK.errors:
        error.printMsg()
    #语法及语义分析
    symbolTable = SymbolTable()
    instructionStream = InstructionStream()
    AN = analyser(infile,TK.head,TK.pointer, symbolTable, instructionStream)
    AN.scan()
    #打印语法及语义分析错误
    for error in AN.errors:
        error.printMsg()

    # magic
    outfile.write('\x43' + '\x30' + '\x3a' + '\x29')
    # version
    outfile.write('\x00' + '\x00' + '\x00' + '\x01')
    # constants_count
    count = "{:#04}".format(len(AN.symbolTable.constant))
    outfile.write(to_utf(count[0:2]) + to_utf(count[2:4]))
    # constants
    # string -> 0 int -> 1 double ->2
    for constant in AN.symbolTable.constant:
        if constant.type == 'I':
            outfile.write('\x01')
            count = '{:08x}'.format(int(constant.value))
            outfile.write(to_utf(count[-8:-6]) + to_utf(count[-6:-4]))
            outfile.write(to_utf(count[-4:-2]) + to_utf(count[-2:]))
        elif constant.type == 'S':
            outfile.write('\x00')
            count = "{:04x}".format(len(constant.value))
            outfile.write(to_utf(count[-4:-2]) + to_utf(count[-2:]))
            for i in range(0,len(constant.value)):
                count = str("{:02x}".format(ord(constant.value[i])))
                outfile.write(to_utf(count[-2:]))
        elif constant.type == 'D':
            outfile.write('\x02')
            for i in range(2,len(constant.value),2):
                #print(constant.value[i:i+2])
                #print(to_utf(constant.value[i:i+2]))
                if constant.value[i:i+2] == "f0":
                    outfile.write('\xF0')
                else:
                    outfile.write(to_utf(constant.value[i:i+2]))
    
    # start_code
    no = 0
    for instruction in instructionStream.instructions:
        if len(instruction.lab) <= 0 :
            no += 1
        else:
            break
    count = str("{:#04}".format(no))
    outfile.write(to_utf(count[-4:-2]) + to_utf(count[-2:]))
    for i in range(0,no):
        instruction = instructionStream.instructions[i]
        ins = str("{:#02}".format(instruction.instruction))
        outfile.write(to_utf(ins[-2:]))
        operator_process(instruction,outfile)
    # functions_count
    func_count = str("{:#04}".format(len(AN.symbolTable.funcs)))
    outfile.write(to_utf(func_count[-4:-2]) + to_utf(func_count[-2:]))
    for i in range(0,len(AN.symbolTable.funcs)):
        func = AN.symbolTable.funcs[i]
        tmp = str("{:#04}".format(func.number))
        outfile.write(to_utf(tmp[-4:-2]) + to_utf(tmp[-2:]))
        tmp = str("{:#04}".format(func.slot))
        outfile.write(to_utf(tmp[-4:-2]) + to_utf(tmp[-2:]))
        tmp = str("{:#04}".format(func.level))
        outfile.write(to_utf(tmp[-4:-2]) + to_utf(tmp[-2:]))
        no = 0
        ins_count = 0
        flag = 0
        mark = 0
        for j in range(0,len(instructionStream.instructions)):
            if ins_count == i+1:
                if flag == 0:
                    mark = j-1
                    flag = 1
                if len(instructionStream.instructions[j].lab) <= 0 :
                    no += 1
                else:
                    ins_count += 1
            else:
                if len(instructionStream.instructions[j].lab) > 0:
                    ins_count += 1
        count = str("{:#04}".format(no+1))
        outfile.write(to_utf(count[-4:-2]) + to_utf(count[-2:]))
        for k in range(mark,mark + no + 1):
            instruction = instructionStream.instructions[k]
            ins = str("{:#02}".format(instruction.instruction))
            outfile.write(to_utf(count[-2:]))
            operator_process(instruction,outfile)
'''
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help = "将输入的 c0 源代码翻译为文本汇编文件",action="store_true") 
    parser.add_argument("-c", help = "将输入的 c0 源代码翻译为二进制目标文件",action="store_true")
    parser.add_argument("-i", help = "设置输入文件")
    parser.add_argument("-o", help = "输出到指定的文件")
    args = parser.parse_args()

    infile = None
    outfile = None

    if args.i:
        infile = open(args.i,'r')
    else:
        infile = open("in.c0",'r')

    tmpfile = open("tmp.s0","w")
    outtext(infile,tmpfile)

    if args.o:
        outfile = open(args.o,'w')
    else:
        outfile = open("out.o0",'w')

    if args.c:
        if args.o:
            tmpfile = open("tmp.s0",'w')
            outtext(infile,tmpfile)
            tmpfile.close()
            os.system('./c0-vm-cpp -a tmp.s0 ' + args.o)
            os.remove('./tmp.s0')
        else:
            tmpfile = open("tmp.s0",'w')
            outtext(infile,tmpfile)
            tmpfile.close()
            os.system('./c0-vm-cpp -a tmp.s0 tmp.o0')
            os.remove('./tmp.s0')
    if args.s:
        outtext(infile,outfile)


