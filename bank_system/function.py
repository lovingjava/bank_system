import pymysql
import random
import time

db = pymysql.connect(host="localhost", port=3306, user='root', password='564445', db='bank_system', charset='utf8')
cursor = db.cursor()


class Function(object):
    # 开户(0)
    def create_user(self):
        print("\n-------------开户(0)-------------")
        name = input("请输入您的姓名：")
        idCard = int(input("请输入您的身份证号码："))
        phone = input("请输入您的电话号码：")
        cardnumber = self.create_card_number()
        password = self.set_password()
        if password == -1:
            print("创建失败！")
            print("即将返回主界面！")
            return -1
        mysql1 = "insert into user values(%s, %s, %s, %s)"
        cursor.execute(mysql1, (name, idCard, phone, cardnumber))
        db.commit()
        # 0表示卡没有被锁, 1表示卡被锁了
        mysql2 = "insert into card values(%s, %s, %s, %s, %s)"
        cursor.execute(mysql2, (cardnumber, password, 0, 0, 0))
        db.commit()
        print("尊敬的 %s 用户，您好！您的账户已创建成功！您的卡号是：%s" % (name, cardnumber))
        print("即将返回主界面！")

    # 随机生成6位卡号
    def create_card_number(self):
        while True:
            cardnumber = ""
            for i in range(6):
                cardnumber += str(random.randrange(0, 10))
            cursor.execute("select * from card where cardnumber = %s", cardnumber)
            card = cursor.fetchone()
            if card is None:
                return cardnumber

    # 设置密码
    def set_password(self):
        for i in range(4):
            password1 = input("请输入您的密码：")
            password2 = input("请再次输入您的密码：")
            if password1 == password2:
                return password1
            if i == 3:
                return -1
            print("对不起，您两次输入的密码不一致，请重新输入！")

    # 查询(1)
    def query(self):
        print("\n-------------查询(1)-------------")
        cardnumber = input("请输入您的卡号：")
        cursor.execute("select * from card where cardnumber = %s", cardnumber)
        card = cursor.fetchone()
        if card is None:
            print("对不起， 您输入的卡号有误！")
            print("即将返回主界面！")
        elif card[3] == '1':
            print("对不起，您的银行卡已被锁定！")
            print("即将返回主界面！")
        else:
            cursor.execute("select * from user where cardnumber = %s", cardnumber)
            data = cursor.fetchone()
            cnt = 0
            for i in range(3):
                password = input("请您输入密码：")
                if password == card[1]:
                    print("尊敬的 ", data[0], " 用户您好！")
                    print("您的余额为：", card[2])
                    de = input("是否打印明细表? 是(y/Y)， 否(f/F)：")
                    if de == 'y' or de == 'Y':
                        print(" -----------------------------------------------------------------------")
                        print("                        徐艺铭--招商银行 查询凭单                      ")
                        print("                                                                       ")
                        print("     余额：%s                                                          " % card[2])
                        print("     账户名：%s                                                        " % data[0])
                        print("     账号：%s                                                          " % card[0])
                        print("     日期：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                        print("     开户行：******支行                                                ")
                        print("     编号：", random.randint(10000000000, 99999999999), "              ")
                        print("                                                                       ")
                        print(" -----------------------------------------------------------------------")
                    elif de == 'f' or de == 'F':
                        print("", end="")
                    break
                else:
                    cnt += 1
                    if cnt == 3:
                        p = '1'
                        cursor.execute("update card set islock = %s where cardnumber = %s", (p, cardnumber))
                        db.commit()
                        print("您的银行卡已被锁定！")
                        print("即将返回主界面！")
                        return 0
                    else:
                        print("密码输入错误，请重新输入！")

    # 存款(2)
    def deposit(self):
        print("\n-------------存款(2)-------------")
        dec = input("定期存款按(d)，活期存款按(h)：")
        if dec == "h":
            cardnumber = input("请输入您的银行卡号：")
            cursor.execute("select * from card where cardnumber = %s", cardnumber)
            card = cursor.fetchone()
            if card is None:
                print("对不起，您输入的卡号有误！")
                print("即将返回主界面！")
                return -1
            cursor.execute("select * from user where cardnumber = %s", cardnumber)
            data = cursor.fetchone()
            if card[3] == '1':
                print("对不起，您的银行卡已被锁，无法存款!")
                print("即将返回主界面！")
                return -1
            cnt = 0
            save_money = ""
            for i in range(6):
                password = input("请输入您的密码：")
                if password == card[1]:
                    print("尊敬的 ", data[0], " 用户您好！")
                    for j in range(4):
                        save_money = input("请输入您要存入的金额：")
                        if not save_money.isdigit():
                            if j == 3:
                                return 0
                            print("您输入的不是数字，请输入数字：")
                            continue
                        elif save_money.isdigit():
                            break
                    if float(save_money) < 0:
                        print("对不起，您输入的金额有误")
                        continue
                    money = str(float(card[2]) + float(save_money))
                    cursor.execute("update card set money = %s where cardnumber = %s", (money, cardnumber))
                    db.commit()
                    print("恭喜您！存款成功，当前账户可用余额为：%s 元" % money)
                    de = input("是否打印明细表? 是(y/Y)， 否(f/F)：")
                    if de == 'y' or de == 'Y':
                        print(" -----------------------------------------------------------------------")
                        print("                      徐艺铭--招商银行 汇款取款凭单                    ")
                        print("                                                                       ")
                        print("     存款金额：%s         (活期存款)                                   " % save_money)
                        print("     存款人：%s                                                        " % data[0])
                        print("     可用余额：%s                                                      " % money)
                        print("     存款人账号：%s                                                    " % data[3])
                        print("     日期：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                        print("     开户行：******支行                                                ")
                        print("     编号：", random.randint(10000000000, 99999999999), "              ")
                        print("                                                                       ")
                        print(" -----------------------------------------------------------------------")
                    elif de == 'f' or de == 'F':
                        print("", end="")
                    print("即将返回主界面！")
                    break
                else:
                    cnt += 1
                    if cnt == 3:
                        p = '1'
                        cursor.execute("update card set islock = %s where cardnumber = %s", (p, cardnumber))
                        db.commit()
                        print("您的银行卡已被锁定！")
                        print("即将返回主界面！")
                        break
                    else:
                        print("密码输入错误，请重新输入！")
        elif dec == "d":
            cardnumber = input("请输入您的银行卡号：")
            cursor.execute("select * from card where cardnumber = %s", cardnumber)
            card = cursor.fetchone()
            if card is None:
                print("对不起，您输入的卡号有误！")
                print("即将返回主界面！")
                return -1
            cursor.execute("select * from user where cardnumber = %s", cardnumber)
            data = cursor.fetchone()
            if card[3] == '1':
                print("对不起，您的银行卡已被锁，无法存款!")
                print("即将返回主界面！")
                return -1
            cnt = 0
            date = ""
            save_money = ""
            moneyg = 0
            for i in range(6):
                password = input("请输入您的密码：")
                if password == card[1]:
                    print("尊敬的 ", data[0], " 用户您好！")
                    print("----------------年利率-----------------")
                    print("|    三个月定期：  1.35%     按(1)    |")
                    print("|    半年定期：    1.55%     按(2)    |")
                    print("|    一年定期：    1.75%     按(3)    |")
                    print("|    二年定期：    2.25%     按(4)    |")
                    print("|    三年定期：    2.75%     按(5)    |")
                    print("|    五年定期：    3.00%     按(6)    |")
                    print("|    五年以上定期：3.35%     按(7)    |")
                    print("---------------------------------------")
                    for m in range(6):
                        date = input("请输入存款时间：")
                        if date not in ['1', '2', '3', '4', '5', '6', '7']:
                            print("请输入正确的编号！")
                            continue
                        for j in range(4):
                            save_money = input("请输入您要存入的金额：")
                            if not save_money.isdigit():
                                if j == 3:
                                    return 0
                                print("您输入的不是数字，请输入数字：")
                                continue
                            elif save_money.isdigit():
                                break
                        if float(save_money) < 0:
                            print("对不起，您输入的金额有误！")
                            continue
                        else:
                            break
                    money = float(float(card[2]) + float(save_money))
                    if date == '1':
                        cursor.execute("update card set date = %s where cardnumber = %s", (date, cardnumber))
                        db.commit()
                        moneyg = money * 1.0135
                    elif date == '2':
                        cursor.execute("update card set date = %s where cardnumber = %s", (date, cardnumber))
                        db.commit()
                        moneyg = money * 1.0155
                    elif date == '3':
                        cursor.execute("update card set date = %s where cardnumber = %s", (date, cardnumber))
                        db.commit()
                        moneyg = money * 1.0175
                    elif date == '4':
                        cursor.execute("update card set date = %s where cardnumber = %s", (date, cardnumber))
                        db.commit()
                        moneyg = money * 2.0225
                    elif data == '5':
                        cursor.execute("update card set date = %s where cardnumber = %s", (date, cardnumber))
                        db.commit()
                        moneyg = money * 2.0275
                    elif date == '6':
                        cursor.execute("update card set date = %s where cardnumber = %s", (date, cardnumber))
                        db.commit()
                        moneyg = money * 1.0300
                    elif date == '7':
                        cursor.execute("update card set date = %s where cardnumber = %s", (date, cardnumber))
                        db.commit()
                        moneyg = money * 1.0335
                    moneyg = str(moneyg)
                    cursor.execute("update card set money = %s where cardnumber = %s", (moneyg, cardnumber))
                    db.commit()
                    print("恭喜您！存款成功，当前账户可用余额为：%s 元" % money)
                    de = input("是否打印明细表? 是(y/Y)， 否(f/F)：")
                    if de == 'y' or de == 'Y':
                        print(" -----------------------------------------------------------------------")
                        print("                      徐艺铭--招商银行 汇款取款凭单                    ")
                        print("                                                                       ")
                        print("     存款金额：%s         (定期存款)                                   " % save_money)
                        print("     存款人：%s                                                        " % data[0])
                        print("     可用余额：%s                                                      " % money)
                        print("     存款人账号：%s                                                    " % data[3])
                        print("     日期：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                        print("     开户行：******支行                                                ")
                        print("     编号：", random.randint(10000000000, 99999999999), "              ")
                        print("                                                                       ")
                        print(" -----------------------------------------------------------------------")
                    elif de == 'f' or de == 'F':
                        print("", end="")
                    print("即将返回主界面！")
                    break
                else:
                    cnt += 1
                    if cnt == 3:
                        p = '1'
                        cursor.execute("update card set islock = %s where cardnumber = %s", (p, cardnumber))
                        db.commit()
                        print("您的银行卡已被锁定！")
                        print("即将返回主界面！")
                        break
                    else:
                        print("密码输入错误，请重新输入！")

    # 取款(3)
    def withdrawal(self):
        print("\n-------------取款(3)-------------")
        dec = input("定期取款按(d)，活期取款按(h)：")
        if dec == "h":
            cardnumber = input("请输入您的银行卡号：")
            cursor.execute("select * from card where cardnumber = %s", cardnumber)
            card = cursor.fetchone()
            if card is None:
                print("对不起，您输入的卡号有误！")
                print("即将返回主界面！")
                return -1
            cursor.execute("select * from user where cardnumber = %s", cardnumber)
            data = cursor.fetchone()
            if card[3] == '1':
                print("对不起，您的银行卡已被锁，无法取款!")
                print("即将返回主界面！")
                return -1
            cnt = 0
            get_money = ""
            for i in range(6):
                password = input("请输入您的密码：")
                if password == card[1]:
                    print("尊敬的 ", data[0], " 用户您好！")
                    for j in range(4):
                        get_money = input("请输入您要取出的金额：")
                        if not get_money.isdigit():
                            if j == 3:
                                return 0
                            print("您输入的不是数字，请输入数字：")
                            continue
                        elif get_money.isdigit():
                            break
                    if float(get_money) < 0:
                        print("对不起，您输入的金额有误")
                        continue
                    if float(get_money) > float(card[2]):
                        print("对不起，您的余额不足！")
                        continue
                    if float(get_money) == 0:
                        print("您的资金未变动！")
                        print("即将返回主界面！")
                        return 0
                    # 活期存款的利息为 0.35%
                    money = str(float(card[2]) * 1.0035 - float(get_money))
                    cursor.execute("update card set money = %s where cardnumber = %s", (money, cardnumber))
                    db.commit()
                    print("恭喜您！取款成功，当前账户可用余额为：%s 元" % money)
                    de = input("是否打印明细表? 是(y/Y)， 否(f/F)：")
                    if de == 'y' or de == 'Y':
                        print(" -----------------------------------------------------------------------")
                        print("                      徐艺铭--招商银行 汇款取款凭单                    ")
                        print("                                                                       ")
                        print("     取款金额：%s         (活期取款)                                   " % get_money)
                        print("     取款人：%s                                                        " % data[0])
                        print("     可用余额：%s                                                      " % money)
                        print("     取款人账号：%s                                                    " % data[3])
                        print("     日期：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                        print("     开户行：******支行                                                ")
                        print("     编号：", random.randint(10000000000, 99999999999), "              ")
                        print("                                                                       ")
                        print(" -----------------------------------------------------------------------")
                    elif de == 'f' or de == 'F':
                        print("", end="")
                    print("即将返回主界面！")
                    break
                else:
                    cnt += 1
                    if cnt == 3:
                        p = '1'
                        cursor.execute("update card set islock = %s where cardnumber = %s", (p, cardnumber))
                        db.commit()
                        print("您的银行卡已被锁定！")
                        print("即将返回主界面！")
                        break
                    else:
                        print("密码输入错误，请重新输入！")
        elif dec == "d":
            cardnumber = input("请输入您的银行卡号：")
            cursor.execute("select * from card where cardnumber = %s", cardnumber)
            card = cursor.fetchone()
            if card is None:
                print("对不起，您输入的卡号有误！")
                print("即将返回主界面！")
                return -1
            cursor.execute("select * from user where cardnumber = %s", cardnumber)
            data = cursor.fetchone()
            if card[3] == '1':
                print("对不起，您的银行卡已被锁，无法取款!")
                print("即将返回主界面！")
                return -1
            cnt = 0
            date = ""
            get_money = ""
            moneyg = 0
            bo = input("是否是提前取款，是(y/Y)，否(f/F)：")
            if bo == 'y' or bo == 'Y':
                for i in range(6):
                    password = input("请输入您的密码：")
                    if password == card[1]:
                        print("尊敬的 ", data[0], " 用户您好！")
                        print("----------------年利率-----------------")
                        print("|    三个月定期：  1.35%     按(1)    |")
                        print("|    半年定期：    1.55%     按(2)    |")
                        print("|    一年定期：    1.75%     按(3)    |")
                        print("|    二年定期：    2.25%     按(4)    |")
                        print("|    三年定期：    2.75%     按(5)    |")
                        print("|    五年定期：    3.00%     按(6)    |")
                        print("|    五年以上定期：3.35%     按(7)    |")
                        print("--注意:提前取款将按活期的0.35%利息计算--")
                        print("----------------------------------------")
                        for m in range(5):
                            date = input("请输入存款时间：")
                            for p in range(3):
                                if date not in ['1', '2', '3', '4', '5', '6', '7']:
                                    print("请输入正确的编号！")
                                    continue
                                else:
                                    break
                            for j in range(4):
                                get_money = input("请输入您要取出的金额：")
                                if not get_money.isdigit():
                                    if j == 3:
                                        return 0
                                    print("您输入的不是数字，请输入数字：")
                                    continue
                                elif get_money.isdigit():
                                    break
                                else:
                                    break
                            if float(get_money) == 0:
                                print("您的资金未变动！")
                                print("即将返回主界面！")
                                return 0
                            if float(get_money) < 0:
                                print("对不起，您输入的金额有误！")
                                continue
                            elif float(get_money) > float(card[2]):
                                print("对不起，您的余额不足！")
                                continue
                            else:
                                break
                        if date == '1':
                            moneyg = float(card[2]) / 1.0135 * 1.0035
                        elif date == '2':
                            moneyg = float(card[2]) / 1.0155 * 1.0035
                        elif date == '3':
                            moneyg = float(card[2]) / 1.0175 * 1.0035
                        elif date == '4':
                            moneyg = float(card[2]) / 2.0225 * 1.0035
                        elif data == '5':
                            moneyg = float(card[2]) / 2.0275 * 1.0035
                        elif date == '6':
                            moneyg = float(card[2]) / 1.0300 * 1.0035
                        elif date == '7':
                            moneyg = float(card[2]) / 1.0335 * 1.0035
                        money = str(moneyg - float(get_money))
                        cursor.execute("update card set money = %s where cardnumber = %s", (money, cardnumber))
                        db.commit()
                        print("恭喜您！取款成功，当前账户可用余额为：%s 元" % money)
                        de = input("是否打印明细表? 是(y/Y)， 否(f/F)：")
                        if de == 'y' or de == 'Y':
                            print(" -----------------------------------------------------------------------")
                            print("                      徐艺铭--招商银行 汇款取款凭单                    ")
                            print("                                                                       ")
                            print("     取款金额：%s         (定期取款) 提前                              " % get_money)
                            print("     取款人：%s                                                        " % data[0])
                            print("     可用余额：%s                                                      " % money)
                            print("     取款人账号：%s                                                    " % data[3])
                            print("     日期：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                            print("     开户行：******支行                                                ")
                            print("     编号：", random.randint(10000000000, 99999999999), "              ")
                            print("                                                                       ")
                            print(" -----------------------------------------------------------------------")
                        elif de == 'f' or de == 'F':
                            print("", end="")
                        print("即将返回主界面！")
                        return 0
                    else:
                        cnt += 1
                        if cnt == 3:
                            p = '1'
                            cursor.execute("update card set islock = %s where cardnumber = %s", (p, cardnumber))
                            db.commit()
                            print("您的银行卡已被锁定！")
                            print("即将返回主界面！")
                            break
                        else:
                            print("密码输入错误，请重新输入！")
            elif bo == 'F' or bo == 'f':
                for i in range(6):
                    password = input("请输入您的密码：")
                    if password == card[1]:
                        print("尊敬的 ", data[0], " 用户您好！")
                        for j in range(4):
                            get_money = input("请输入您要取出的金额：")
                            if not get_money.isdigit():
                                if j == 3:
                                    return 0
                                print("您输入的不是数字，请输入数字：")
                                continue
                            elif get_money.isdigit():
                                break
                        if float(get_money) < 0:
                            print("对不起，您输入的金额有误")
                            continue
                        if float(get_money) > float(card[2]):
                            print("对不起，您的余额不足！")
                            continue
                        money = str(float(card[2]) - float(get_money))
                        cursor.execute("update card set money = %s where cardnumber = %s", (money, cardnumber))
                        db.commit()
                        print("恭喜您！取款成功，当前账户可用余额为：%s 元" % money)
                        de = input("是否打印明细表? 是(y/Y)， 否(f/F)：")
                        if de == 'y' or de == 'Y':
                            print(" -----------------------------------------------------------------------")
                            print("                      徐艺铭--招商银行 汇款取款凭单                    ")
                            print("                                                                       ")
                            print("     取款金额：%s         (定期取款)                                   " % get_money)
                            print("     取款人：%s                                                        " % data[0])
                            print("     可用余额：%s                                                      " % money)
                            print("     取款人账号：%s                                                    " % data[3])
                            print("     日期：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                            print("     开户行：******支行                                                ")
                            print("     编号：", random.randint(10000000000, 99999999999), "              ")
                            print("                                                                       ")
                            print(" -----------------------------------------------------------------------")
                        elif de == 'f' or de == 'F':
                            print("", end="")
                        print("即将返回主界面！")
                        break
                    else:
                        cnt += 1
                        if cnt == 3:
                            p = '1'
                            cursor.execute("update card set islock = %s where cardnumber = %s", (p, cardnumber))
                            db.commit()
                            print("您的银行卡已被锁定！")
                            print("即将返回主界面！")
                            break
                        else:
                            print("密码输入错误，请重新输入！")

    # 转账(4)
    def transfer(self):
        print("\n-------------转账(6)-------------")
        mycardnumber = input("请输入您的银行账号：")
        cursor.execute("select * from card where cardnumber = %s", mycardnumber)
        card1 = cursor.fetchone()
        if card1 is None:
            print("对不起，您输入的卡号有误！")
            print("即将返回主界面！")
            return -1
        if card1[3] == '1':
            print("您的银行卡已经被锁定，无法转账！")
            print("即将返回主界面！")
            return 0
        cursor.execute("select * from user where cardnumber = %s", mycardnumber)
        data1 = cursor.fetchone()
        cnt = 0
        for i in range(6):
            password1 = input("请输入您的密码：")
            if password1 == card1[1]:
                print("尊敬的 ", data1[0], " 用户您好！")
                othercardnumber = input("请输入对方的银行账号：")
                cursor.execute("select * from card where cardnumber = %s", othercardnumber)
                card2 = cursor.fetchone()
                if card2 is None:
                    print("对不起，收款人的卡号有误，请重新输入！")
                    continue
                cursor.execute("select * from user where cardnumber = %s", othercardnumber)
                data2 = cursor.fetchone()
                idd = str(int(data2[1]))
                id4 = idd[-1:-5:-1]
                id4 = id4[::-1]
                print("------------------------------")
                print("   收款人的姓名：%s           " % data2[0])
                print("   收款人身份证后四位：%s     " % id4)
                print("------------------------------")
                boo = input("请确认收款人信息，确认(y/Y)，取消(f/F)：")
                money = ""
                if boo == 'y' or boo == 'Y':
                    for ii in range(6):
                        for j in range(4):
                            money = input("请输入转账金额：")
                            if not money.isdigit():
                                if j == 3:
                                    return 0
                                print("您输入的不是数字，请输入数字：")
                                continue
                            elif money.isdigit():
                                break
                        if float(money) < 0:
                            print("对不起，您输入的金额有误！")
                            continue
                        if float(money) > float(card1[2]):
                            print("对不起，您的余额不足！")
                            continue
                        booo = input("请确认是否转账，确认(y/Y)，取消(f/F)：")
                        if booo == 'y' or booo == 'Y':
                            transfer_money1 = str(float(card2[2]) + float(money))
                            cursor.execute("update card set money = %s where cardnumber = %s",
                                           (transfer_money1, othercardnumber))
                            db.commit()
                            transfer_money2 = str(float(card1[2]) - float(money))
                            cursor.execute("update card set money = %s where cardnumber = %s",
                                           (transfer_money2, mycardnumber))
                            db.commit()
                            print("恭喜您！转账成功，当前账户可用余额为：%s 元" % transfer_money2)
                            de = input("是否打印明细表? 是(y/Y)， 否(f/F)：")
                            if de == 'y' or de == 'Y':
                                print(" -----------------------------------------------------------------------")
                                print("                         徐艺铭--招商银行 转账凭单                       ")
                                print("                                                                       ")
                                print("     转账金额：%s                                                     " % money)
                                print("     转账人：%s                                                        " % data1[0])
                                print("     收款人：%s                                                        " % data2[0])
                                print(
                                    "     可用余额：%s                                                      " % transfer_money2)
                                print("     转账人账号：%s                                                    " % card1[0])
                                print("     收款人账号：%s                                                    " % card2[0])
                                print("     日期：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                                print("     开户行：******支行                                                ")
                                print("     编号：", random.randint(10000000000, 99999999999), "              ")
                                print("                                                                       ")
                                print(" -----------------------------------------------------------------------")
                            elif de == 'f' or de == 'F':
                                print("", end="")
                            print("即将返回主界面！")
                            return 0
                        elif booo == 'f' or booo == 'F':
                            print("取消成功！")
                            print("即将返回主界面！")
                            return 0
                elif boo == 'f' or boo == 'F':
                    print("取消成功！")
                    return 0
            else:
                cnt += 1
                if cnt == 3:
                    print("对不起，您的银行卡已被锁定！")
                    return -1
                else:
                    print("密码输入错误，请重新输入！")

    # 改密(5)
    def change_password(self):
        print("\n-------------改密(5)-------------")
        cardnumber = input("请输入您的银行卡号：")
        cursor.execute("select * from card where cardnumber = %s", cardnumber)
        card = cursor.fetchone()
        if card is None:
            print("对不起，您输入的卡号有误！")
            print("即将返回主界面！")
            return -1
        cursor.execute("select * from user where cardnumber = %s", cardnumber)
        data = cursor.fetchone()
        if card[3] == '1':
            print("对不起，您的银行卡已被锁，无法修改密码!")
            print("即将返回主界面！")
            return -1
        iidcard = str(input("请输入您的身份证："))
        if str(data[1]) != iidcard:
            print("对不起，您输入的身份证有误！")
            print("即将返回主界面！")
            return -1
        phone = input("请输入您的手机号码：")
        if data[2] != phone:
            print("对不起，您输入的手机号有误!")
            print("即将返回主界面！")
            return -1
        cnt = 0
        for i in range(6):
            password = input("请输入您的密码：")
            if password == card[1]:
                print("尊敬的 ", data[0], " 用户您好！")
                for j in range(3):
                    password1 = input("请输入您的新密码：")
                    password2 = input("请再次输入您的新密码：")
                    if password1 != password2:
                        print("对不起，您输入的密码不一致，请重新输入：")
                        continue
                    else:
                        cursor.execute("update card set password = %s where cardnumber = %s", (password1, cardnumber))
                        db.commit()
                        print("恭喜您！您的密码修改成功！")
                        print("即将返回主界面！")
                        return 0
            else:
                cnt += 1
                if cnt == 3:
                    p = '1'
                    cursor.execute("update card set islock = %s where cardnumber = %s", (p, cardnumber))
                    db.commit()
                    print("您的银行卡已被锁定！")
                    print("即将返回主界面！")
                    break
                else:
                    print("密码输入错误，请重新输入！")

    # 锁定(6)
    def lock(self):
        print("\n-------------锁定(6)-------------")
        cardnumber = input("请输入您的银行卡号：")
        cursor.execute("select * from card where cardnumber = %s", cardnumber)
        card = cursor.fetchone()
        if card is None:
            print("对不起，您输入的卡号有误！")
            print("即将返回主界面！")
            return -1
        cursor.execute("select * from user where cardnumber = %s", cardnumber)
        data = cursor.fetchone()
        if card[3] == '1':
            print("您的银行卡已经被锁定!")
            print("即将返回主界面！")
            return 0
        idcard = input("请输入您的身份证号：")
        if str(data[1]) != idcard:
            print("您的身份证有误!")
            print("即将返回主界面！")
            return -1
        cnt = 0
        for i in range(6):
            password = input("请输入您的密码：")
            if password == card[1]:
                print("尊敬的 ", data[0], " 用户您好！")
                p = '1'
                cursor.execute("update card set islock = %s where cardnumber = %s", (p, cardnumber))
                db.commit()
                print("恭喜您！银行卡锁定成功！")
                print("即将返回主界面！")
                return 0
            else:
                cnt += 1
                if cnt == 3:
                    print("对不起，银行卡锁定失败！")
                    print("即将返回主界面！")
                    break
                else:
                    print("密码输入错误，请重新输入！")

    # 解锁(7)
    def unlock(self):
        print("\n-------------解锁(7)-------------")
        cardnumber = input("请输入您的银行卡号：")
        cursor.execute("select * from card where cardnumber = %s", cardnumber)
        card = cursor.fetchone()
        if card is None:
            print("对不起，您输入的卡号有误！")
            print("即将返回主界面！")
            return -1
        cursor.execute("select * from user where cardnumber = %s", cardnumber)
        data = cursor.fetchone()
        if card[3] == '0':
            print("您的银行卡没有被锁定!")
            print("即将返回主界面！")
            return -1
        idcard = input("请输入您的身份证号：")
        if str(data[1]) != idcard:
            print("您的身份证有误!")
            print("即将返回主界面！")
            return -1
        cnt = 0
        for i in range(6):
            password = input("请输入您的密码：")
            if password == card[1]:
                print("尊敬的 ", data[0], " 用户您好！")
                p = '0'
                cursor.execute("update card set islock = %s where cardnumber = %s", (p, cardnumber))
                db.commit()
                print("恭喜您！银行卡解锁成功！")
                print("即将返回主界面！")
                return 0
            else:
                cnt += 1
                if cnt == 3:
                    print("对不起，银行卡解锁失败！")
                    print("即将返回主界面！")
                    break
                else:
                    print("密码输入错误，请重新输入！")

    # 补卡(8)
    def reapply(self):
        print("\n-------------补卡(8)-------------")
        idcard1 = input("请输入您的身份证号码：")
        if not idcard1.isdigit():
            print("您输入的为非数字！")
            print("即将返回主界面！")
            return -1
        cursor.execute("select * from user where idcard = %s", idcard1)
        user = cursor.fetchone()
        if user is None:
            print("您输入的身份证有误！")
            print("即将返回主界面！")
            return -1
        cardnumber1 = user[3]
        cursor.execute("select * from card where cardnumber = %s", cardnumber1)
        card = cursor.fetchone()
        phone_peo = input("请输入您的手机号码：")
        if phone_peo != user[2]:
            print("您输入的手机号码有误！")
            print("即将返回主界面！")
            return -1
        money = card[2]
        print("您之前的卡还剩余额：%s 元" % money)
        boo = input("是否执行补卡，确认(y/Y)，取消(f/F)：")
        password = ""
        if boo == 'y' or boo == 'Y':
            name = input("请输入您的姓名：")
            idCard = int(input("请输入您的身份证号码："))
            phone = input("请输入您的电话号码：")
            cardnumber = self.create_card_number()
            for j in range(4):
                if j == 3:
                    print("正在返回主界面！")
                    return -1
                password = input("请输入您的密码：")
                password1 = input("您再次输入您的密码：")
                if password != password1:
                    print("两次密码不一致，请重新输入！")
                    continue
                else:
                    break
            # 把原先的账户注销掉
            cursor.execute("delete from card where cardnumber = %s", cardnumber1)
            db.commit()
            cursor.execute("delete from user where cardnumber = %s", cardnumber1)
            db.commit()
            # 插入新的账户
            mysql1 = "insert into user values(%s, %s, %s, %s)"
            cursor.execute(mysql1, (name, idCard, phone, cardnumber))
            db.commit()
            # 0表示卡没有被锁, 1表示卡被锁了
            mysql2 = "insert into card values(%s, %s, %s, %s, %s)"
            cursor.execute(mysql2, (cardnumber, password, money, 0, 0))
            db.commit()
            print("尊敬的 %s 用户，您好！您已补卡成功！您的新卡号是：%s ，您当前的余额为：%s" % (name, cardnumber, card[2]))
            print("您的旧卡已被注销！")
            print("即将返回主界面！")
            return 0
        elif boo == 'f' or boo == 'F':
            print("补卡失败，即将返回主界面！")
            return 0

    # 销户(9)
    def destory(self):
        print("\n-------------销户(9)-------------")
        cardnumber = input("请输入您的银行卡号：")
        cursor.execute("select * from card where cardnumber = %s", cardnumber)
        card = cursor.fetchone()
        if card is None:
            print("对不起，您输入的卡号有误！")
            print("即将返回主界面！")
            return -1
        cursor.execute("select * from user where cardnumber = %s", cardnumber)
        data = cursor.fetchone()
        if card[3] == '1':
            print("您的银行卡已被锁定!")
            print("即将返回主界面！")
            return -1
        idcard = input("请输入您的身份证号：")
        if str(data[1]) != idcard:
            print("您的身份证有误!")
            print("即将返回主界面！")
            return -1
        cnt = 0
        for i in range(6):
            password = input("请输入您的密码：")
            if password == card[1]:
                print("尊敬的 ", data[0], " 用户您好！")
                print("您的账户里还有余额：%s" % card[2])
                aoo = input("是否取出余额，是(y/Y)，否(f/F)：")
                if aoo == 'y' or aoo == 'Y':
                    coo = input("请输入您的密码：")
                    if coo == card[1]:
                        print("您的余额已取出！")
                        boo = input("是否执行销户，确认(y/Y)，取消(f/F)：")
                        if boo == 'y' or boo == 'Y':
                            cursor.execute("delete from card where cardnumber = %s", cardnumber)
                            db.commit()
                            cursor.execute("delete from user where cardnumber = %s", cardnumber)
                            db.commit()
                            print("该账户已注销，即将返回主界面！")
                            return 0
                        elif boo == 'f' or boo == 'F':
                            print("注销失败，即将返回主界面！")
                            return 0
                    elif coo != card[1]:
                        print("您输入的密码有误！")
                        continue
                elif aoo == 'f' or aoo == 'F':
                    print("注销失败！")
                    return 0
            else:
                cnt += 1
                if cnt == 3:
                    print("对不起，银行卡销户失败！")
                    print("即将返回主界面！")
                    break
                else:
                    print("密码输入错误，请重新输入！")
