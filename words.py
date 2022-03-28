import random
from collections import namedtuple

Point = namedtuple('Point', 'X Y')
Block = namedtuple('Block', 'image start_pos end_pos name next')

# 土字相关偏旁——编号为1,
# 木字相关偏旁——编号为2,
# 日字相关偏旁——编号为3
TU_BLOCK = [Block("images/tu.png", Point(0, 0), Point(0, 1), "1", 1),
            Block("images/tu.png", Point(0, 0), Point(1, 0), "1", 2),
            Block("images/tu.png", Point(0, 0), Point(1, 1), "1", 0)
            ]

MU_BLOCK = [Block("images/mu.png", Point(0, 0), Point(0, 1), "2", 1),
            Block("images/mu.png", Point(0, 0), Point(1, 0), "2", 2),
            Block("images/mu.png", Point(0, 0), Point(1, 1), "2", 0)]

RI_BLOCK = [Block("images/ri.png", Point(0, 0), Point(0, 1), "3", 1),
            Block("images/ri.png", Point(0, 0), Point(1, 0), "3", 2),
            Block("images/ri.png", Point(0, 0), Point(1, 1), "3", 0)]

# 触发消除的汉字
# 晶
# 林
# 杳
# 昌
# 杲

BLOCKS = {'1': TU_BLOCK,
          '2': MU_BLOCK,
          '3': RI_BLOCK,
          }


def get_block():
    block_name = random.choice('23')
    b = BLOCKS[block_name]

    idx = random.randint(0, len(b) - 1)
    return b[idx]


def get_next_block(block):
    b = BLOCKS[block.name]
    return b[block.next]
