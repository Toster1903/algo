from __future__ import annotations

import copy
import multiprocessing as mp
import os
import random
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).parent
REFERENCE_FILE = BASE_DIR / "zach.py"

CLASS_TASKS: dict[int, str] = {
    16: "BrowserHistory",
    19: "Stack",
    20: "Queue",
    21: "MinStack",
    49: "DSU",
}

app = Flask(__name__)


class Node:
    def __init__(self, val: int = 0, next: Any = None):
        self.val = val
        self.next = next


class Tree:
    def __init__(self, val: int, left: Any = None, right: Any = None):
        self.val = val
        self.left = left
        self.right = right


@dataclass
class TaskMeta:
    task_id: int
    title: str
    signature: str
    description: str
    task_kind: str
    entry_name: str
    time_limit_ms: float = 40.0


def parse_reference_blocks(file_path: Path) -> dict[int, dict[str, str]]:
    source = file_path.read_text(encoding="utf-8")
    pattern = re.compile(r"'''(\d+)\.\s*(.*?)'''", re.DOTALL)
    matches = list(pattern.finditer(source))
    blocks: dict[int, dict[str, str]] = {}
    for i, match in enumerate(matches):
        task_id = int(match.group(1))
        desc = match.group(2).strip()
        code_start = match.end()
        code_end = matches[i + 1].start() if i + 1 < len(matches) else len(source)
        code = source[code_start:code_end].strip()
        if code:
            blocks[task_id] = {"description": desc, "code": code}
    return blocks


REFERENCE_BLOCKS = parse_reference_blocks(REFERENCE_FILE)


def random_string(min_len: int = 0, max_len: int = 20, alphabet: str = "abcdefghijklmnopqrstuvwxyz") -> str:
    n = random.randint(min_len, max_len)
    return "".join(random.choice(alphabet) for _ in range(n))


