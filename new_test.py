import pytest
import time

def test_petfriends(web_browser):
   # Open PetFriends base page:
   web_browser.get("https://petfriends.skillfactory.ru/")

   time.sleep(5)  # just for demo purposes, do NOT repeat it on real projects!

   # click on the new user button
   btn_newuser = web_browser.find_element_by_xpath("//button[@onclick=\"document.location='/new_user';\"]")
   btn_newuser.click()

   # click existing user button
   btn_exist_acc = web_browser.find_element_by_link_text(u"У меня уже есть аккаунт")
   btn_exist_acc.click()

   # add email
   field_email = web_browser.find_element_by_id("email")
   field_email.clear()
   field_email.send_keys("tanya214@yandex.ru")

   # add password
   field_pass = web_browser.find_element_by_id("pass")
   field_pass.clear()
   field_pass.send_keys("Metro")

   # click submit button
   btn_submit = web_browser.find_element_by_xpath("//button[@type='submit']")
   btn_submit.click()

   # click submit button
   btn_my_pets = web_browser.find_element_by_link_text(u"Мои питомцы")
   btn_my_pets.click()

   time.sleep(5)


   assert  web_browser.current_url == 'https://petfriends.skillfactory.ru/my_pets',"login error"
   assert web_browser.find_element_by_tag_name('h2').text == "Andrey11"
   # Выбираем моих питомцев
   my_pets = web_browser.find_elements_by_xpath('//*[@id="all_my_pets"]/table[1]/tbody[1]/tr[2]/th[1]/img[1] ')
   # Выбираем все элементы фотографий питомцев
   images = web_browser.find_elements_by_xpath('//th/img')
   # Назначаем переменную для подсчёта количества питомцев с фотографией
   photo_presence = 0
   web_browser.implicitly_wait(5)
   # Через проверку у всех питомцев, что attribute 'src' не пустое значение, определяем
   # количество питомцев с фотографией
   for i in range(len(my_pets)):
       if images[i].get_attribute('src') != '':
           photo_presence += 1
       else:
           photo_presence = photo_presence
   # Проверяем, что половина всех питомцев имеет фотографию
   assert photo_presence >= (len(my_pets) / 2)
   # У всех питомцев есть имя, возраст и порода.
   assert web_browser.find_element_by_xpath(
       '//*[@id="all_my_pets"]/table/tbody/tr[1]'
       and '//*[@id="all_my_pets"]/table/tbody/tr[2]'
   ).text != ''
   # Присутствуют все питомцы(количество питомцев взяли из статистики пользователя)
   number_pets = 2
   assert number_pets==photo_presence*2
   # У всех питомцев разные имена, породы и возраст.
   name_breed_age1 = web_browser.find_element_by_xpath(
       '//*[@id="all_my_pets"]/table/tbody/tr[1]/td[1]'
       and '//*[@id="all_my_pets"]/table/tbody/tr[1]/td[2]'
   )
   name_breed_age2 = web_browser.find_element_by_xpath(
       '//*[@id="all_my_pets"]/table/tbody/tr[2]/td[1]'
       and '//*[@id="all_my_pets"]/table/tbody/tr[2]/td[2]'
   )

   assert name_breed_age1 != name_breed_age2

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep

@pytest.fixture
def web_browser(request, selenium):

    browser = selenium
    browser.set_window_size(1400, 1000)

    # Return browser instance to test case:
    yield browser


#для запуска
#python -m pytest -v --driver Chrome --driver-path chromedriver.exe new_test.py


