import argparse
#定义所有常量
import struct

class ConstDefine:
    # 运算符定义
    EQ = 1          # ==
    LE = 2          # <=
    LT = 3          # <
    GE = 4          # >=
    GT = 5          # >
    NE = 6          # !=
    PLUS = 7        # +
    MINUS = 8       # -
    STAR = 9        # *
    SLASH = 10      # /         
    B_SLASH = 11    # \  

    # 数据类型定义
    
    CHAR_LITERAL = 12
    DOUBLE_LITERAL = 13

    STRING_LITERAL = 14
    INTEGER_LITERAL = 15 
    HEX_LITERAL = 16

    #保留字定义
    IF = 21         
    ELSE = 22
    WHILE = 23
    CONST = 24
    VOID = 25
    STRUCT = 26
    RETURN = 27
    PRINT = 28
    SCAN = 29
    INT = 30
    CHAR = 31
    DOUBLE = 32

    SWITCH = 33
    CASE = 34
    DEFAULT = 35
    FOR = 36
    DO = 37
    BREAK = 38
    CONTINUE = 39
    

    #特殊符号定义
    L_PARENTHESIS = 41      # (
    R_PARENTHESIS = 42      # )
    L_BRACKET = 43          # [
    R_BRACKET = 44          # ]
    L_BRACE = 45            # {
    R_BRACE = 46            # }
    COMMA = 47              # ,
    SEMICOLON = 48          # ;
    ASSIGN = 49             # =
    EXCLAMATION = 50        # !
    COLON = 51              # :  
    S_QUATATION = 52        # '
    D_QUATATION = 53        # "
    EOF = 54     

    #标识符类型定义
    ID = 61                 
    RESERVE = 62
    ANNOTATION = 63

    #Vn类型定义
    EMPTY = 100
    C0PROGRAM = 101       # <C0-program> ✅
    VAR_DEC = 102       # <variable-declaration> ✅
    CON_DEC = 103       # <const-declaration> ✅
    INIT_DEC = 104      # <init-declarator> ✅
    INIT = 105          # <initializer> ✅
                           
    FUNC_DEF = 106      # <function-definition> ✅
    PARA_CLA = 107      # <parameter-clause> ✅
    PARA_DEC_LIST = 108 # <parameter-declaration-list> ✅
    PARA_DEC = 109      # <parameter-declaration> ✅
    COM_STATE = 110     # <compound-statement> ✅
    STAT_SEQ = 111      # <statement-seq> ✅
    STAT = 112          # <statement> ✅

    COND_STATE = 113    # <condition-statement> ✅ 🚗
    CONDITION = 114     # <condition> ✅ 🚗
    LABE_STATE = 115    # <labeled-statement> ❌
    LOOP_STATE = 116    # <loop-statement> ✅ 🚗
    FOR_INIT = 117      # <for-init-statement> ❌
    FOR_UPDATE = 118    # <for-update-expression> ❌
    JUMP_STATE = 119    # <jump-statement> ❌
    RET_STATE = 120     # <return-statement> ✅
    SCAN_STATE = 121    # <scan-statement> ✅ 🚗
    PRINT_STATE = 122   # <print-statement> ✅ 🚗
    PRINT_LIST = 123    # <printable-list> ✅ 🚗
    PRINTABLE = 124     # <printable> ✅ 🚗
    ASSIGN_EXP = 125    # <assignment-expression> ✅
    FUNC_CALL =  126    # <function-call> ✅
    EXP_LIST = 127      # <expression-list> ✅
    EXP = 128           # <expressioin> ✅
    MUL_EXP = 129       # <multiplicative-expression> ✅
    CAST_EXP = 130      # <cast-expression> ✅
    UNARY_EXP = 131     # <unary-expression> ✅
    PRIM_EXP = 132      # <primary-expression> ✅
    MAIN_FUNC = 133     # 用来识别主函数 ✅

const = ConstDefine

