import logging, sys, os, requests
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


data = {'국산': '00', '원양산': '01', '수입산': '02', '상세설명에 표시': '03',
        '직접입력': '04', '원산지 표기 의무대상 아님': '05', '강원도': '0001',
        '경기도': '0002',
        '경상남도': '0003',
        '경상북도': '0004',
        '광주광역시': '0005',
        '대구광역시': '0006',
        '대전광역시': '0007',
        '부산광역시': '0008',
        '서울특별시': '0009',
        '울산광역시': '0010',
        '인천광역시': '0011',
        '전라남도': '0012',
        '전라북도': '0013',
        '제주특별자치도': '0014',
        '충청남도': '0015',
        '충청북도': '0016',
        '세종특별자치시': '0017',
        '태평양': '0100',
        '대서양': '0101',
        '인도양': '0102',
        '남빙양': '0103',
        '북빙양': '0104',
        '아시아': '0200',
        '유럽': '0201',
        '아프리카': '0202',
        '오세아니아': '0203',
        '북아메리카(북미)': '0204',
        '라틴아메리카(남미)': '0205',
        '춘천시': '0001110',
        '원주시': '0001130',
        '강릉시': '0001150',
        '동해시': '0001170',
        '태백시': '0001190',
        '속초시': '0001210',
        '삼척시': '0001230',
        '홍천군': '0001720',
        '횡성군': '0001730',
        '영월군': '0001750',
        '평창군': '0001760',
        '정선군': '0001770',
        '철원군': '0001780',
        '화천군': '0001790',
        '양구군': '0001800',
        '인제군': '0001810',
        '고성군': '0001820',
        '양양군': '0001830',
        '수원시': '0002110',
        '수원시 장안구': '0002111',
        '수원시 권선구': '0002113',
        '수원시 팔달구': '0002115',
        '수원시 영통구': '0002117',
        '성남시': '0002130',
        '성남시 수정구': '0002131',
        '성남시 중원구': '0002133',
        '성남시 분당구': '0002135',
        '의정부시': '0002150',
        '안양시': '0002170',
        '안양시 만안구': '0002171',
        '안양시 동안구': '0002173',
        '부천시': '0002190',
        '광명시': '0002210',
        '평택시': '0002220',
        '동두천시': '0002250',
        '안산시': '0002270',
        '안산시 상록구': '0002271',
        '안산시 단원구': '0002273',
        '고양시': '0002280',
        '고양시 덕양구': '0002281',
        '고양시 일산동구': '0002285',
        '고양시 일산서구': '0002287',
        '과천시': '0002290',
        '구리시': '0002310',
        '남양주시': '0002360',
        '오산시': '0002370',
        '시흥시': '0002390',
        '군포시': '0002410',
        '의왕시': '0002430',
        '하남시': '0002450',
        '용인시': '0002460',
        '용인시 처인구': '0002461',
        '용인시 기흥구': '0002463',
        '용인시 수지구': '0002465',
        '파주시': '0002480',
        '이천시': '0002500',
        '안성시': '0002550',
        '김포시': '0002570',
        '화성시': '0002590',
        '광주시': '0002610',
        '양주시': '0002630',
        '포천시': '0002650',
        '여주시': '0002670',
        '연천군': '0002800',
        '가평군': '0002820',
        '양평군': '0002830',
        '창원시': '0003120',
        '창원시 의창구': '0003121',
        '창원시 성산구': '0003123',
        '창원시 마산합포구': '0003125',
        '창원시 마산회원구': '0003127',
        '창원시 진해구': '0003129',
        '진주시': '0003170',
        '통영시': '0003220',
        '사천시': '0003240',
        '김해시': '0003250',
        '밀양시': '0003270',
        '거제시': '0003310',
        '양산시': '0003330',
        '의령군': '0003720',
        '함안군': '0003730',
        '창녕군': '0003740',
        '고성군': '0003820',
        '남해군': '0003840',
        '하동군': '0003850',
        '산청군': '0003860',
        '함양군': '0003870',
        '거창군': '0003880',
        '합천군': '0003890',
        '포항시': '0004110',
        '포항시 남구': '0004111',
        '포항시 북구': '0004113',
        '경주시': '0004130',
        '김천시': '0004150',
        '안동시': '0004170',
        '구미시': '0004190',
        '영주시': '0004210',
        '영천시': '0004230',
        '상주시': '0004250',
        '문경시': '0004280',
        '경산시': '0004290',
        '군위군': '0004720',
        '의성군': '0004730',
        '청송군': '0004750',
        '영양군': '0004760',
        '영덕군': '0004770',
        '청도군': '0004820',
        '고령군': '0004830',
        '성주군': '0004840',
        '칠곡군': '0004850',
        '예천군': '0004900',
        '봉화군': '0004920',
        '울진군': '0004930',
        '울릉군': '0004940',
        '동구': '0005110',
        '서구': '0005140',
        '남구': '0005155',
        '북구': '0005170',
        '광산구': '0005200',
        '중구': '0006110',
        '동구': '0006140',
        '서구': '0006170',
        '남구': '0006200',
        '북구': '0006230',
        '수성구': '0006260',
        '달서구': '0006290',
        '달성군': '0006710',
        '동구': '0007110',
        '중구': '0007140',
        '서구': '0007170',
        '유성구': '0007200',
        '대덕구': '0007230',
        '중구': '0008110',
        '서구': '0008140',
        '동구': '0008170',
        '영도구': '0008200',
        '부산진구': '0008230',
        '동래구': '0008260',
        '남구': '0008290',
        '북구': '0008320',
        '해운대구': '0008350',
        '사하구': '0008380',
        '금정구': '0008410',
        '강서구': '0008440',
        '연제구': '0008470',
        '수영구': '0008500',
        '사상구': '0008530',
        '기장군': '0008710',
        '종로구': '0009110',
        '중구': '0009140',
        '용산구': '0009170',
        '성동구': '0009200',
        '광진구': '0009215',
        '동대문구': '0009230',
        '중랑구': '0009260',
        '성북구': '0009290',
        '강북구': '0009305',
        '도봉구': '0009320',
        '노원구': '0009350',
        '은평구': '0009380',
        '서대문구': '0009410',
        '마포구': '0009440',
        '양천구': '0009470',
        '강서구': '0009500',
        '구로구': '0009530',
        '금천구': '0009545',
        '영등포구': '0009560',
        '동작구': '0009590',
        '관악구': '0009620',
        '서초구': '0009650',
        '강남구': '0009680',
        '송파구': '0009710',
        '강동구': '0009740',
        '중구': '0010110',
        '남구': '0010140',
        '동구': '0010170',
        '북구': '0010200',
        '울주군': '0010710',
        '중구': '0011110',
        '동구': '0011140',
        '미추홀구': '0011177',
        '연수구': '0011185',
        '남동구': '0011200',
        '부평구': '0011237',
        '계양구': '0011245',
        '서구': '0011260',
        '강화군': '0011710',
        '옹진군': '0011720',
        '목포시': '0012110',
        '여수시': '0012130',
        '순천시': '0012150',
        '나주시': '0012170',
        '광양시': '0012230',
        '담양군': '0012710',
        '곡성군': '0012720',
        '구례군': '0012730',
        '고흥군': '0012770',
        '보성군': '0012780',
        '화순군': '0012790',
        '장흥군': '0012800',
        '강진군': '0012810',
        '해남군': '0012820',
        '영암군': '0012830',
        '무안군': '0012840',
        '함평군': '0012860',
        '영광군': '0012870',
        '장성군': '0012880',
        '완도군': '0012890',
        '진도군': '0012900',
        '신안군': '0012910',
        '전주시': '0013110',
        '전주시 완산구': '0013111',
        '전주시 덕진구': '0013113',
        '군산시': '0013130',
        '익산시': '0013140',
        '정읍시': '0013180',
        '남원시': '0013190',
        '김제시': '0013210',
        '완주군': '0013710',
        '진안군': '0013720',
        '무주군': '0013730',
        '장수군': '0013740',
        '임실군': '0013750',
        '순창군': '0013770',
        '고창군': '0013790',
        '부안군': '0013800',
        '제주시': '0014110',
        '서귀포시': '0014130',
        '천안시': '0015130',
        '천안시 동남구': '0015131',
        '천안시 서북구': '0015133',
        '공주시': '0015150',
        '보령시': '0015180',
        '아산시': '0015200',
        '서산시': '0015210',
        '논산시': '0015230',
        '계룡시': '0015250',
        '당진시': '0015270',
        '금산군': '0015710',
        '부여군': '0015760',
        '서천군': '0015770',
        '청양군': '0015790',
        '홍성군': '0015800',
        '예산군': '0015810',
        '태안군': '0015825',
        '청주시': '0016110',
        '청주시 상당구': '0016111',
        '청주시 서원구': '0016112',
        '청주시 흥덕구': '0016113',
        '청주시 청원구': '0016114',
        '충주시': '0016130',
        '제천시': '0016150',
        '보은군': '0016720',
        '옥천군': '0016730',
        '영동군': '0016740',
        '증평군': '0016745',
        '진천군': '0016750',
        '괴산군': '0016760',
        '음성군': '0016770',
        '단양군': '0016800',
        '그루지야': '0200000',
        '네팔': '0200001',
        '대만': '0200002',
        '동티모르': '0200003',
        '라오스': '0200004',
        '레바논': '0200005',
        '리비아': '0200006',
        '마카오': '0200007',
        '말레이시아': '0200008',
        '몰디브': '0200009',
        '몽골': '0200010',
        '미얀마': '0200011',
        '바레인': '0200012',
        '방글라데시': '0200013',
        '베트남': '0200014',
        '부탄': '0200015',
        '북한': '0200016',
        '브루나이': '0200017',
        '사우디아라비아': '0200018',
        '스리랑카': '0200019',
        '시리아': '0200020',
        '싱가포르': '0200021',
        '아랍에미리트': '0200022',
        '아르메니아': '0200023',
        '아프가니스탄': '0200024',
        '예멘': '0200025',
        '오만': '0200026',
        '요르단': '0200027',
        '우즈베키스탄': '0200028',
        '우크라이나': '0200029',
        '이라크': '0200030',
        '이란': '0200031',
        '이스라엘': '0200032',
        '인도': '0200033',
        '인도네시아': '0200034',
        '인도양식민지': '0200035',
        '일본': '0200036',
        '중국': '0200037',
        '카자흐스탄': '0200038',
        '카타르': '0200039',
        '캄보디아': '0200040',
        '쿠웨이트': '0200041',
        '키리기스스탄': '0200042',
        '타지키스탄': '0200043',
        '태국': '0200044',
        '투르크메니스탄': '0200045',
        '티베트': '0200046',
        '파키스탄': '0200047',
        '필리핀': '0200048',
        '홍콩': '0200049',
        '그리스': '0201000',
        '그린란드': '0201001',
        '네덜란드': '0201002',
        '노르웨이': '0201003',
        '덴마크': '0201004',
        '독일': '0201005',
        '라트비아': '0201006',
        '러시아연방': '0201007',
        '룩셈부르크': '0201008',
        '리투아니아': '0201009',
        '리히텐슈타인': '0201010',
        '마케도니아': '0201011',
        '말타': '0201012',
        '모나코': '0201013',
        '몰도바공화국': '0201014',
        '몰타': '0201015',
        '바티칸': '0201016',
        '벨기에': '0201017',
        '벨라루스': '0201018',
        '벨로루시': '0201019',
        '보스니아-헤르체고비나': '0201020',
        '불가리아': '0201021',
        '사이프러스': '0201022',
        '스웨덴': '0201023',
        '스위스': '0201024',
        '스페인': '0201025',
        '슬로바키아': '0201026',
        '슬로베니아': '0201027',
        '아이슬란드': '0201028',
        '아일랜드공화국': '0201029',
        '아제르바이잔': '0201030',
        '안도라': '0201031',
        '알메니아': '0201032',
        '알바니아': '0201033',
        '에스토니아': '0201034',
        '영국': '0201035',
        '오스트리아': '0201036',
        '유고': '0201037',
        '이탈리아': '0201038',
        '조지아': '0201039',
        '체코': '0201040',
        '크로아티아': '0201041',
        '터키': '0201042',
        '페로스제도': '0201043',
        '포르투갈': '0201044',
        '폴란드': '0201045',
        '프랑스': '0201046',
        '핀란드': '0201047',
        '헝가리': '0201048',
        '루마니아': '0201049',
        '세르비아': '0201050',
        '가나': '0202000',
        '가봉': '0202001',
        '가이아나': '0202002',
        '감비아': '0202003',
        '기니': '0202004',
        '기니비사우': '0202005',
        '나미비아': '0202006',
        '나이지리아': '0202007',
        '남아프리카공화국': '0202008',
        '니제르': '0202009',
        '라이베리아': '0202010',
        '레소토': '0202011',
        '르완다': '0202012',
        '마다가스카르': '0202013',
        '마르티니크': '0202014',
        '말라위': '0202015',
        '말리': '0202016',
        '모로코': '0202017',
        '모리셔스': '0202018',
        '모리타니': '0202019',
        '모잠비크': '0202020',
        '베냉': '0202021',
        '보츠와나': '0202022',
        '부룬디': '0202023',
        '부르키나파소': '0202024',
        '사오토메프린시페': '0202025',
        '상투메 프린시페': '0202026',
        '서사하라': '0202027',
        '세네갈': '0202028',
        '세이셀': '0202029',
        '소말리아': '0202030',
        '수단': '0202031',
        '스와질랜드': '0202032',
        '시에라리온': '0202033',
        '알제리': '0202034',
        '앙골라': '0202035',
        '에디오피아': '0202036',
        '에리트리아': '0202037',
        '우간다': '0202038',
        '이집트': '0202039',
        '잠비아': '0202040',
        '적도기니공화국': '0202041',
        '중앙아프리카공화국': '0202042',
        '지부티': '0202043',
        '지브롤터': '0202044',
        '짐바브웨': '0202045',
        '차드': '0202046',
        '카메룬': '0202047',
        '카보베르데': '0202048',
        '케냐': '0202049',
        '코모로': '0202050',
        '코모로스': '0202051',
        '코트디브와르': '0202052',
        '콩고': '0202053',
        '콩고민주공화국': '0202054',
        '탄자니아': '0202055',
        '터크스앤카이코스제도': '0202056',
        '토고': '0202057',
        '튀니지': '0202058',
        '괌': '0203000',
        '나우루': '0203001',
        '노퍽아일랜드': '0203002',
        '뉴질랜드': '0203003',
        '뉴칼레도니아': '0203004',
        '마리아나군도': '0203005',
        '마셜군도': '0203006',
        '마이크로네시아': '0203007',
        '미크로네시아': '0203008',
        '바누아투': '0203009',
        '서사모아': '0203010',
        '세인트빈센트': '0203011',
        '솔로몬군도': '0203012',
        '아메리칸사모아': '0203013',
        '코코스섬': '0203014',
        '쿡아일랜드': '0203015',
        '크리스마스섬': '0203016',
        '키리바시': '0203017',
        '통가': '0203018',
        '투발루': '0203019',
        '파푸아뉴기니': '0203020',
        '팔라우': '0203021',
        '폴리네시아(프랑스령)': '0203022',
        '피지': '0203023',
        '호주': '0203024',
        '후투나': '0203025',
        '미국': '0204000',
        '바베이도스': '0204001',
        '세인트 빈센트 그레나딘': '0204002',
        '아이티': '0204003',
        '앤티가 바부다': '0204004',
        '유에스버진아일랜드': '0204005',
        '캐나다': '0204006',
        '과델루페': '0205000',
        '과테말라': '0205001',
        '그레나다': '0205002',
        '네비스': '0205003',
        '니카라과': '0205004',
        '도미니카': '0205005',
        '도미니카공화국': '0205006',
        '멕시코': '0205007',
        '몬체라트': '0205008',
        '바바도스': '0205009',
        '바하마': '0205010',
        '버뮤다': '0205011',
        '베네수엘라': '0205012',
        '벨리제': '0205013',
        '볼리비아': '0205014',
        '브라질': '0205015',
        '브리티시 버진아일랜드': '0205016',
        '세인트루시아': '0205017',
        '수리남': '0205018',
        '아루바': '0205019',
        '아르헨티나': '0205020',
        '아센션 이스난드': '0205021',
        '안티구아': '0205022',
        '앙길라': '0205023',
        '에콰도르': '0205024',
        '엘살바도르': '0205025',
        '온두라스': '0205026',
        '우루과이': '0205027',
        '자메이카': '0205028',
        '칠레': '0205029',
        '코스타리카': '0205030',
        '콜롬비아': '0205031',
        '쿠바': '0205032',
        '트리니다드토바고': '0205033',
        '파나마': '0205034',
        '파라과이': '0205035',
        '페루': '0205036',
        '포크랜드': '0205037',
        '푸에르토리코': '0205038',
        '프랑스령 기아나': '0205039',
        '하이티': '0205040'}
