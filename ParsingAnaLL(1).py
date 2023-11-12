class GrammerAna:
    def __init__(self):
        self.startS='E'#默认起始字符为E
        self.terminalS=set()
        self.NterminalS=set()
        self.generate={}
        self.LL1={}
        self.first={}
        self.follow={}
        self.nullable={}
    def unused_nterminal(self):   
        #找到可以添加的非终结符
        canuse='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i in canuse:
            if i not in self.NterminalS:
                self.NterminalS.add(i)
                return i
    def solve_left_recursion(self):
        #消除左递归
        keylist = list(self.generate.keys())
        for key in keylist: 
            expression = self.generate[key]
            left_recursion = [i for i in expression if i[0]==key]
            if left_recursion:
                new_key = self.unused_nterminal()
                self.generate[key] = [i+new_key for i in expression if i[0]!=key]
                self.generate[new_key] = [i[1:]+new_key for i in left_recursion]
                self.generate[new_key].append('')
    def get_first_follow(self):
        #求first集和follow集
        oldnull = {}
        for key in self.NterminalS:
            self.nullable[key] = False
        while oldnull != self.nullable:
            oldnull = self.nullable.copy()
            for k, v in self.generate.items():
                self.nullable[k] = False
                for expression in v:
                    nullable=True
                    for i in expression:
                        if not(i in self.NterminalS and ''in self.generate[i]):
                            nullable = False
                    self.nullable[k] = self.nullable[k] or nullable
        #求first集
        old_first=set()
        for k in self.NterminalS:
            self.first[k] = set()
        for k, v in self.generate.items():
            for expression in v:
                for i in expression:
                    if i not in self.NterminalS:
                        self.first[i]=set(i)
        while old_first!=self.first:
            old_first=self.first.copy()
            for k, v in self.generate.items():
                for expression in v:
                    new = True
                    if expression=='':
                        self.first[k].add('')
                    for i in expression:
                        if new:
                            self.first[k] = self.first[k].union(self.first[i])
                            new = new and (i in self.NterminalS and self.nullable[i])
        
        #求follow集
        old_follow=set()
        for k in self.NterminalS:
            self.follow[k] = set()
        for k, v in self.generate.items():
            for expression in v:
                for i in expression:
                    if i not in self.NterminalS:
                        self.follow[i]=set(i)
        self.follow[self.startS].add('$')
        while old_follow!=self.follow:
            old_follow=self.follow.copy()
            for key, v in self.generate.items():
                for expression in v:
                    for i in range(len(expression)):
                        new =True
                        for j in range(i+1,len(expression)):
                            new = new and (expression[j] in self.NterminalS and  self.nullable[expression[j]])
                        if new :
                            self.follow[expression[i]] = self.follow[expression[i]].union(self.follow[key])
                        for j in range(i+1,len(expression)):
                            new = True
                            for k in range(i+1,j):
                                new = new and (expression[k] in self.NterminalS and self.nullable[expression[k]])
                            if new:
                                self.follow[expression[j]] = self.follow[expression[i]].union(self.first[expression[j]])
        keys = list(self.first.keys())
        for i in keys:
            if i not in self.NterminalS:
                self.first.pop(i)
        keys = list(self.follow.keys())
        for i in keys:
            if i not in self.NterminalS:
                self.follow.pop(i)
        for k,v in self.follow.items():
            if '' in v:
                v.remove('')
        
    def get_first(self,expression):
        if expression =='':
            return set('')
        for i in expression:
            if i in self.NterminalS:
                if not self.nullable[i]:
                    return self.first[i]
            else:
                return set(i)
        return set()
    def get_nullable(self,expression):
        if expression =='':
            return True
        return '' in self.get_first(expression)
    def build_LL1(self):
        for k in self.NterminalS:
            self.LL1[k] = {}
        for k,v in self.generate.items():
            for expression in v:
                for i in self.get_first(expression):
                    self.LL1[k][i] = expression
                if self.get_nullable(expression):
                    for i in self.follow[k]:
                        self.LL1[k][i] = expression
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
                i = 0
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
                
                        
class tLL:
    def __init__(self,grammer,expression):
        self.grammer = grammer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
        self.lexer = Process(expression)
        self.stack = ['$',self.grammer.start]
    def parse(self):
        while self.stack[-1]!='$':
            if self.stack[-1] not in self.grammer.NterminalS:
                if self.stack[-1] ==self.lexer.peek_token():
                    self.stack.pop()
                    self.lexer.next_token()
                else:
                    raise RuntimeError
            else:
                expression =self.grammer.LL1[self.stack[-1]][self.lexer.peek_token()]
                print(self.stack[-1]+'->'+(expression if expression!='' else '\'\''))
                self.stack.pop()
                for i in expression[::-1]:
                    self.stack.append(i)
    
if __name__ == '__main__':
        expression = "(3 + 5) + 4"
        grammer = GrammerAna()
        grammer.start = 'E'
        grammer.NterminalS.add('E')
        grammer.NterminalS.add('T')
        grammer.NterminalS.add('F')
        grammer.terminalS.add('+')
        grammer.terminalS.add('-')
        grammer.terminalS.add('*')
        grammer.terminalS.add('/')
        grammer.generate['E']=['E+T','E-T','T']
        grammer.generate['T']=['T*F','T/F','F']
        grammer.generate['F']=['(E)','n']
        print(grammer.generate)
        grammer.solve_left_recursion()
        print(grammer.generate)
        grammer.get_first_follow()
        print(grammer.first)        
        print(grammer.follow)
        print(grammer.nullable)
        grammer.build_LL1()
        print(grammer.LL1)
        ll= tLL(grammer,expression)
        ll.parse()