const taskSelect = document.getElementById("taskSelect");
const taskSignature = document.getElementById("taskSignature");
const taskLimit = document.getElementById("taskLimit");
const roundsInput = document.getElementById("roundsInput");
const codeInput = document.getElementById("codeInput");
const resultOutput = document.getElementById("resultOutput");
const runBtn = document.getElementById("runBtn");

let tasks = [];

function templateForSignature(signature) {
  const raw = signature.startsWith("solution") ? signature.slice("solution".length) : "(...)";
  return `def solution${raw}:\n    # TODO: write your code\n    pass\n`;
}

function templateForClass(name) {
  if (name === "BrowserHistory") {
    return `class BrowserHistory:\n    def __init__(self, homepage: str):\n        pass\n\n    def visit(self, url: str) -> None:\n        pass\n\n    def back(self, steps: int) -> str:\n        pass\n\n    def forward(self, steps: int) -> str:\n        pass\n`;
  }
  if (name === "Stack") {
    return `class Stack:\n    def __init__(self):\n        pass\n\n    def push(self, x: int) -> None:\n        pass\n\n    def pop(self) -> int:\n        pass\n\n    def peek(self) -> int:\n        pass\n\n    def is_empty(self) -> bool:\n        pass\n`;
  }
  if (name === "Queue") {
    return `class Queue:\n    def __init__(self):\n        pass\n\n    def enqueue(self, x: int) -> None:\n        pass\n\n    def dequeue(self) -> int:\n        pass\n\n    def front(self) -> int:\n        pass\n\n    def is_empty(self) -> bool:\n        pass\n`;
  }
  if (name === "MinStack") {
    return `class MinStack:\n    def __init__(self):\n        pass\n\n    def push(self, x: int) -> None:\n        pass\n\n    def pop(self) -> int:\n        pass\n\n    def get_min(self) -> int:\n        pass\n`;
  }
  if (name === "DSU") {
    return `class DSU:\n    def __init__(self, n: int):\n        pass\n\n    def find(self, x: int) -> int:\n        pass\n\n    def union(self, x: int, y: int) -> None:\n        pass\n`;
  }
  return `class ${name}:\n    pass\n`;
}

function showTask(task) {
  taskSignature.textContent = `Сигнатура: ${task.signature}`;
  taskLimit.textContent = `Лимит на 1 тест: ${task.time_limit_ms} ms`;
  if (task.task_kind === "class") {
    codeInput.value = templateForClass(task.entry_name);
  } else {
    codeInput.value = templateForSignature(task.signature);
  }
}

async function loadTasks() {
  const res = await fetch("/api/tasks");
  const data = await res.json();
  tasks = data.tasks || [];

  taskSelect.innerHTML = "";
  for (const t of tasks) {
    const opt = document.createElement("option");
    opt.value = t.id;
    opt.textContent = `${t.id}. ${t.title}`;
    taskSelect.appendChild(opt);
  }

  if (tasks.length) {
    showTask(tasks[0]);
  }
}

taskSelect.addEventListener("change", () => {
  const id = Number(taskSelect.value);
  const task = tasks.find((t) => t.id === id);
  if (task) {
    showTask(task);
  }
});

runBtn.addEventListener("click", async () => {
  const id = Number(taskSelect.value);
  const rounds = Number(roundsInput.value || 80);
  const code = codeInput.value;

  resultOutput.textContent = "Запуск проверки...";

  try {
    const res = await fetch("/api/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task_id: id, rounds, code }),
    });
    const data = await res.json();

    if (data.ok) {
      resultOutput.textContent = [
        "Статус: OK",
        `Тестов: ${data.rounds}`,
        `Среднее время: ${data.timing.avg_ms} ms`,
        `Макс время: ${data.timing.max_ms} ms`,
        `Мин время: ${data.timing.min_ms} ms`,
        `Лимит: ${data.timing.limit_ms} ms`,
      ].join("\n");
      return;
    }

    let out = `Статус: WA/TLE\nОшибка: ${data.error || "unknown"}`;
    if (data.sample) {
      out += "\n\nПример теста:";
      out += `\nargs = ${JSON.stringify(data.sample.args)}`;
      if ("expected" in data.sample) out += `\nexpected = ${JSON.stringify(data.sample.expected)}`;
      if ("got" in data.sample) out += `\ngot = ${JSON.stringify(data.sample.got)}`;
    }
    resultOutput.textContent = out;
  } catch (err) {
    resultOutput.textContent = `Сетевая ошибка: ${err}`;
  }
});

loadTasks();
