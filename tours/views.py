# Create your views here.
#from django.conf import settings
from django.shortcuts import render
from django.views import View

# импорт данных из tours/data.py
from tours.data import (title, subtitle, description, departures, tours)
# импорт модуля для генерации случайных чисел
import random

# Дополнение в словари ключа id соответствуюего номеру тура
# можно (и стоило бы) добавить их непосредственно в данные, но я
# решил немного вспомнить работу со словарями
for key, value in tours.items():
    value['id']=key


#обработчики

class MainView(View):
    def get(self, request):
        #генерация списка 6 случайных неповторяющихся туров из полного словаря tours
        rand_tours = random.sample([tour for tour in tours.values()], 6)
        return render(request, 'index.html',
                      context = {'title' : title,
                                 'subtitle' : subtitle,
                                 'description' : description,
                                 'departures' : departures,
                                 'tours' : rand_tours})




class DepartureView(View):
    def get(self, request, depart_id: str):
        #формируем список из мест отправления по полученному из url значению depart_id
        depart_tours=[tour for tour in tours.values() if tour['departure'] == depart_id]
        #определяем количество найденных туров kol_tours
        kol_tours=len(depart_tours)
        # сортируем список найденных туров по возрастанию цены (dictionary - аргумент лямбда-функции)
        # можно было не сортировать, а просто найти минимум и максимум, но пока оставил так
        depart_tours.sort(key=lambda dictionary: dictionary['price'])
        #минимальная цена тура - нулевой элемент отсортированного словаря
        min_price = depart_tours[0]['price']
        # максимальная цена тура - последний элемент отсортированного словаря
        max_price = depart_tours[-1]['price']
        # сортируем список найденных туров по возрастанию числа ночей
        depart_tours.sort(key=lambda dictionary: dictionary['nights'])
        # минимальное число ночей
        min_nights = depart_tours[0]['nights']
        # максимальное число ночей
        max_nights = depart_tours[-1]['nights']
        # вообще, можно было сделать всё за один проход в цикле for, с подсчетом минимумов и максимумов

        #передаем список в шаблон - список отсортирован по числу ночей
        depart_city = departures[depart_id]
        return render(request, 'departure.html',
                      context = {'depart_tours' : depart_tours,
                                 'kol_tours' : kol_tours,
                                 'min_price' : min_price,
                                 'max_price' : max_price,
                                 'min_nights' : min_nights,
                                 'max_nights' : max_nights,
                                 'departures' : departures,
                                 'depart_city' : depart_city})




class TourView(View):
    def get(self, request, tour_id: int):
        # передача словаря конкретного тура по tour_id
        # и остальных данных для формирования страницы
        return render(request, 'tour.html',
                      context = {'tour_id' : tour_id,
                                 'title' : title,
                                 'subtitle' : subtitle,
                                 'description' : description,
                                 'departures' : departures,
                                 'tour' : tours[tour_id],
                                 'depart' : departures[tours[tour_id]['departure']]})