reservers = {
    'const':const.CONST,
    'void':const.VOID,
    'int':const.INT,
    'char':const.CHAR,
    'double':const.DOUBLE,
    'struct':const.STRUCT,
    'if':const.IF,
    'else':const.ELSE,
    'switch':const.SWITCH,
    'case':const.CASE,
    'default':const.DEFAULT,
    'while':const.WHILE,
    'for':const.FOR,
    'do':const.DO,
    'print':const.PRINT,
    'scan':const.SCAN,
    'return':const.RETURN
}


# 定义V类型，作为终结符和非终结符的基类
class  V:
    def __init__(self, vtype):
        # V类型
        self.vtype = vtype
    # 判断当前实例是否是指定类型
    def isType(self, vtype):
        return self.vtype == vtype
    def isEmpty(self):
        return self.vtype == const.EMPTY
    def isVT(self):
        return self.vtype < 100
    def isVN(self):
        return self.vtype >= 100
    # 判断当前单词是否是<加法运算符>
    def isAdditiveOperator(self):
        return self.vtype == const.PLUS or self.vtype == const.MINUS
    # 判断当前单词是否是<乘法运算符>
    def isMultiplicativeOperator(self):
        return self.vtype == const.STAR or self.vtype == const.SLASH
    # 判断当前单词是否是<关系运算符>
    def isRelationOperator(self):
        return self.vtype == const.LT or self.vtype == const.LE \
               or self.vtype == const.GT or self.vtype == const.GE \
               or self.vtype == const.NE or self.vtype == const.EQ
    # 判断当前单词是否是<（>
    def isL_Parenthesis(self):
        return self.vtype == const.L_PARENTHESIS
    # 判断当前单词是否是<)>
    def isR_Parenthesis(self):
        return self.vtype == const.R_PARENTHESIS
    # 判断当前单词是否是<{>
    def isL_Brace(self):
        return self.vtype == const.L_BRACE
    # 判断当前单词是否是<}>
    def isR_Brace(self):
        return self.vtype == const.R_BRACE
    # 判断当前单词是否是<,> 逗号
    def isComma(self):
        return self.vtype == const.COMMA
    # 判断当前单词是否是<;> 分号
    def isSemicolon(self):
        return self.vtype == const.SEMICOLON
    # 判断当前单词是否是<=> 等号
    def isAssign(self):
        return self.vtype == const.ASSIGN
    # 判断当前单词是否是<字符串>
    def isString(self):
        return self.vtype == const.STRING_LITERAL
    # 判断当前单词是否是<整数>
    def isInteger(self):
        return self.vtype == const.INTEGER_LITERAL
    # 判断当前单词是否是<十六进制整数>
    def isHex(self):
        return self.vtype == const.HEX_LITERAL
    # 判断当前单词是否是<浮点数>
    def isDouble(self):
        return self.vtype == const.DOUBLE_LITERAL
    # 判断当前单词是否是<字符>
    def isChar(self):
        return self.vtype == const.CHAR_LITERAL
    # 判断当前单词是否是 EOF
    def isEOF(self):
        return self.vtype == const.EOF
    # 判断当前单词是否是<标识符>
    def isID(self):
        return self.vtype == const.ID
    # 判断当前单词是否是保留字
    def isReserve(self):
        return self.vtype >= 20 and self.vtype < 40
    # 判断当前单词是否是保留字<const>
    def isR_Const(self):
        return self.vtype == const.CONST
    # 判断当前单词是否是保留字<void>
    def isR_Void(self):
        return self.vtype == const.VOID
    # 判断当前单词是否是保留字<int>
    def isR_Int(self):
        return self.vtype == const.INT
    # 判断当前单词是否是保留字<char>
    def isR_Char(self):
        return self.vtype == const.CHAR
    # 判断当前单词是否是保留字<double>
    def isR_Double(self):
        return self.vtype == const.DOUBLE
    # 判断当前单词是否是保留字<struct>
    def isR_Struct(self):
        return self.vtype == const.STRUCT
    # 判断当前单词是否是保留字<if>
    def isR_If(self):
        return self.vtype == const.IF
    # 判断当前单词是否是保留字<else>
    def isR_Else(self):
        return self.vtype == const.ELSE
    # 判断当前单词是否是保留字<switch>
    def isR_Switch(self):
        return self.vtype == const.SWITCH
    # 判断当前单词是否是保留字<case>
    def isR_Case(self):
        return self.vtype == const.CASE
    # 判断当前单词是否是保留字<default>
    def isR_Default(self):
        return self.vtype == const.DEFAULT
    # 判断当前单词是否是保留字<while>
    def isR_While(self):
        return self.vtype == const.WHILE
    # 判断当前单词是否是保留字<for>
    def isR_For(self):
        return self.vtype == const.FOR
    # 判断当前单词是否是保留字<do>
    def isR_Do(self):
        return self.vtype == const.DO
    # 判断当前单词是否是保留字<return>
    def isR_Return(self):
        return self.vtype == const.RETURN
    # 判断当前单词是否是保留字<break>
    def isR_Break(self):
        return self.vtype == const.BREAK
    # 判断当前单词是否是保留字<continue>
    def isR_Continue(self):
        return self.vtype == const.CONTINUE
    # 判断当前单词是否是保留字<print>
    def isR_Print(self):
        return self.vtype == const.PRINT
    # 判断当前单词是否是保留字<scan>
    def isR_Scan(self):
        return self.vtype == const.SCAN


