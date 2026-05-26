# Thanks to SK lee who provided the skeleton code

import math, sys
import pandas as pd
import numpy as np
from tqdm import tqdm


class Node:
    def __init__(self, leaf=False):
        self.keys = []
        self.parent = []
        self.children = []
        self.leaf = leaf


class BTree:
    def __init__(self, t):
        '''
        # create a instance of the Class of a B-Tree
        # t : the minimum degree t
        # (the max num of keys is 2*t -1, the min num of keys is t-1)
        '''
        self.root = Node(True)
        self.t = t

    # B-Tree-Split-Child
    def split_child(self, x, i): 
        '''
        # split the node x's i-th child that is full
        # x: the current node
        # i: the index of the node x's child to be split
        # return: None
        '''
        t = self.t

        # 분할할 자식 노드
        y = x.children[i]

        # 새로 만들어질 오른쪽 노드
        z = Node(y.leaf)

        # 중앙값
        middle_key = y.keys[t - 1]

        # 오른쪽 절반 key를 새 노드 z로 이동
        z.keys = y.keys[t:]

        # 왼쪽 절반만 y에 남김
        y.keys = y.keys[:t - 1]

        # leaf가 아니라면 자식도 나눠야 함
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]

        # 부모 x에 새 자식 삽입
        x.children.insert(i + 1, z)

        # 부모 x에 중앙 key 삽입
        x.keys.insert(i, middle_key)


    # B-Tree-Insert
    def insert(self, k):
        '''
        # insert the key k into the B-Tree
        # return: None
        '''
        root = self.root

        # Case 1: if the root is full
        if len(root.keys) == 2 * self.t - 1:
            # 새로운 root 생성
            new_root = Node(False)

            # 기존 root를 새 root의 자식으로 연결
            new_root.children.append(root)

            # B-Tree의 root를 새 root로 변경
            self.root = new_root

            # 기존 root를 split
            self.split_child(new_root, 0)

            # split 이후 알맞은 위치에 key 삽입
            self.insert_key(new_root, k)

        # Case 2: if the root is not full
        else:
            self.insert_key(root, k)
        


    # B-Tree-Insert-Nonfull
    def insert_key(self, x, k):
        '''
        # insert the key k into node x
        # return: None
        '''

        i = len(x.keys) - 1

        # Case 1: if the node x is leaf
        if x.leaf:
            # 새 key가 들어갈 공간을 먼저 하나 만든다
            x.keys.append(None)

            # 뒤에서부터 비교하면서 k보다 큰 key들을 한 칸씩 오른쪽으로 민다
            while i >= 0 and k[0] < x.keys[i][0]:
                x.keys[i + 1] = x.keys[i]
                i -= 1

            # 올바른 위치에 새 key-value 삽입
            x.keys[i + 1] = k

        # Case 2: if the node x is an internal node
        else:
            # k가 내려가야 할 자식 위치를 찾는다
            while i >= 0 and k[0] < x.keys[i][0]:
                i -= 1

            # while이 끝나면 i는 k보다 작은 key의 위치
            # 실제 내려갈 자식은 i + 1
            i += 1

            # 내려갈 자식이 full이면 먼저 split
            if len(x.children[i].keys) == 2 * self.t - 1:
                self.split_child(x, i)

                # split 후, 부모로 올라온 key와 비교해서
                # 오른쪽 자식으로 갈지 왼쪽 자식으로 갈지 결정
                if k[0] > x.keys[i][0]:
                    i += 1

            # 적절한 자식으로 재귀 삽입
            self.insert_key(x.children[i], k)


    # B-Tree-Search
    def search_key(self, x, key):
        '''
        # search for the key in node x
        # return: the node x that contains the key, the index of the key if the key is in the B-tree
        '''

        i = 0

        # 현재 노드 x 안에서 key가 들어갈 위치를 찾는다.
        # x.keys[i][0]은 [key, value] 중 key 값이다.
        while i < len(x.keys) and key > x.keys[i][0]:
            i += 1

        # 현재 노드에서 key를 찾은 경우
        if i < len(x.keys) and key == x.keys[i][0]:
            return x, i

        # 현재 노드가 leaf라면 더 내려갈 자식이 없으므로 탐색 실패
        if x.leaf:
            return None

        # leaf가 아니라면 적절한 자식 노드로 내려가서 다시 탐색
        return self.search_key(x.children[i], key)


    def delete(self, k):
        '''
        # delete the key k from the B-tree
        # return: None
        '''
        self.delete_key(self.root, k)
        
        # 루트가 비었고 자식이 있으면 높이를 줄인다
        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.children[0] 

    def delete_key(self, x, k):
        t = self.t
        i = 0

        while i < len(x.keys) and k > x.keys[i][0]:
            i += 1

        if i < len(x.keys) and k == x.keys[i][0]:
            if x.leaf:
                self.delete_leaf_node(x, i)
            else:
                self.delete_internal_node(x, i)
            return

        if x.leaf:
            return

        flag = (i == len(x.keys))

        if len(x.children[i].keys) < t:
            self.fill_child(x, i)

        if flag and i > len(x.keys):
            self.delete_key(x.children[i - 1], k)
        else:
            self.delete_key(x.children[i], k)

    def delete_leaf_node(self, x, i):
        '''
        # delete the key in a leaf node
        '''
        x.keys.pop(i)

    def delete_internal_node(self, x, i):
        '''
        # delete the key in an internal node
        '''
        t = self.t
        k = x.keys[i]

        left_child = x.children[i]
        right_child = x.children[i + 1]

        # Case 1: 왼쪽 자식에 key가 충분하면 predecessor로 대체
        if len(left_child.keys) >= t:
            pred = self.find_predecessor(left_child)
            x.keys[i] = pred
            self.delete_key(left_child, pred[0])

        # Case 2: 오른쪽 자식에 key가 충분하면 successor로 대체
        elif len(right_child.keys) >= t:
            succ = self.find_successor(right_child)
            x.keys[i] = succ
            self.delete_key(right_child, succ[0])

        # Case 3: 양쪽 자식 모두 최소 key 수라면 merge
        else:
            self.merge_children(x, i)
            self.delete_key(left_child, k[0])

    def find_predecessor(self, x):
        # 왼쪽 서브트리에서 가장 큰 key
        while not x.leaf:
            x = x.children[-1]
        return x.keys[-1]


    def find_successor(self, x):
        # 오른쪽 서브트리에서 가장 작은 key
        while not x.leaf:
            x = x.children[0]
        return x.keys[0]


    def fill_child(self, x, i):
        t = self.t

        # 왼쪽 형제에게 빌릴 수 있으면 빌림
        if i != 0 and len(x.children[i - 1].keys) >= t:
            self.borrow_from_prev(x, i)

        # 오른쪽 형제에게 빌릴 수 있으면 빌림
        elif i != len(x.children) - 1 and len(x.children[i + 1].keys) >= t:
            self.borrow_from_next(x, i)

        # 둘 다 못 빌리면 merge
        else:
            if i != len(x.children) - 1:
                self.merge_children(x, i)
            else:
                self.merge_children(x, i - 1)


    def borrow_from_prev(self, x, i):
        child = x.children[i]
        sibling = x.children[i - 1]

        # 부모 key를 child 앞으로 내림
        child.keys.insert(0, x.keys[i - 1])

        # 왼쪽 형제의 마지막 key를 부모로 올림
        x.keys[i - 1] = sibling.keys.pop()

        # internal node면 자식도 같이 이동
        if not sibling.leaf:
            child.children.insert(0, sibling.children.pop())


    def borrow_from_next(self, x, i):
        child = x.children[i]
        sibling = x.children[i + 1]

        # 부모 key를 child 뒤로 내림
        child.keys.append(x.keys[i])

        # 오른쪽 형제의 첫 key를 부모로 올림
        x.keys[i] = sibling.keys.pop(0)

        # internal node면 자식도 같이 이동
        if not sibling.leaf:
            child.children.append(sibling.children.pop(0))


    def merge_children(self, x, i):
        child = x.children[i]
        sibling = x.children[i + 1]

        # 부모 key를 child로 내림
        child.keys.append(x.keys.pop(i))

        # 오른쪽 형제 key들을 child에 합침
        child.keys.extend(sibling.keys)

        # internal node면 자식들도 합침
        if not child.leaf:
            child.children.extend(sibling.children)

        # 오른쪽 형제 제거
        x.children.pop(i + 1)

    # implement whatever you need 
    #  def borrow_merge(self, x, j):
        #  pass

    #  def check_smaller_than_t(self, x):
        #  pass

    #  def find_predecessor(self, x):
        #  pass

    #  def merge_sibling(self, x, i, j):
        #  pass

    #  def borrow_sibling(self, x, i, j):
        #  pass


    # for printing the statistic of the resulting B-tree
    def traverse_key(self, x, level=0, level_counts=None):
        '''
        # run BFS on the B-tree to count the number of keys at every level
        # return: level_counts
        '''
        if level_counts is None:
            level_counts = {}

        if x:
            # counting the number of keys at the current level
            if level in level_counts:
                level_counts[level] += len(x.keys)
            else:
                level_counts[level] = len(x.keys)

            # recursively call the traverse_key() for further traverse
            for child in x.children:
                self.traverse_key(child, level + 1, level_counts)

        return level_counts