category_data = pd.read_csv(resource_path('category_data.csv'), encoding='cp949')
# category_data.iloc[0]['data']


header = ['상품번호', '상품상태', '제조사', '브랜드', '모델명', '원산지', '이벤트', '제조일자']
category_header = ['가구/인테리어', '도서', '식품', '디지털/가전', '생활/건강', '스포츠/레저', '화장품/미용', '출산/육아', '여가/생활편의', '패션잡화', '패션의류']
header2 = ['A/S 안내', '판매자 특이사항', '인증정보']  # 위쪽 상단 에서 영수증발급이 포함된 표에서 헤더를 모은것
header3 = ['제품하자가 아닌 소비자의 단순변심, 착오구매에 따른 청약철회 시 소비자가 부담하는 반품비용 등에 관한 정보']
jpg_pathes = []


def make_logger(name=None):
    # 1 logger instance를 만든다.
    logger = logging.getLogger(name)

    # 2 logger의 level을 가장 낮은 수준인 DEBUG로 설정해둔다.
    logger.setLevel(logging.DEBUG)

    # 3 formatter 지정
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # 4 handler instance 생성
    console = logging.StreamHandler()
    file_handler = logging.FileHandler(filename="test.log")

    # 5 handler 별로 다른 level 설정
    console.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)

    # 6 handler 출력 format 지정
    console.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # 7 logger에 handler 추가
    logger.addHandler(console)
    logger.addHandler(file_handler)

    return logger