# 定义VT类型，指代终结符
class VT(V):
    def __init__(self, vtype, line, text, wordNo = 0,level = 0):
        V.__init__(self,vtype)
        # 终结符链表的next指针
        self.next = None
        # 终结符链表的previous指针
        self.previous = None
        # 终结符的文字，为其值的字符串形式
        self.text = text
        # 终结符所在的行数
        self.line = line
        # 终结符在一行中所处的次序
        self.wordNo = wordNo
        self.level = level
    def printMsg(self):
        print('Vt Msg: In line ' + str(self.line) + " at " + str(self.wordNo) + ", Vt type " + str(self.vtype) + ", text is " + self.text)
    def printFormula(self):
        print(self.text, end='')
    def msg(self):
        return self.text


# 定义VN类型，指代非终结符
class VN(V):
    FORMULA = {
            const.EMPTY : "<empty>",
            const.C0PROGRAM : "<C0-program>",
            const.VAR_DEC : "<variable-declaration>",
            const.CON_DEC :"<const-declaration>",
            const.INIT_DEC : "<init-declarator>",
            const.INIT : "<initializer>",
            const.FUNC_DEF : "<function-definition>",
            const.PARA_CLA : "<parameter-clause>",
            const.PARA_DEC_LIST : "<parameter-declaration-list>",
            const.PARA_DEC : "<parameter-declaration>",
            const.COM_STATE : "<compound-statement>",
            const.STAT_SEQ : "<statement-seq>",
            const.STAT : "<statement>",
            const.COND_STATE : "<condition-statement>",
            const.CONDITION : "<condition>",
            const.LABE_STATE : "<labeled-statement>",
            const.LOOP_STATE : "<loop-statement>",
            const.FOR_INIT : "<for-init-statement>",
            const.FOR_UPDATE : "<for-update-expression>",
            const.JUMP_STATE : "<jump-statement>",
            const.RET_STATE : "<return-statement>",
            const.SCAN_STATE : "<scan-statement>",
            const.PRINT_STATE : "<print-statement>",
            const.PRINT_LIST : "<printable-list>",
            const.PRINTABLE : "<printable>",
            const.ASSIGN_EXP : "<assignment-expression>",
            const.FUNC_CALL : "<function-call>",
            const.EXP_LIST : "<expression-list>",
            const.EXP : "<expressioin>",
            const.MUL_EXP : "<multiplicative-expression>",
            const.CAST_EXP : "<cast-expression>",
            const.UNARY_EXP : "<unary-expression>",
            const.PRIM_EXP : "<primary-expression>",
            const.MAIN_FUNC: "<main-function>"
    }
    def __init__(self, vtype,level):
        V.__init__(self,vtype)
        # Vn的子节点数组
        self.level = level
        self.children = []
    def empty(self):
        self.children = []
        self.vtype = const.EMPTY
        return self
    def hasVn(self):
        for child in self.children:
            if isinstance(child, VN):
                return True
        return False
    def append(self, child, forceAppend = False):
        # 传进来的child 必须是V
        assert isinstance(child, V)
        if forceAppend == True or (not self.isEmpty()):
            self.children.append(child)
        else:
            print('Warning: Trying to add child into an empty Vn!')
        return self
    def printFormula(self):
        print(self.msg(), end='')
    def printChildren(self):
        print(self.msg())
        for child in self.children:
            print("vtype.%-3d%-10s"%(child.vtype, child.msg()))
    def findChild(self, childType):
        for child in self.children:
            if child.vtype == childType:
                return child
        return None
    # 搜索子节点树，找到指定类型的所有子孙节点
    def findGrandChildren(self, childType):
        children = []
        for child in self.children:
            if child.vtype == childType:
                children.append(child)
            elif isinstance(child, VN):
                children += child.findGrandChildren(childType)
        return children
    def findChildren(self, childType):
        result = []
        for child in self.children:
            if child.vtype == childType:
                result.append(child)
        return result
    def hasChild(self, childType):
        return not self.findChild(childType) == None
    def hasGrandChild(self,childType):
        return len(self.findGrandChildren(childType)) > 0
    def msg(self):
        return VN.FORMULA[self.vtype]
    @staticmethod
    # 返回一个创建的空Vn对象
    def create(vtype,level):
        return VN(vtype,level)



