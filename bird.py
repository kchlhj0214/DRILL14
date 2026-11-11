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

    def update(self):
        self.frame = (self.frame + FLIGHT_FRAMES_PER_SECOND *
                      game_framework.frame_time) % FLIGHT_FRAME_COUNT
        left = DRAW_WIDTH / 2
        right = get_canvas_width() - DRAW_WIDTH / 2
        span = right - left
        if span <= 0:
            self.x = get_canvas_width() / 2
            return
        # 왕복 경로를 펼친 좌표로 계산해 여러 번 반사되는 긴 dt도 보존.
        position = max(0.0, min(span, self.x - left))
        phase = position if self.dir == 1 else 2 * span - position
        phase = (phase + FLY_SPEED_PPS * game_framework.frame_time) % (2 * span)
        self.dir = 1 if phase < span else -1
        self.x = left + (phase if phase < span else 2 * span - phase)

    def draw(self):
        # 파일은 위에서 아래 순서, pico2d의 원점은 왼쪽 아래.
        row, column = divmod(int(self.frame), SHEET_COLUMNS)
        left = column * self.image.w // SHEET_COLUMNS
        right = (column + 1) * self.image.w // SHEET_COLUMNS
        top = self.image.h - row * self.image.h // SHEET_ROWS
        bottom = self.image.h - (row + 1) * self.image.h // SHEET_ROWS
        self.image.clip_composite_draw(
            left, bottom, right - left, top - bottom,
            0, '' if self.dir == 1 else 'h',
            self.x, self.y, DRAW_WIDTH, DRAW_HEIGHT
        )