def search_category(search_word):
    result = str()
    for word in category_data['data']:
        if search_word in str(word):
            result += word + '\n'
    return result


def return_int(text):
    text = text.replace('(', '').replace(')', '').replace('원', '').replace(',', '')
    try:
        price = int(text)
        print(text + "를 가격으로 변환")
    except:
        print(text + "를 가격으로 변환실패")
        price = 0
    return price


def get_nameNprice(text):
    if ' (+' in text:
        try:
            price = return_int(text.split(' (+')[-1])
            if len(text.split(' (+')[-1]) == 2:
                name = text.split(' (+')[0]
            else:
                word = str()
                for part in text.split(' (+')[:-1]:
                    word += part
                name = word
        except:
            price = 0
            name = text
    elif ' (-' in text:
        try:
            price = -int(text.split(' (-')[-1])
            if len(return_int(text.split(' (-')[-1])) == 2:
                name = text.split(' (-')[0]
            else:
                word = str()
                for part in text.split(' (-'[:-1]):
                    word += part
                name = word
        except:
            price = 0
            name = text
    else:
        price = 0
        name = text

    return name, price


def goto_url(url):
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get(url)


def get_major_info(text):
    print(text)
    product_num = None
    product_status = None
    brand = None
    model_name = None
    origin = None
    manufacturer = None
    lines = text.split('\n')
    for a_line in lines:
        words = a_line.split(' ')
        if "상품번호" in a_line:
            product_num = words[1]
        if "상품상태" in a_line:
            for i in range(len(words)):
                if words[i] == "상품상태":
                    product_status = words[i + 1]
        if "브랜드" in a_line:
            for i in range(len(words)):
                if words[i] == "브랜드":
                    brand = words[i + 1]
                    if i + 1 != len(words):
                        for suffix in words[i + 2:]:
                            if suffix in header:
                                break
                            else:
                                brand += suffix
        if "모델명" in a_line:
            for i in range(len(words)):
                if words[i] == "모델명":
                    model_name = words[i + 1]
                    if i + 1 != len(words):
                        for suffix in words[i + 2:]:
                            if suffix in header:
                                break
                            else:
                                model_name += suffix
        if "원산지" in a_line:
            for i in range(len(words)):
                if words[i] == "원산지":
                    origin = words[i + 1]
                    if i + 1 != len(words):
                        for suffix in words[i + 2:]:
                            if suffix in header:
                                break
                            else:
                                origin += suffix
        if "제조사" in a_line:
            print("제조사 출력 시작" + a_line)
            for i in range(len(words)):
                if words[i] == "제조사":
                    manufacturer = words[i + 1]
                    if i + 1 != len(words):
                        for suffix in words[i + 2:]:
                            if suffix in header:
                                break
                            else:
                                manufacturer += suffix
    print(str([product_num, product_status, brand, model_name, origin, manufacturer]))
    return product_num, product_status, brand, model_name, origin, manufacturer