# 数据块类，用来管理变量常量的地址空间
class DataBlock():
    def __init__(self):
        # 数据区的栈用来分配空间给变量
        # 静态栈栈底
        self.bp = 0
        # 静态栈指针, 初始化时等于栈底
        self.sp = self.bp
        # 堆指针
        self.np = 8192
    # 栈分配空间函数，参数为需要分配的字节数,默认为4
    # 返回值为分配的地址
    def stackAllocation(self, bytes = 4):
        self.sp += bytes
        return self.sp - 4
    # 堆分配空间函数，参数为需要分配的字节数,默认为4
    # 返回值为分配的地址
    def heapAllocation(self, bytes = 4):
        self.np -= bytes
        return self.np


dataBlock = DataBlock()


class Instruction():
    nop     = 0 #什么都不做
    bipush  = 1 
    ipush   = 2 
    pop     = 4
    pop2    = 5
    popn    = 6
    dup     = 7
    dup2    = 8
    loadc   = 9
    loada   = 10
    new     = 11
    snew    = 12
    iload   = 16
    dload   = 17
    aload   = 18
    iaload  = 24
    daload  = 25
    aaload  = 26
    istore  = 32
    dstore  = 33
    astore  = 34
    iastore = 40
    dastore = 41
    aastore = 42
    iadd    = 48
    dadd    = 49
    isub    = 52
    dsub    = 53
    imul    = 56
    dmul    = 57
    idiv    = 60
    ddiv    = 61
    ineg    = 64
    dneg    = 65
    icmp    = 68
    dcmp    = 69
    i2d     = 96
    d2i     = 97
    i2c     = 98
    jmp     = 112
    je      = 113
    jne     = 114
    jl      = 115
    jge     = 116
    jg      = 117
    jle     = 118
    call    = 128
    ret     = 136
    iret    = 137
    dret    = 138
    aret    = 139
    iprint  = 160
    dprint  = 161
    cprint  = 162
    sprint  = 163
    printl  = 175
    iscan   = 176
    dscan   = 177
    cscan   = 178
    
    Msg = {
            nop:"nop",
            bipush:"bipush",
            ipush:"ipush",
            pop:"pop",
            pop2:"pop2",
            popn:"popn",
            dup:"dup",
            dup2:"dup2",
            loadc:"loadc",
            loada:"loada",
            new:"new",
            snew:"snew",
            iload:"iload",
            dload:"dload",
            aload:"aload",
            iaload:"iaload",
            daload:"daload",
            aaload:"aaload",
            istore:"istore",
            dstore:"dstore",
            astore:"astore",
            iastore:"iastore",
            dastore:"dastore",
            aastore:"aastore",
            iadd:"iadd",
            dadd:"dadd",
            isub:"isub",
            dsub:"dsub",
            imul:"imul",
            dmul:"dmul",
            idiv:"idiv",
            ddiv:"ddiv",
            ineg:"ineg",
            dneg:"dneg",
            icmp:"icmp",
            dcmp:"dcmp",
            i2d:"i2d",
            d2i:"d2i",
            i2c:"j2c",
            jmp:"jmp",    
            je:"je",
            jne:"jne",
            jl:"jl",
            jg:"jg",
            jle:"jle",
            jge:"jge",
            call:"call",
            ret:"ret",
            iret:"iret",
            dret:"dret",
            aret:"aret",
            iprint:"iprint",
            dprint:"dprint",
            cprint:"cprint",
            sprint:"sprint",
            printl:"printl",
            iscan:"iscan",
            dscan:"dscan",
            cscan:"cscan",
    }

    labNo = 0
    def __init__(self, instruction, operator1 = None, operator2 =None, lab = []):
        self.instruction = instruction
        if isinstance(operator1, int):
            self.operator1 = str(operator1)
        else:
            self.operator1 = operator1
        if isinstance(operator2, int):
            self.operator2 = str(operator2)
        else:
            self.operator2 = operator2
        self.lab = lab
    def msg(self,AN):
        if not self.operator1 is None:
            if not self.operator2 is None:
                op = self.operator1 + ',' + self.operator2
            else:
                op = self.operator1     
        else :
            op = ''
        return [Instruction.Msg[self.instruction], op]



