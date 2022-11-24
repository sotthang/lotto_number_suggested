import requests
import random
import numpy as np
from tqdm import tqdm

minDrwNo = 1  # 시작 회차
maxDrwNo = 1042  # 종료 회차
drwtNo1 = []  # 1등 첫번째 번호 리스트
drwtNo2 = []  # 1등 두번째 번호 리스트
drwtNo3 = []  # 1등 세번째 번호 리스트
drwtNo4 = []  # 1등 네번째 번호 리스트
drwtNo5 = []  # 1등 다섯번째 번호 리스트
drwtNo6 = []  # 1등 여섯번째 번호 리스트
bnusNo = []  # 1등 보너스 번호 리스트
drwNoDate = []  # 로또 추첨일 리스트

# 시작 회차부터 종료 회차까지 당첨 번호 리스트
def get_lotto_number_history(startdrwno, lastdrwno):
    global unique, counts
    for i in tqdm(range(startdrwno, lastdrwno + 1, 1)):
        # 1등 번호를 취득
        req_lotto = requests.get("https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=" + str(i))
        lottoNo = req_lotto.json()
        drwNoDate.append(lottoNo['drwNoDate'])  # 로또 추첨일
        drwtNo1.append(lottoNo['drwtNo1'])  # 1등 첫번째 번호 저장
        drwtNo2.append(lottoNo['drwtNo2'])  # 1등 두번째 번호 저장
        drwtNo3.append(lottoNo['drwtNo3'])  # 1등 세번째 번호 저장
        drwtNo4.append(lottoNo['drwtNo4'])  # 1등 네번째 번호 저장
        drwtNo5.append(lottoNo['drwtNo5'])  # 1등 다섯번째 번호 저장
        drwtNo6.append(lottoNo['drwtNo6'])  # 1등 여섯번째 번호 저장
        bnusNo.append(lottoNo['bnusNo'])  # 1등 보너스 번호 저장

        # 로또 1등 번호를 하나의 리스트로 합치기
        # 보너스 번호를 포함해 분석 하고 싶은 경우 drwtNo6뒤에 bnusNo를 추가
        h = np.hstack((drwtNo1, drwtNo2, drwtNo3, drwtNo4, drwtNo5, drwtNo6, bnusNo))
        unique, counts = np.unique(h, return_counts=True)
    return dict(zip(unique, counts))

def lotto_winnings(last_lotto_winning_num, guess_lotto_num):
    count = 0

    for x in last_lotto_winning_num[:6]:
        if x in guess_lotto_num[:6]:
            count += 1

    if count == 6:
        return "1등"
    elif count == 5 and last_lotto_winning_num[6] == guess_lotto_num[6]:
        return "2등"
    elif count == 5:
        return "3등"
    elif count == 4:
        return "4등"
    elif count == 3:
        return "5등"
    else:
        return "미당첨"


# 빈도수 낮은 순으로 15개, 15개, 15개로 나눈후 제일 빈도수 낮은 15개에는 60%, 그다음 15개는 30%, 마지막 15개는 10% 의 가중치를 주어 7개의 난수를 추출
def get_lotto_numbers():
    guess_lotto_numbers = []
    while len(guess_lotto_numbers) < 7:
        num = random.choices(
            [x for x in frequency_descending_order],
            weights=[
                6 / 150, 6 / 150, 6 / 150, 6 / 150, 6 / 150, 6 / 150, 6 / 150, 6 / 150,
                6 / 150, 6 / 150, 6 / 150, 6 / 150, 6 / 150, 6 / 150, 6 / 150,
                3 / 150, 3 / 150, 3 / 150, 3 / 150, 3 / 150, 3 / 150, 3 / 150, 3 / 150,
                3 / 150, 3 / 150, 3 / 150, 3 / 150, 3 / 150, 3 / 150, 3 / 150,
                1 / 150, 1 / 150, 1 / 150, 1 / 150, 1 / 150, 1 / 150, 1 / 150, 1 / 150,
                1 / 150, 1 / 150, 1 / 150, 1 / 150, 1 / 150, 1 / 150, 1 / 150
            ],
            k=1)
        if num not in guess_lotto_numbers:
            guess_lotto_numbers.append(num[0])
    return guess_lotto_numbers

lotto_count = get_lotto_number_history(minDrwNo, maxDrwNo)

# 빈도수 내림차순
frequency_descending_order = sorted(lotto_count, key=lambda x: lotto_count[x], reverse=False)

# 번호별 확률
for i in range(1, 46):
    print(str(i) + " 번 확률 : " + str(lotto_count[i] / maxDrwNo))

# 마지막 회차 당첨 번호
last_lotto_num = [drwtNo1[-1], drwtNo2[-1], drwtNo3[-1], drwtNo4[-1], drwtNo5[-1], drwtNo6[-1], bnusNo[-1]]

print(f"{maxDrwNo}회차 로또 당첨 번호 :", " ".join(map(str, sorted(last_lotto_num[:6]))), "+", last_lotto_num[6])
print(f"{maxDrwNo}회차 로또 추측 번호 :", " ".join(map(str, sorted(get_lotto_numbers()[:6]))), "+", get_lotto_numbers()[6])
print(lotto_winnings(last_lotto_num, get_lotto_numbers()))

test_dict = {
    "1등":0, "2등":0, "3등":0, "4등":0, "5등":0, "미당첨":0
}

# 테스트 코드
for x in range(10000):
    test_dict[lotto_winnings(last_lotto_num, get_lotto_numbers())] += 1

print(test_dict)