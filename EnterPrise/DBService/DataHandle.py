"""
这个文件主要用于数据脱敏处理，默认的脱敏处理方法是用*替换
rep_char:代表用于替换的字符
rep_star:开始提换的位置
rep_end:替换结束的位置（包含）
"""


def desensitize(data: str, rep_star: int = 1, rep_end: int = None, rep_char: str = "*"):
    char = data[0:rep_star]
    length = len(data)
    if rep_end and length - 1 > rep_end >= rep_star:
        bol = True  # 判断时候还有尾部需要拼接
        end = rep_end
    else:
        bol = False
        end = length - 1
    for i in range(rep_star, end + 1):
        char += rep_char
    if bol:
        for index in range(end + 1, length):
            char += data[index]
    print(char)
    return char