# 指令流类，用来存放最终生成的指令流
class InstructionStream():
    def __init__(self):
        self.instructions = []
        self.no = -1
        self.lab = []
    def setLab(self, lab):
        self.lab.append(lab)
    def append(self, instruction):
        assert isinstance(instruction, Instruction)
        self.no += 1
        instruction.lab = self.lab
        self.lab = []
        self.instructions.append(instruction)
    def printstart(self,AN,file):
        file.write(".start:" + '\n')
        no = 0
        for instruction in self.instructions:
            if len(instruction.lab) <= 0 :
                arr = tuple([no]+ instruction.msg(AN))
                file.write("%-3d%-6s%-8s"%arr + '\n')
                # instruction.printMsg()
                no += 1
            else:
                break
        return no
    def printAllInstructions(self,AN,file):
        no = 0
        flag = 0
        funcnum = 0
        for instruction in self.instructions:
            if flag == 0:
                if not len(instruction.lab) <= 0 :
                    flag = 1
            if flag == 1:       
                if len(instruction.lab) > 0:
                    file.write(".F" + str(funcnum) + ":" + '\n')
                    funcnum += 1
                    no = 0
                arr = tuple([no]+ instruction.msg(AN))
                file.write("%-4d%-7s%-8s"%arr + '\n')
                # instruction.printMsg()
                no += 1



class SymbolTableIndex:
    def __init__(self, name, level, itemNo):
        self.name = name
        self.level = level
        self.itemNo = itemNo


