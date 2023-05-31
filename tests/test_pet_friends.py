from petfriends.api import PetFriends
from petfriends.settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Кабанчик', animal_type='Песел',
                                     age='4', pet_photo='images\kaban.jpeg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_without_photo(name='Кабан', animal_type='Песел', age='4'):
    """Проверяем что можно добавить питомца с корректными данными без фото"""
    # No.1
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_photo(pet_photo='images\ej.jpg'):
    """Проверяем что можно добавить фото питомца к имеющейся записи"""
    # No.2
    # Запрашиваем ключ api и сохраняем в переменную auth_key, запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового без фото и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Пес", "собака", "5",)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Берём id первого питомца из списка и отправляем запрос на добавление фото
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.add_photo(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images\ej.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_delete_strangers_pet():
    """Проверяем возможность удаления чужого питомца"""
    # No.3
    # Получаем ключ auth_key и запрашиваем список питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    # Проверяем - если список питомцев пустой, то добавляем нового и опять запрашиваем список питомцев
    if len(all_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images\ej.jpg")
        _, all_pets = pf.get_list_of_pets(auth_key, "")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = all_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список питомцев
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in all_pets.values()


def test_successful_update_self_pet_info(name='Пес', animal_type='Кабачок', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There are no my pets")


def test_successful_update_strangers_pet_info(name='Чубака', animal_type='Выдра', age=7):
    """Проверяем возможность обновления информации о чужом питомце"""
    # No.4
    # Получаем ключ auth_key и список питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(all_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, all_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии питомцев
        raise Exception("There are no pets")


def test_login(email='teraretss@gmail.com', passw='skillfactory01'):
    """Проверяем что можно залогиниться"""
    # No.5
    # Отправляем запрос на авторизацию
    status = pf.login(email, passw)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200


def test_reg(name='testnewuser', email='new@gmail.com', passw='newpass'):
    """Проверяем что можно зарегистрировать нового пользователя"""
    # No.6
    # Отправляем запрос на регистрацию
    status = pf.reg(name, email, passw)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    # Пробуем авторизоваться с новыми данными
    status = pf.login(email, passw)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200


def test_add_new_pet_invalid_data_without_photo(name='      ', animal_type='890', age='пес'):
    """Проверяем что можно добавить питомца с НЕкорректными данными без фото"""
    # No.7
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


invalid_email = '___@___.com'
invalid_password = '///////'


def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """ Проверяем запрос api ключа с неверными данными"""
    # #8
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, _ = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status != 200
  #  assert 'key' in result


def test_add_new_pet_with_invalid_data(name='Кабанчик', animal_type='Песел',
                                     age='4', pet_photo='images/text.txt'):
    """Проверяем что можно добавить питомца c загрузкой некорректного файла вместо фото"""
    # №9
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    # Сайт не должен принимать текст, но фактически принял, запись создалась
    assert status == 200
    assert result['name'] == name


def test_successful_update_self_pet_invalid_data(name='                 ', animal_type='###', age=321733432423):
    """Проверяем возможность обновления информации о своем питомце c НЕкорректными данными"""
    # №10
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There are no my pets")

