class LR1:
    def __init__(self):
        self.grammer={}
        self.action={}
        self.goto={}

class Process:
    def __init__(self,expression):
        self.expression = (expression +'$').replace(' ','')
        self.token = None
    def next_token(self):
        if self.token:
            temp = self.token
            self.token = None
            return temp
        else:
            if self.expression == '':
                return None
            c = self.expression[0]
            if c =='(' or c ==')' or c=='+'or c=='*' or c=='-'or c=='/'or c=='$':
                self.expression = self.expression[1:]
                return c
            else:
                result=None
                i = 1
                try:
                    while i<len(self.expression):
                        if self.expression[i] == '.':
                            i+=1
                        result = float(self.expression[:i])
                        i+=1
                except:
                    self.expression = self.expression[i-1:]
                    return 'n'#当作num
            t = len(self.expression)
            self.expression = self.expression[i-1:]
            if i==t:
                return 'n'
            else:
                return result
    def peek_token(self):
        if not self.token:
            self.token = self.next_token()
        return self.token
class LR1parser:
    def __init__(self,table,expression):
        self.stack=[]
        self.table = table
        self.lexer = Process(expression)
        self.stack.append((0,''))
    def parse(self):
        flag=True
        while flag:
            print(self.stack)
            s=self.stack[-1][0]
            c=self.lexer.peek_token()
            print(str(s)+','+self.stack[-1][1]+'--'+c)
            action = self.table.action[s][c]
            if action[0]=='S':
                self.stack.append((action[1],c))
                self.lexer.next_token()
                flag=True
            elif action[0]=='R':
                r=self.table.grammer[action[1]]
                for i in range(len(r)):
                    self.stack.pop()
                if action[1]!=0:
                    self.stack.append((self.table.goto[self.stack[-1][0]][r[0]],r))
                print(r[0]+'->'+r[1])
                flag= (action!=0)
            else:
                print('error')
                flag=False