class SymbolTableItem:
    TYPE_CONST = 1
    TYPE_INT = 2
    TYPE_FUNCTION = 3
    TYPE_PARAMETER = 4
    TYPE_VOID = 5
    TYPE_STRING = 6
    TYPE_CHAR = 7
    TYPE_DOUBLE = 8
    String = {
        TYPE_CONST:"Const",
        TYPE_INT:"Int",
        TYPE_FUNCTION:"Function",
        TYPE_PARAMETER:"Parameter",
        TYPE_VOID:"Void",
        TYPE_STRING:"String",
        TYPE_CHAR:"Char",
        TYPE_DOUBLE:"Double"
    }

    def __init__(self, name, value, level, itemType, no, returnValue = None, paraNum = 0, space = 0, constants = [], paraslot = 0):
        self.name = name
        # value对于普通变量就是值，对于函数指针就是代码段下标，
        self.value = value
        self.level = level
        self.itemType = itemType
        self.no = no
        # 函数类型需要的参数数量
        self.paraNum = paraNum
        self.paraslot = paraslot
        # 函数类型需要的定长空间
        self.space = space
        self.constants = constants
        # returnType对于普通变量等于itemType,对于函数变量等于返回值类型
        if self.itemType != SymbolTableItem.TYPE_FUNCTION:
            self.returnType = itemType
        else:
            self.returnType = returnValue
        # 为变量分配地址
    def isConst(self):
        return self.itemType == SymbolTableItem.TYPE_CONST
    def isInt(self):
        return self.itemType == SymbolTableItem.TYPE_INT
    def isParameter(self):
        return self.itemType == SymbolTableItem.TYPE_PARAMETER
    def isFunction(self):
        return self.itemType == SymbolTableItem.TYPE_FUNCTION
    def setValue(self, value):
        self.value = value


class SymbolTable():
    def __init__(self):
        self.level = 1
        self.index = []
        self.table = []
        self.constant = []
        self.var = []
        self.funcs = []
        self.no = -1
        self.offset = [0,0,0,0,0,0,0,0,0,0]
        # 加入“program”索引
        self.index.append(SymbolTableIndex('C0program', self.level, 0))
    def addIndex(self, name):
        self.level += 1
        self.index.append(SymbolTableIndex(name, self.level, self.no + 1))
    def addItem(self, name, value, itemType, returnValue = None , constants = []):
        aSameItem = self.getItem(name)
        # 如果未找到同层变量，定义！
        if aSameItem is None or aSameItem.level != self.level:
            self.no += 1
            self.table.append(SymbolTableItem(name, value, self.level, itemType, self.no, returnValue, constants))
            return self.no
        # 否则即为找到同层定义，返回-1报错！
        elif aSameItem.level == self.level:
            return -1
    def getItem(self, name):
        present = self.no
        while present >= 0:
            if self.table[present].name == name:
                return self.table[present]
            present -= 1
        return None
    def getVar(self,name):
        for i in range(0,len(self.var)):
            if self.var[i].value == name:
                return self.var[i]
        return None
    def getConstant_by_value(self,value):
        for i in range(0,len(self.constant)):
            if self.constant[i].value == value:
                return i
        return None 
    def getFunc(self,name):
        for i in range(0,len(self.funcs)):
            if self.funcs[i].name == name:
                return i
        return None 
    def getItemIndex(self,name):
        present = self.no
        while present >= 0:
            if self.table[present].name == name:
                return present
            present -= 1
        return None
    '''
    # 收起指定函数下的符号，同时设置函数项 space 字段，此后level - 1
    # 同时index弹出一项
    def collapseToFunction(self, funcName):
        funcItem = self.getItem(funcName)
        if not funcItem.isFunction():
            return
        start = funcItem.no
        for i in range(0, self.no - start):
            self.table.pop()
        # 设置space字段，因为有返回地址，所以要 + 1
        funcItem.space = self.no - start + 1
        self.no = start
        self.level -= 1
        self.index.pop()
    '''
    def print_const_Table(self,file):
        file.write(".constants:" + '\n')
        for i in range(0,len(self.constant)):
            if self.constant[i].type == "S":
                TEMP = '\"' + self.constant[i].value + '\"'
                self.constant[i].value  = TEMP
            file.write("%-3d%-3s%-15s"%(i, self.constant[i].type , self.constant[i].value) + '\n')

    def printfunction(self,file):
        file.write(".functions:" + '\n')
        for i in range(0,len(self.funcs)):
            file.write("%-3s%-3s%-3s%-3s"%(i ,self.funcs[i].number, self.funcs[i].slot, self.funcs[i].level) + '\n') 
    def isunique(self,name):
        for i in self.constant:
            if i.value == name:
                return 1
        return 0 


