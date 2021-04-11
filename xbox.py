# import signal
from xbox360controller import Xbox360Controller


def on_button_pressed(button):
    print('Button {0} was pressed'.format(button.name))


def on_button_released(button):
    print('Button {0} was released'.format(button.name))


def on_axis_moved(axis):
    print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))

try:
    while True:
        with Xbox360Controller(0, axis_threshold=0.1) as controller:
            # Button A events
            #controller.button_a.when_pressed = on_button_pressed
            #controller.button_a.when_released = on_button_released
            # Left and right axis move event
            print(controller.axis_l.x)
            print(controller.trigger_r._value)
            #controller.axis_r.when_moved = on_axis_moved
            
        #signal.pause()
except KeyboardInterrupt:
    pass