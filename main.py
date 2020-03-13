import json
from urllib.request import urlretrieve
import requests
from colorama import init, Fore, Back, Style
init()

print("MaskFinder - 공적 마스크 판매 정보 제공")
print("주의: 이 프로그램에서 제공하는 마스크 재고 정보는 실제와 차이가 있을 수 있습니다.")

try:
    addr = input("주소를 입력하세요: ")
    api_key = "YOUR_KAKAO_REST_API_KEY"
    res = requests.get("https://dapi.kakao.com/v2/local/search/address.json", headers={"Authorization":"KakaoAK "+api_key}, params={"query":addr})
    data = json.loads(res.text)
    
    x = data["documents"][0]["address"]["x"]
    y = data["documents"][0]["address"]["y"]
except IndexError:
    print("잘못된 주소입니다.")
    input("엔터 키로 종료합니다...")
    exit(1)
except KeyError:
    print("주소를 입력하지 않았거나 API 키가 잘못되었습니다.")
    input("엔터 키로 종료합니다...")
    exit(1)

m = input("몇m 주변을 검색할지 입력하세요(최대 5000m): ")

urlretrieve("https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByGeo/json?lat="+y+"&lng="+x+"&m"+m, "./data.json")

with open("./data.json", "r", encoding='utf-8') as f:
    data = json.load(f)


print("데이터를 성공적으로 불러왔습니다. " + addr + "(으)로부터 "+ m +"미터 이내에 있는 공적 마스크 판매장소는 총 " + str(data["count"]) + "개 입니다.")

print("|                  주소                  |     명칭     |  재고  |")
print("------------------------------------------------------------------")

for i in range(0, data["count"]):
    try:
        if data["stores"][i]["remain_stat"] == "plenty":
            pass
    except KeyError:
        continue
    if data["stores"][i]["remain_stat"] == "plenty":
        print(Fore.GREEN + Style.BRIGHT, end="")
    elif data["stores"][i]["remain_stat"] == "some":
        print(Fore.YELLOW + Style.BRIGHT, end="")
    elif data["stores"][i]["remain_stat"] == "few":
        print(Fore.RED + Style.BRIGHT, end="")
    elif data["stores"][i]["remain_stat"] == None:
        print(Fore.WHITE, end="")
    else:
        print(Fore.WHITE, end="")
    print("|  ", end="")
    print(data["stores"][i]["addr"], end="")
    print("  |  ", end="")
    print(data["stores"][i]["name"], end="")
    print("  |  ", end="")
    if data["stores"][i]["remain_stat"] == "plenty":
        print("100개 이상", end="")
    elif data["stores"][i]["remain_stat"] == "some":
        print("30~99개", end="")
    elif data["stores"][i]["remain_stat"] == "few":
        print("2~29개", end="")
    elif data["stores"][i]["remain_stat"] == None:
        print("알 수 없음", end="")
    else:
        print("0~1개", end="")
    print("  |"+Fore.RESET+Style.RESET_ALL)

input("엔터 키로 종료합니다...")
