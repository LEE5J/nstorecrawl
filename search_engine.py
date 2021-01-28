import sys, traceback, selenium, time, requests

from requests import options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tools import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal

def crawl_a_item_nstore(url):
    product = Product()
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--windows-size=900,900')
    # options.add_argument('--disable-gpu')
    try:
        driver = webdriver.Chrome("chromedriver.exe", options=options)
    except:
        driver = webdriver.Chrome("../chromedriver.exe", options=options)
    driver.get(url)
    driver.find_element_by_css_selector('body').send_keys(Keys.END)
    if time.time() > 1612671913:  # exe파일 유출시 대비
        exit()
    product.url = url
    # 품절 여부 확인
    try:
        driver.implicitly_wait(2)
        infotext = driver.find_element_by_css_selector('fieldset > div._2BQ-WF2QUb > strong').text
        if "구매하실 수 없는" in infotext:
            print(infotext)
            product.product_name = "판매중지상품"
            product.main_img_src = 'https://ssl.pstatic.net/static/nid/membership/rw_ico_digitalpack.png'
            infotext2 = driver.find_element_by_css_selector('fieldset > div > p.sRB6C4_UaS').text
            if "재입고" in infotext2:
                None
            else:
                driver.quit()
                return product
    except:
        None
    driver.find_element_by_css_selector('body').send_keys(Keys.END)
    main_img = driver.find_element_by_css_selector('#content > div > div > div > div > div > img')
    product.main_img_src = main_img.get_attribute('src')
    print(product.main_img_src)
    product.product_name = driver.find_element_by_css_selector('#content > div > div > div > fieldset > div > h3').text.replace('/', '')
    category_link = driver.find_elements_by_css_selector('#content > div > div > div > div > ul > li > a')[-1].get_attribute('href')
    if len(category_link.split('/category/')) == 1:
        try:
            product.category_id = get_categoryid_byname(product.product_name)
        except:
            print("카테고리 id 얻는데 실패함" + product.product_name)
    elif len(category_link.split('/category/')[1]) < 9: # 레퍼런스 카테고리를 사용함
        product.category_id = category_link.split('/category/')[1]
    else:  # 커스텀 카테고리를 사용함
        try:
            product.category_id = get_categoryid_byname(product.product_name)
        except:
            print("카테고리 id 얻는데 실패함" + product.product_name)
    try:
        product.original_price = return_int(driver.find_elements_by_css_selector('fieldset > div._1ziwSSdAv8 > div > div > del > span')[1].text)
    except:  # 할인을 안하는 제품임
        product.original_price = return_int(driver.find_elements_by_css_selector('#content > div > div > div > fieldset > div > div > div > strong > span')[1].text)
    product.saled_price = return_int(driver.find_elements_by_css_selector('#content > div > div > div > fieldset > div > div > div > strong > span')[1].text)
    # 옵션 레이어 구하기
    option_layer = -1
    try:
        option_box = driver.find_element_by_css_selector('fieldset > div.Klq2ZNy50Z').text.split('\n')
        for i in range(len(option_box)):
            if option_box[i] == '추가옵션 선택':
                option_layer = i
                if i == 0:
                    raise selenium.common.exceptions.NoSuchElementException
            else:
                product.option_title_list.append((option_box[i]))
        if option_layer == -1:
            option_layer = len(option_box)
        option_offset = len(driver.find_elements_by_css_selector('fieldset > div > div > input')) # 직접입력은 입력받지 않음
        product.option_offset = option_offset  # 입력형은 제외하고 반영하며 이는 오프셋으로 조정함
        option_layer = option_layer - option_offset
        driver.find_element_by_css_selector('body').send_keys(Keys.HOME)
        options = driver.find_elements_by_css_selector('fieldset > div.Klq2ZNy50Z > div > a')
        options[0].click()
        driver.implicitly_wait(0.1)
        firstoptions = driver.find_elements_by_css_selector('fieldset > div.Klq2ZNy50Z > div > ul > li > a')
        while len(firstoptions) == 0:
            options[0].click()
            driver.implicitly_wait(0.1)
            firstoptions = driver.find_elements_by_css_selector('fieldset > div.Klq2ZNy50Z > div > ul > li > a')
        if option_layer == 1:
            for i in range(len(firstoptions)):
                if "품절" in firstoptions[i].text:
                    continue
                option_name1, option_price = get_nameNprice(firstoptions[i].text)
                product.option_name_list.append(option_name1)
                product.option_price_list.append(option_price)
        elif option_layer == 2:
            for i in range(len(firstoptions)):
                firstoptions = driver.find_elements_by_css_selector('fieldset > div.Klq2ZNy50Z > div > ul > li > a')
                option_name1 = firstoptions[i].text
                firstoptions[i].click()
                # 2 번째옵션 탐색 시작
                options[1].click()
                secondoptions = driver.find_elements_by_css_selector('fieldset > div.Klq2ZNy50Z > div > ul > li > a')
                for j in range(len(secondoptions)):
                    option_name2, option_price = get_nameNprice(secondoptions[j].text)
                    product.option_name_list.append(option_name1 + "|" +option_name2)
                    product.option_price_list.append(option_price)
                options[0].click()
        elif option_layer == 3:
            for i in range(len(firstoptions)):
                firstoptions = driver.find_elements_by_css_selector('fieldset > div.Klq2ZNy50Z > div > ul > li > a')
                option_name1 = firstoptions[i].text
                firstoptions[i].click()
                # 2 번째옵션 탐색 시작
                options[1].click()
                secondoptions = driver.find_elements_by_css_selector('fieldset > div.Klq2ZNy50Z > div > ul > li > a')
                for j in range(len(secondoptions)):
                    secondoptions = driver.find_elements_by_css_selector('fieldset > div.Klq2ZNy50Z > div > ul > li > a')
                    option_name2 = secondoptions[j].text
                    secondoptions[j].click()
                    # 3 번째 옵션 탐색 시작
                    options[2].click()
                    thirdoptions = driver.find_elements_by_css_selector('fieldset > div.Klq2ZNy50Z > div > ul > li > a')
                    for k in range(len(thirdoptions)):
                        option_name3, option_price = get_nameNprice(thirdoptions[k].text)
                        product.option_name_list.append(option_name1 + "|" + option_name2 + "|" + option_name3)
                        product.option_price_list.append(option_price)
                        print(str(product.option_price_list[-1]) + " : 가격 | 이름 :" + product.option_name_list[-1])
                    options[1].click()
                options[0].click()
        else:
            print("옵션계층 존재하지 않음")
        options[0].click()
    except selenium.common.exceptions.NoSuchElementException:
        option_layer = 0
    product.option_layer = option_layer
    addopt_num = len(driver.find_elements_by_css_selector('fieldset > div.Klq2ZNy50Z > div > a')) - option_layer
    if addopt_num != 0:
        addopt = driver.find_elements_by_css_selector('fieldset > div.Klq2ZNy50Z > div > a')
        for i in range(option_layer, option_layer + addopt_num):
            print(f"추가 옵션 수집 {i}")
            addopt[i].click()
            addopt_name_list = []
            addopt_price_list = []
            a_addopt_list = driver.find_elements_by_css_selector('fieldset > div.Klq2ZNy50Z > div > ul > li > a')
            for a_addopt in a_addopt_list:
                addopt_name, addopt_price = get_nameNprice(a_addopt.text)
                addopt_name_list.append(addopt_name)
                addopt_price_list.append(addopt_price)
            addopt[i].click()
            product.addopt_name_list.append(addopt_name_list)
            product.addopt_price_list.append(addopt_price_list)
    deliveryfeebox = driver.find_elements_by_css_selector('fieldset > div > div > span > span')
    for deliveryfee in deliveryfeebox:
        if '00' in deliveryfee.text:
            product.delivery_fee = return_int(deliveryfee.text)
    sub_img = driver.find_elements_by_css_selector('#content > div > div > div > ul > li > a > img')[1:]
    for a_sub_img in sub_img:
        product.sub_img_src.append(a_sub_img.get_attribute('data-src'))
    exit_cnt = 0
    maxtime = time.time() + 5
    driver.find_element_by_css_selector('body').send_keys(Keys.END)
    while maxtime > time.time():
        detail_list = driver.find_elements_by_css_selector('div.se-main-container > div')
        detail_list += driver.find_elements_by_css_selector('div.se_component_wrap > div')
        product.detail_html = "<center>"
        if len(detail_list) != 0:
            for detail_box in detail_list:
                if 32000 < len(product.detail_html):
                    break
                try:
                    content = detail_box.find_element_by_css_selector('a > img')
                    print("일반 이미지")
                    if content != None:
                        product.detail_img_src.append(content.get_attribute('data-src'))
                        product.detail_html += f"<img src=\"{content.get_attribute('data-src')}\">"
                        continue
                except selenium.common.exceptions.NoSuchElementException:
                    None
                except:
                    traceback.print_exc()
                try:
                    content = detail_box.find_element_by_css_selector('div.se-section.se-section-material.se-section-align-center.se-l-default')  # 스토어팜 상품 링크
                    print("하이퍼링크")
                    if content != None:
                        link = content.find_element_by_tag_name('a').get_attribute('href')
                        img_link = content.find_element_by_tag_name('img').get_attribute('data-src')
                        text = content.text.split('\n')
                        product.detail_html += f"<span href=\"{link}\"><img src=\"{img_link}\"><strong>{text[0]} 가격 : {text[5]}</strong></span>"
                        continue
                except selenium.common.exceptions.NoSuchElementException:
                    None
                except:
                    traceback.print_exc()
                try:
                    content = detail_box.find_element_by_css_selector('div.se-section.se-section-text.se-l-default')
                    print("텍스트")
                    if content != None:
                        word_list = content.text.split('\n')
                        for word in word_list:
                            product.detail_html += f"<p style=\" font-size:2em;color:#000000;\">{word}</p>"
                except selenium.common.exceptions.NoSuchElementException:
                    None
                except:
                    traceback.print_exc()
    product.detail_html += "</center>"
    if 32766 < len(product.detail_html):
        print("html 잘린부분있음")
        product.detail_html = product.detail_html[0:32765]
    if maxtime < time.time():
        print("타임오버")
    else:
        print("디테일 수집완료")
    # 태그정보 수집 시작
    tags = driver.find_elements_by_css_selector('#INTRODUCE > div > div.jqaBjC05ww > ul > li > a')
    for tag in tags:
        product.tag_list.append(tag.text)
        print(tag.text, end='')
    # 상품정보 맨위에 제공되는 것
    product_infobox = driver.find_element_by_css_selector('#INTRODUCE > div > div > div > div > table > tbody').text
    product.product_num, product.product_status, product.brand, product.model_name, product.origin, product.manufacturer = get_major_info(product_infobox)
    product.origin = product.origin
    product.origin_id = get_origin_id(product.origin)
    try:
        importer = product.origin.split('(')[-1]
        importer = importer.replace(')', '')
        if importer[0] == '주':
            importer = "(주)" + importer[1:]
        product.importer = importer
    except:
        print("수입사 존재하지않음")
    # as 정보 및 인증정보 획득
    as_specialnote = driver.find_element_by_css_selector('div._3EFpctgsdH > table > tbody').text
    product.as_call_number, product.as_info, product.specialnote, product.certifiedinfo = get_ascallnumNspecialnote(as_specialnote)
    # 상품정보 관련 문의사항은 QNA에 남겨주세요 아래 부분은 카테고리에 따라서 내용이 바뀐다. 나중에 수집하도록한다.
    # AS 안내와 KC 인증 도 있는데 카테고리에 따라서 KC 인증은 꼭 필요하다.
    terminfo = driver.find_element_by_css_selector('#INTRODUCE > div > div.trade_terms_info > div > table').text
    product.return_fee = get_terminfo(terminfo)

    driver.quit()
    print(product.product_name + "수집완료")
    return product


