print("=================================Task1=====================================")


def find_and_print(messages, current_station):
    # 給定station編號
    stations = {
        "Songshan": 0,
        "Nanjing Sanmin": 1,
        "Taipei Arena": 2,
        "Nanjing Fuxing": 3,
        "Songjiang Nanjing ": 4,
        "Zhongshan": 5,
        "Beimen": 6,
        "Ximen": 7,
        "Xiaonanmen": 8,
        "Chiang Kai-Shek Memorial Hall": 9,
        "Guting": 10,
        "Taipower Building": 11,
        "Gongguan": 12,
        "Wanlong": 13,
        "Jingmei": 14,
        "Dapinglin": 15,
        "Qizhang": 16,
        "Xiaobitan": 17,
        "Xindian City Hall": 17,
        "Xindian": 18,
    }
    curr_location_number = stations.get(current_station)
    # handle edge case 改變相對位置
    if current_station != "Xiaobitan" and curr_location_number >= 17:
        stations["Xiaobitan"] = 15
    elif current_station == "Xiaobitan":
        stations["Xindian City Hall"] = 19
        stations["Xindian"] = 20

    personWithStaNumber = []  # [(name,車站編號)]
    res = [0, float("inf")]  # [name, 差距站數]

    # 尋找msg當中對應的站名，把匹配結果放入personWithStaNumber
    for name, msg in messages.items():
        for station in stations:
            if station in msg:
                personWithStaNumber.append((name, stations.get(station)))

    # 比較每個人的距離，找差距最小的結果放入res當中
    for i in personWithStaNumber:
        num = abs(i[1] - curr_location_number)
        if res[1] > num:
            res[0] = i[0]
            res[1] = num
    print(res[0])
    return res[0]


messages = {
    "Leslie": "I'm at home near Xiaobitan station.",
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Vivian": "I'm at Xindian station waiting for you."
}
find_and_print(messages, "Wanlong")  # print Mary
find_and_print(messages, "Songshan")  # print Copper
find_and_print(messages, "Qizhang")  # print Leslie
find_and_print(messages, "Ximen")  # print Bob
find_and_print(messages, "Xindian City Hall")  # print Vivian

print("=================================Task2=====================================")


class Book_schedule():
    consultants_schedule = {}

    def __init__(self, name):
        self.schedule = []  # tuple(start_time, end_time)
        self.name = name

    def booking(self, start, duration):
        end = start + duration

        for start_time, end_time in self.schedule:
            if start <= start_time and end >= end_time:
                # 欲預約時間完全涵蓋已預約時間
                return None
            elif start >= start_time and end <= end_time:
                # 初始即終止預約時間在已預約時間之內
                return None
            elif start_time < end <= end_time or start_time <= start < end_time:
                # 欲預約之起始時間或終止時間涵蓋已預約時間
                return None
        self.schedule.append((start, end))
        return self.name


def book(consultants, hour, duration, criteria):
    if criteria == "price":
        consultants = sorted(consultants, key=lambda x: x["price"])
    else:
        consultants = sorted(
            consultants, key=lambda x: x["rate"], reverse=True)

    for consultant in consultants:
        if consultant["name"] not in Book_schedule.consultants_schedule:
            Book_schedule.consultants_schedule[consultant["name"]
                                               ] = Book_schedule(consultant["name"])

        result = Book_schedule.consultants_schedule[consultant["name"]].booking(
            hour, duration)
        if result:
            print(result)
            return result
    print("No Service")
    return "No Service"


consultants = [
    {"name": "John", "rate": 4.5, "price": 1000},
    {"name": "Bob", "rate": 3, "price": 1200},
    {"name": "Jenny", "rate": 3.8, "price": 800}
]
book(consultants, 15, 1, "price")  # Jenny
book(consultants, 11, 2, "price")  # Jenny
book(consultants, 10, 2, "price")  # John
book(consultants, 20, 2, "rate")  # John
book(consultants, 11, 1, "rate")  # Bob
book(consultants, 11, 2, "rate")  # No Service
book(consultants, 14, 3, "price")  # John
# book(consultants, 13, 2, "price")
# Debug
# print(Book_schedule.consultants_schedule)
# for consultant, obj in Book_schedule.consultants_schedule.items():
#     print(f"Consultant: {consultant}, Schedule: {obj.schedule}")

print("=================================Task3=====================================")


def func(*data):
    word_count = {}
    # 尋找中間名
    for name in data:
        if len(name) == 5:
            # 名字長度等於5
            word = name[2]
        elif len(name) >= 3:
            # 名字長度大於等於3,小於5
            word = name[-2]
        elif len(name) == 2:
            # 名字長度只有2
            word = name[-1]
        # {word: (count, name)}, ex: {大: (1, 彭大明), 明:(2, 吳明)}
        word_count[word] = word_count.get(word, [0, name])[0] + 1, name

    # 確認中間名數量
    for value in word_count.values():
        if value[0] == 1:
            print(value[1])
            return
    # 都沒有的狀況
    print("沒有")
    # return "沒有"


func("彭大牆", "陳王明雅", "吳明")  # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花")  # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花")  # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆")  # print 夏曼藍波安
print("=================================Task4=====================================")


def get_number(index):
    # edge case
    if index == 0:
        print(0)
        return
    count = 0
    res = 0
    for _ in range(0, index):
        count += 1
        if count % 3 != 0:
            res += 4
        else:
            res -= 1
    print(res)


get_number(1)  # print 4
get_number(5)  # print 15
get_number(10)  # print 25
get_number(30)  # print 70
print("=================================Task5=====================================")


def find(spaces, stat, n):
    stack = []  # stack = [index]
    res = float("inf")

    for i in range(len(stat)):
        # 確認spaces availability
        if stat[i] == 0:
            continue
        # 如果spaces大於或等於人數
        if spaces[i] >= n:
            res = min(res, spaces[i])  # 找到最適數量
            if res == spaces[i]:  # 記錄符合條件的index
                stack.append(i)
    if not stack:
        print(-1)
        return
    print(stack[-1])


find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2)  # print 5
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4)  # print -1
find([4, 6, 5, 8], [0, 1, 1, 1], 4)  # print 2
