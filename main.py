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

    #tmpfile = open("tmp.s0","w")
    #outtext(infile,tmpfile)

    if args.o:
        outfile = open(args.o,'w')
    else:
        outfile = open("out",'w')

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
            os.system('./c0-vm-cpp -a tmp.s0 out')
            os.remove('./tmp.s0')
    elif args.s:
        outtext(infile,outfile)

    infile.close()
    outfile.close()
