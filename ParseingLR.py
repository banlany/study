class LR:
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
            print('stack:',end='')
            for i in self.stack:
                print(i[1],end='')
            print('^')
            s=self.stack[-1][0]
            c=self.lexer.peek_token()
            print('state:'+str(s))
            print('读头：'+str(self.stack[-1][1])+'·'+c)
            action = self.table.action[s][c]
            if action[0]=='S':
                self.stack.append((action[1],c))
                self.lexer.next_token()
                flag=True
            elif action[0]=='R':
                r=self.table.grammer[action[1]]
                for i in range(len(r[1])):
                    self.stack.pop()
                if action[1]!=0:
                    self.stack.append((self.table.goto[self.stack[-1][0]][r[0]],r[0]))
                print('规约：',end='')
                print(r[0]+'->'+r[1])
                flag= (action[1]!=0)
            else:
                print('error')
                flag=False
if __name__ == '__main__':
    LRt=LR()
    LRt.grammer= {
        0: ("S", "E"),
        1: ("E", "E+T"),
        2: ("E", "E-T"),
        3: ("E", "T"),
        4: ("T", "T*F"),
        5: ("T", "T/F"),
        6: ("T", "F"),
        7: ("F", "(E)"),
        8: ("F", "n")
    }
    LRt.goto = {
        0: {
            'E': 1,
            'T': 2,
            'F': 3
        },
        4: {
            'E': 10,
            'T': 2,
            'F': 3
        },
        6: {
            'T': 11,
            'F': 3
        },
        7: {
            'T': 12,
            'F': 3
        },
        8: {
            'F': 13
        },
        9: {
            'F': 14
        }
    }
    LRt.action = {
        0: {
            '(': ('S', 4),
            'n': ('S', 5)
        },
        1: {
            '+': ('S', 6),
            '-': ('S', 7),
            '$': ('R', 0)
        },
        2: {
            '+': ('R', 3),
            '-': ('R', 3),
            '*': ('S', 8),
            '/': ('S', 9),
            ')': ('R', 3),
            '$': ('R', 3)
        },
        3: {
            '+': ('R', 6),
            '-': ('R', 6),
            '*': ('R', 6),
            '/': ('R', 6),
            ')': ('R', 6),
            '$': ('R', 6)
        },
        4: {
            '(': ('S', 4),
            'n': ('S', 5)
        },
        5: {
            '+': ('R', 8),
            '-': ('R', 8),
            '*': ('R', 8),
            '/': ('R', 8),
            ')': ('R', 8),
            '$': ('R', 8)
        },
        6: {
            '(': ('S', 4),
            'n': ('S', 5)
        },
        7: {
            '(': ('S', 4),
            'n': ('S', 5)
        },
        8: {
            '(': ('S', 4),
            'n': ('S', 5)
        },
        9: {
            '(': ('S', 4),
            'n': ('S', 5)
        },
        10: {
            '+': ('S', 6),
            '-': ('S', 7),
            ')': ('S', 15)
        },
        11: {
            '+': ('R', 1),
            '-': ('R', 1),
            '*': ('S', 8),
            '/': ('S', 9),
            ')': ('R', 1),
            '$': ('R', 1)
        },
        12: {
            '+': ('R', 2),
            '-': ('R', 2),
            '*': ('S', 8),
            '/': ('S', 9),
            ')': ('R', 2),
            '$': ('R', 2)
        },
        13: {
            '+': ('R', 4),
            '-': ('R', 4),
            '*': ('R', 4),
            '/': ('R', 4),
            ')': ('R', 4),
            '$': ('R', 4)
        },
        14: {
            '+': ('R', 5),
            '-': ('R', 5),
            '*': ('R', 5),
            '/': ('R', 5),
            ')': ('R', 5),
            '$': ('R', 5)
        },
        15: {
            '+': ('R', 7),
            '-': ('R', 7),
            '*': ('R', 7),
            '/': ('R', 7),
            ')': ('R', 7),
            '$': ('R', 7)
        }
    }
    parser = LR1parser(LRt,'(1 + 1) * 5')
    parser.parse()

