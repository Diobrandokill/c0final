from dataStruct import const
from dataStruct import reservers
from dataStruct import VT
from dataStruct import Error
from dataStruct import double_to_hex

class tokennizer:
    def __init__(self, file):
        self.file = file       
        self.head = None
        self.pointer = self.head
        self.line = 1
        self.token = ''
        self.char = None
        self.symbol = 0             #记录token类型
        self.errors = []
        self.inError = False
        self.wordNo = 0             #记录读取到的token个数
        self.wordNoLast = 0
    
    # 光标回退函数
    def recract(self):
        self.file.seek(self.file.tell() - 1, 0)
        # 退格时记得将行计数器减1
        if self.wordNo != 0:
            self.wordNo -= 1
        else:
            self.wordNo = self.wordNoLast
        self.char = ' '
        return

    # 清空char
    def clearChar(self):
        self.char = ''
        return

    ###Token操作
    # 清除token
    def clearToken(self):
        self.token = ''
        self.inError = False
    # 将读入的字符拼接到token中
    def catToken(self):
        self.token += self.char
        return
        
    # 获取当前token的保留字编号,如果不是保留字，返回0
    def reserver(self):
        if self.token in reservers:
            return reservers[self.token]
        else:
            return 0

    ###判断函数
    # 判断是否为空格
    def isSpace(self):
        if self.char == ' ':
            return True
        else :
            return False
    # 判断是否是Tab
    def isTab(self):
        if self.char == '\t':
            return True
        else :
            return False
    # 判断是否是换行\n
    def isNewline(self):
        if self.char == '\n':
            return True
        else :
            return False
    # 判断是否是回车\r
    def isEnter(self):
        if self.char == '\r':
            return True
        else :
            return False       
    def isLetter(self):
        return self.char.isalpha()
    def isDigit(self):
        return self.char.isdigit()
    def isHex(self):
        if self.char >= '0' and self.char <= '9':
            return 1
        if self.char >= 'a' and self.char <= 'f':
            return 1
        if self.char >= 'A' and self.char <= 'F':
            return 1
        return 0 
    # 判断是否是小数点
    def isPoint(self):
        return self.char == '.'
    # 判断是否是逗号
    def isComma(self):
        return self.char == ','
    # 判断是否是分号
    def isSemicolon(self):
        return self.char == ';'
    # 判断是否是冒号
    def isColon(self):
        return self.char == ':'
    # 判断是否是感叹号
    def isExclamation(self):
        return self.char == '!'
    # 判断是否是等号
    def isAssign(self):
        return self.char == '='
    # 判断是否是大于号
    def isGT(self):
        return self.char == '>'
    # 判断是否是小于号
    def isLT(self):
        return self.char == '<'
    # 判断是否是加号+
    def isPlus(self):
        return self.char == '+'
    # 判断是否是减号-
    def isMinus(self):
        return self.char == '-'
    # 判断是否是星号*
    def isStar(self):
        return self.char == '*'
    # 判断是否是斜竖
    def isSlash(self):
        return self.char == '/'
    # 判断是否是反斜竖
    def isB_Slash(self):
        return self.char == '\\'
    # 判断是否是左圆括号
    def isL_Parenthesis(self):
        return self.char == '('
    # 判断是否是右圆括号
    def isR_Parenthesis(self):
        return self.char == ')'
    # 判断是否是左中括号
    def isL_Bracket(self):
        return self.char == '['
    # 判断是否是右中括号
    def isR_Bracket(self):
        return self.char == ']'
    # 判断是否是左大括号
    def isL_Brace(self):
        return self.char == '{'
    # 判断是否是右大括号
    def isR_Brace(self):
        return self.char == '}'
    # 判断是否是单引号
    def isS_Quatation(self):
        return self.char == '\''
    # 判断是否是右大括号
    def isD_Quatation(self):
        return self.char == '\"'
    # 判断是否是EOF
    def isEOF(self):
        return self.char == ''
    # 判断是否合法字符
    def islegal(self):
        if ord(self.char) in range(32,127):
            return True
        else:
            return False

    # 创建终结符
    def createVT(self):
        # 如果读取到的是注释，不创建节点，直接跳过
        if self.symbol == const.ANNOTATION:
            return
        # 如果处于出错状态，不创建节点
        if self.isInError():
            return
        Vt = VT(self.symbol, self.line, self.token, self.wordNo)
        # 如果head 都没有被初始化，处理链表第一个元素
        if self.head is None:
            self.head = Vt
            self.pointer = Vt
        else:
            Vt.previous = self.pointer
            self.pointer.next = Vt
            self.pointer = Vt

    # 分析下一个单词,注意调用这个函数时已经读入一个char
    def getsym(self):
        # 首先清除token
        self.clearToken()
        while self.isSpace() or self.isTab() or self.isNewline() or self.isEnter():
            self.getchar()
        # 第一个字符为字母，则进入标识符分析
        if self.isLetter():
            while self.isLetter() or self.isDigit():
                self.catToken()
                self.getchar()
            # 记得多读的要回退一格,但是如果是到EOF则不回退
            if(not self.isEOF()):
                self.recract()
            # 根据保留字查询结果设置当前要创建的节点的symbol值
            resultValue = self.reserver()
            if resultValue == 0:
                self.symbol = const.ID
            else:
                self.symbol = resultValue
        # 第一个字符为数字，则进入常数分析
        elif self.isDigit():
            flag = 0 # 判断double还是int
            #第一个数为0
            if self.char == '0':
                self.getchar()
                if self.char == 'x' or self.char == 'X':
                    self.token += '0'
                    self.catToken()
                    self.getchar()
                    if not self.isHex():
                        self.error(Error.TK_ILLEGAL_INPUT, "Word Analysis Error: invalid input!")
                        self.inError = True
                    else:
                        while self.isHex():
                            self.catToken()
                            self.getchar()
                    # 记得多读的要回退一格,但是如果是到EOF则不回退
                    if(not self.isEOF()):
                        self.recract()
                    self.symbol = const.HEX_LITERAL
                elif self.isSpace() or self.isTab() or self.isNewline() or self.isEnter() or self.isSemicolon() or self.isR_Parenthesis():
                    self.token += '0'
                    self.symbol = const.INTEGER_LITERAL
                    if(not self.isEOF()):
                        self.recract()
                elif self.isPoint():
                    while(self.isDigit() or self.isPoint()):
                        self.catToken()
                        self.getchar()
                    self.token = double_to_hex(float(self.token))
                    self.symbol = const.DOUBLE_LITERAL
                    if(not self.isEOF()):
                        self.recract()
                '''
                else:
                    self.error(Error.TK_ILLEGAL_INPUT, "Word Analysis Error: invalid input!")
                    self.inError = True
                '''
            else:
                while(self.isDigit() or self.isPoint()):
                    if self.isPoint():
                        flag = 1
                    self.catToken()
                    self.getchar()
                if not flag:
                    self.symbol = const.INTEGER_LITERAL
                else:
                    self.token = double_to_hex(float(self.token))
                    self.symbol = const.DOUBLE_LITERAL
                if int(self.token) > 2147483647:
                    self.token = "2147483647"
                # 记得多读的要回退一格,但是如果是到EOF则不回退
                if(not self.isEOF()):
                    self.recract()
        # 以下判断读入字符是否是特殊字符
        # 包括" , : = + * - / ( ) [ ] { } "
        elif self.isComma():
            self.catToken()
            self.symbol = const.COMMA
        elif self.isSemicolon():
            self.catToken()
            self.symbol = const.SEMICOLON
        elif self.isColon():
            self.catToken()
            self.symbol = const.COLON
        elif self.isAssign():
            self.catToken()
            self.getchar()
            # 这就是 ==
            if self.isAssign():
                self.catToken()
                self.symbol = const.EQ
            else :
                # 退格
                self.recract()
                self.symbol = const.ASSIGN
        elif self.isExclamation():
            self.catToken()
            self.getchar()
            if self.isAssign():
                self.catToken()
                self.symbol = const.NE
            else :
                # 退格
                self.recract()
                self.error(Error.TK_ILLEGAL_INPUT, "Word Analysis Error: single char \"!\" is illegal!")
                self.inError = True
        elif self.isGT():
            self.catToken()
            self.getchar()
            # 这就是 >=
            if self.isAssign():
                self.catToken()
                self.symbol = const.GE
            else :
                # 退格
                self.recract()
                self.symbol = const.GT
        elif self.isLT():
            self.catToken()
            self.getchar()
            # 这就是 <=
            if self.isAssign():
                self.catToken()
                self.symbol = const.LE
            else :
                # 退格
                self.recract()
                self.symbol = const.LT
        elif self.isPlus():
            self.catToken()
            self.symbol = const.PLUS
        elif self.isMinus():
            self.catToken()
            self.symbol = const.MINUS
        elif self.isStar():
            self.catToken()
            self.symbol = const.STAR
        elif self.isL_Parenthesis():
            self.catToken()
            self.symbol = const.L_PARENTHESIS
        elif self.isR_Parenthesis():
            self.catToken()
            self.symbol = const.R_PARENTHESIS
        elif self.isL_Bracket():
            self.catToken()
            self.symbol = const.L_BRACKET
        elif self.isR_Bracket():
            self.catToken()
            self.symbol = const.R_BRACKET
        elif self.isL_Brace():
            self.catToken()
            self.symbol = const.L_BRACE
        elif self.isR_Brace():
            self.catToken()
            self.symbol = const.R_BRACE
        elif self.isSlash():
            self.catToken()
            self.getchar()
            # 如果下一个是*,则处理/*...*/型注释
            if self.isStar():
                # 无论如何，这意思就是要处理注释了，找到 */ 为止！
                while True:
                    # 先读入一个字符
                    self.getchar()
                    while not self.isStar():
                        self.getchar()
                    # 跳出循环时，已经读到了一个*
                    self.getchar()
                    if self.isSlash():
                        # 置symbol 为注释类型
                        self.symbol = const.ANNOTATION
                        return 0
                    else:
                        # 退格
                        self.recract()
            # 如果下一个是/， 则处理//型注释
            elif self.isSlash():
                self.getchar()
                # 读到一个\n为止
                while not self.isNewline() and not self.isEnter():
                    self.getchar()
                # 置symbol 为注释类型
                self.symbol = const.ANNOTATION
                return 0
            else:
                # 如果后面不是*号,也不是/号，那么就是普通除号
                self.recract()
                self.symbol = const.SLASH
        # 输入为 "  进入字符串分析
        elif self.isD_Quatation():
            self.catToken()
            self.getchar()
            if self.islegal():
                while not self.isD_Quatation():
                    self.catToken()
                    self.getchar()
                    if not self.islegal():
                        print(ord(self.char))
                        self.error(Error.TK_ILLEGAL_INPUT, "Word Analysis Error: Unrecognized Char.")
                        self.inError = True
                        break
                    # 检测到\" ,做特殊处理,相当于手工跳过
                    if self.isB_Slash():
                        self.catToken()
                        self.getchar()
                        if self.isD_Quatation():
                            self.catToken()
                            self.getchar()
                            continue
                self.catToken()
            else:
                self.error(Error.TK_ILLEGAL_INPUT, "Word Analysis Error: Unrecognized Char.")
                self.inError = True
            self.symbol = const.STRING_LITERAL
        # 输入为 ' 进入字符分析
        elif self.isS_Quatation():
            self.getchar()
            if self.islegal():
                self.char = str(ord(self.char))
                self.catToken()
                self.getchar()
                if not self.isS_Quatation():
                    self.error(Error.TK_ILLEGAL_INPUT, "Word Analysis Error: Missing R_Quatation.")
                    self.inError = True
                self.symbol = const.CHAR_LITERAL
            else:
                self.error(Error.TK_ILLEGAL_INPUT, "Word Analysis Error: Unrecognized Char.")
                self.inError = True
        elif self.isEOF():
            self.clearChar()
            self.inError = True
            return 0
        else:
            self.error(Error.TK_ILLEGAL_INPUT, "Word Analysis Error: Unrecognized Char.")
            self.inError = True
            return 0
            
    def getchar(self):
        if self.isEOF():
            return ''
        char = self.file.read(1)
        self.wordNo += 1
        # 如果空格后才获取换行符,或者空格后才获取EOF，通过换行
        if self.isNewline() or self.isTab() or self.isEnter():
            self.line += 1
            self.wordNoLast = self.wordNo
            self.wordNo = 0
            self.char = char
        # 对于普通字符，直接通过
        else:
            self.char = char
        return

    # 错误处理函数
    def error(self,errorNo = Error.TK_UNDEFINED, msg = ''):
        err = Error(self.file, errorNo, self.line, msg, self.wordNo)
        self.errors.append(err)
        return
    def isInError(self):
        return self.inError
    # 恢复file指针
    def restorFile(self):
        self.file.seek(0,0)

    def createEOF(self):
        Vt = VT(const.EOF, self.line, '', self.wordNo)
        # 如果head 都没有被初始化，处理链表第一个元素
        if self.head is None:
            self.head = Vt
            self.pointer = Vt
        else:
            Vt.previous = self.pointer
            self.pointer.next = Vt
            self.pointer = Vt

    def scan(self):
        self.getchar()
        # 每次读取一个字符，如果不为EOF，则读取并新建一个终结符节点
        while not self.isEOF():
            self.getsym()
            self.createVT()
            self.getchar()
        self.createEOF()
        self.restorFile()

    # 输出词法分析的所有节点信息
    def printAllVt(self):
        Vs = self.head
        Ve = self.pointer
        while Vs is not Ve:
            Vs.printMsg()
            Vs = Vs.next
        Ve.printMsg()