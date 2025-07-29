# This program prints the name in a pattern using the specified design.
# It uses functions to define the pattern for each letter and a main function to handle the input and output.
def a(i,style):
    # for i in range(1,10):
        for j in range(7):
            if(((i==1) and (j==0 or j==6)) or (((1<i<5) or i>5) and (0<j<6))):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
        # print()

def b(i,style):
    # for i in range(1,10):
        for j in range(6):
            if( ((i==1 or i==5 or i==9) and j==5) or ((1<i<5 or 5<i<9) and (j>0 and j<5))):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
        # print()

def c(i,style):
    # for i in range(1,10):
        for j in range(7):
            if( ((i==1 or i==9) and (j==0 or j==6)) or ((i==2 or i==3 or i==8 or i==7) and (j>0 and j<6)) or ((3<i<7) and (j>0))):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
#         print()

def d(i,style):
    # for i in range(1,10):
        for j in range(1,8):
            if( ((i==1 or i==9) and (j==6 or j==7)) or ((i==2 or i==8) and ((j>1 and j<6)or j==7)) or ((i>2 and i<8) and (j>1 and j<7))):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
#         print()

def e(i,style):
    # for i in range(1,10):
        for j in range(1,8):
            if(((i>1 and i<5)or(i>5 and i<9)) and (j>1)):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
#         print()

def f(i,style):
    # for i in range(1,10):
        for j in range(1,8):
            if(((i>1 and i<5)or(i>5)) and (j>1)):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
#         print()

def g(i,style):
    # for i in range(1,10):
        for j in range(1,9):
            if((i==1 and (j==1 or j==2 or j==7 or j==8))or (i==2 and (j==1 or j==8 or (j>2 and j<7)))or(i==3 and (j>1 and j<8))or ((i>3 and i<7) and j>1)or (i==7 and (j>1 and j<6))or(i==8 and (j==1 or j==7 or (j>2 and j<6)))or(i==9 and (j==1 or j==2 or j==6 or j==7))):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
        # print()

def h(i,style):
    # for i in range(1,10):
        for j in range(1,8):
            if(((i>=1 and i<5)or(i>5))and(j>1 and j<7)):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
#         print()


def i(i,style):
    # for i in range(1,10):
        for j in range(1,8):
            if(1<i<9 and (j<4 or j>4)):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
#     print()

def j(i,style):
    # for i in range(1,10):
        if(i==1):
            for j in range(7):
                print(f"{style} ",end="")
            print("  ",end="")
        elif(1<i<7):
            for j in range(6):
                print("  ",end="")
            print(f"{style}   ",end="")
            # print("   ",end="")
        else:
            for j in range(1,8):
                if((i==7 and (j>1 and j<7))or(i==8 and (j==1 or j==7 or 2<j<6)) or (i==9 and (j==1 or j==2 or j==6 or j==7))):
                    print("  ",end="")
                else:
                    print(f"{style} ",end="")
            print("  ",end="")
#             print()

def k(i,style):
    # for i in range(1,10):
        for j in range(1,7):
            if( ((i==1 or i==9)and 1<j<6) or ((i==2 or i==8)and(j==6 or 1<j<5)) or ((i==3 or i==7)and ( j==2 or j==3 or j==5 or j==6))or ((i==4 or i==6)and(j==2 or j==4 or j==5 or j==6))or (i==5 and (2<j<7))):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
#         print()
    
def l(i,style):
    # for i in range(1,10):
        for j in range(1,8):
            if((i>=1 and i<9) and (j>1 and j<8)):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
#         print()    

def m(i,style):
    # for i in range(1,10):
        for j in range(7):
            if(((i==1 or i>4) and (j>0 and j<6 )) or (i==2 and (j>1 and j<5)) or (i==3 and (j==1 or j==3 or j==5)) or (i==4 and (0<j<3 or 3<j<6))):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")

        # print()

def n(i,style):
    # for i in range(1,10):
        for j in range(1,10):
            if(((i==1 or i==9)and(1<j<9))or(i==2 and 2<j<9)or(i==3 and (j==2 or 3<j<9))or(i==4 and (1<j<4 or 4<j<9))or(i==5 and (1<j<5 or 5<j<9))or (i==6 and (1<j<6 or 6<j<9))or(i==7 and (1<j<7 or 7<j<9))or(i==8 and (1<j<8))):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
        

def o(i,style):
    # for i in range(1,10):
        for j in range(1,8):
            if(((i==1 or i==9)and(j==1 or j==7))or (1<i<9 and 1<j<7)):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
#         print()

def p(i,style):
    # for i in range(1,10):
        for j in range(1,8):
            if(((i==1 or i==5) and j==7) or ((1<i<5) and 1<j<7) or (5<i<10 and j>1)):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
#         print()
        