def get_origin_id(origin):
    text = origin.split('(')[0]
    try:
        return data[text]
    except:
        print(f"{text}해당 원산지가 없음 변환시도")
    if text[-1] == '산':
        try:
            text = text[:-1]
            return data[text]
        except:
            print(f"{text}해당 원산지가 없음")


def get_categoryid_byname(title):
    req = requests.get(f'https://search.shopping.naver.com/search/all?query={title}')
    html = BeautifulSoup(req.text, "html.parser")
    category_link = html.select('div.basicList_depth__2QIie > a')
    for i in range(1, len(category_link)):
        print(category_link[i].text)
        if category_link[i].text in category_header:
            print(category_link[i - 1]['href'])
            return int(category_link[i - 1]['href'].split('=')[-1])
    print("검색결과가 1개만 존재하는 케이스")
    return int(category_link[i]['href'].split('=')[-1])


def get_ascallnumNspecialnote(text):
    lines = text.split('\n')
    as_call_num = ""
    as_info = ""
    specialnote = ""
    certifiedinfo = ""
    i = -1
    while i < len(lines) - 1:
        i += 1
        if 'A/S 안내' == lines[i]:
            as_call_num = lines[i + 1]
            as_info = lines[i + 2]
            for j in range(i + 3, len(lines)):
                if lines[j] in header2:
                    i = j
                    break
                else:
                    as_info += lines[j]
            continue
        if '판매자 특이사항' == lines[i]:
            specialnote = lines[i + 1]
            for j in range(i + 2, len(lines)):
                if lines[j] in header2:
                    i = j
                    break
                else:
                    specialnote += lines[j]
        if '인증정보' == lines[i]:
            certifiedinfo = lines[i + 1]
            for j in range(i + 2, len(lines)):
                if lines[j] in header2:
                    i = j
                    break
                else:
                    certifiedinfo += lines[j]
    return as_call_num, as_info, specialnote, certifiedinfo