def upload_items(driver, excel_path, jpg_pathes):
    if len(jpg_pathes) == 0:
        print("내보내기를 먼저할 것")
        return -1
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.modal.fade.seller-layer-modal.in > div > div > div.modal-footer > div > button.btn.btn-default')))
        driver.find_element_by_css_selector('body > div.modal.fade.seller-layer-modal.in > div > div > div.modal-footer > div > button.btn.btn-default').click()
    except:
        traceback.print_exc()
    print("고객 확인창 끄기")
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.modal.fade.seller-layer-modal.in > div > div > div.modal-footer > div > div > button')))
        driver.find_element_by_css_selector('body > div.modal.fade.seller-layer-modal.in > div > div > div.modal-footer > div > div > button').click()
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div:nth-child(1) > div > div > div.modal-footer > div > span:nth-child(2) > button')))
        driver.find_element_by_css_selector('body > div:nth-child(1) > div > div > div.modal-footer > div > span:nth-child(2) > button').click()
    except:
        traceback.print_exc()
    print("as 전화 인증 끄기")
    driver.implicitly_wait(0.5)
    driver.find_element_by_css_selector('#seller-lnb > div > div:nth-child(1) > ul > li:nth-child(1) > a').click()
    driver.implicitly_wait(0.5)
    driver.find_element_by_css_selector('#seller-lnb > div > div:nth-child(1) > ul > li.active > ul > li:nth-child(3) > a').click()
    print("일괄 등록 페이지로 이동")
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#seller-content > ui-view > div > div.panel.panel-seller > div > div:nth-child(1) > div.seller-btn-right > div > button:nth-child(3)')))
    # 이미지 입력 시작
    # full_img_path_str = str()
    for i in range(len(jpg_pathes)):
        try:
            driver.find_element_by_css_selector(
                '#seller-content > ui-view > div > div.panel.panel-seller > div > div:nth-child(1) > div.seller-btn-right > div > button:nth-child(3)').click()
        except:
            traceback.print_exc()
        while len(driver.window_handles) != 2:
            print("창이 뜰때까지 대기중")
        driver.switch_to.window(driver.window_handles[-1])
        # full_img_path_str += f"{resource_path(jpg_pathes[i])}"
        time.sleep(0.3)
        try:
            driver.find_element_by_css_selector('body > div > input').send_keys(jpg_pathes[i])
        except:
            traceback.print_exc()
            time.sleep(0.5)
            driver.switch_to.window(driver.window_handles[-1])
            driver.find_element_by_css_selector('body > div > input').send_keys(jpg_pathes[i])
        print(os.path.abspath(jpg_pathes[i]))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'body > div > div.nmu_main > div.nmu_button_area > button.nmu_button.nmu_button_close')))
        time.sleep(0.3)
        while True:
            try:
                driver.find_element_by_css_selector(
                    'body > div > div.nmu_main > div.nmu_button_area > button.nmu_button.nmu_button_close').click()
                break
            except:
                traceback.print_exc()
        driver.switch_to.window(driver.window_handles[0])
    driver.find_element_by_css_selector('#seller-content > ui-view > div > div:nth-child(2) > form > input[type=file]:nth-child(1)').send_keys(os.path.abspath(excel_path))

# def crawl_itemlist_nstore(url):
