from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from .models import SfuLocation, SfuRecord, KrasLocation, KrasRecord
import random
import traceback
from math import radians, sin, cos, sqrt, atan2


def home(request):
    return render(request, 'mainpage/home.html')


def play(request):
    return render(request, 'mainpage/play.html')


# ───────────────────────────────────────────────
# Общие вспомогательные функции
# ───────────────────────────────────────────────

def haversine(lat1, lon1, lat2, lon2):
    """Расстояние между двумя точками на Земле в километрах (формула Haversine)"""
    R = 6371.0  # радиус Земли в км
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def calculate_score(distance_km):
    """Очки за раунд: от 5000 (0 км) до 0 (≥50 км)"""
    max_distance = 50.0
    if distance_km >= max_distance:
        return 0
    return max(0, 5000 - int(distance_km * (5000 / max_distance)))


def calculate_score_kras(distance_km):
    """
    Подсчёт очков для большого города.
    Плавное падение очков на дистанциях до ~25 км.
    """
    max_score = 5000
    max_distance = 25.0
    if distance_km <= 0:
        return max_score
    if distance_km >= max_distance:
        return 0

    # Экспоненциальная кривая, нормированная так, чтобы на max_distance было 0.
    k = 7.0  # "масштаб" города (км): больше k -> медленнее падение
    import math
    raw = math.exp(-distance_km / k)
    raw_min = math.exp(-max_distance / k)
    normalized = (raw - raw_min) / (1.0 - raw_min)
    return max(0, int(round(max_score * normalized)))


def calculate_score_sfu(distance_km):
    """
    Подсчёт очков для кампуса.
    Быстрое падение очков на малых дистанциях (до ~2 км).
    """
    max_score = 5000
    max_distance = 2.0
    if distance_km <= 0:
        return max_score
    if distance_km >= max_distance:
        return 0

    # Экспоненциальная кривая, нормированная так, чтобы на max_distance было 0.
    k = 0.45  # "масштаб" кампуса (км)
    import math
    raw = math.exp(-distance_km / k)
    raw_min = math.exp(-max_distance / k)
    normalized = (raw - raw_min) / (1.0 - raw_min)
    return max(0, int(round(max_score * normalized)))


def pick_unique_location_ids(model, count=5):
    """
    Случайно выбирает count локаций без повторов "места" в пределах одной игры.
    "Место" считаем одинаковым, если совпадает фото (путь к файлу),
    иначе — если совпадают координаты (с округлением).
    """
    rows = list(model.objects.values_list('id', 'latitude', 'longitude', 'photo'))
    random.shuffle(rows)

    picked_ids = []
    seen_places = set()

    for loc_id, lat, lon, photo in rows:
        photo_path = (str(photo) if photo is not None else '').strip().lower()
        if photo_path:
            place_key = ('photo', photo_path)
        else:
            place_key = ('coords', round(lat, 6), round(lon, 6))
        if place_key in seen_places:
            continue
        seen_places.add(place_key)
        picked_ids.append(loc_id)
        if len(picked_ids) >= count:
            break

    return picked_ids


# ───────────────────────────────────────────────
# Режим СФУ
# ───────────────────────────────────────────────

@ensure_csrf_cookie
def sfu_mode(request):
    print(f"\n=== SFU MODE === Method: {request.method} Session: {dict(request.session)}")

    if request.method == 'POST':
        # Подтверждение выбора точки
        if 'confirm_guess' in request.POST:
            current_round = request.session.get('sfu_current_round', 1)
            location_ids = request.session.get('sfu_location_ids', [])

            if current_round > 5 or not location_ids:
                return JsonResponse({'success': False, 'error': 'Игра завершена или сессия сломана'})

            try:
                correct_id = location_ids[current_round - 1]
                correct_loc = SfuLocation.objects.get(id=correct_id)

                user_lat = float(request.POST['lat'])
                user_lon = float(request.POST['lon'])

                distance = haversine(correct_loc.latitude, correct_loc.longitude, user_lat, user_lon)
                score = calculate_score_sfu(distance)

                scores = request.session.get('sfu_scores', [])
                scores.append(score)
                request.session['sfu_scores'] = scores

                request.session.modified = True

                total_score = sum(scores)

                return JsonResponse({
                    'success': True,
                    'score': score,
                    'total_score': total_score,
                    'distance': round(distance, 2),
                    'correct_lat': correct_loc.latitude,
                    'correct_lon': correct_loc.longitude,
                    'is_last_round': current_round == 5,
                    'next_round': current_round + 1
                })

            except Exception as e:
                print("Ошибка:", str(e))
                return JsonResponse({'success': False, 'error': f'Ошибка: {str(e)}'})

        # Переход к следующему раунду (от "Далее")
        elif 'next_round' in request.POST:
            current_round = request.session.get('sfu_current_round', 1)
            request.session['sfu_current_round'] = current_round + 1
            request.session.modified = True
            return redirect('sfu_mode')

        # Сохранение имени
        elif 'submit_name' in request.POST:
            name = request.POST.get('name', '').strip()
            if not name:
                return JsonResponse({'success': False, 'error': 'Имя не может быть пустым'})

            total_score = sum(request.session.get('sfu_scores', [0]*5))

            if SfuRecord.objects.filter(name=name).exists():
                return JsonResponse({'success': False, 'error': 'Имя уже занято'})

            SfuRecord.objects.create(name=name, score=total_score)

            for key in ['sfu_location_ids', 'sfu_scores', 'sfu_current_round']:
                request.session.pop(key, None)

            return JsonResponse({'success': True, 'total_score': total_score})

    # GET — начало игры или новый раунд
    if 'sfu_location_ids' not in request.session or request.session.get('sfu_current_round', 1) > 5:
        picked_ids = pick_unique_location_ids(SfuLocation, count=5)
        if len(picked_ids) < 5:
            return render(request, 'mainpage/sfu.html', {'error': 'Недостаточно локаций'})

        request.session['sfu_location_ids'] = picked_ids
        request.session['sfu_scores'] = []
        request.session['sfu_current_round'] = 1
        request.session.modified = True

    current_round = request.session['sfu_current_round']
    current_id = request.session['sfu_location_ids'][current_round - 1]

    try:
        current_loc = SfuLocation.objects.get(id=current_id)
    except SfuLocation.DoesNotExist:
        for key in ['sfu_location_ids', 'sfu_scores', 'sfu_current_round']:
            request.session.pop(key, None)
        return redirect('sfu_mode')

    return render(request, 'mainpage/sfu.html', {
        'current_round': current_round,
        'photo_url': current_loc.photo.url,
        'total_rounds': 5,
    })


