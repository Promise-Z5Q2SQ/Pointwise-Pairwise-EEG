import os

query_list_img = []
cnt = 0
for root, dirs, files in os.walk('./data/images/'):
    for name in dirs:
        query_list_img.append(name)
    for name in files:
        cnt += 1
print(cnt)  # 783-59 = 724

info = open('./data/query_info.txt')
query_list_info = []
for each_line in info:
    query = each_line.split(' ')[0].split('\t')[0]
    query_list_info.append(query)
query_list_info.sort()
query_list_img.sort()
print(query_list_info)
print(query_list_img)

info.close()
