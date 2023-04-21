import numpy as np


class PID:
    def __init__(self, kp, ki, kd):
        super().__init__()
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.list = [0 for i in range(100)]  # guarda los últimos 100 errores
        self.integral = 0
        self.derivate = 0
        self.limit = 5000

    def add_error(self, err):
        self.list.append(-err)  # Actualiza la lista de errores
        self.list.pop(0)	# agregando el nuevo y sacando el anterior.
        self.integral = sum(self.list)  # Suma de los últimos 100 errores.
        if self.integral > 100:
            self.integral = 100
        if self.integral < -100:
            self.integral = -100
        self.derivate = self.list[-2] - self.list[-1]

    def output(self):
        out = self.kp * self.list[-1] + self.integral * self.ki + self.kd * self.derivate
        if out < -self.limit:
            out = -self.limit
        if out > self.limit:
            out = self.limit
        return out