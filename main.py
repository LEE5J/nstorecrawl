import traceback
import requests, sys, os, time
import pandas as pd
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, pyqtProperty, QSize, QBasicTimer
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
# from openpyxl import Workbook
import urllib.request
from tools import *
from search_engine import *
import threading
import webbrowser
from urllib.parse import quote
from selenium import webdriver
form_class = uic.loadUiType(resource_path("nstore.ui"))[0]
sys.setrecursionlimit(5000)




class main_frame(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_event()
        self.chkbox_list = []
        self.product_list = []
        self.errorurl_list = []  # 크롤링 실패한 것들을 모아놓는 곳
        self.current_row = 0
        self.show()
        self.id = None
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
            driver.quit()
        except selenium.common.exceptions.WebDriverException:
            QMessageBox.about(self, "완료", "내보내기 완료")
        except:
            traceback.print_exc()


    def init_event(self):
        self.crawl_item_btn.pressed.connect(self.search_a_item_nstore)
        self.crawl_store_btn.pressed.connect(self.crawl_a_store)
        self.retry_btn.pressed.connect(self.retry_errorurl)
        self.checkall_btn.pressed.connect(self.checkall)
        self.uncheckall_btn.pressed.connect(self.uncheckall)
        self.delete_btn.pressed.connect(self.delete_item)
        self.search_start_btn.pressed.connect(self.load_a_store)
        self.search_num.textChanged.connect(self.numberfiltering)
        self.export_data_btn.pressed.connect(self.export_data)
        self.search_category_btn.pressed.connect(self.search_category)
        self.upload_btn.pressed.connect(self.upload2naver)
        # self.resizeCompleted.connect(self.resize_qtable)

    def closeEvent(self, event):
        self.deleteLater()


    # def resize_qtable(self):
        # self.data_table = QTableWidget()
        # self.data_table.resize(Qsize(self.get))
    def search_category(self):
        search_word, flag = QInputDialog.getText(self,"카테고리 검색", "검색어 입력")
        try:
            box = QMessageBox()
            box.setIcon(QMessageBox.Information)
            box.setWindowTitle('결과')
            box.setText(search_category(search_word))
            box.setStandardButtons(QMessageBox.Yes)
            box.exec_()
        except:
            traceback.print_exc()

    def numberfiltering(self):
        try:
            if self.search_num.text() == "":
                return 0
            if len(self.item_link_list) < int(self.search_num.text()):
                self.search_num.setText(str(len(self.item_link_list)))
            self.expect_time.setText(f'{int(int(self.search_num.text()) / 4 )}분{int(int(self.search_num.text())%4)*32}초')
        except:
            self.search_num.clear()

    def init_load_a_store(self):
        try:
            thread = threading.Thread(target=self.load_a_store, args=())
            thread.start()
        except:
            traceback.print_exc()

    def load_a_store(self):
        start_time = time.time()
        item_link_list = self.item_link_list
        item_link_list = item_link_list[:int(self.search_num.text())]
        self.progressBar.setValue(0)
        print("크롤링 시작")
        print(item_link_list)
        for i, url in enumerate(item_link_list):
            self.progressBar.setValue(int((100 * i) / len(item_link_list)))
            self.repaint()
            self.set_item(url)
            self.progressBar.repaint()
        self.progressBar.setValue(100)
        self.url_LE.clear()
        self.retry_errorurl()
        self.retry_errorurl()
        self.retry_errorurl()
        running_time = int(time.time() - start_time)
        self.running_time.setText(f'{int(running_time/60)}분{ running_time % 60 }초')
        self.item_link_list.clear()
        self.search_num.clear()
        self.max_search_num.setText('0')

    def upload2naver(self):

        try:
            driver = webdriver.Chrome("chromedriver.exe")
        except:
            driver = webdriver.Chrome("../chromedriver.exe")
            traceback.print_exc()
        driver.get('https://sell.smartstore.naver.com/#/login')
        if self.is_sellerid :
            print("판매자 아이디로 진행")
            driver.execute_script(f"document.getElementById('loginId').value = '{self.id}'")
            driver.execute_script(f"document.getElementById('loginPassword').value = '{self.pw}'")
            driver.find_element_by_css_selector('#loginButton').click()
        else:
            print("네이버아이디로 진행")
            while True:
                try:
                    driver.find_element_by_css_selector(
                        'body > ui-view.wrap > div.seller-join-wrap > div > div > div > form > div.panel.panel-seller > ul > li:nth-child(2) > a').click()
                except:
                    None
                if driver.current_url == 'https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fsell.smartstore.naver.com%2F%23%2FnaverLoginCallback%3Furl%3Dhttps%253A%252F%252Fsell.smartstore.naver.com%252F%2523':
                    break
            print("로그인페이지로 이동")
            driver.execute_script(f"document.getElementById('id').value = '{self.id}'")
            driver.execute_script(f"document.getElementById('pw').value = '{self.pw}'")
            driver.find_element_by_xpath('//*[@id="log.login"]').click()
            time.sleep(1)
            if 'https://nid.naver.com/login/ext/deviceConfirm.nhn' in driver.current_url:
                driver.find_element_by_css_selector('#new\.save').click()
        while True:
            if driver.current_url == 'https://sell.smartstore.naver.com/#/home/dashboard':
                break
        print("로그인 완료 등록 시작")
        upload_items(driver, f"{self.prefix}/{self.prefix}.xls", self.jpg_pathes)

    def export_data(self):
        if self.id == None:
            self.id, flag = QInputDialog.getText(self, 'ID', None)
            self.pw, flag = QInputDialog.getText(self, 'PW', None)
            box = QMessageBox()
            box.setIcon(QMessageBox.Question)
            box.setWindowTitle('아이디 유형')
            box.setText('스토어 팜 아이디 유형을 선택해주세요')
            box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            buttonY = box.button(QMessageBox.Yes)
            buttonY.setText('판매자 아이디')
            buttonN = box.button(QMessageBox.No)
            buttonN.setText('네이버 아이디')
            box.exec_()
            if box.clickedButton() == buttonY:
                self.is_sellerid = True
            elif box.clickedButton() == buttonN:
                self.is_sellerid = False
        prefix = self.id + time.strftime('%y%m%d%H%M%S', time.localtime(time.time()))
        self.prefix = prefix
        os.makedirs(f'./{prefix}')
        os.chdir(f'./{prefix}')
        product_header = ['상품상태', '카테고리ID', '상품명', '판매가', '재고수량', 'A/S 안내내용', 'A/S 전화번호', '대표 이미지 파일명', '추가 이미지 파일명',
                          '상품 상세정보', '판매자 상품코드', '판매자 바코드', '제조사', '브랜드', '제조일자', '유효일자', '부가세', '미성년자 구매',
                          '구매평 노출여부', '원산지 코드', '수입사', '복수원산지 여부', '원산지 직접입력', '배송방법', '배송비 유형', '기본배송비',
                          '배송비 결제방식', '조건부무료-상품판매가합계', '수량별부과-수량', '반품배송비', '교환배송비', '지역별 차등배송비 정보', '별도설치비',
                          '판매자 특이사항', '즉시할인 값', '즉시할인 단위', '복수구매할인 조건 값', '복수구매할인 조건 단위', '복수구매할인 값', '복수구매할인 단위',
                          '상품구매시 포인트 지급 값', '상품구매시 포인트 지급 단위', '텍스트리뷰 작성시 지급 포인트', '포토/동영상 리뷰 작성시 지급 포인트',
                          '한달사용\n텍스트리뷰 작성시 지급 포인트', '한달사용\n포토/동영상리뷰 작성시 지급 포인트', '톡톡친구/스토어찜고객\n리뷰 작성시 지급 포인트',
                          '무이자 할부 개월', '사은품', '옵션형태', '옵션명', '옵션값', '옵션가', '옵션 재고수량', '추가상품명', '추가상품값',
                          '추가상품가', '추가상품 재고수량', '상품정보제공고시 품명', '상품정보제공고시 모델명', '상품정보제공고시 인증허가사항',
                          '상품정보제공고시 제조자', '스토어찜회원 전용여부', '문화비 소득공제', 'ISBN', '독립출판']
        data = []
        self.jpg_pathes = []
        for i, product in enumerate(self.product_list):
            try:
                data.append(convert_to_frame(product, f"{prefix}{i}", i, self.jpg_pathes))
                print(data[-1])
            except:
                traceback.print_exc()
        try:
            df = pd.DataFrame(data, index=None, columns=product_header)
        except:
            traceback.print_exc()
        try:
            df.to_excel(f"{prefix}.xls", encoding='cp949', index=False)
        except:
            traceback.print_exc()
        if len(self.jpg_pathes) != 0:
            self.upload_btn.setEnabled(True)
        os.chdir('..')
        try:
            QMessageBox.about(self, "완료", "내보내기 완료")
        except:
            traceback.print_exc()
        return prefix

    def delete_item(self):
        temp_product_list = []
        for i in range(len(self.chkbox_list)):
            if self.chkbox_list[i].isChecked() == False:
                temp_product_list.append(self.product_list[i])
        self.product_list = temp_product_list
        # self.data_table = QTableWidget()
        self.data_table.setRowCount(0)
        self.chkbox_list = []
        for i in range(len(self.product_list)):
            self.batch_item(self.product_list[i])

    def url_img_button(self, url, img_src):
        img = urllib.request.urlopen(img_src).read()
        pixmap = QPixmap()
        pixmap.loadFromData(img)
        pixmap.scaled(100, 90)
        icon = QIcon(pixmap)
        btn = QPushButton()
        btn.setIcon(icon)
        btn.setIconSize(QSize(100,90))
        btn.setFixedSize(100, 90)
        btn.pressed.connect(lambda: webbrowser.open(url))
        return btn

    def crawl_a_store(self):
        self.success_num.setText('0')
        self.fail_num.setText('0')
        start_time = time.time()
        # 페이지 최대값 알아내기
        if "category" in self.url_LE.text():
            if self.url_LE.text().endswith('/'): # 존재하는 경우의 수가 아님
                url = f"{self.url_LE.text()}&st=POPULAR&free=false&dt=IMAGE&page=1&size=80"
            else:
                if self.url_LE.text().endswith('?cp=1'):
                    url = f"{self.url_LE.text()}&st=POPULAR&free=false&dt=IMAGE&page=1&size=80"
                else:
                    url = f"{self.url_LE.text()}?st=POPULAR&free=false&dt=IMAGE&page=1&size=80"
        else:
            if self.url_LE.text().endswith('/'):
                url = f"{self.url_LE.text()}category/ALL?st=POPULAR&free=false&dt=IMAGE&page=1&size=80"
            else:
                url = f"{self.url_LE.text()}/category/ALL?st=POPULAR&free=false&dt=IMAGE&page=1&size=80"
        self.search_target = url.split('/')[-3]
        print(url)
        try:
            req = requests.get(url)
        except requests.exceptions.ConnectionError:
            print("url오류의심")
            return -2
        if req.status_code == requests.ConnectionError:
            print("접속오류")
            return -1
        else:
            print("접속성공")
        html = BeautifulSoup(req.text, "html.parser")
        try:
            max_page = int(html.select('#CategoryProducts > div > a')[-2].text)
        except:
            max_page = 1
            print(sys.exc_info())
            etype, evalue, tb = sys.exc_info()
            traceback.print_exception(etype, evalue, tb)
            traceback.print_exc()
        print("최대페이지획득완료")
        # 아이템 리스트 크롤링 시작
        item_link_list = []
        for i in range(1,max_page+1):
            if "category" in self.url_LE.text():
                if self.url_LE.text().endswith('/'):  # 존재하는 경우의 수가 아님
                    url = f"{self.url_LE.text()}&st=POPULAR&free=false&dt=IMAGE&page={i}&size=80"
                else:
                    if self.url_LE.text().endswith('?cp=1'):
                        url = f"{self.url_LE.text()}&st=POPULAR&free=false&dt=IMAGE&page={i}&size=80"
                    else:
                        url = f"{self.url_LE.text()}?st=POPULAR&free=false&dt=IMAGE&page={i}&size=80"
            else:
                if self.url_LE.text().endswith('/'):
                    url = f"{self.url_LE.text()}category/ALL?st=POPULAR&free=false&dt=IMAGE&page={i}&size=80"
                else:
                    url = f"{self.url_LE.text()}/category/ALL?st=POPULAR&free=false&dt=IMAGE&page={i}&size=80"
            print(url + "을 요청합니다")
            req = requests.get(url)
            if req.status_code == requests.ConnectionError:
                print("접속오류")
            html = BeautifulSoup(req.text, "html.parser")
            print("파싱 성공")
            item_list = html.select('#CategoryProducts > ul > li > a')
            if len(item_list) == 0:
                print("아이템을 가져오지못함" + url)
            # CategoryProducts > ul > li:nth-child(74) > a
            for j in range(len(item_list)):
                src = item_list[j]['href']
                item_link_list.append(f"https://smartstore.naver.com{src}")
                print(str(j) + " https://smartstore.naver.com" + str(src))
        self.item_link_list = item_link_list
        self.max_search_num.setText(str(len(item_link_list)))
        self.search_num.setText(str(len(item_link_list)))
        self.expect_time.setText(f'{int(len(item_link_list)*32 / 60 )}분{int(len(item_link_list)%4)*32}초')
        minute = int(int(time.time() - start_time) / 60)
        sec = int(time.time() - start_time) % 60
        self.running_time.setText(f'{minute}분{sec}초')

    def search_a_item_nstore(self):
        self.success_num.setText('0')
        self.fail_num.setText('0')
        url = self.url_LE.text()
        if '/products/' in url:
            self.url_LE.clear()
            self.set_item(url)
        else:
            self.url_LE.setText("상품URL 아님")

    def batch_item(self, product):
        self.data_table.setRowCount(self.data_table.rowCount()+1)
        self.chkbox_list.append(QCheckBox())
        self.data_table.setCellWidget(self.data_table.rowCount()-1, 0, self.chkbox_list[-1])
        self.data_table.setCellWidget(self.data_table.rowCount()-1, 1, self.url_img_button(product.url, product.main_img_src))
        if int(self.data_table.rowCount()) <= 1:
            self.data_table.resizeRowsToContents()
            self.data_table.resizeColumnsToContents()
        self.data_table.setItem(self.data_table.rowCount()-1, 2, QTableWidgetItem(product.product_name))
        self.data_table.setItem(self.data_table.rowCount() - 1, 3, QTableWidgetItem(str(product.original_price)))
        self.data_table.setItem(self.data_table.rowCount()-1, 4, QTableWidgetItem(str(product.saled_price)))
        if len(product.option_name_list) != 0:
            self.data_table.setItem(self.data_table.rowCount()-1, 5, QTableWidgetItem(str(product.option_name_list)))
        if len(product.option_price_list) != 0:
            self.data_table.setItem(self.data_table.rowCount()-1, 6, QTableWidgetItem(str(product.option_price_list)))
        if len(product.addopt_name_list) != 0:
            self.data_table.setItem(self.data_table.rowCount()-1, 7, QTableWidgetItem(str(product.addopt_name_list)))
        if len(product.addopt_price_list) != 0:
            self.data_table.setItem(self.data_table.rowCount()-1, 8, QTableWidgetItem(str(product.addopt_price_list)))
        self.data_table.setItem(self.data_table.rowCount()-1, 9, QTableWidgetItem(str(product.delivery_fee)))
        self.data_table.setItem(self.data_table.rowCount() - 1, 10, QTableWidgetItem(str(product.return_fee)))
        if len(product.main_img_src) != 0 and product.url != 'https://ssl.pstatic.net/static/nid/membership/rw_ico_digitalpack.png':
            self.data_table.setItem(self.data_table.rowCount()-1, 11, QTableWidgetItem(str(product.main_img_src)))
        if len(product.sub_img_src) != 0:
            self.data_table.setItem(self.data_table.rowCount()-1, 12, QTableWidgetItem(str(product.sub_img_src)))
        if len(product.detail_html) != 0:
            self.data_table.setItem(self.data_table.rowCount()-1, 13, QTableWidgetItem(str(product.detail_html)))
        if len(product.tag_list) != 0:
            self.data_table.setItem(self.data_table.rowCount() - 1, 14, QTableWidgetItem(str(product.tag_list)))
        self.data_table.setItem(self.data_table.rowCount() - 1, 15, QTableWidgetItem(str(product.origin)))
        self.data_table.setItem(self.data_table.rowCount() - 1, 16, QTableWidgetItem(str(product.importer)))

        self.data_table.setItem(self.data_table.rowCount() - 1, 17, QTableWidgetItem(str(product.as_call_number)))
        self.data_table.setItem(self.data_table.rowCount() - 1, 18, QTableWidgetItem(str(product.as_info)))
        self.data_table.setItem(self.data_table.rowCount() - 1, 19, QTableWidgetItem(str(product.brand)))
        self.data_table.setItem(self.data_table.rowCount() - 1, 20, QTableWidgetItem(str(product.manufacturer)))
        self.data_table.setItem(self.data_table.rowCount() - 1, 21, QTableWidgetItem(str(product.product_status)))
        self.data_table.setItem(self.data_table.rowCount() - 1, 22, QTableWidgetItem(str(product.category_id)))

    def set_item(self, url):
        try:
            product = crawl_a_item_nstore(url)
            self.batch_item(product)
            self.product_list.append(product)
            self.success_num.setText(str(int(self.success_num.text()) + 1))
            print(self.success_num.text() + "완료")
        except:
            # print(sys.exc_info())
            etype, evalue, tb = sys.exc_info()
            traceback.print_exception(etype, evalue, tb)
            traceback.print_exc()
            product = Product()
            product.url = url
            product.main_img_src = "https://ssl.pstatic.net/static/nid/membership/rw_ico_digitalpack.png"
            product.product_name = "가져오기 실패상품"
            self.batch_item(product)
            self.product_list.append(product)
            self.fail_num.setText(str(int(self.fail_num.text()) + 1))
            if int(self.data_table.rowCount()) <= 1:
                self.data_table.resizeRowsToContents()
                self.data_table.resizeColumnsToContents()

    def retry_errorurl(self):
        error_url = []
        error_index = []
        for i in range(len(self.product_list)):
            if self.product_list[i].product_name == "가져오기 실패상품":
                error_url.append(self.product_list[i].url)
                error_index.append(i)
        print("탐색완료")
        if len(error_url) == 0:
            return 0
        self.data_table.setRowCount(0)
        for i in range(len(error_index)):
            try:
                self.product_list.pop(error_index[-1-i])
            except:
                traceback.print_exc()

        print("초기화 완료 재배치 시작")
        self.chkbox_list = []
        for i in range(len(self.product_list)):
            self.batch_item(self.product_list[i])
        print("재검색 시작")
        for i in range(len(error_index)):
            self.set_item(error_url[i])

    def checkall(self):
        for chkbox in self.chkbox_list:
            chkbox.setChecked(True)

    def uncheckall(self):
        for chkbox in self.chkbox_list:
            chkbox.setChecked(False)








def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    try:
        # log.debug('debug')
    # log.info('info')
    # log.warning('warning')
    # log.error('error')
    # log.critical('critical')
        app = QApplication(sys.argv)
        ex = main_frame()
        sys.exit(app.exec_())
    except:
        traceback.print_exc()
