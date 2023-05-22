import json
import discord
from discord.ext import commands
import random
bot = commands.Bot(command_prefix='$')

user_experience = {}

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    author_id = str(message.author.id)
    if author_id not in user_experience:
        user_experience[author_id] = {
            'experience': 0,
            'name': message.author.name,
            'joined_at': str(message.author.joined_at)
        }

    experience_gain = random.randint(1, 20) #1~20經驗值隨機增加
    user_experience[author_id]['experience'] += experience_gain

    await bot.process_commands(message)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    author_id = str(message.author.id)
    if author_id not in user_experience:
        user_experience[author_id] = {
            'experience': 0,
            'name': message.author.name,
            'joined_at': str(message.author.joined_at)
        }

    experience_gain = random.randint(1, 20)
    user_experience[author_id]['experience'] += experience_gain

    await bot.process_commands(message)

# 等級系統指令示範：rank 指令
@bot.command() 
async def rank(ctx):
    author_id = str(ctx.author.id)
    if author_id not in user_experience or ctx.guild.get_member(int(author_id)) is None:
        await ctx.send('你還沒有等級或不存在於該伺服器。') #當成員不存在伺服器或未曾發言過時會顯示的
        return

    user_level = get_user_level(user_experience[author_id]['experience'])  # 獲取用戶等級
    experience = user_experience[author_id]['experience']
    message = f'{ctx.author.mention}，你的等級是 {user_level}，經驗值為 {experience}。'
    await ctx.send(message)

# 自訂函式示範：根據經驗值計算等級
def get_user_level(experience):
    level = experience // 100  # 假設每100經驗值升一級
    return level

# 儲存用戶等級至 user_levels.js 檔案
def save_user_levels():
    with open('user_levels.js', 'w') as file:
        json.dump(user_experience, file)

# 讀取用戶等級從 user_levels.js 檔案
def load_user_levels():
    global user_experience
    try:
        with open('user_levels.js', 'r') as file:
            user_experience = json.load(file)
    except FileNotFoundError:
        # 若找不到檔案，則初始化為空字典
        user_experience = {}

# 在機器人啟動時讀取用戶等級>讀取位置在user_levels-js
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('Hello, I am your Discord Bot. Nice to meet you!')
    load_user_levels()

# 在機器人關閉時儲存用戶等級
@bot.event
async def on_disconnect():
    save_user_levels()

# 音樂系統示範：播放音樂
@bot.command()
async def play(ctx, url):
    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()

    # 根據url播放音樂的相應邏輯 #因爲沒有spotif的API的關係 有可能會中YouTube的版權炮

    # 當播放完畢後，機器人會離開語音頻道
    await voice_client.disconnect()

# 計算系統示範：計算指令
@bot.command()
async def calculate(ctx, expression):
    try:
        result = eval(expression)
        await ctx.send(f'計算結果：{result}')   #計算結果
    except Exception as e:
        await ctx.send(f'計算時發生錯誤：{e}')  #計算時出現錯誤

bot.run('bot.token')  # 將bot.token替換為您的機器人令牌
