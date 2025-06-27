from collections import deque
from typing import Iterable, Generator, List, Tuple
import heapq

# https://docs.python.org/3/library/collections.abc.html
# https://docs.python.org/3/library/collections.html
# https://docs.python.org/3/library/heapq.html


"""
░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1.1 将序列分解为单独变量 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░
────────────────────────────────────────────────────────────────────────────────────────────
⭐ 适用对象 : 所有可迭代对象 (元组 / 列表 / 字符串 / 文件对象 / 迭代器 / 生成器 …)
⭐ 数量匹配 : 变量数量必须与序列元素数量一致，否则抛 ValueError
⭐ 结构匹配 : 支持嵌套结构解包，例如 (year, mon, day) = date_tuple
⭐ 占位符   : 使用下划线 _ 忽略不需要的值
⭐ 部分解包 : Python 无专门语法，必须为每个元素提供变量名 (或占位符)
♻️ 可迭代判定 : 对象只需实现 __iter__() 即视作 Iterable
────────────────────────────────────────────────────────────────────────────────────────────
万物皆对象  Everything is an Object (identity / type / value)
🔥🔥🔥 Python 运行期把任何东西（数字、字符串、函数、类、模块、None …）都视作 object 的一个实例。
每个对象自带三块核心元信息
⭐ identity  — id(obj) 返回的整数，通常映射到对象在内存中的地址；在对象的生命周期内保持不变。
⭐ type — type(obj) 返回对象所属的 class，决定它支持哪些操作、方法与运算符。
⭐ value  — 对象存储的数据本体。
   - 不可变对象 (int, str, tuple, frozenset …) 一旦创建其值不可修改；“修改” 会得到新对象，身份改变。
   - 可变对象 (list, dict, set, bytearray …) 可在原身份上原地修改其值
────────────────────────────────────────────────────────────────────────────────────────────
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
────────────────────────────────────────────────────────────────────────────────────────────
⭐ 适用场景 : 当可迭代对象元素多于变量时，用 *var 接收剩余元素
⭐ 收集类型 : *var 永远是 list（即便为空）
⭐ 位置灵活 : *var 可在开头、中间、结尾（*head, last / first, *mid, last / first, *tail）
⭐ 占位符   : 若仅想丢弃余下元素，用 *_ 或其他占位名
────────────────────────────────────────────────────────────────────────────────────────────
"""
def drop_first_last(grades):                     # grades = [10, 9, 8, 7, 6]
    first, *middle, last = grades
    return sum(middle) / len(middle)             # → 8.0

record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
name, email, *phones = record  # name='Dave', email='dave@example.com', phones=['773-555-1212','847-555-1212']
line = 'nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false'
uname, *_, homedir, shell = line.split(':')       # uname='nobody', homedir='/var/empty', shell='/usr/bin/false'


"""
░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1.3 保留最后 N 个元素 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░
────────────────────────────────────────────────────────────────────────────────────────────
⭐ 问题     : 迭代或其他操作中，仅需保留最近 N 条记录
⭐ 解决方案 : 使用 collections.deque(maxlen=N) 自动丢弃最老元素
⭐ 特点     : append 操作 O(1)，满时自动剔除队首；appendleft, pop, popleft 同样高效
────────────────────────────────────────────────────────────────────────────────────────────
⭐ 容器 (Container)
   • 定义 : 实现 __contains__(self, item) 或支持 in 运算的对象，可存放其他对象的盒子
   • 典型 : list, tuple, set, dict, str, deque, 自定义类实现 __iter__/__len__/__contains__ 亦可视为容器
   • 特性 : 可配合 len(), in, 迭代等操作; 多数容器同样是 Iterable / Collection
⭐ 生成器 (Generator)
   • 定义 : 含有 yield 的函数调用结果，返回一个延迟计算的迭代器；或 (expr for x in iterable) 推导式产生
   • 协议 : 同时实现 __iter__() 和 __next__()，每次 next() 产出一个值，直至抛 StopIteration
   • 优势 : 惰性、节省内存，可无限序列或大数据流; 可配合 send() /throw() /close() 做协程
────────────────────────────────────────────────────────────────────────────────────────────
"""
def search(lines: Iterable[str], pattern: str, history: int = 3) -> Generator[Tuple[str, List[str]], None, None]:
    prev: deque[str] = deque(maxlen=history)
    for line in lines:
        if pattern in line:
            yield line, list(prev)
        prev.append(line)