def build_list(values: list[int], cycle_at: int = -1) -> Node | None:
    if not values:
        return None
    nodes = [Node(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if 0 <= cycle_at < len(nodes):
        nodes[-1].next = nodes[cycle_at]
    return nodes[0]


def list_to_py(head: Any, limit: int = 1000) -> list[int]:
    out: list[int] = []
    seen = set()
    cur = head
    steps = 0
    while cur is not None and steps < limit:
        if id(cur) in seen:
            out.append("<cycle>")
            break
        seen.add(id(cur))
        out.append(getattr(cur, "val", None))
        cur = getattr(cur, "next", None)
        steps += 1
    return out


def build_tree(values: list[int | None]) -> Tree | None:
    if not values:
        return None
    nodes = [None if v is None else Tree(v) for v in values]
    kids = nodes[::-1]
    root = kids.pop()
    for node in nodes:
        if node is not None:
            if kids:
                node.left = kids.pop()
            if kids:
                node.right = kids.pop()
    return root


def make_undirected_graph(n: int, edge_prob: float = 0.2) -> dict[int, list[int]]:
    g = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < edge_prob:
                g[i].append(j)
                g[j].append(i)
    return g


def make_directed_graph(n: int, edge_prob: float = 0.2, dag: bool = False) -> dict[int, list[int]]:
    g = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if dag and i >= j:
                continue
            if random.random() < edge_prob:
                g[i].append(j)
    return g


def to_edge_list(g: dict[int, list[int]], undirected: bool = True) -> list[tuple[int, int]]:
    edges: list[tuple[int, int]] = []
    seen = set()
    for u, arr in g.items():
        for v in arr:
            if undirected:
                key = tuple(sorted((u, v)))
                if key not in seen:
                    seen.add(key)
                    edges.append((key[0], key[1]))
            else:
                edges.append((u, v))
    return edges


def make_weighted_edges(n: int, undirected: bool = True, allow_negative: bool = False) -> list[tuple[int, int, int]]:
    edges: list[tuple[int, int, int]] = []
    seen = set()
    prob = min(0.35, 4.0 / max(n, 1))
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if undirected and i >= j:
                continue
            if random.random() < prob:
                lo = -15 if allow_negative else 1
                hi = 20
                w = random.randint(lo, hi)
                if undirected:
                    key = (i, j)
                    if key not in seen:
                        seen.add(key)
                        edges.append((i, j, w))
                else:
                    edges.append((i, j, w))
    return edges


def gen_case(task_id: int) -> tuple[tuple[Any, ...], dict[str, Any]]:
    if task_id == 1:
        return (random.randint(1, 10**6), random.randint(1, 10**6)), {}
    if task_id == 2:
        return (random.randint(1, 10**6),), {}
    if task_id == 3:
        return (random.randint(1, 10**5), random.randint(1, 10**5)), {}
    if task_id == 4:
        return (random.randint(1, 260),), {}
    if task_id in {5, 6}:
        return (random_string(1, 120),), {}
    if task_id == 7:
        a = random_string(1, 40)
        k = random.randint(0, len(a) - 1)
        b = a[k:] + a[:k] if random.random() < 0.7 else random_string(len(a), len(a))
        return (a, b), {}
    if task_id == 8:
        return (random_string(1, 80, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"),), {}
    if task_id == 9:
        return (random_string(1, 130), random_string(0, 12)), {}
    if task_id == 10:
        base = random_string(1, 8)
        s = base * random.randint(1, 20) if random.random() < 0.7 else random_string(1, 120)
        return (s,), {}
    if task_id == 11:
        return (random_string(0, 40),), {}
    if task_id == 12:
        return (random_string(0, 120, alphabet="()"),), {}
    if task_id == 13:
        return (build_list([random.randint(-20, 20) for _ in range(random.randint(0, 40))]),), {}
    if task_id == 14:
        n = random.randint(0, 50)
        values = [random.randint(0, 20) for _ in range(n)]
        cycle = random.randint(0, n - 1) if n and random.random() < 0.35 else -1
        return (build_list(values, cycle_at=cycle),), {}
    if task_id == 15:
        a = sorted([random.randint(-80, 80) for _ in range(random.randint(0, 40))])
        b = sorted([random.randint(-80, 80) for _ in range(random.randint(0, 40))])
        return (build_list(a), build_list(b)), {}
    if task_id == 17:
        vals = [random.randint(0, 9) for _ in range(random.randint(0, 35))]
        if random.random() < 0.45:
            vals = vals[: len(vals) // 2] + vals[: len(vals) // 2][::-1]
        return (build_list(vals),), {}
    if task_id == 18:
        return (random_string(0, 120, alphabet="(){}[]"),), {}
    if task_id == 22:
        n, m = random.randint(1, 12), random.randint(1, 12)
        image = [[random.randint(0, 4) for _ in range(m)] for _ in range(n)]
        sr, sc = random.randint(0, n - 1), random.randint(0, m - 1)
        return (image, sr, sc, random.randint(0, 4)), {}
    if task_id in {23, 24, 25, 32, 34, 35, 36, 77}:
        n = random.randint(0, 260)
        return ([random.randint(-1000, 1000) for _ in range(n)],), {}
    if task_id == 26:
        n = random.randint(2, 130)
        nums = [random.randint(-250, 250) for _ in range(n)]
        i, j = random.sample(range(n), 2)
        return (nums, nums[i] + nums[j]), {}
    if task_id == 27:
        n = random.randint(1, 70)
        arr = [random_string(0, 10) for _ in range(n)]
        return (arr,), {}
    if task_id in {28, 29}:
        n = random.randint(0, 300)
        nums = sorted(random.sample(range(-3000, 3001), n)) if n <= 6001 else []
        return (nums, random.randint(-3300, 3300)), {}
    if task_id == 30:
        n = random.randint(1, 300)
        base = sorted(random.sample(range(-4000, 4001), n))
        shift = random.randint(0, n - 1)
        return (base[shift:] + base[:shift], random.randint(-4500, 4500)), {}
    if task_id == 31:
        n = random.randint(1, 220)
        nums = [random.randint(-2000, 2000) for _ in range(n)]
        return (nums, random.randint(1, n)), {}
    if task_id == 33:
        a = sorted([random.randint(-300, 300) for _ in range(random.randint(0, 140))])
        b = sorted([random.randint(-300, 300) for _ in range(random.randint(0, 140))])
        return (a, b), {}
    if task_id in {37, 38, 42}:
        n = random.randint(1, 40)
        g = make_undirected_graph(n, edge_prob=min(0.25, 5.0 / n))
        return (n, to_edge_list(g, undirected=True)), {}
    if task_id == 39:
        n = random.randint(1, 30)
        g = make_undirected_graph(n, edge_prob=min(0.25, 5.0 / n))
        adj = [[0] * n for _ in range(n)]
        for u, v in to_edge_list(g, undirected=True):
            adj[u][v] = 1
            adj[v][u] = 1
        return (n, adj), {}
    if task_id == 40:
        n = random.randint(1, 40)
        g = make_directed_graph(n, edge_prob=min(0.2, 4.0 / n), dag=False)
        return (n, to_edge_list(g, undirected=False)), {}
    if task_id == 41:
        n = random.randint(1, 40)
        return (n, make_weighted_edges(n, undirected=True, allow_negative=False)), {}
    if task_id == 43:
        n = random.randint(1, 45)
        g = make_undirected_graph(n, edge_prob=min(0.2, 4.0 / n))
        return (g, random.randint(0, n - 1)), {}
    if task_id == 44:
        n = random.randint(1, 45)
        g = make_undirected_graph(n, edge_prob=min(0.2, 4.0 / n))
        return (g, n), {}
    if task_id == 45:
        n = random.randint(1, 45)
        g = make_directed_graph(n, edge_prob=min(0.2, 4.0 / n), dag=True)
        return (g, n), {}
    if task_id == 46:
        n = random.randint(1, 45)
        g = make_directed_graph(n, edge_prob=min(0.2, 4.0 / n), dag=False)
        return (g, n), {}
    if task_id == 47:
        n = random.randint(1, 45)
        g = make_undirected_graph(n, edge_prob=min(0.2, 4.0 / n))
        return (g, random.randint(0, n - 1)), {}
    if task_id == 48:
        n = random.randint(1, 45)
        g = make_undirected_graph(n, edge_prob=min(0.2, 4.0 / n))
        return (g, random.randint(0, n - 1), random.randint(0, n - 1)), {}
    if task_id == 50:
        n = random.randint(1, 45)
        edges = make_weighted_edges(n, undirected=True, allow_negative=False)
        return (n, edges), {}
    if task_id == 51:
        n = random.randint(1, 45)
        edges = make_weighted_edges(n, undirected=True, allow_negative=False)
        graph = {i: [] for i in range(n)}
        for u, v, w in edges:
            graph[u].append((v, w))
            graph[v].append((u, w))
        return (n, graph), {}
    if task_id == 52:
        n = random.randint(1, 45)
        edges = make_weighted_edges(n, undirected=False, allow_negative=False)
        graph = {i: [] for i in range(n)}
        for u, v, w in edges:
            graph[u].append((v, w))
        return (n, graph, random.randint(0, n - 1)), {}
    if task_id == 53:
        n = random.randint(1, 35)
        edges = make_weighted_edges(n, undirected=False, allow_negative=True)
        return (n, edges, random.randint(0, n - 1)), {}
    if task_id == 54:
        n = random.randint(1, 28)
        inf = float("inf")
        adj = [[inf] * n for _ in range(n)]
        for i in range(n):
            adj[i][i] = 0.0
        for i in range(n):
            for j in range(n):
                if i != j and random.random() < min(0.25, 5.0 / n):
                    adj[i][j] = float(random.randint(1, 30))
        return (adj,), {}
    if task_id == 55:
        n = random.randint(1, 40)
        edges = make_weighted_edges(n, undirected=False, allow_negative=True)
        return (n, edges), {}
    if task_id in {56, 57, 58, 59, 60, 61, 62, 63, 65}:
        size = random.randint(0, 63)
        vals: list[int | None] = []
        for i in range(size):
            vals.append(None if i > 0 and random.random() < 0.25 else random.randint(-40, 40))
        if vals and vals[0] is None:
            vals[0] = random.randint(-5, 5)
        return (build_tree(vals),), {}
    if task_id == 64:
        values = sorted(set(random.randint(-100, 100) for _ in range(random.randint(1, 50))))

        def build_bst(arr: list[int]) -> Tree | None:
            if not arr:
                return None
            mid = len(arr) // 2
            root = Tree(arr[mid])
            root.left = build_bst(arr[:mid])
            root.right = build_bst(arr[mid + 1 :])
            return root

        root = build_bst(values)
        return (root, random.randint(-110, 110)), {}
    if task_id == 66:
        n = random.randint(0, 60)
        keys = random.sample(range(-150, 151), n)
        treap = [(k, random.randint(1, 1000)) for k in keys]
        return (treap, random.randint(-160, 160)), {}
    if task_id == 67:
        n1 = random.randint(0, 40)
        n2 = random.randint(0, 40)
        left_keys = random.sample(range(-300, -1), n1)
        right_keys = random.sample(range(1, 300), n2)
        left = [(k, random.randint(1, 1000)) for k in left_keys]
        right = [(k, random.randint(1, 1000)) for k in right_keys]
        return (left, right), {}
    if task_id == 68:
        n = random.randint(0, 60)
        keys = random.sample(range(-180, 181), n)
        treap = [(k, random.randint(1, 1000)) for k in keys]
        return (treap, random.randint(-200, 200), random.randint(1, 1000)), {}
    if task_id == 69:
        n = random.randint(0, 120)
        intervals = []
        for _ in range(n):
            a = random.randint(0, 200)
            b = random.randint(a, a + random.randint(0, 30))
            intervals.append((a, b))
        return (intervals,), {}
    if task_id == 70:
        n = random.randint(1, 40)
        freqs = [random.randint(0, 50) for _ in range(n)]
        if sum(freqs) == 0:
            freqs[random.randint(0, n - 1)] = 1
        return (freqs,), {}
    if task_id == 71:
        return ([random.randint(1, 1000) for _ in range(random.randint(0, 120))],), {}
    if task_id == 72:
        return (random.randint(0, 2000),), {}
    if task_id == 73:
        return (random.randint(0, 200),), {}
    if task_id == 74:
        n = random.randint(1, 60)
        weights = [random.randint(1, 30) for _ in range(n)]
        values = [random.randint(1, 80) for _ in range(n)]
        cap = random.randint(1, 200)
        return (weights, values, cap), {}
    if task_id in {75, 76}:
        return (random_string(0, 60), random_string(0, 60)), {}
    if task_id == 78:
        n = random.randint(1, 260)
        nums = [random.randint(-1000, 1000) for _ in range(n)]
        q = random.randint(1, 160)
        queries = []
        for _ in range(q):
            l = random.randint(0, n - 1)
            r = random.randint(l, n - 1)
            queries.append((l, r))
        return (nums, queries), {}
    if task_id == 79:
        n = random.randint(1, 45)
        g = make_undirected_graph(n, edge_prob=min(0.2, 4.0 / n))
        return (g, n), {}
    raise ValueError(f"Неизвестный task_id: {task_id}")


def custom_oracle_29(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


CUSTOM_ORACLES: dict[int, Callable[..., Any]] = {29: custom_oracle_29}


def build_tasks() -> dict[int, TaskMeta]:
    tasks: dict[int, TaskMeta] = {}
    for task_id in sorted(REFERENCE_BLOCKS):
        block = REFERENCE_BLOCKS[task_id]
        ns: dict[str, Any] = {}
        try:
            exec(block["code"], ns, ns)
        except Exception:
            continue
        title = block["description"].splitlines()[0].strip()

        if callable(ns.get("solution")):
            import inspect

            sig = f"solution{inspect.signature(ns['solution'])}"
            tasks[task_id] = TaskMeta(task_id, title, sig, block["description"], "function", "solution")
            continue

        class_name = CLASS_TASKS.get(task_id)
        if class_name and class_name in ns and isinstance(ns[class_name], type):
            tasks[task_id] = TaskMeta(
                task_id,
                title,
                f"class {class_name}(...)",
                block["description"],
                "class",
                class_name,
                80.0,
            )
    return tasks


TASKS = build_tasks()


def serialize_value(value: Any, depth: int = 0) -> Any:
    if depth > 4:
        return "<...>"
    if value is None or isinstance(value, (int, float, bool, str)):
        return value
    if isinstance(value, list):
        return [serialize_value(x, depth + 1) for x in value[:60]]
    if isinstance(value, tuple):
        return [serialize_value(x, depth + 1) for x in value[:60]]
    if isinstance(value, dict):
        out = {}
        count = 0
        for k, v in value.items():
            out[str(serialize_value(k, depth + 1))] = serialize_value(v, depth + 1)
            count += 1
            if count >= 60:
                break
        return out
    if hasattr(value, "val") and hasattr(value, "next"):
        return {"linked_list": list_to_py(value)}
    if hasattr(value, "val") and (hasattr(value, "left") or hasattr(value, "right")):
        return {"tree_root": getattr(value, "val", None)}
    return repr(value)


def normalize_grouped_anagrams(value: Any) -> Any:
    return sorted(sorted(group) for group in value)


def normalize_components(value: Any) -> Any:
    return sorted(sorted(comp) for comp in value)


def normalize_edges(value: Any) -> Any:
    return sorted(tuple(sorted(e)) for e in value)


def validate_topological_order(order: Any, graph: dict[int, list[int]], n: int) -> bool:
    if not isinstance(order, list) or len(order) != n:
        return False
    if set(order) != set(range(n)):
        return False
    pos = {v: i for i, v in enumerate(order)}
    for u, arr in graph.items():
        for v in arr:
            if pos[u] > pos[v]:
                return False
    return True


def shortest_dist(graph: dict[int, list[int]], start: int, end: int) -> int:
    from collections import deque

    q = deque([start])
    dist = {start: 0}
    while q:
        v = q.popleft()
        if v == end:
            return dist[v]
        for to in graph.get(v, []):
            if to not in dist:
                dist[to] = dist[v] + 1
                q.append(to)
    return -1


def validate_path(graph: dict[int, list[int]], start: int, end: int, path: Any) -> bool:
    d = shortest_dist(graph, start, end)
    if d == -1:
        return path == []
    if not isinstance(path, list) or len(path) != d + 1:
        return False
    if path[0] != start or path[-1] != end:
        return False
    for i in range(len(path) - 1):
        if path[i + 1] not in graph.get(path[i], []):
            return False
    return True


def is_prefix_free(code_map: dict[int, str]) -> bool:
    codes = list(code_map.values())
    for i in range(len(codes)):
        for j in range(len(codes)):
            if i != j and codes[j].startswith(codes[i]):
                return False
    return True


def huffman_cost(freqs: list[int], codes: dict[int, str]) -> int:
    total = 0
    for i, f in enumerate(freqs):
        if i not in codes:
            return 10**18
        total += f * len(codes[i])
    return total


def compare_answer(task_id: int, args: tuple[Any, ...], expected: Any, got: Any) -> bool:
    if task_id == 13:
        return list_to_py(got) == list_to_py(expected)
    if task_id == 15:
        return list_to_py(got) == list_to_py(expected)
    if task_id == 26:
        if not isinstance(got, list) or len(got) != 2:
            return False
        i, j = got
        nums, target = args
        if not isinstance(i, int) or not isinstance(j, int) or i == j:
            return False
        if not (0 <= i < len(nums) and 0 <= j < len(nums)):
            return False
        return nums[i] + nums[j] == target
    if task_id == 27:
        return normalize_grouped_anagrams(got) == normalize_grouped_anagrams(expected)
    if task_id == 39:
        return normalize_edges(got) == normalize_edges(expected)
    if task_id == 44:
        return normalize_components(got) == normalize_components(expected)
    if task_id == 45:
        graph, n = args
        return validate_topological_order(got, graph, n)
    if task_id == 48:
        graph, start, end = args
        return validate_path(graph, start, end, got)
    if task_id == 70:
        if not isinstance(got, dict):
            return False
        try:
            got_map = {int(k): str(v) for k, v in got.items()}
        except Exception:
            return False
        freqs = args[0]
        if set(got_map.keys()) != set(range(len(freqs))):
            return False
        if not is_prefix_free(got_map):
            return False
        expected_cost = huffman_cost(freqs, expected)
        got_cost = huffman_cost(freqs, got_map)
        return got_cost == expected_cost
    if task_id == 79:
        return normalize_edges(got) == normalize_edges(expected)
    return got == expected


def class_scenario(task_id: int) -> dict[str, Any]:
    if task_id == 16:
        homepage = f"site-{random.randint(1, 9)}"
        ops: list[tuple[str, Any]] = []
        for _ in range(random.randint(20, 80)):
            r = random.random()
            if r < 0.4:
                ops.append(("visit", f"u{random.randint(1, 400)}"))
            elif r < 0.7:
                ops.append(("back", random.randint(1, 7)))
            else:
                ops.append(("forward", random.randint(1, 7)))
        return {"init": (homepage,), "ops": ops}
    if task_id == 19:
        ops = []
        size = 0
        for _ in range(random.randint(20, 120)):
            if size == 0 or random.random() < 0.55:
                ops.append(("push", random.randint(-200, 200)))
                size += 1
            else:
                r = random.random()
                if r < 0.34:
                    ops.append(("pop",))
                    size -= 1
                elif r < 0.67:
                    ops.append(("peek",))
                else:
                    ops.append(("is_empty",))
        return {"init": (), "ops": ops}
    if task_id == 20:
        ops = []
        size = 0
        for _ in range(random.randint(20, 120)):
            if size == 0 or random.random() < 0.55:
                ops.append(("enqueue", random.randint(-200, 200)))
                size += 1
            else:
                r = random.random()
                if r < 0.34:
                    ops.append(("dequeue",))
                    size -= 1
                elif r < 0.67:
                    ops.append(("front",))
                else:
                    ops.append(("is_empty",))
        return {"init": (), "ops": ops}
    if task_id == 21:
        ops = []
        size = 0
        for _ in range(random.randint(20, 120)):
            if size == 0 or random.random() < 0.58:
                ops.append(("push", random.randint(-300, 300)))
                size += 1
            else:
                if random.random() < 0.5:
                    ops.append(("pop",))
                    size -= 1
                else:
                    ops.append(("get_min",))
        return {"init": (), "ops": ops}
    if task_id == 49:
        n = random.randint(2, 120)
        ops = []
        for _ in range(random.randint(40, 220)):
            if random.random() < 0.6:
                ops.append(("union", random.randint(0, n - 1), random.randint(0, n - 1)))
            else:
                ops.append(("find", random.randint(0, n - 1)))
        return {"init": (n,), "ops": ops}
    raise ValueError(f"Нет сценария для class task {task_id}")


def run_class_ops(obj: Any, scenario: dict[str, Any]) -> list[Any]:
    out = []
    for op in scenario["ops"]:
        name = op[0]
        args = op[1:]
        method = getattr(obj, name)
        val = method(*args)
        out.append(val)
    return out


def eval_function_task(task: TaskMeta, ref_callable: Callable[..., Any], cand_callable: Callable[..., Any], rounds: int) -> dict[str, Any]:
    times: list[float] = []
    for idx in range(rounds):
        args, _ = gen_case(task.task_id)
        ref_args = copy.deepcopy(args)
        cand_args = copy.deepcopy(args)

        try:
            expected = ref_callable(*ref_args)
        except Exception as exc:
            return {"ok": False, "error": f"Ошибка эталона на тесте {idx + 1}: {exc}"}

        start = time.perf_counter()
        try:
            got = cand_callable(*cand_args)
        except Exception as exc:
            return {
                "ok": False,
                "error": f"Решение упало на тесте {idx + 1}: {exc}",
                "sample": {"args": serialize_value(args), "expected": serialize_value(expected)},
            }
        dt_ms = (time.perf_counter() - start) * 1000.0
        times.append(dt_ms)

        if dt_ms > task.time_limit_ms:
            return {
                "ok": False,
                "error": f"Превышен лимит времени на тесте {idx + 1}: {dt_ms:.3f} ms",
                "sample": {
                    "args": serialize_value(args),
                    "expected": serialize_value(expected),
                    "got": serialize_value(got),
                },
            }

        if not compare_answer(task.task_id, args, expected, got):
            return {
                "ok": False,
                "error": f"Неверный ответ на тесте {idx + 1}",
                "sample": {
                    "args": serialize_value(args),
                    "expected": serialize_value(expected),
                    "got": serialize_value(got),
                },
            }

    return {
        "ok": True,
        "rounds": rounds,
        "timing": {
            "avg_ms": round(sum(times) / len(times), 3),
            "max_ms": round(max(times), 3),
            "min_ms": round(min(times), 3),
            "limit_ms": task.time_limit_ms,
        },
    }


def eval_class_task(task: TaskMeta, ref_class: type, user_class: type, rounds: int) -> dict[str, Any]:
    times: list[float] = []
    for idx in range(rounds):
        sc = class_scenario(task.task_id)
        try:
            ref_obj = ref_class(*sc["init"])
            expected = run_class_ops(ref_obj, sc)
        except Exception as exc:
            return {"ok": False, "error": f"Ошибка эталона на сценарии {idx + 1}: {exc}"}

        try:
            user_obj = user_class(*copy.deepcopy(sc["init"]))
        except Exception as exc:
            return {"ok": False, "error": f"Ошибка конструктора на сценарии {idx + 1}: {exc}"}

        start = time.perf_counter()
        try:
            got = run_class_ops(user_obj, copy.deepcopy(sc))
        except Exception as exc:
            return {
                "ok": False,
                "error": f"Ошибка при операциях класса на сценарии {idx + 1}: {exc}",
                "sample": serialize_value(sc),
            }
        dt_ms = (time.perf_counter() - start) * 1000.0
        times.append(dt_ms)

        if dt_ms > task.time_limit_ms:
            return {
                "ok": False,
                "error": f"Превышен лимит времени на сценарии {idx + 1}: {dt_ms:.3f} ms",
                "sample": serialize_value(sc),
            }

        if got != expected:
            return {
                "ok": False,
                "error": f"Неверное поведение класса на сценарии {idx + 1}",
                "sample": {
                    "scenario": serialize_value(sc),
                    "expected": serialize_value(expected),
                    "got": serialize_value(got),
                },
            }

    return {
        "ok": True,
        "rounds": rounds,
        "timing": {
            "avg_ms": round(sum(times) / len(times), 3),
            "max_ms": round(max(times), 3),
            "min_ms": round(min(times), 3),
            "limit_ms": task.time_limit_ms,
        },
    }


def eval_submission(payload: dict[str, Any]) -> dict[str, Any]:
    task_id = int(payload["task_id"])
    user_code = payload["code"]
    rounds = int(payload.get("rounds", 60))
    rounds = max(5, min(rounds, 250))

    task = TASKS.get(task_id)
    if task is None:
        return {"ok": False, "error": "Эта задача не найдена."}

    if task.task_kind == "function" and "def solution" not in user_code:
        return {"ok": False, "error": "В коде должна быть функция solution(...)."}
    if task.task_kind == "class" and f"class {task.entry_name}" not in user_code:
        return {"ok": False, "error": f"В коде должен быть класс {task.entry_name}."}

    ref_ns: dict[str, Any] = {}
    exec(REFERENCE_BLOCKS[task_id]["code"], ref_ns, ref_ns)

    user_ns: dict[str, Any] = {}
    try:
        exec(user_code, user_ns, user_ns)
    except Exception as exc:
        return {"ok": False, "error": f"Ошибка в коде: {exc}"}

    if task.task_kind == "function":
        ref_callable = CUSTOM_ORACLES.get(task_id, ref_ns.get(task.entry_name))
        cand_callable = user_ns.get(task.entry_name)
        if not callable(cand_callable):
            return {"ok": False, "error": "Функция solution не найдена после выполнения кода."}
        return eval_function_task(task, ref_callable, cand_callable, rounds)

    ref_class = ref_ns.get(task.entry_name)
    user_class = user_ns.get(task.entry_name)
    if not isinstance(user_class, type):
        return {"ok": False, "error": f"Класс {task.entry_name} не найден после выполнения кода."}
    return eval_class_task(task, ref_class, user_class, rounds)


def run_eval_in_subprocess(payload: dict[str, Any], timeout_s: float = 10.0) -> dict[str, Any]:
    parent_conn, child_conn = mp.Pipe(duplex=False)

    def worker(conn, data):
        try:
            conn.send(eval_submission(data))
        except Exception as exc:
            conn.send({"ok": False, "error": f"Внутренняя ошибка: {exc}"})
        finally:
            conn.close()

    proc = mp.Process(target=worker, args=(child_conn, payload), daemon=True)
    proc.start()
    proc.join(timeout_s)

    if proc.is_alive():
        proc.terminate()
        proc.join()
        return {"ok": False, "error": "Проверка прервана по общему таймауту."}
    if parent_conn.poll():
        return parent_conn.recv()
    return {"ok": False, "error": "Не удалось получить результат проверки."}


def make_template(task: TaskMeta) -> str:
    if task.task_kind == "function":
        return ""
    return ""


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/tasks")
def api_tasks():
    data = []
    for task in sorted(TASKS.values(), key=lambda x: x.task_id):
        data.append(
            {
                "id": task.task_id,
                "title": task.title,
                "signature": task.signature,
                "description": task.description,
                "task_kind": task.task_kind,
                "entry_name": task.entry_name,
                "time_limit_ms": task.time_limit_ms,
            }
        )
    return jsonify({"tasks": data})


@app.post("/api/run")
def api_run():
    payload = request.get_json(force=True, silent=True) or {}
    task_id = payload.get("task_id")
    if task_id is None:
        return jsonify({"ok": False, "error": "Не выбран task_id"}), 400
    result = run_eval_in_subprocess(
        {
            "task_id": task_id,
            "code": payload.get("code", ""),
            "rounds": payload.get("rounds", 60),
        }
    )
    return jsonify(result), (200 if result.get("ok") else 400)


if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", "5000")), debug=False)
