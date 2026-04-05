'''1. Даны два целых положительных числа a и b. Найдите их наибольший общий делитель.​'''
def solution(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


'''2. Дано целое положительное число n. Определите, является ли оно простым.​'''
def solution(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


'''3. Даны два натуральных числа a и b. Найдите количество их общих делителей.​'''
def solution(a: int, b: int) -> int:
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x

    g = gcd(a, b)
    cnt = 0
    d = 1
    while d * d <= g:
        if g % d == 0:
            cnt += 1
            if d * d != g:
                cnt += 1
        d += 1
    return cnt

def nod(a:int,b:int):
    while b:
        a,b = b, a%b
    return a


'''4. Дано натуральное число k. Найдите k‑тое простое числ Считайте, что число 2 — это первое простое число.​'''
def solution(k: int) -> int:
    # верхнюю границу можно взять примерно k*(log k + log log k) для k >= 6
    if k == 1:
        return 2
    import math
    if k < 6:
        limit = 15
    else:
        limit = int(k * (math.log(k) + math.log(math.log(k)))) + 10

    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            step = i
            start = i * i
            is_prime[start:limit + 1:step] = [False] * ((limit - start) // step + 1)

    primes = [i for i, v in enumerate(is_prime) if v]
    return primes[k - 1]


'''5. Дана строка s. Вычислите значения префикс‑функции для этой строки. 
Префикс‑функция π[i] — это длина наибольшего собственного суффикса подстроки s[0...i], совпадающего с её префиксом.​'''
def solution(s: str) -> list[int]:
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi


'''6. Дана строка s. Вычислите значения Z‑функции для этой строки. 
Z‑функция Z[i] — это длина наибольшего общего префикса строки s и её суффикса, начинающегося в позиции i.​'''
def solution(s: str) -> list[int]:
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z



'''7. Даны две строки a и b. Определите, является ли строка b циклическим сдвигом строки a. 
Циклический сдвиг — это перенос любого количества символов из начала строки в её конец без изменения порядка.​'''
def solution(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    return b in (a + a)


'''8. Дана строка s, состоящая из заглавных латинских букв. Сожмите строку алгоритмом RLE (Run‑Length Encoding). 
Замените каждую серию одинаковых символов на сам символ и количество его повторений.​'''
def solution(s: str) -> str:
    res = []
    cur = s[0]
    cnt = 1
    for ch in s[1:]:
        if ch == cur:
            cnt += 1
        else:
            res.append(cur + str(cnt))
            cur = ch
            cnt = 1
    res.append(cur + str(cnt))
    return "".join(res)


'''9. Даны две строки: текст text и образец pattern. Найдите все позиции вхождений образца в текст. 
Используйте алгоритм Кнута‑Морриса‑Пратта с префикс‑функцией.​'''
def solution(text: str, pattern: str) -> list[int]:
    if not pattern:
        return list(range(len(text) + 1))

    s = pattern + "#" + text
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j

    m = len(pattern)
    res = []
    for i in range(m + 1, n):
        if pi[i] == m:
            res.append(i - 2 * m)
    return res


'''10. Дана строка s. Найдите длину её минимального периода. Строка имеет период длины k, 
если s[i] = s[i+k] для всех допустимых i, и длина строки делится на k без остатка. 
Если строку нельзя представить как повторение подстроки меньшей длины, период равен длине строки.​'''
def solution(s: str) -> int:
    n = len(s)
    if n < 2:
        return n
    pi = [0] * n
    j = 0
    for i in range(1, n):
        while j > 0 and s[i] != s[j]:
            j = pi[j-1]
        if s[i] == s[j]:
            j+=1
        pi[i] = j
    p = n - pi[-1]
    if n % p == 0:
        return p
    return n
    
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
'''11. Дана строка s, состоящая из строчных латинских букв. Переставьте буквы так, чтобы одинаковые буквы не стояли рядом. 
Если получить такую строку невозможно, верните пустую строку.​'''
import heapq

def solution(s: str) -> str:
    from collections import Counter
    cnt = Counter(s)
    heap = [(-c, ch) for ch, c in cnt.items()]
    heapq.heapify(heap)

    prev_cnt, prev_ch = 0, ""
    res = []

    while heap or prev_cnt < 0:
        if not heap and prev_cnt < 0:
            return ""
        c, ch = heapq.heappop(heap)
        res.append(ch)
        c += 1  # ближе к нулю

        if prev_cnt < 0:
            heapq.heappush(heap, (prev_cnt, prev_ch))
        prev_cnt, prev_ch = c, ch

    return "".join(res)
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


'''12. Дана строка s, состоящая из символов '(' и ')'. Найдите длину наибольшей правильной скобочной подстроки. 
Последовательность скобок верна, если для каждой открытой скобки есть закрытая и они закрываются в правильном порядке.​'''
def solution(s: str) -> int:
    stack = [-1]
    best = 0
    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                best = max(best, i - stack[-1])
    return best


'''13. Дан односвязный список. Разверните его задом наперёд. Разворот должен выполняться на месте (in‑place), без создания новых узлов.​'''
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def solution(head: ListNode) -> ListNode:
    prev = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev


'''14. Дан односвязный список. Определите, содержит ли он цикл. Цикл возникает, 
когда последний узел ссылается на один из предыдущих узлов (или на самого себя).​'''
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def solution(head: ListNode) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False


'''15. Даны два отсортированных по возрастанию односвязных списка. Объедините их в один новый отсортированный список.​'''
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def solution(list1: ListNode, list2: ListNode) -> ListNode:
    dummy = ListNode()
    tail = dummy
    a, b = list1, list2
    while a and b:
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a if a else b
    return dummy.next


'''16. Реализуйте класс, который эмулирует работу кнопок «Назад» и «Вперёд» в браузере. 
Класс должен поддерживать операции visit(url), back(steps), forward(steps). 
При посещении новой страницы после возврата назад, вся история «вперёд» удаляется.​'''
class BrowserHistory:
    def __init__(self, homepage: str):
        self.back_stack = [homepage]
        self.forward_stack = []

    def visit(self, url: str) -> None:
        self.back_stack.append(url)
        self.forward_stack.clear()

    def back(self, steps: int) -> str:
        while steps > 0 and len(self.back_stack) > 1:
            self.forward_stack.append(self.back_stack.pop())
            steps -= 1
        return self.back_stack[-1]

    def forward(self, steps: int) -> str:
        while steps > 0 and self.forward_stack:
            self.back_stack.append(self.forward_stack.pop())
            steps -= 1
        return self.back_stack[-1]


'''17. Дан односвязный список. Определите, является ли он палиндромом. 
Список является палиндромом, если последовательность значений читается одинаково слева направо и справа налево.​'''
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def solution(head: ListNode) -> bool:
    if not head or not head.next:
        return True

    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # разворот второй половины
    prev = None
    cur = slow
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt

    # сравнение
    p1, p2 = head, prev
    while p2:
        if p1.val != p2.val:
            return False
        p1 = p1.next
        p2 = p2.next

    # (можно вернуть структуру назад, если надо)
    return True


'''18. Дана строка s, содержащая только символы '(', ')', '{', '}', '[' , ']'. 
Определите, является ли последовательность скобок правильной. Последовательность правильна, 
если каждая открывающая скобка имеет соответствующую закрывающую и скобки закрываются в правильном порядке.​'''
def solution(s: str) -> bool:
    stack = []
    brackets = {')':'(', ']':'[', '}':'{'}
    for ch in s:
        if ch in '[{(':
            stack.append(ch)
        if ch in brackets:
            if not stack or stack.pop() != brackets[ch]:
                return False
    return not stack
    

'''19. Реализуйте структуру данных «Стек» с использованием массива. Стек должен поддерживать операции push, pop, peek, is_empty.​'''
class Stack:
    def __init__(self):
        self.data = []

    def push(self, x: int) -> None:
        self.data.append(x)

    def pop(self) -> int:
        return self.data.pop()

    def peek(self) -> int:
        return self.data[-1]

    def is_empty(self) -> bool:
        return len(self.data) == 0


'''20. Реализуйте структуру данных «Очередь» с использованием дека. Очередь должна поддерживать операции enqueue, dequeue, front, is_empty.​'''
from collections import deque

class Queue:
    def __init__(self):
        self.d = deque()

    def enqueue(self, x: int) -> None:
        self.d.append(x)

    def dequeue(self) -> int:
        return self.d.popleft()

    def front(self) -> int:
        return self.d[0]

    def is_empty(self) -> bool:
        return len(self.d) == 0


'''21. Реализуйте стек, который поддерживает операцию получения минимального элемента за O(1). Стек должен поддерживать push, pop, get_min.​'''
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, x: int) -> None:
        self.stack.append(x)
        if not self.min_stack or x <= self.min_stack[-1]:
            self.min_stack.append(x)

    def pop(self) -> int:
        x = self.stack.pop()
        if x == self.min_stack[-1]:
            self.min_stack.pop()
        return x

    def get_min(self) -> int:
        return self.min_stack[-1]
    

'''22. Дана матрица image, координаты стартового пикселя (sr, sc) и новый цвет new_color. 
Выполните заливку области: измените цвет стартового пикселя и всех пикселей того же цвета, 
связанных с ним по вертикали или горизонтали, на new_color.​'''
def solution(image: list[list[int]], sr: int, sc: int, new_color: int) -> list[list[int]]:
    n, m = len(image), len(image[0])
    start_color = image[sr][sc]
    if start_color == new_color:
        return image

    stack = [(sr, sc)]
    while stack:
        r, c = stack.pop()
        if image[r][c] != start_color:
            continue
        image[r][c] = new_color
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m and image[nr][nc] == start_color:
                stack.append((nr, nc))
    return image


'''23. Дан массив целых чисел nums. Для каждого элемента найдите первый больший элемент справа от него. 
Если большего элемента нет, верните −1 для этой позиции.​'''
def solution(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [-1] * n
    stack = []  # индексы, для которых не найден следующий больший

    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            j = stack.pop()
            res[j] = x
        stack.append(i)
    return res


'''24. Дан массив целых чисел nums. Определите, содержит ли он дубликаты. 
Верните True, если какое‑либо число встречается хотя бы дважды, иначе False.​'''
def solution(nums: list[int]) -> bool:
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False


'''25. Дан массив целых чисел nums. Подсчитайте частоту каждого элемента. 
Верните словарь, где ключи — элементы массива, а значения — количество их вхождений.​'''
def solution(nums: list[int]) -> dict[int, int]:
    freq: dict[int, int] = {}
    for x in nums:
        freq[x] = freq.get(x, 0) + 1
    return freq


'''26. Дан массив целых чисел nums и целое число target. Найдите индексы двух чисел, сумма которых равна target. 
Предполагается, что существует ровно одно решение; один и тот же элемент нельзя использовать дважды.​'''
def solution(nums: list[int], target: int) -> list[int]:
    pos = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in pos:
            return [pos[need], i]
        pos[x] = i
    return []  # по условию всегда есть решение


'''27. Дан массив строк strs. Сгруппируйте анаграммы вместе. Анаграммы — строки, которые содержат одинаковые буквы в разном порядке.​'''
def solution(strs: list[str]) -> list[list[str]]:
    groups: dict[tuple[int, ...], list[str]] = {}
    for s in strs:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - ord('a')] += 1
        key = tuple(cnt)
        groups.setdefault(key, []).append(s)
    return list(groups.values())


'''28. Дан отсортированный по возрастанию массив nums и число target. 
Найдите индекс элемента target в массиве. Если элемент не найден, верните −1.​'''
def solution(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


'''29. Дан отсортированный по возрастанию массив nums и число target. Найдите индекс, 
на котором должно располагаться число target, чтобы сохранить порядок сортировки. Если число уже есть в массиве, верните его индекс.​'''
def solution(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

'''30. Дан отсортированный по возрастанию массив nums, который был ротирован на некоторое количество позиций. 
Найдите индекс элемента target в этом массиве.​'''
def solution(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid

        if nums[lo] <= nums[mid]:
            # левая половина отсортирована
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            # правая половина отсортирована
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


'''31. Дан массив целых чисел nums и число k. Найдите k‑тый наименьший элемент массива (элемент, 
который был бы на позиции k−1 в отсортированном массиве).​'''
import random

def solution(nums: list[int], k: int) -> int:
    k -= 1  # делаем 0-индексацию

    def partition(l, r, pivot_index):
        pivot = nums[pivot_index]
        nums[pivot_index], nums[r] = nums[r], nums[pivot_index]
        store = l
        for i in range(l, r):
            if nums[i] < pivot:
                nums[store], nums[i] = nums[i], nums[store]
                store += 1
        nums[store], nums[r] = nums[r], nums[store]
        return store

    l, r = 0, len(nums) - 1
    while True:
        pivot_index = random.randint(l, r)
        p = partition(l, r, pivot_index)
        if p == k:
            return nums[p]
        if p < k:
            l = p + 1
        else:
            r = p - 1


'''32. Дан массив целых чисел nums. Отсортируйте его по возрастанию алгоритмом вставок и верните количество перестановок, 
выполненных в процессе сортировки.​'''
def solution(nums: list[int]) -> int:
    a = nums[:]  # если не нужно портить исходный
    swaps = 0
    for i in range(1, len(a)):
        j = i
        while j > 0 and a[j] < a[j - 1]:
            a[j], a[j - 1] = a[j - 1], a[j]
            swaps += 1
            j -= 1
    return swaps


'''33. Даны два отсортированных по возрастанию массива arr1 и arr2. Объедините их в один новый отсортированный массив.​'''
def solution(arr1: list[int], arr2: list[int]) -> list[int]:
    i = j = 0
    res = []
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            res.append(arr1[i])
            i += 1
        else:
            res.append(arr2[j])
            j += 1
    res.extend(arr1[i:])
    res.extend(arr2[j:])
    return res


'''34. Дан массив целых чисел nums. Отсортируйте его по возрастанию алгоритмом слияния (Merge Sort).​'''
def solution(nums: list[int]) -> list[int]:
    def merge_sort(a):
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        left = merge_sort(a[:mid])
        right = merge_sort(a[mid:])
        i = j = 0
        res = []
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                res.append(left[i])
                i += 1
            else:
                res.append(right[j])
                j += 1
        res.extend(left[i:])
        res.extend(right[j:])
        return res

    return merge_sort(nums)


'''35. Дан массив целых чисел nums. Отсортируйте его по возрастанию алгоритмом быстрой сортировки (Quick Sort).​'''
import random

def solution(nums: list[int]) -> list[int]:
    a = nums[:]

    def quicksort(l, r):
        if l >= r:
            return
        pivot_index = random.randint(l, r)
        pivot = a[pivot_index]
        a[pivot_index], a[r] = a[r], a[pivot_index]
        i = l
        for j in range(l, r):
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[r] = a[r], a[i]
        quicksort(l, i - 1)
        quicksort(i + 1, r)

    quicksort(0, len(a) - 1)
    return a


'''36. Дан массив целых чисел nums. Отсортируйте его по возрастанию алгоритмом пирамидальной сортировки (Heap Sort).​'''
def solution(nums: list[int]) -> list[int]:
    a = nums[:]
    n = len(a)

    def heapify(i, heap_size):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < heap_size and a[l] > a[largest]:
            largest = l
        if r < heap_size and a[r] > a[largest]:
            largest = r
        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            heapify(largest, heap_size)

    for i in range(n // 2 - 1, -1, -1):
        heapify(i, n)

    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        heapify(0, end)

    return a


'''37. Дан неориентированный граф, заданный списком рёбер edges. Постройте список смежности этого графа.​'''
def solution(n: int, edges: list[tuple[int, int]]) -> dict[int, list[int]]:
    g: dict[int, list[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)
    return g


'''38. Дан неориентированный граф, заданный списком рёбер edges. Постройте матрицу смежности этого графа.​'''
def solution(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj = [[0] * n for _ in range(n)]
    for u, v in edges:
        adj[u][v] = 1
        adj[v][u] = 1
    return adj


'''39. Дан неориентированный граф, заданный матрицей смежности adj. Постройте список рёбер этого графа.​'''
def solution(n: int, adj: list[list[int]]) -> list[tuple[int, int]]:
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if adj[i][j]:
                edges.append((i, j))
    return edges


'''40. Дан ориентированный граф, заданный списком рёбер edges. Постройте список смежности этого графа.​'''
def solution(n: int, edges: list[tuple[int, int]]) -> dict[int, list[int]]:
    g: dict[int, list[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        g[u].append(v)
    return g


'''41. Дан неориентированный взвешенный граф, заданный списком рёбер с весами. Постройте список смежности этого графа.​'''
def solution(n: int, edges: list[tuple[int, int, int]]) -> dict[int, list[tuple[int, int]]]:
    g: dict[int, list[tuple[int, int]]] = {i: [] for i in range(n)}
    for u, v, w in edges:
        g[u].append((v, w))
        g[v].append((u, w))
    return g


'''42. Дан неориентированный граф, заданный списком рёбер edges. Постройте матрицу инцидентности этого графа.​'''
def solution(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    m = len(edges)
    if m == 0:
        return []
    inc = [[0] * m for _ in range(n)]
    for idx, (u, v) in enumerate(edges):
        inc[u][idx] = 1
        inc[v][idx] = 1
    return inc


'''43. Дан неориентированный граф, заданный списком смежности graph, и стартовая вершина start. Выполните обход графа в глубину (DFS), 
верните порядок посещения вершин.​'''
def solution(graph: dict[int, list[int]], start: int) -> list[int]:
    visited = set()
    order = []

    def dfs(v: int):
        visited.add(v)
        order.append(v)
        for to in graph.get(v, []):
            if to not in visited:
                dfs(to)

    dfs(start)
    return order


'''44. Дан неориентированный граф, заданный списком смежности graph. 
Найдите все компоненты связности графа и верните список списков вершин по компонентам.​'''
def solution(graph: dict[int, list[int]], n: int) -> list[list[int]]:
    visited = [False] * n
    comps: list[list[int]] = []

    def dfs(v: int, cur: list[int]):
        visited[v] = True
        cur.append(v)
        for to in graph.get(v, []):
            if not visited[to]:
                dfs(to, cur)

    for v in range(n):
        if not visited[v]:
            cur = []
            dfs(v, cur)
            comps.append(cur)
    return comps


'''45. Дан ориентированный ациклический граф (DAG), заданный списком смежности graph. 
Выполните топологическую сортировку вершин и верните один из возможных порядков.​'''
def solution(graph: dict[int, list[int]], n: int) -> list[int]:
    visited = [0] * n  # 0 - не посещен, 1 - в стеке, 2 - завершен
    order = []

    def dfs(v: int):
        visited[v] = 1
        for to in graph.get(v, []):
            if visited[to] == 0:
                dfs(to)
        visited[v] = 2
        order.append(v)

    for v in range(n):
        if visited[v] == 0:
            dfs(v)
    order.reverse()
    return order


'''46. Дан ориентированный граф, заданный списком смежности graph. Определите, является ли граф ациклическим (не содержит циклов).​'''
def solution(graph: dict[int, list[int]], n: int) -> bool:
    color = [0] * n  # 0 - белый, 1 - серый, 2 - черный

    def dfs(v: int) -> bool:
        color[v] = 1
        for to in graph.get(v, []):
            if color[to] == 1:
                return False
            if color[to] == 0 and not dfs(to):
                return False
        color[v] = 2
        return True

    for v in range(n):
        if color[v] == 0:
            if not dfs(v):
                return False
    return True


'''47. Дан неориентированный граф, заданный списком смежности graph, и стартовая вершина start. 
Выполните обход графа в ширину (BFS), верните порядок посещения вершин.​'''
from collections import deque

def solution(graph: dict[int, list[int]], start: int) -> list[int]:
    visited = set([start])
    q = deque([start])
    order = []
    while q:
        v = q.popleft()
        order.append(v)
        for to in graph.get(v, []):
            if to not in visited:
                visited.add(to)
                q.append(to)
    return order


'''48. Дан неориентированный невзвешенный граф, заданный списком смежности graph, и две вершины start и end. 
Найдите кратчайший путь от start до end или верните пустой список, если пути нет.​'''
from collections import deque

def solution(graph: dict[int, list[int]], start: int, end: int) -> list[int]:
    q = deque([start])
    dist = {start: 0}
    parent = {start: -1}
    while q:
        v = q.popleft()
        if v == end:
            break
        for to in graph.get(v, []):
            if to not in dist:
                dist[to] = dist[v] + 1
                parent[to] = v
                q.append(to)

    if end not in dist:
        return []

    path = []
    cur = end
    while cur != -1:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


'''49. Реализуйте структуру данных DSU (Union‑Find) с сжатием путей и объединением по рангу, поддерживающую операции find и union.​'''
class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1


'''50. Дан неориентированный взвешенный граф, заданный списком рёбер edges. 
Найдите сумму весов рёбер минимального остовного дерева (алгоритм Краскала).​'''
def solution(n: int, edges: list[tuple[int, int, int]]) -> int:
    edges_sorted = sorted(edges, key=lambda x: x[2])

    class DSU:
        def __init__(self, n):
            self.parent = list(range(n))
            self.rank = [0] * n

        def find(self, x):
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]

        def union(self, x, y):
            rx, ry = self.find(x), self.find(y)
            if rx == ry:
                return False
            if self.rank[rx] < self.rank[ry]:
                rx, ry = ry, rx
            self.parent[ry] = rx
            if self.rank[rx] == self.rank[ry]:
                self.rank[rx] += 1
            return True

    dsu = DSU(n)
    total = 0
    for u, v, w in edges_sorted:
        if dsu.union(u, v):
            total += w
    return total


'''51. Дан неориентированный взвешенный граф, заданный списком смежности graph. 
Найдите сумму весов рёбер минимального остовного дерева алгоритмом Прима с приоритетной очередью.​'''
import heapq

def solution(n: int, graph: dict[int, list[tuple[int, int]]]) -> int:
    visited = [False] * n
    pq = [(0, 0)]  # (weight, vertex)
    total = 0
    used = 0

    while pq and used < n:
        w, v = heapq.heappop(pq)
        if visited[v]:
            continue
        visited[v] = True
        total += w
        used += 1
        for to, wt in graph.get(v, []):
            if not visited[to]:
                heapq.heappush(pq, (wt, to))
    return total


'''52. Дан ориентированный взвешенный граф с неотрицательными весами (список смежности graph) и стартовая вершина start. 
Найдите кратчайшие расстояния от start до всех вершин (Дейкстра).​'''
import heapq

def solution(n: int, graph: dict[int, list[tuple[int, int]]], start: int) -> list[int]:
    INF = 10**18
    dist = [INF] * n
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, v = heapq.heappop(pq)
        if d != dist[v]:
            continue
        for to, w in graph.get(v, []):
            nd = d + w
            if nd < dist[to]:
                dist[to] = nd
                heapq.heappush(pq, (nd, to))
    return dist


'''53. Дан ориентированный взвешенный граф (список рёбер edges) и стартовая вершина start. 
Найдите кратчайшие расстояния от start до всех вершин (Беллман‑Форд) или верните None, если достижим цикл отрицательного веса.​'''
def solution(n: int, edges: list[tuple[int, int, int]], start: int) -> list[int] | None:
    INF = 10**18
    dist = [INF] * n
    dist[start] = 0

    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break

    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return None
    return dist


'''54. Дан ориентированный взвешенный граф, заданный матрицей весов adj (adj[i][j] — вес ребра или inf). 
Найдите кратчайшие расстояния между всеми парами вершин (Флойд‑Уоршелл).​'''
def solution(adj: list[list[float]]) -> list[list[float]]:
    n = len(adj)
    dist = [row[:] for row in adj]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


'''55. Дан ориентированный взвешенный граф, заданный списком рёбер edges. Определите, содержит ли граф цикл отрицательного веса.​'''
def solution(n: int, edges: list[tuple[int, int, int]]) -> bool:
    INF = 10**18
    dist = [0] * n  # можно стартовать с 0 для всех

    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break

    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return True
    return False


'''56. Дано бинарное дерево. Выполните прямой обход (preorder: корень‑левый‑правый) и верните список значений узлов.​'''
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def solution(root: TreeNode) -> list[int]:
    res = []
    def dfs(node: TreeNode):
        if not node:
            return
        res.append(node.val)
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    return res


'''57. Дано бинарное дерево. Выполните центрированный обход (inorder: левый‑корень‑правый) и верните список значений узлов.​'''
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def solution(root: TreeNode) -> list[int]:
    res = []
    def dfs(node: TreeNode):
        if not node:
            return
        dfs(node.left)
        res.append(node.val)
        dfs(node.right)
    dfs(root)
    return res


'''58. Дано бинарное дерево. Выполните обратный обход (postorder: левый‑правый‑корень) и верните список значений узлов.​'''
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def solution(root: TreeNode) -> list[int]:
    res = []
    def dfs(node: TreeNode):
        if not node:
            return
        dfs(node.left)
        dfs(node.right)
        res.append(node.val)
    dfs(root)
    return res


'''59. Дано бинарное дерево. Выполните обход по уровням (BFS слева направо) и верните список значений узлов.​'''
from collections import deque

class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def solution(root: TreeNode) -> list[int]:
    if not root:
        return []
    res = []
    q = deque([root])
    while q:
        node = q.popleft()
        res.append(node.val)
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    return res


'''60. Дано бинарное дерево. Найдите его высоту (число узлов на самом длинном пути от корня до листа).​'''
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def solution(root: TreeNode) -> int:
    if not root:
        return 0
    return 1 + max(solution(root.left), solution(root.right))


'''61. Дано бинарное дерево. Найдите его ширину (максимальное количество узлов на одном уровне).​'''
from collections import deque

class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def solution(root: TreeNode) -> int:
    if not root:
        return 0
    q = deque([root])
    ans = 0
    while q:
        level_size = len(q)
        ans = max(ans, level_size)
        for _ in range(level_size):
            node = q.popleft()
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
    return ans


'''62. Дано бинарное дерево. Определите, является ли оно сбалансированным (разница высот левого и правого поддерева каждого узла не превышает 1).​'''
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def solution(root: TreeNode) -> bool:
    def dfs(node: TreeNode) -> int:
        if not node:
            return 0
        lh = dfs(node.left)
        if lh == -1:
            return -1
        rh = dfs(node.right)
        if rh == -1:
            return -1
        if abs(lh - rh) > 1:
            return -1
        return 1 + max(lh, rh)

    return dfs(root) != -1


'''63. Дано бинарное дерево. Определите, является ли оно бинарным деревом поиска (BST):
все значения в левом поддереве меньше значения узла, все в правом — больше.​'''
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def solution(root: TreeNode) -> bool:
    def dfs(node: TreeNode, low, high) -> bool:
        if not node:
            return True
        if not (low < node.val < high):
            return False
        return dfs(node.left, low, node.val) and dfs(node.right, node.val, high)

    return dfs(root, float("-inf"), float("inf"))


'''64. Дано бинарное дерево поиска и значение target. Найдите узел с этим значением, верните True, если найден, иначе False.​'''
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def solution(root: TreeNode, target: int) -> bool:
    node = root
    while node:
        if node.val == target:
            return True
        if target < node.val:
            node = node.left
        else:
            node = node.right
    return False


'''65. Дано бинарное дерево. Найдите количество тупиковых узлов (листьев, то есть узлов без потомков).​'''
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def solution(root: TreeNode) -> int:
    if not root:
        return 0
    if not root.left and not root.right:
        return 1
    return solution(root.left) + solution(root.right)


'''66. Дан треп (список пар (ключ, приоритет)) и значение ключа x. 
Разделите треп на два: с ключами < x и с ключами ≥ x; верните оба списка ключей.​'''
def solution(treap: list[tuple[int, int]], x: int) -> tuple[list[int], list[int]]:
    left_keys = []
    right_keys = []
    for key, pr in treap:
        if key < x:
            left_keys.append(key)
        else:
            right_keys.append(key)
    left_keys.sort()
    right_keys.sort()
    return left_keys, right_keys


'''67. Даны два трепа left и right, где все ключи в left меньше всех ключей в right. Объедините их в один треп и верните список ключей.​'''
def solution(left: list[tuple[int, int]], right: list[tuple[int, int]]) -> list[int]:
    keys = [k for k, _ in left] + [k for k, _ in right]
    keys.sort()
    return keys


'''68. Дан треп и новый элемент (ключ, приоритет). Вставьте элемент в треп с сохранением свойств и верните список ключей после вставки.​'''
def solution(treap: list[tuple[int, int]], new_key: int, new_priority: int) -> list[int]:
    keys = [k for k, _ in treap]
    keys.append(new_key)
    keys.sort()
    return keys


'''69. Дан список интервалов времени (start, end). Найдите максимальное количество непересекающихся интервалов.​'''
def solution(intervals: list[tuple[int, int]]) -> int:
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[1])
    count = 0
    last_end = -1  # или intervals[0][0], но -1 безопасен при start >= 0

    for start, end in intervals:
        if start >= last_end:
            count += 1
            last_end = end

    return count


'''70. Даны частоты символов. Постройте коды Хаффмана и верните словарь индекс → код.​'''
import heapq

def solution(freqs: list[int]) -> dict[int, str]:
    if not freqs:
        return {}

    heap = []
    for i, f in enumerate(freqs):
        heap.append((f, i, None, None))
    heapq.heapify(heap)

    if len(heap) == 1:
        f, idx, _, _ = heap[0]
        return {idx: "0"}

    node_id = len(freqs)

    while len(heap) > 1:
        f1, id1, left1, right1 = heapq.heappop(heap)
        f2, id2, left2, right2 = heapq.heappop(heap)
        merged = (f1 + f2, node_id, (f1, id1, left1, right1), (f2, id2, left2, right2))
        node_id += 1
        heapq.heappush(heap, merged)

    _, _, left, right = heap[0]
    codes: dict[int, str] = {}

    def dfs(node, code: str):
        if node is None:
            return
        f, idx, l, r = node
        if l is None and r is None:
            codes[idx] = code
            return
        dfs(l, code + "0")
        dfs(r, code + "1")

    dfs(left, "0")
    dfs(right, "1")
    return codes


'''71. Даны n кабелей разной длины. За один шаг можно соединить любые два кабеля, стоимость равна сумме их длин. 
Найдите минимальную суммарную стоимость объединения всех кабелей в один. (Дальнейшее условие на странице обрывается.)​'''
import heapq

def solution(ropes: list[int]) -> int:
    if len(ropes) <= 1:
        return 0

    heapq.heapify(ropes)
    total = 0

    while len(ropes) > 1:
        a = heapq.heappop(ropes)
        b = heapq.heappop(ropes)
        cost = a + b
        total += cost
        heapq.heappush(ropes, cost)

    return total


'''72. Дано целое число n. Найдите n-е число Фибоначчи. Числа Фибоначчи определяются как: F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2).'''
def solution(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


'''73. Дано количество ступенек n. Мячик может прыгать на 1, 2 или 3 ступеньки вниз. 
Найдите количество всех возможных маршрутов с вершины на землю.'''
def solution(n: int) -> int:
    if n == 0:
        return 1  # одна пустая траектория
    if n == 1:
        return 1
    if n == 2:
        return 2
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1
    dp[2] = 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2] + dp[i - 3]
    return dp[n]


'''74. Даны n предметов с весами и стоимостями, а также вместимость рюкзака.
Найдите максимальную стоимость предметов, которую можно поместить в рюкзак. Каждый предмет можно взять либо целиком, либо не взять.'''
def solution(weights: list[int], values: list[int], capacity: int) -> int:
    n = len(weights)
    dp = [0] * (capacity + 1)
    for i in range(n):
        w = weights[i]
        v = values[i]
        for c in range(capacity, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]


'''75. Даны две строки s1 и s2. Найдите длину их наибольшей общей подпоследовательности. 
Общая подпоследовательность — это последовательность, которая встречается в обеих строках в том же порядке (но не обязательно подряд).'''
def solution(s1: str, s2: str) -> int:
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][m]


'''76. Даны две строки s1 и s2. Найдите расстояние Левенштейна между ними. 
Расстояние Левенштейна — это минимальное количество операций (вставка, удаление, замена символа) для превращения одной строки в другую.'''
def solution(s1: str, s2: str) -> int:
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # удаление
                dp[i][j - 1] + 1,      # вставка
                dp[i - 1][j - 1] + cost  # замена / совпадение
            )
    return dp[n][m]


'''77. Дан массив целых чисел. Найдите длину наибольшей возрастающей подпоследовательности. 
Возрастающая подпоследовательность — это последовательность, где каждый элемент строго больше предыдущего.'''
def solution(nums: list[int]) -> int:
    if not nums:
        return 0
    import bisect

    tail = []  # tail[k] — минимальный возможный последний элемент возрастающей подпоследовательности длины k+1
    for x in nums:
        i = bisect.bisect_left(tail, x)
        if i == len(tail):
            tail.append(x)
        else:
            tail[i] = x
    return len(tail)


'''78. Дан массив и список запросов, где каждый запрос — это пара (l, r). Для каждого запроса найдите минимум на диапазоне [l, r].'''
def solution(nums: list[int], queries: list[tuple[int, int]]) -> list[int]:
    n = len(nums)
    tree = [0] * (4 * n)
    def build(v, tl, tr):
        if tl == tr:
            tree[v] = nums[tl]
        else:
            tm = (tl + tr) // 2
            build(2 * v, tl, tm)
            build(2 * v + 1, tm + 1, tr)
            tree[v] = min(tree[2 * v], tree[2 * v + 1])
    def query(v, tl, tr, l, r):
        if l > r:
            return float('inf')
        if l == tl and r == tr:
            return tree[v]
        tm = (tl + tr) // 2
        return min(query(2 * v, tl, tm, l, min(r, tm)),
                   query(2 * v + 1, tm + 1, tr, max(l, tm + 1), r))
    build(1, 0, n - 1)
    results = []
    for l, r in queries:
        results.append(query(1, 0, n - 1, l, r))
    return results


'''79. Дан неориентированный граф, заданный списком смежности. Найдите все мосты графа.
Мост — это ребро, удаление которого увеличивает количество компонент связности.'''
def solution(graph: dict[int, list[int]], n: int) -> list[tuple[int, int]]:
    tin = [-1] * n
    low = [-1] * n
    bridges = []
    timer = 0
    def dfs(v, p=-1):
        nonlocal timer
        tin[v] = low[v] = timer
        timer += 1
        for to in graph.get(v, []):
            if to == p: continue
            if tin[to] != -1:
                low[v] = min(low[v], tin[to])
            else:
                dfs(to, v)
                low[v] = min(low[v], low[to])
                if low[to] > tin[v]:
                    bridges.append(tuple(sorted((v, to))))
    for i in range(n):
        if tin[i] == -1:
            dfs(i)
    return bridges