logs = ['a','python error','b','c','python ok','d']
for match, prev in search(logs, 'python', history=2):
    print(match, prev)                          # → 'python error', ['a']
                                                # → 'python ok', ['b', 'c']


"""
░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1.4 查找最大或最小的 N 个元素 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░
────────────────────────────────────────────────────────────────────────────────────────────
⭐ 场景     : 从序列或可迭代对象中快速获得最大 / 最小的前 N 个元素
⭐ 核心 API : heapq.nlargest(N, data, key=...) / heapq.nsmallest(...)
⭐ 性能优势 : 当 N ≪ 数据量时，复杂度 ~ O(len(data) · log N)，优于整体排序
• N == 1          → 直接用 min() / max() 更快
• N 接近数据量     → 直接排序后切片; sorted(data)[:N] / [-N:]
• N 远小于数据量   → heapq.nlargest/nsmallest 优势最大
────────────────────────────────────────────────────────────────────────────────────────────
常用堆操作 API（heapq 模块）
⭐ heapq.heapify(seq)
   • 将任意序列原地转成最小堆；时间复杂度 O(len(seq))
⭐ heapq.heappush(heap, item)
   • 向堆插入新元素并保持堆性质
⭐ heapq.heappop(heap)
   • 弹出并返回最小元素（堆顶）
⭐ heapq.heappushpop(heap, item)
   • 先 push 再 pop，但只做一次平衡；比先 push 再 pop 更快
⭐ heapq.heapreplace(heap, item)
   • 先 pop 最小元素，再 push 新元素；与 heappushpop 作用相反
⭐ heapq.merge(*iterables)
   • 多个已排序输入按顺序合并生成器，节省内存；适合外排序
⏩ 记忆要点：heap[0] 永远是最小值，所有操作都围绕维护这一不变式
────────────────────────────────────────────────────────────────────────────────────────────
"""
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
heapq.nlargest(3, nums)   # → [42, 37, 23]
heapq.nsmallest(3, nums)  # → [-4, 1, 2]
portfolio = [
    {'name': 'IBM',  'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50,  'price': 543.22},
    {'name': 'FB',   'shares': 200, 'price': 21.09},
    {'name': 'HPQ',  'shares': 35,  'price': 31.75},
    {'name': 'YHOO', 'shares': 45,  'price': 16.35},
    {'name': 'ACME', 'shares': 75,  'price': 115.65},
]
cheap      = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
expensive  = heapq.nlargest(3,  portfolio, key=lambda s: s['price'])


"""
░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1.5 实现一个优先级队列 (Priority Queue) ░░░░░░░░░░░░░░░░░░░░░░░░░░░░
────────────────────────────────────────────────────────────────────────────────────────────
⭐ 场景     : 需要按优先级（权重）依次取元素，最高优先级先出队
⭐ 数据结构 : heapq + 元组 (-priority, index, item) 形成稳定的最大堆
⭐ 复杂度   : push / pop 均为 O(log n)，适合海量数据
⭐ index   : 避免同优先级元素不可比较，并确保 FIFO 顺序
────────────────────────────────────────────────────────────────────────────────────────────
"""
class PriorityQueue:
    """最大堆优先级队列，支持同优先级 FIFO。"""
    def __init__(self):
        self._queue: list[tuple[int, int, object]] = []  # (-priority, index, item)
        self._index: int = 0

    def push(self, item, priority: int) -> None:
        # -priority ↔ 最大堆；index 保证同优先级按插入顺序 (稳定)
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        """弹出优先级最高且最早插入的元素"""
        return heapq.heappop(self._queue)[-1]


"""
░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 1.6 字典中的键映射多个值 (Multi‑Dict) ░░░░░░░░░░░░░░░░░░░░░░░░░░░░
──────────────────────────────────────────────
⭐ 场景     : 需要让同一个键关联多个值（如日志归类、倒排索引）
⭐ 推荐做法 : collections.defaultdict( list / set ) —— 自动初始化容器
⭐ 何时用哪种容器
   • list  → 保留插入顺序，允许重复
   • set   → 去重且不关心顺序
"""
list_map: defaultdict[str, list[int]] = defaultdict(list)
list_map['a'].append(1)
list_map['a'].append(2)
list_map['b'].append(4)
# list_map == {'a': [1, 2], 'b': [4]}

set_map: defaultdict[str, set[int]] = defaultdict(set)
set_map['a'].add(1)
set_map['a'].add(2)
set_map['a'].add(2)  # 重复被忽略
set_map['b'].add(4)
# set_map == {'a': {1, 2}, 'b': {4}}
