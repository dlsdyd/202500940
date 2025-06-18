import sys
import math
import random 
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QTimer, QRectF, Qt

radius = 20
x = 50
y = 580
vx = 0
vy = 0
score = 0
sign = 0
attempt = 10

gravity = 0.5
elasticity = 0.8
rx = random.randint(100, 650)
ry = random.randint(250, 570)
clicked = False

# 게임 상태 변수
game_started = False
game_over = False


# update 함수 정의
def update_position():
    global x, y, vx, vy, score, sign, rx, ry, clicked

    if not game_started or game_over:
        return

    # 공 움직임
    vy += gravity
    x += vx
    y += vy

    # 바닥 충돌
    if y + radius > window.height():
        x = 50
        y = 580
        vy = 0
        vx = 0
        clicked = False

    # 골에 넣음
    if rx <= x + radius and x - radius <= rx + 100 and ry <= y + radius and y - radius <= ry + 10:
        score += 1
        sign += 1
        x = 50
        y = 580
        vy = 0
        vx = 0
        clicked = False

    # 공위치 초기화
    if sign == 1:
        sign = 0
        rx = random.randint(100, 700)
        ry = random.randint(250, 570)

    # 좌우 벽 충돌
    if x - radius < 0:
        x = radius
        vx = -vx * elasticity
    elif x + radius > window.width():
        x = window.width() - radius
        vx = -vx * elasticity

    # 장애물 충돌
    if 100 - radius < x < 110 + radius and 500 - radius < y < 600 + radius:
        if x < 105:
            x = 100 - radius
            vx = -vx * elasticity
        else:
            x = 110 + radius
            vx = -vx * elasticity

    window.update()

# 그리기 함수
def paint_event(event):
    painter = QPainter(window)

    # 시작
    if not game_started:
        painter.setPen(QColor(0, 0, 0))
        painter.setFont(painter.font())
        painter.drawText(window.rect(), Qt.AlignCenter, "Press Enter to Start"+'\n'+"마우스 클릭으로 공을 던지세요")
        return

    # 공
    painter.setBrush(QColor(255, 180, 100))
    painter.setPen(QColor(50, 50, 50))
    painter.drawEllipse(QRectF(x - radius, y - radius, radius * 2, radius * 2))


    # 골 영역
    if not game_over:
        painter.setBrush(QColor(255, 0, 0))
        painter.setPen(QColor(200, 0, 0))
        painter.drawRect(rx, ry, 100, 10)

    # 장애물
    painter.setBrush(QColor(0, 0, 0))
    painter.setPen(QColor(0, 0, 0)) 
    painter.drawRect(100, 500, 10, 100) 

    # 종료
    painter.setPen(QColor(0, 0, 0))
    painter.drawText(10, 20, f"Score: {score}")
    painter.drawText(10, 40, f"Attempts Left: {attempt}")
    
    if game_over:
        painter.setPen(QColor(200, 0, 0))
        painter.setFont(painter.font())
        painter.drawText(window.rect(), Qt.AlignCenter, f"Game Over!\nFinal Score: {score}")

# 마우스 클릭 처리
def mouse_click(event):
    global x, y, vx, vy, clicked, attempt, game_over

    if not game_started or game_over:
        return

    # 시도는 다 썼지만 공은 아직 움직이고 있을 수 있음 → 클릭으로 종료
    if attempt <= 0:
        if abs(vx) < 0.1 and abs(vy) < 0.1:
            game_over = True
            window.update()
        return

    # 공 던진 후 초기로 돌아올 때까지 클릭 무시
    if clicked:
        return 
    
    clicked = True
    
    # 공의 움직임
    mx = event.x()
    my = event.y()

    dx = mx - x
    dy = my - y
    distance = math.hypot(dx, dy)

    if distance == 0:
        return

    dx /= distance * 1.4
    dy /= distance * 1.4

    power = min(distance * 0.3, 35)

    vx = dx * power
    vy = dy * power

    # 시도횟수 -1
    attempt -= 1

# 키 입력 처리
def key_press(event):
    global game_started
    if event.key() == Qt.Key_Return and not game_started:
        game_started = True
        window.update()

# 윈도우 생성 및 설정
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Kick the Ball")
window.setGeometry(100, 100, 800, 600)

# 이벤트 연결
window.paintEvent = paint_event
window.mousePressEvent = mouse_click
window.keyPressEvent = key_press

# 타이머 설정
timer = QTimer()
timer.timeout.connect(update_position)
timer.start(16)  # 약 60 FPS

window.show()
sys.exit(app.exec_())
