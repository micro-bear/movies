import lib

tableFields = {
    "title":"電影名稱",
    "director":"導演",
    "genre":"類型",
    "year":"上映年份",
    "rating":"評分"
}

def start():
    print("--- 電影管理系統 ---")
    
    options = [
        "1. 匯入電影資料檔",
        "2. 查詢電影",
        "3. 新增電影",
        "4. 修改電影",
        "5. 刪除電影",
        "6. 匯出電影",
        "7. 離開系統"
    ]
    for option in options:
        print(option)
    
    input_option = input("請選擇操作選項 (1-7):")

    if(input_option == '1') :
        lib.import_movies()
    elif(input_option == '2'):
        input_search = input("查詢全部電影嗎？(y/n):")
        if(input_search == 'y'):
            movies = lib.search_movies()
        else:
            input_search_key = input("請輸入電影名稱:")
            movies = lib.search_movies(input_search_key)
        if(movies == [] ):
            print("查無資料")
        else:
            printTable(movies)
    elif(input_option == '3'):
        insertFields = {
            "title": "電影名稱:",
            "director": "導演:",
            "genre": "類型:",
            "year": "上映年份:",
            "rating": "評分 (1.0 - 10.0):"
        }
        insertData = {}
        for name, field in insertFields.items():
            insertData[name] = input(field)
        connection, database = lib.connect_db()
        lib.add_movie(connection, database, insertData)
        database.close()
        print("電影已新增")
        
    elif(input_option == '4'):
        input_search = input("請輸入要修改的電影名稱:")
        movies = lib.search_movies(input_search)
        updateData = {}
        for title, value in tableFields.items():
            input_data = input("請輸入新的" + value + " (若不修改請直接按 Enter):")
            if(input_data):
                updateData[title] = input_data
        connection, database = lib.connect_db()
        lib.modify_movie(connection, database, updateData, movies[0]["title"])
        
        print("資料已修改")
        
    elif(input_option == '5'):
        input_delete = input("刪除全部電影嗎？(y/n):")
        input_search = ''
        if(input_delete == 'y'):
            movies = lib.search_movies()
            printTable(movies)
        else:
            input_search = input("請輸入要刪除的電影名稱:")
            movies = lib.search_movies(input_search)
        
        printTable(movies)
        input_confirm = input("是否要刪除(y/n):")
        if(input_confirm == 'y'):
            connection, database = lib.connect_db()
            lib.delete_movies(connection, database, input_search)
        print("電影已刪除")
    elif(input_option == '6'):
        input_export = input("匯出全部電影嗎？(y/n):")
        if(input_export == 'y'):
            movies = lib.search_movies()
        else:
            input_search = input("請輸入要匯出的電影名稱:")
            movies = lib.search_movies(input_search)

        lib.export_movies(movies)
        print("電影資料已匯出至 exported.json")
    elif(input_option == '7'):
        print("系統已退出。")
        exit()
        
def printTable(items):
    global tableFields
    print("       ".join(list(tableFields.values())))
    print("---------------------------------------")
    for item in items:
        print("     ".join(str(item) for item in list(item.values())))

def searchTable(tableData, name):
    return [row for row in tableData if row[1] == name]

def deleteTableData(tableData, name):
    return [row for row in tableData if row[1] != name]

while(True):
    start()