def get_terminfo(text):
    lines = text.split('\n')
    return_fee = 0
    for a_line in lines:
        if '제품하자가 아닌 소비자의 단순변심, 착오구매에 따른 청약철회 시 소비자가 부담하는 반품비용 등에 관한 정보' in a_line:
            text = a_line.replace('제품하자가 아닌 소비자의 단순변심, 착오구매에 따른 청약철회 시 소비자가 부담하는 반품비용 등에 관한 정보 편도 ', '')
            text2 = text.replace('원 (최초 배송비 무료인 경우', '').split(' ')[0]
            return_fee = return_int(text2)
    return return_fee


def convert_to_frame(product, prefix):
    path = f'./{product.product_name}'
    os.makedirs(path)
    line = []
    line.append(product.product_status)  # 상품상태
    line.append(product.category_id)  # 카테고리 id
    line.append(product.product_name)  # 상품명
    line.append(product.original_price)  # 판매가 = 할인전 가격
    line.append(999)  # 재고수량
    line.append(product.as_info)  # A/S 안내내용
    line.append(product.as_call_number)  # A/S 전화번호
    main_img_path = f"{path}/{prefix}_mainimg.jpg"
    main_img_name = f"{prefix}_mainimg.jpg"
    urllib.request.urlretrieve(product.main_img_src, main_img_path)
    jpg_pathes.append(main_img_path)
    line.append(main_img_name)  # 대표 이미지 파일명
    if len(product.sub_img_src) != 0:
        text = str()
        if len(product.sub_img_src) > 9:
            product.sub_img_src = product.sub_img_src[0:8]
        for i in range(len(product.sub_img_src)):
            url = product.sub_img_src[i].split("?")[0]
            sub_img_path = f"{path}/{prefix}_sub_img{i}.jpg"
            sub_img_name = f"{prefix}_sub_img{i}.jpg"
            urllib.request.urlretrieve(url, sub_img_path)
            jpg_pathes.append(sub_img_path)
            if i == 0:
                text += sub_img_name
            else:
                text += f", {sub_img_name}"
        line.append(text)
    else:
        line.append("")  # 추가 이미지 파일명
    line.append(product.detail_html)  # 상품 상세정보
    line.append("")  # 판매자 상품코드
    line.append("")  # 판매자 바코드
    line.append("")  # 제조사
    line.append("")  # 브랜드
    line.append("")  # 제조일자
    line.append("")  # 유효일자
    line.append("과세상품")  # 부가세
    line.append("Y")  # 미성년자구매
    line.append("Y")  # 구매평 노출 여부
    line.append(str(product.origin_id))  # 원산지 코드
    if product.origin_id == "02":
        if product.importer == "":
            product.importer = "수입사"
    line.append(product.importer)  # 수입사
    line.append("N")  # 복수 원산지 여부
    line.append("")  # 원산지 직접입력
    line.append("택배‚ 소포‚ 등기")  # 배송방법
    if product.delivery_fee == 0:
        line.append("무료")
        line.append("")
    else:
        line.append("유료")  # 배송비 유형
        line.append(product.delivery_fee)  # 기본배송비
    line.append("착불 또는 선결제")  # 착불또는 선결제
    line.append("")  # 조건부 무료-상품판매가 합계
    line.append("")  # 수량별부과-수량
    line.append(product.return_fee)  # 반품배송비
    line.append(product.return_fee * 2)  # 교환배송비
    line.append("")  # 지역별 차등 배송비
    line.append("")  # 별도설치
    line.append("")  # 판매자 특이사항
    line.append(product.original_price - product.saled_price)  # 즉시할인 값
    line.append("원")  # 즉시할인 단위
    line.append("")  # 복수구매할인 조건 값
    line.append("")  # 복수 구매 할인 조건 단위
    line.append("")  # 복수구매 할인 값
    line.append("")  # 복수구매 할인 단위
    line.append("")  # 상품구매시 포인트 지급 값
    line.append("")  # 상품구매시 포인트 지급 단위
    line.append("")  # 텍스트리뷰작성시 지급 포이트
    line.append("")  # 포토/동영상 리뷰 작성시 지급 포인트
    line.append("")  # 한달사용 텍스트리뷰작성시 지급 포이트
    line.append("")  # 한달사용 포토/동영상 리뷰 작성시 지급 포인트
    line.append("")  # 톡톡친구/스토어찜 고객리뷰 작성시 지급 포인트
    line.append("")  # 무이자 할부 개월
    line.append("")  # 사은품
    # 옵션형태, 제목,
    if product.option_layer == 0:
        line.append("")  # 옵션 형태
        line.append("")  # 옵션 제목
        line.append("")  # 옵션 명
        line.append("")  # 옵션별 가격
        line.append("")  # 옵션별 재고
    else:
        line.append("조합형")  # 옵션 형태
        # for i in range(product.option_layer):
        #     if i == 0:
        #         optiontitle = product.option_title_list[i]
        #     else:
        #         optiontitle += f'\n{product.option_title_list[i]}'
        optiontitle = "옵션선택"
        line.append(optiontitle)
        option_name = str()
        for i in range(len(product.option_name_list)):
            if "(품절)" in product.option_name_list[i]:
                product.option_name_list[i] = product.option_name_list[i].replace("(품절)",'')
            if len(product.option_name_list[i]) > 24 :
                product.option_name_list[i] = product.option_name_list[i][-24:]
            option_name += product.option_name_list[i]
            if i != len(product.option_name_list)-1 :
                option_name += ','
        line.append(option_name)
        option_price = str()
        option_stock = str()
        for i in range(len(product.option_price_list)):
            option_price += str(product.option_price_list[i])
            option_stock += '9999'
            if i != len(product.option_price_list)-1:
                option_price += ','
                option_stock += ','
        line.append(option_price)
        line.append(option_stock)
    if len(product.addopt_name_list) == 0:
        line.append("")  # 추가상품명
        line.append("")  # 추가상품값
        line.append("")  # 추가상품가
        line.append("")  # 추가상품재고수량
    else:
        addopt_title = str()
        for i in range(product.option_layer, len(product.option_title_list)):
            addopt_title += product.option_title_list[i]
            if i != len(product.option_title_list)-1:
                addopt_title += '\n'
        line.append(addopt_title)
        addopt_name = str()
        addopt_price = str()
        addopt_stock = str()
        for i in range(len(product.addopt_name_list)):
            for j in range(len(product.addopt_name_list[i])):
                addopt_name += product.addopt_name_list[i][j]
                addopt_price += str(product.addopt_price_list[i][j])
                addopt_stock += '9999'
                if j != len(product.addopt_name_list[i])-1:
                    addopt_name += ','
                    addopt_price += ','
                    addopt_stock += ','
            if i != len(product.addopt_name_list) -1:
                addopt_name += '\n'
                addopt_price += '\n'
                addopt_stock += '\n'
        line.append(addopt_name)
        line.append(addopt_price)
        line.append(addopt_stock)
    try:
        if len(product.full_product_name) > 49:
            product.full_product_name = product.full_product_name[0:49]
    except:
        None
    line.append(product.full_product_name)  # 상품정보제공고시품명
    try:
        if len(product.model_name) > 49:
            product.model_name = product.model_name[0:49]
    except:
        None
    line.append(product.model_name)  # 상품정보제공고시모델명
    line.append("")  # 상품정보제공고시 인증허가사항
    line.append("")  # 상품정보제공고시 제조자
    line.append("N")  # 스토어찜회원 전용여부
    line.append("")  # 문화비 소득공제
    line.append("")  # isbn
    line.append("")  # 독립출판
    return line


class Product:
    def __init__(self):
        self.url = ""
        self.main_img_name = None
        self.main_img_src = None
        self.category_id = None
        self.product_name = None
        self.original_price = None
        self.saled_price = None
        self.sub_img_src = []
        self.detail_html = str()
        self.origin = ""
        self.origin_id = "00"
        self.delivery_fee = 0
        self.return_fee = "미구현"
        self.option_name_list = []
        self.option_price_list = []
        self.option_layer = 0
        self.addopt_name_list = []
        self.addopt_price_list = []
        self.tag_list = []
        self.full_product_name = ""
        self.model_name = ""
        self.brand = ""
        self.importer = ""
        self.manufacturer = ""
        self.product_status = "신상품"
        self.as_call_number = "획득실패"
        self.as_info = "세부사항 참조"
        self.product_num = 0  # 바코드를 의미함
        self.specialnote = ""
        self.certifiedinfo = ""
        self.option_title_list = []