# ───────────────────────────────────────────────
# Режим Красноярск (аналогично с отладкой)
# ───────────────────────────────────────────────

@ensure_csrf_cookie
def kras_mode(request):
    print(f"\n=== KRAS MODE === Method: {request.method} Session: {dict(request.session)}")

    if request.method == 'POST':
        # Подтверждение выбора точки
        if 'confirm_guess' in request.POST:
            current_round = request.session.get('kras_current_round', 1)
            location_ids = request.session.get('kras_location_ids', [])

            if current_round > 5 or not location_ids:
                return JsonResponse({'success': False, 'error': 'Игра завершена или сессия сломана'})

            try:
                correct_id = location_ids[current_round - 1]
                correct_loc = KrasLocation.objects.get(id=correct_id)

                user_lat = float(request.POST['lat'])
                user_lon = float(request.POST['lon'])

                distance = haversine(correct_loc.latitude, correct_loc.longitude, user_lat, user_lon)
                score = calculate_score_kras(distance)

                scores = request.session.get('kras_scores', [])
                scores.append(score)
                request.session['kras_scores'] = scores

                request.session.modified = True

                total_score = sum(scores)

                return JsonResponse({
                    'success': True,
                    'score': score,
                    'total_score': total_score,
                    'distance': round(distance, 2),
                    'correct_lat': correct_loc.latitude,
                    'correct_lon': correct_loc.longitude,
                    'is_last_round': current_round == 5,
                    'next_round': current_round + 1
                })

            except Exception as e:
                print("Ошибка:", str(e))
                return JsonResponse({'success': False, 'error': f'Ошибка: {str(e)}'})

        # Переход к следующему раунду (от "Далее")
        elif 'next_round' in request.POST:
            current_round = request.session.get('kras_current_round', 1)
            request.session['kras_current_round'] = current_round + 1
            request.session.modified = True
            return redirect('kras_mode')

        # Сохранение имени
        elif 'submit_name' in request.POST:
            name = request.POST.get('name', '').strip()
            if not name:
                return JsonResponse({'success': False, 'error': 'Имя не может быть пустым'})

            total_score = sum(request.session.get('kras_scores', [0]*5))

            if KrasRecord.objects.filter(name=name).exists():
                return JsonResponse({'success': False, 'error': 'Имя уже занято'})

            KrasRecord.objects.create(name=name, score=total_score)

            for key in ['kras_location_ids', 'kras_scores', 'kras_current_round']:
                request.session.pop(key, None)

            return JsonResponse({'success': True, 'total_score': total_score})

    # GET — начало игры или новый раунд
    if 'kras_location_ids' not in request.session or request.session.get('kras_current_round', 1) > 5:
        picked_ids = pick_unique_location_ids(KrasLocation, count=5)
        if len(picked_ids) < 5:
            return render(request, 'mainpage/kras.html', {'error': 'Недостаточно локаций'})

        request.session['kras_location_ids'] = picked_ids
        request.session['kras_scores'] = []
        request.session['kras_current_round'] = 1
        request.session.modified = True

    current_round = request.session['kras_current_round']
    current_id = request.session['kras_location_ids'][current_round - 1]

    try:
        current_loc = KrasLocation.objects.get(id=current_id)
    except KrasLocation.DoesNotExist:
        for key in ['kras_location_ids', 'kras_scores', 'kras_current_round']:
            request.session.pop(key, None)
        return redirect('kras_mode')

    return render(request, 'mainpage/kras.html', {
        'current_round': current_round,
        'photo_url': current_loc.photo.url,
        'total_rounds': 5,
    })


# ───────────────────────────────────────────────
# Таблица рекордов
# ───────────────────────────────────────────────

def records(request):
    sfu_records = SfuRecord.objects.order_by('-score')[:10]
    kras_records = KrasRecord.objects.order_by('-score')[:10]

    return render(request, 'mainpage/records.html', {
        'sfu_records': sfu_records,
        'kras_records': kras_records,
    })


def reset_game(request, mode: str):
    mode = (mode or '').lower()
    if mode == 'sfu':
        for key in ['sfu_location_ids', 'sfu_scores', 'sfu_current_round']:
            request.session.pop(key, None)
        request.session.modified = True
        return redirect('play')
    if mode == 'kras':
        for key in ['kras_location_ids', 'kras_scores', 'kras_current_round']:
            request.session.pop(key, None)
        request.session.modified = True
        return redirect('play')
    return redirect('play')