class tableitem:
    def __init__(self, itype, value,level,offset,flag):
        self.type = itype
        self.value = value
        self.level = level
        self.offset = offset
        self.flag = flag #判断是否是const

class func:
    def __init__(self,name, number, slot,level,para):
        self.number = number
        self.name = name
        self.slot = slot
        self.level = level
        self.para = para

class Error:
    # Error类型定义
    TK_UNDEFINED = 1
    TK_EOF = 2
    TK_ILLEGAL_INPUT = 3

    AN_UNDEFINED = 31
    AN_MISS_SEMICOLON = 32
    AN_MISS_IDENTIFIER = 33
    AN_MISS_ASSIGN = 34
    AN_MISS_INTEGER = 35
    AN_ILLEGAL_CONST_ILLUSTRATE = 36 #常量定义类型不对
    AN_MISS_MAIN_FUNCTION = 37
    AN_MISS_VAR_ILLUSTRATE = 38
    AN_MISS_COMMA = 39
    AN_ILLEGAL_INPUT = 40
    AN_ILLEGAL_TYPE = 41
    AN_ILLEGAL_EOF = 42
    AN_MISS_L_PARENTHESIS = 43
    AN_MISS_R_PARENTHESIS = 44
    AN_MISS_L_BRACE = 45
    AN_MISS_R_BRACE = 46
    AN_MISS_TYPE = 47
    AN_MISS_EXPRESSION = 48
    AN_MISS_SENTENCE = 49
    AN_MISS_RET_STATEMENT = 50

    ST_REPEATED_ID = 70
    ST_UNDEFINED_ID = 71
    ST_ASSIGN_CONST = 72
    ST_UNDEFINED_FUNCTION = 73
    ST_CALL_PARANUM_EXCEED = 74
    ST_CALL_PARANUM_LACK = 75
    ST_ILLEGAL_RETURN = 76
    ERROR_MSG = {
        TK_UNDEFINED : "Word Analysis Error: Undefined Error.",
        TK_EOF : "Word Analysis Error: Illegal EOF.",
        TK_ILLEGAL_INPUT : "Word Analysis Error: Illegal Input.",
        AN_UNDEFINED : "Gramma Analysis Error: Undefined Error.",
        AN_MISS_SEMICOLON : "Gramma Analysis Error: A \';\' is expected.",
        AN_MISS_IDENTIFIER : "Gramma Analysis Error: A identifier is expected.",
        AN_MISS_ASSIGN : "Gramma Analysis Error: \'=\' is expected.",
        AN_MISS_INTEGER : "Gramma Analysis Error: An integer is expected.",
        AN_ILLEGAL_CONST_ILLUSTRATE : "Gramma Analysis Error: Illegal const illustrate block.",
        AN_MISS_MAIN_FUNCTION : "Gramma Analysis Error: A main function is expected.",
        AN_MISS_VAR_ILLUSTRATE : "Gramma Analysis Error: A const illustate block is expected.",
        AN_MISS_COMMA : "Gramma Analysis Error: A \',\' is expected.",
        AN_ILLEGAL_INPUT : "Gramma Analysis Error: Illegal input..",
        AN_ILLEGAL_TYPE : "Gramma Analysis Error: Undefined Variable Type.",
        AN_ILLEGAL_EOF : "Gramma Analysis Error: Illegal EOF.",
        AN_MISS_L_PARENTHESIS : "Gramma Analysis Error: A \'(\' is expected.",
        AN_MISS_R_PARENTHESIS : "Gramma Analysis Error: A \')\' is expected.",
        AN_MISS_L_BRACE : "Gramma Analysis Error: A \'{\' is expected.",
        AN_MISS_R_BRACE : "Gramma Analysis Error: A \'}\' is expected.",
        AN_MISS_TYPE : "Gramma Analysis Error: A variable type declaration is expected.",
        AN_MISS_EXPRESSION : "Gramma Analysis Error: An expression is expected.",
        AN_MISS_SENTENCE : "Gramma Analysis Error: A sentence is expected.",
        AN_MISS_RET_STATEMENT : "Gramma Analysis Error: A return statement is expected.",
        ST_REPEATED_ID : "Symbol Table Error: Try to redefine a identifier in the same level.",
        ST_UNDEFINED_ID : "Symbol Table Error: Try to use a undefined identifier.",
        ST_ASSIGN_CONST : "Symbol Table Error: Trying to assign to a const.",
        ST_UNDEFINED_FUNCTION : "Symbol Table Error: Trying to call a undefined function.",
        ST_CALL_PARANUM_EXCEED : "Symbol Table Error: Function Call failed, parameters exceed, expect less parameters.",
        ST_CALL_PARANUM_LACK : "Symbol Table Error: Function Call failed, parameters lacked, expect more parameters.",
        ST_ILLEGAL_RETURN : "Symbol Table Error: Trying to return an illegal value which not match function define.",
    }
    def __init__(self, file, errornumber, linenum, msg, wordNo = 0):
        self.file = file
        self.line = linenum
        self.no = errornumber
        self.msg = msg
        if self.msg == '':
            self.msg = Error.ERROR_MSG[self.no]
        self.wordNo = wordNo
    # 恢复file指针
    def restoreFile(self):
        self.file.seek(0,0)
    def getErrorLine(self):
        lineNum = 1
        line = self.file.readline()
        while lineNum < self.line:
            # print("line." + str(lineNum) + line)
            line = self.file.readline()
            lineNum += 1
        return line
    def printAllLine(self):
        self.restoreFile()
        lineNum = 1
        line = self.file.readline()
        while line:
            print("Line."+str(lineNum)+":"+line)
            line = self.file.readline()
            lineNum += 1
        return
    def printMsg(self):
        print("Error No." + str(self.no) + "\tIn line " + str(self.line) + " at " + str(self.wordNo) + ",\t" + self.msg)
        self.restoreFile()
        errorLine = self.getErrorLine()
        # 排除\n影响
        if len(errorLine) > 1 and errorLine[-1] == '\n':
            errorLine = errorLine[0:-1]
        # 输出原错误行
        print('\t' + errorLine)
        # 输出错误地点指示
        print('\t',end='')
        ws = 0
        while ws < self.wordNo:
            print(' ',end='')
            ws += 1
        print('^')
    def fileOutMsg(self, file):
        file.write("Error No." + str(self.no) + "\tIn line " + str(self.line) + " at " + str(self.wordNo) + ",\t" + self.msg + '\n')
        self.restoreFile()
        errorLine = self.getErrorLine()
        # 排除\n影响
        if len(errorLine) > 1 and errorLine[-1] == '\n':
            errorLine = errorLine[0:-1]
        # 输出原错误行
        file.write('\t' + errorLine + '\n')
        # 输出错误地点指示
        file.write('\t')
        ws = 0
        while ws < self.wordNo:
            file.write(' ')
            ws += 1
        file.write('^' + '\n')

#double转16进制
def double_to_hex(f):
    return hex(struct.unpack('<Q', struct.pack('<d', f))[0])