import pytest
from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat4.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
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
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_new_pet_without_photo_and_valid_data(name='Барбос', animal_type='двортерьер', age=2):
    """Проверка добавления питомца с корректными данными без фото"""

    _, auth_key = pf.create_pet_simple(valid_email, valid_password, animal_type, age)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_add_photo_to_pet(pet_id='65118307-0993-43b0-a3ed-438bbcf92fb3',
                          pet_photo='images/cat3.jpg'):

    _, auth_key = pf.add_photo_of_pet(valid_email, valid_password, pet_photo)
    _, my_pets = os.path.join(os.path.dirname(__file__), pet_photo)

    status, result = pf.add_photo_of_pet(auth_key, pet_id)

    assert status == 200
    assert result['name'] == name

def test_delete_self_pet_with_valid_pet_id():
    """Проверка возможности удалить питомца """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = os.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        pet_id = "65118307-0993-43b0-a3ed-438bbcf92fb3"
        status, _ = pf.delete_pet(auth_key, pet_id)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        assert status == 400
    else:
        raise Exception("There is no my pets")

def test_input_invalid_age(name='Барбоскин', animal_type='двортерьер',
                        age='10a', pet_photo='images/cat4.jpg'):
    """Проверка неверного ввода возраста"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    if age != int:
        print("Не верно введен возраст")
        except ValueError
    else:
        assert status == 400
        assert result['age'] == age

def test_input_invalid_animal_type(name='Барбоскин', animal_type='!%$',
                        age='10', pet_photo='images/cat4.jpg'):
    """Проверка неверного ввода породы"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    if animal_type != text:
        print("Не верно введена порода")
        except ValueError
    else:
        assert status == 400
        assert result['animal_type'] == animal_type

def test_input_invalid_name(name='12!;%', animal_type='двортерьер',
                        age='10', pet_photo='images/cat4.jpg'):
    """Проверка неверного ввода имени"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    if name != text:
        print("Не верно введено имя")
        except ValueError
    else:
        assert status == 400
        assert result['name'] == name
