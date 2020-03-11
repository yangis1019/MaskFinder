import json
from urllib.request import urlretrieve
from urllib.parse import quote, unquote

addr = quote(input("조회하고 싶은 지역을 입력하세요(시/군/구까지): "))

urlretrieve("https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByAddr/json?address="+addr, "./data.json")

with open("./data.json", "r", encoding='utf-8') as f:
    data = json.load(f)

print("데이터를 성공적으로 불러왔습니다. " + unquote(addr) + "에 있는 공적 마스크 판매장소는 총 " + str(data["count"]) + "개 입니다.")

n = int(input("번호를 입력하세요: "))
n -= 1

print("주소: " + data["stores"][n]["addr"])
print("명칭: " + data["stores"][n]["name"])
if data["stores"][n]["remain_stat"] == "plenty":
    print("남은 마스크 수: 100개 이상")
elif data["stores"][n]["remain_stat"] == "some":
    print("남은 마스크 수: 30개 이상 100개 미만")
elif data["stores"][n]["remain_stat"] == "few":
    print("남은 마스크 수: 2개 이상 30개 미만")
elif data["stores"][n]["remain_stat"] == None:
    print("남은 마스크의 수를 알 수 없습니다.")
else:
    print("해당 판매처의 마스크가 매진되었습니다.")

store_type = ["", "약국", "우체국", "농협"]

print("판매처 유형: " + store_type[int(data["stores"][n]["type"])])

if data["stores"][n]["stock_at"] == None:
    print("마지막으로 입고된 시간을 알 수 없습니다.")
else:
    print("마지막으로 입고된 시간: " + data["stores"][n]["stock_at"])

if data["stores"][n]["created_at"] == None:
    print("마지막으로 해당 데이터가 업데이트된 시간을 알 수 없습니다.")
else:
    print("마지막으로 해당 데이터가 업데이트된 시간: " + data["stores"][n]["created_at"])
