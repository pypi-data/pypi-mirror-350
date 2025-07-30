import turtle as t
import math as m

def fill(f):     # 함수를 매개변수로 받는다. 채우기를 시작한 후 함수를 실행하고 채우기를 종료한다.
    t.begin_fill()
    f()
    t.end_fill()
    
def cgoto(x,y,h=False):     # 거북이를 (x, y) 위치로 이동시키되, 이동 경로에 그림을 그리지 않는다.
    t.pu()
    t.goto(x,y)
    if h:
        t.setheading(h)   # 3번째 int 파라미터 h가 입력되었다면, 그 방향을 거북이가 바라보게 한다.
    t.pd()

def makeGons(rad, sides, x, y, h):   # 반지름, 변 수, 시작 위치와 방향을 파라미터로 받는다.
    theta = m.radians(360/sides)
    return [[x + rad*m.cos(m.radians(h) + i*theta), y + rad*m.sin(m.radians(h) + i*theta)] for i in range(sides+1)]
    # 호도법을 이용하여, 현재 위치를 중심으로 하는 입력받은 변 수의 정다각형의 점 위치를 계산한다.

def drawGons(rad, sides):   # 반지름과 변 수를 파라미터로 받는다. sides가 0일 시 원을 그린다.
    origin = t.xcor(), t.ycor(), t.heading()   # 현재 거북이의 위치와 방향을 저장한다.
    if sides != 0:
        point = makeGons(rad, sides, *origin)   # 파라미터가 5개인 makeGons에 origin을 언팩하여 전달한다.
        cgoto(*point[0])   # 이하 부분에선 이전에 계산한 점 위치에 순서대로 거북이를 움직여 그 경로를 그리는 것으로 다각형을 그린다.
        for i in point[1:]:   
            t.goto(i)
        cgoto(*origin)  # 도형을 다 그렸다면 원래의 위치와 방향으로 복귀한다.
    else:
        cgoto(origin[0], origin[1] - rad/2)   # sides = 0의 경우이다. 원의 중심에서 반지름/2만큼 내려간다.
        t.circle(rad)
        cgoto(origin[0], origin[1] + rad/2)  # 원을 그린 후 내려간 만큼 다시 올라와 원래 자리로 돌아온다.

def cGons(rad, sides, f=False):    # 매개변수 f를 추가해 도형의 색칠 여부를 받는다.
    if f:    # f가 0, “”, False가 아니라면 모두 True로 간주된다.
        fill(lambda: drawGons(rad, sides))   # 함수 fill에 drawGons 함수를 전달한다. 이때, fill 안의 f는 f()로 매개변수 없이 사용되었으므로, 람다를 이용하여 이미 매개변수가 입력된 함수를 전달한다.
    else:
        drawGons(rad, sides)  # 채우지 않는 경우에는 그냥 실행한다.

def cStar(rad, sides):  # 별을 그리는 함수이다.
    origin = t.xcor(), t.ycor(), t.heading()
    if sides % 2 == 1:  # 각이 홀수인 별을 그리는 경우이다.
        point = makeGons(rad, sides, *origin)
        cgoto(*point[0])
        ps = list(range(0,sides,2)) + list(range(1,sides,2)) + [0]  # 다각형과 다르게, 방문하는 꼭짓점의 순서를 교차해야 한다.
        for i in ps:
            t.goto(point[i])
    elif sides//2 % 2 == 1:  # 각이 짝수인 별은 같은 모양의 도형 두 개를 뒤집어서 그린 뒤 겹쳐야 한다. ##################### 겹쳐지는 도형이 홀수 변의 다각형인 경우이다.
        cGons(rad,sides//2)
        t.lt(180)  # 단순히 방향을 반대로 돌려 그리면 된다.
        cGons(rad,sides//2)
        t.rt(180)
    else:   # 겹쳐지는 도형이 짝수 변의 다각형인 경우이다.
        cGons(rad,sides//2)
        t.lt(360/sides)   # t.lt(180)으로 반대로 회전시킬 경우 원본과 모양이 동일해진다. 원하는 별 모양이 나오도록 각을 조절한다.
        cGons(rad,sides//2)
        t.rt(360/sides)
    cgoto(*origin)   # 도형을 다 그렸다면 원래의 위치와 방향으로 복귀한다.