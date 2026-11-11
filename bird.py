from pico2d import get_canvas_width, load_image

import game_framework


# 소년과 같은 축척과 km/h -> m/min -> m/s -> pixel/s 변환.
PIXEL_PER_METER = 10.0 / 0.3
FLY_SPEED_KMPH = 30.0
FLY_SPEED_MPM = FLY_SPEED_KMPH * 1000.0 / 60.0
FLY_SPEED_MPS = FLY_SPEED_MPM / 60.0
FLY_SPEED_PPS = FLY_SPEED_MPS * PIXEL_PER_METER

# 소년의 보폭에 대응하는 한 번의 날갯짓당 이동 거리(게임 설정).
FLIGHT_CYCLE_DISTANCE_M = 5.0
FLIGHT_FRAME_COUNT = 14
FLIGHT_FRAMES_PER_SECOND = (
    FLY_SPEED_MPS / FLIGHT_CYCLE_DISTANCE_M * FLIGHT_FRAME_COUNT
)
SHEET_COLUMNS = 5
SHEET_ROWS = 3
DRAW_WIDTH = 80
DRAW_HEIGHT = 74


class Bird:
    image = None

    def __init__(self, x, y, direction=1, frame=0.0):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.dir = 1 if direction >= 0 else -1
        self.frame = frame % FLIGHT_FRAME_COUNT
