import time


class stepper2pin:
    stepper_position = 0

    def __init__(self, **kwargs):
        self.p = kwargs.get('device')
        self.dir_pin = kwargs.get('dir_pin','OD1')
        self.step_pin = kwargs.get('step_pin','SQ1')
        self.p.set_state(**{self.step_pin: False})

    def stepper_move(self, steps: int, forward: bool, step_delay=0.01):
        self.p.set_state(**{self.dir_pin: forward})
        for a in range(steps):
            self.p.set_state(**{self.step_pin: True})
            time.sleep(step_delay)
            self.p.set_state(**{self.step_pin: False})
            time.sleep(step_delay)