def q(i,style):
    # for i in range(1,10):
        for j in range(1,9):
            if(((i==1) and (j==7 or j==1 or j==8)) or ((1<i<7 or i==8) and (1<j<7 or j==8)) or (i==7 and (1<j<6 or j==8)) or (i==9 and (j==1 or j==7)) ):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
#         print()

def r(i,style):
    # for i in range(1,10):
        for j in range(1,8):
            if(((i==1 or i==5) and j==7) or ((1<i<5) and 1<j<7) or (i==6 and (1<j<5 or j==6 or j==7)) or (i==7 and (1<j<6 or j==7)) or ((i==8 or i==9) and 1<j<7)):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
#         print()

def s(i,style):
    # for i in range(1,10):
        for j in range(1,8):
            if(((i==1 or i==5 or i==9) and (j==1 or j==7)) or ((i==2 or i==8) and 1<j<7) or ((i==3 or i==4)and (j>1)) or ((i==6 or i==7)and(j<7))):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
#         print()

def t(i,style):
    # for i in range(1,10):
        for j in range(1,8):
            if((1<i<10) and (j<4 or j>4)):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
        # print()    
    
def u(i,style):
    # for i in range(1,10):
        for j in range(1,8):
            if( (( i==9)and(j==1 or j==7))or (0<i<9 and 1<j<7)):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
        # print()
        
def v(i,style):
    # for i in range(1,10):
        for j in range(1,8):
            if( (0<i<7 and 1<j<7) or (i==7 and (j==1 or j==7 or 2<j<6)) or (i==8 and (0<j<3 or j==4 or 5<j<8)) or (i==9 and (j<4 or j>4)) ):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
        # print()

def w(i,style):
    # for i in range(1,10):
        for j in range(1,8):
            if(((0<i<6 or i==9) and (j>1 and j<7 )) or (i==8 and (j>2 and j<6)) or (i==7 and (j==2 or j==4 or j==6)) or (i==6 and (j==2 or j==3 or j==6 or j==5))):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
        # print()

def x(i,style):
    # for i in range(1,10):
        for j in range(1,10):
            if(((i==1 or i==9)and (1<j<9)) or ((i==2 or i==8)and(j==1 or j==9 or 2<j<8)) or ((i==3 or i==7)and(j<3 or j>7 or 3<j<7)) or ((i==4 or i==6)and(j<4 or j>6 or j==5)) or (i==5 and (j<5 or j>5))):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
        # print()

def y(i,style):
    # for i in range(1,9):
        for j in range(1,8):
            if( ((i==1 or i==2) and 1<j<7) or (i==3 and (j==1 or j==7 or 2<j<6)) or (i==4 and (0<j<3 or j==4 or 5<j<8)) or (4<i<10 and (j<4 or j>4)) ):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
        # print()
        
        
def z(i,style):
    # for i in range(1,10):
        for j in range(1,10):
            if( (i==2 and (j==9 or j<8)) or (i==3 and (j==8 or j==9 or j<7)) or (i==4 and (6<j or j<6)) or (i==5 and (j>5 or j<5)) or (i==6 and (j>4 or j<4)) or (i==7 and (j>3 or j<3)) or (i==8 and (j>2 or j<2)) ):
                print("  ",end="")
            else:
                print(f"{style} ",end="")
        print("   ",end="")
        # print()

# It is the function that takes the name and design as input and prints the name in the specified pattern and design.
# It uses the match-case statement to call the appropriate function for each character in the name.
def text(person_name, design):
    for loop in range(1, 10):
        for num in person_name:
            match num:
                case 'a' | 'A':
                    a(loop, design)
                case 'b' | 'B':
                    b(loop, design)
                case 'c' | 'C':
                    c(loop, design)
                case 'd' | 'D':
                    d(loop, design)
                case 'e' | 'E':
                    e(loop, design)
                case 'f' | 'F':
                    f(loop, design)
                case 'g' | 'G':
                    g(loop, design)
                case 'h' | 'H':
                    h(loop, design)
                case 'i' | 'I':
                    i(loop, design)
                case 'j' | 'J':
                    j(loop, design)
                case 'k' | 'K':
                    k(loop, design)
                case 'l' | 'L':
                    l(loop, design)
                case 'm' | 'M':
                    m(loop, design)
                case 'n' | 'N':
                    n(loop, design)
                case 'o' | 'O':
                    o(loop, design)
                case 'p' | 'P':
                    p(loop, design)
                case 'q' | 'Q':
                    q(loop, design)
                case 'r' | 'R':
                    r(loop, design)
                case 's' | 'S':
                    s(loop, design)
                case 't' | 'T':
                    t(loop, design)
                case 'u' | 'U':
                    u(loop, design)
                case 'v' | 'V':
                    v(loop, design)
                case 'w' | 'W':
                    w(loop, design)
                case 'x' | 'X':
                    x(loop, design)
                case 'y' | 'Y':
                    y(loop, design)
                case 'z' | 'Z':
                    z(loop, design)
                case ' ':
                    print("\t", end="")
        print()