# Btree Class done


def get_file():
    '''
    # read an input file (.csv) with its name
    '''
    file_name = (input("Enter the file name you want to insert or delete ▷ (e.g., insert1 or delete1_50 or delete1_90 or ...) "))

    while True:
        try:
            file = pd.read_csv('inputs/'+file_name+'.csv',
                               delimiter='\t', names=['key', 'value'])
            return file
        except FileNotFoundError:
            print("File does not exist.")
            file_name = (input("Enter the file name again. ▷ "))


def insertion_test(B, file):
    '''
    #   read all keys and values from the file and insert them into the B-tree
    #   B   : an empty B-tree
    #   file: a csv file that contains keys to be inserted
    #   return: the resulting B-tree
    '''

    file_key = file['key']
    file_value = file['value']

    print('===============================')
    print('[ Insertion start ]')

    for i in tqdm(range(len(file_key))): # tqdm shows the insertion progress and the elapsed time
        B.insert([file_key[i], file_value[i]])

    print('[ Insertion complete ]')
    print('===============================')
    print()

    return B


def deletion_test(B, delete_file):
    '''
    #   read all keys and values from the file and delete them from the B-tree
    #   B   : the current B-tree
    #   file: a csv file that contains keys to be deleted
    #   return: the resulting B-tree
    '''

    delete_key = delete_file['key']

    print('===============================')
    print('[ Deletion start ]')

    for i in tqdm(range(len(delete_key))):
        B.delete(delete_key[i])

    print('[ Deletion complete ]')
    print('===============================')
    print()

    return B


