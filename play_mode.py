from pico2d import *
import game_world
import game_framework
from boy import Boy
from grass import Grass
from bird import Bird, DRAW_WIDTH, FLIGHT_FRAME_COUNT

boy = None
BIRD_COUNT = 10


def handle_events():


    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def init():
    global boy

    boy = Boy()
    game_world.add_oject(boy)

    grass = Grass()
    game_world.add_oject(grass, 0)

    # 서로 다른 높이와 날갯짓 위상으로 열 마리를 구별한다.
    for index in range(BIRD_COUNT):
        x = DRAW_WIDTH / 2 + (get_canvas_width() - DRAW_WIDTH) * (index + 1) / (BIRD_COUNT + 1)
        y = get_canvas_height() * (0.5 + 0.09 * (index % 5))
        bird = Bird(x, y, frame=index * FLIGHT_FRAME_COUNT / BIRD_COUNT)
        game_world.add_oject(bird)


def pause():
    boy.pause()


def resume():
    pass


def finish():
    global boy
    game_world.clear()
    boy = None


def update():
    game_world.update()
    # delay(0.1) # 강제적인 프레임 시간 증가 

def render():
    clear_canvas()
    game_world.render()
    update_canvas()









