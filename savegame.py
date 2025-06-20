import pygame
from locations import *

class SaveGame:
    def __init__(self):
        self.save_file = 'save.txt'
        self.default_level = 1
    
    def save_progress(self, current_location):
        """Сохраняет текущий прогресс"""
        level = self._get_level_number(current_location)
        try:
            with open(self.save_file, 'w') as f:
                f.write(str(level))
        except IOError:
            print('В сохранении что то пошло не так(')
    
    def load_progress(self):
        """Загружает сохраненный прогресс"""
        try:
            with open(self.save_file, 'r') as f:
                level = int(f.read())
                return self._get_location_class(level)
        except:
            return self._get_location_class(self.default_level)
    
    def reset_progress(self):
        """Сбрасывает прогресс к начальному состоянию"""
        try:
            with open(self.save_file, 'w') as f:
                f.write(str(self.default_level))
        except:
            print('Ошибка сброса сохранения')
    
    def _get_level_number(self, location):
        """Определяет номер уровня по классу локации"""
        if isinstance(location, Locations1): 
            return 1
        elif isinstance(location, Locations2): 
            return 2
        elif isinstance(location, Locations3): 
            return 3
        elif isinstance(location, Locations4): 
            return 4
        elif isinstance(location, Locations5): 
            return 5
        elif isinstance(location, Locations6): 
            return 6
        elif isinstance(location, Locations7): 
            return self.default_level
        return self.default_level
    
    def _get_location_class(self, level):
        """Возвращает класс локации по номеру уровня"""
        if level == 1: 
            return Locations1()
        elif level == 2: 
            return Locations2()
        elif level == 3: 
            return Locations3()
        elif level == 4: 
            return Locations4()
        elif level == 5: 
            return Locations5()
        elif level == 6: 
            return Locations6()
        elif level == 7: 
            return Locations7()
        return Locations1()