def print_statistic(B):
    '''
    # print the information about the current B-tree
    # the number of keys at each level
    # the total number of keys in the B-tree
    '''
    print('===============================')
    print('[ Print statistic of tree ]')

    level_counts = B.traverse_key(B.root)

    for level, counts in level_counts.items():
        if level == 0:
            print(f'Level {level} (root): Key Count = {counts}')
        else:
            print(f'Level {level}: Key Count = {counts}')
    print('-------------------------------')
    total_keys = sum(counts for counts in level_counts.values())
    print(f'Total number of keys across all levels: {total_keys}')
    print('[ Print complete ]')
    print('===============================')
    print()

def main():
    while True:
        try:
            num = int(input("1.insertion 2.deletion. 3.statistic 4.end ▶  "))

            # 1. Insertion
            if num == 1: 
                t = 3 # minimum degree
                B = BTree(t) # make an empty b-tree with the minimum degree t

                insert_file = get_file()
                B = insertion_test(B, insert_file)

            # 2. Deletion
            elif num == 2:
                delete_file = get_file()
                B = deletion_test(B, delete_file)

            # 3. Statistic
            elif num == 3:
                print_statistic(B)

            # 4. End program
            elif num == 4:
                sys.exit(1)

            else:
                print("Invalid input. Please enter 1, 2, 3, or 4.")

        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == '__main__':
    main()