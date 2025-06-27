"""
░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1.1 将序列分解为单独变量 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░
──────────────────────────────────────────────
⭐ 适用对象 : 所有可迭代对象 (元组 / 列表 / 字符串 / 文件对象 / 迭代器 / 生成器 …)
⭐ 数量匹配 : 变量数量必须与序列元素数量一致，否则抛 ValueError
⭐ 结构匹配 : 支持嵌套结构解包，例如 (year, mon, day) = date_tuple
⭐ 占位符   : 使用下划线 _ 忽略不需要的值
⭐ 部分解包 : Python 无专门语法，必须为每个元素提供变量名 (或占位符)
♻️ 可迭代判定 : 对象只需实现 __iter__() 即视作 Iterable
──────────────────────────────────────────────
万物皆对象  Everything is an Object (identity / type / value)
──────────────────────────────────────────────
🔥🔥🔥 Python 运行期把任何东西（数字、字符串、函数、类、模块、None …）都视作 object 的一个实例。
每个对象自带三块核心元信息
⭐ identity  — id(obj) 返回的整数，通常映射到对象在内存中的地址；在对象的生命周期内保持不变。
⭐ type — type(obj) 返回对象所属的 class，决定它支持哪些操作、方法与运算符。
⭐ value  — 对象存储的数据本体。
   - 不可变对象 (int, str, tuple, frozenset …) 一旦创建其值不可修改；“修改” 会得到新对象，身份改变。
   - 可变对象 (list, dict, set, bytearray …) 可在原身份上原地修改其值
"""

# 基本解包
x, y = (4, 5)
# 列表 + 嵌套元组
data = ['ACME', 50, 91.1, (2012, 12, 21)]
name, shares, price, (year, mon, day) = data  # 嵌套解包
# 使用占位符 _ 忽略不需要的值
_, shares, price, _ = data
# ❌ 解包数量不匹配示例 (抛 ValueError)
try:
    a, b, c = (1, 2)
except ValueError as err:
    print("ValueError:", err)


"""
░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1.2 解压可迭代对象赋值给多个变量 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░
⭐ 适用场景 : 当可迭代对象元素多于变量时，用 *var 接收剩余元素
⭐ 收集类型 : *var 永远是 list（即便为空）
⭐ 位置灵活 : *var 可在开头、中间、结尾（*head, last / first, *mid, last / first, *tail）
⭐ 占位符   : 若仅想丢弃余下元素，用 *_ 或其他占位名
"""

def drop_first_last(grades):                     # grades = [10, 9, 8, 7, 6]
    first, *middle, last = grades
    return sum(middle) / len(middle)             # → 8.0

record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
name, email, *phones = record  # name='Dave', email='dave@example.com', phones=['773-555-1212','847-555-1212']

*prev, current = [10, 8, 7, 1, 9, 5, 10, 3]      # prev=[10,8,7,1,9,5,10], current=3
line = 'nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false'
uname, *_, homedir, shell = line.split(':')       # uname='nobody', homedir='/var/empty', shell='/usr/bin/false'
