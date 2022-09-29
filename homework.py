from typing import Dict, Type

COEFKKAL1 = 18
COEFKKAL2 = 20
COEFF_CALORIE_1 = 1.1
COEFF_CALORIE_2 = 2
COEF_CALORIE_1 = 0.035
COEF_CALORIE_2 = 0.029


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float, ):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        rslt1 = (COEFKKAL1 * self.get_mean_speed() - COEFKKAL2) * self.weight
        return rslt1 / self.M_IN_KM * self.duration * 60


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float, ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        rslt1 = self.get_mean_speed() ** 2 // self.height
        rslt2 = COEF_CALORIE_2 * self.weight
        rslt3 = COEF_CALORIE_1 * self.weight + rslt1 * rslt2
        return rslt3 * self.duration * 60


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float, ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        rslt1 = self.length_pool * self.count_pool
        return rslt1 / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        rslt1 = self.get_mean_speed() + COEFF_CALORIE_1
        return rslt1 * COEFF_CALORIE_2 * self.weight


SPORTS_TYPE: Dict[str, Type[Training]] = {'RUN': Running,
                                          'WLK': SportsWalking,
                                          'SWM': Swimming}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in SPORTS_TYPE:
        raise NotImplementedError('Incorrect key')
    return SPORTS_TYPE[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
