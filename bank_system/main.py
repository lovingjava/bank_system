import time
from bank_system import function

Function = function.Function()

class Main(object):
    def run(self):
        while True:
            print("正在跳转至主界面，请稍后", end="")
            for i in range(5):
                print(".", end="", flush=True)
                time.sleep(0.4)
            print("")
            self.UI()
            number = input("请输入您要选择的功能编号：")
            if number not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'q']:
                print("请输入正确的编码！")
            if number == "0":
                Function.create_user()
            elif number == "1":
                Function.query()
            elif number == "2":
                Function.deposit()
            elif number == "3":
                Function.withdrawal()
            elif number == "4":
                Function.transfer()
            elif number == "5":
                Function.change_password()
            elif number == "6":
                Function.lock()
            elif number == "7":
                Function.unlock()
            elif number == "8":
                Function.reapply()
            elif number == "9":
                Function.destory()
            elif number == "q":
                print("正在退出系统，请稍后", end=" ")
                for i in range(6):
                    print(".", end=" ", flush=True)
                    time.sleep(0.5)
                break

    def UI(self):
        print("*****************************************************")
        print("**             欢迎进入--徐艺铭--招商银行           **")
        print("**       开户(0)                       查询(1)     **")
        print("**       存款(2)                       取款(3)     **")
        print("**       转账(4)                       改密(5)     **")
        print("**       锁定(6)                       解锁(7)     **")
        print("**       补卡(8)                       销户(9)     **")
        print("**                       退出(q)                   **")
        print("*****************************************************")

if __name__ == "__main__":
    Main().run()
