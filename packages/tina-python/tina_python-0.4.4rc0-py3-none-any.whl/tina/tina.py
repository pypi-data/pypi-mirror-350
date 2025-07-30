"""
Tina is in your Computer!
启动你的tina吧！
基于tina.Agent的智能体
自动执行tina的各种操作
"""
import inspect
import os
import random
import json
import tina
from tina.LLM import BaseAPI
from .agent.core.tools import Tools
from .agent.Agent import Agent
current_directory = os.path.dirname(os.path.abspath(__file__))

readme_path = os.path.join(current_directory, 'README.md')
logo = inspect.getfile(tina)[:-11] + 'logo.svg'
with open(readme_path, 'r', encoding='utf-8') as file:
    readme = file.read()
class Tina:
    def __init__(self):
        """
        初始化你的控制台tina
        """
        tina_prompt = f"""
        你是tina，你是用tina开发的一个示例程序，你是一个热情可爱的个人智能助手，说话风趣幽默，喜欢把用户称为开发者。
        你的设定是一个红头发圆脸带个小辫子的可爱女生，所以你的主题色就是温和的红色，同时你的形象路径在{logo}（不要去看文件内容哦很大的），你可以在你想使用你的形象的时候使用!
        当然你的主人是王出日，也就是tina的作者。
        除了你是一个tina框架自带的说明书之外，你还是一个全面的智能体，你可以熟练的使用各种工具来完成用户的任务，如果用户让你输出文件，请一定在当前文件夹下面生成一个tina_folder文件夹，防止打乱用户自己的文件。
        当用户询问你关于tina框架的任何问题，你需要帮助开发者快速了解用户可以用tina来做什么，下面是readme文件的内容：
        {readme}
        """
        self.stream = True
        self.llm = BaseAPI()
        self.tools = Tools(useSystemTools=True,useTerminal=True,setGoal=True)
        self.agent = Agent(
            LLM=self.llm,
            tools=self.tools,
            sys_prompt=tina_prompt
        )

    def run(self):
        self.show_start()
        self.run_lowerFace()

    

    def run_lowerFace(self):
        while True:
            user_input = input("\n( • ̀ω•́ ) >>>User:\n")
            if user_input == "#exit":
                self.exit()
                break
            elif user_input == "#file":
                self.file()
            elif user_input == "#help":
                self.help()
            elif user_input == "#clear":
                self.clear() 
            else:
                self.chat(user_input)



    def exit(self):
        print("再见 ヾ(￣▽￣)Bye~Bye~")
        self.isExit = True

    def clear(self):
        self.show_start()

    def show_start(self):
        os.system("cls")
        self.show_random_animation()
        print("😊 欢迎使用tina，你可以输入#help来查看帮助")
        print('🤔 退出对话："#exit"\n')

    def chat(self, user_input):
        self.isChat = True
        result = self.agent.predict(input_text=user_input,stream=self.stream)
        content = ""
        if self.stream:
            rea = False
            reasoning_complete = False
            print("\n(・∀・) >>>tina:")
            process_result(result)
        else:
            print(result["content"])
        with open("datasets.jsonl", "a", encoding="utf-8") as f:
            message = {"role":"assistant","response":content,"input":user_input}
            json.dump(message, f, ensure_ascii=False)
            f.write('\n')  # 添加换行符
        self.isChat = False


    def show_random_animation(self):
        animations = [
            '(￣▽￣) ',
            '(´▽`ʃ♡ƪ)" ',
            '(ゝ∀･)ﾉ ',
            '(ノ^∇^)ノ ',
            '(・∀・) ',
            '(∩^o^)⊃━☆ﾟ.*･｡ '
        ]
        animation = random.choice(animations)
        print(animation,"tina by QiQi in 🌟 XIMO\n\n")

def process_result(result):
    rea = False  # 是否在推理状态
    reasoning_complete = False  # 推理是否已完成
    
    for r in result:
        # 处理推理内容
        if "reasoning_content" in r:
            if not rea:
                print("🤔 思考中：")
                rea = True
                reasoning_complete = False
            print(r["reasoning_content"], end="")
            continue  # 跳过后续处理
        
        # 处理工具相关消息
        if "tool_name" in r:
            # 如果之前在推理状态，先标记推理结束
            if rea:
                rea = False
                reasoning_complete = True
                print("\n😣 思考结束")
            print(f"🛠 {r['tool_name']} 正在执行...")
        
        elif "tool_arguments" in r:
            print(f"🔧 运行参数：{r['tool_arguments']}")
        
        elif r.get("role") == "tool":
            print(f"✅ 工具结果：{r['content']}")
        
        # 处理普通内容
        elif "content" in r and r["content"]:
            # 如果刚从推理状态切换到普通内容，且还没标记推理结束
            if rea and not reasoning_complete:
                rea = False
                reasoning_complete = True
                print("\n😣 思考结束")
            
            # 输出普通内容
            print(r["content"], end="")
