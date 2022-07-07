def add_card():
    global card_list
    add_card = {'index': len(card_list), 'name': input("请输入姓名"), 'mobile': input("请输入手机号")}
    card_list.append(add_card)


def remove_card():
    remove_card_index = int(input("请输入要删除名片的序号"))
    global card_list
    card_list.pop(remove_card_index)


def find_card():
    find_method = input("请选择你要查找名片的方法，\n1.按照姓名查找\n2.按照号码查找\n输入0返回主菜单")

    def find_name():
        global card_list
        name = input("请输入你要查找的姓名")
        for i in card_list:
            if i['name'] == name:
                print("查找到了" + i)
        else:
            print("找不到任何项目")

    def find_num():
        pass

    if find_method == "1":
        find_name()
    elif find_method == "2":
        find_num()
    elif find_method == "0":
        return None
    else:
        pass


def edit_card():
    global card_list
    replace_card = {}
    replace_card_index = int(input("请输入你要更改的名片的序号"))
    replace_card['index'] = replace_card_index
    replace_card['name'] = input("请输入姓名")
    replace_card['mobile'] = input("请输入手机号")
    card_list[replace_card_index] = replace_card


def list_card():
    print(card_list)


def man_card():
    while True:
        print("        名片管理系统 \n 1.添加名片 \n 2.修改名片 \n 3.删除名片 \n 4.查找名片 \n 5.显示所有名片 \n 6.退出系统")
        num = int(input("请输入要执行的操作"))
        if num == 1:
            add_card()
        elif num == 2:
            edit_card()
        elif num == 3:
            remove_card()
        elif num == 4:
            find_card()
        elif num == 5:
            list_card()
        elif num == 6:
            card_exit = input("您真的要退出吗？确认请输入0")
            if card_exit == "0":
                break


card_list = []
man_card()
