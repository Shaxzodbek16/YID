emojis = ["1⃣️️️️️️", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", " 9️⃣", "🔟"]


async def num_to_emoji(num: int) -> str:
    is_negative = False
    res_str = []
    if num < 0:
        is_negative = True
    num = abs(num)
    while num > 10:
        res_str.append(emojis[num % 10 - 1])
        num //= 10
    res_str.append(emojis[num - 1])
    res_str.reverse()
    res_str = "".join(res_str)
    return "➖" + res_str if is_negative else res_str
