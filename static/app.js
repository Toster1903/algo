const taskSelect = document.getElementById("taskSelect");
const taskSignature = document.getElementById("taskSignature");
const taskLimit = document.getElementById("taskLimit");
const taskDescription = document.getElementById("taskDescription");
const roundsInput = document.getElementById("roundsInput");
const testTaskCountInput = document.getElementById("testTaskCountInput");
const codeEditorEl = document.getElementById("codeEditor");
const syntaxStatus = document.getElementById("syntaxStatus");
const resultOutput = document.getElementById("resultOutput");
const runBtn = document.getElementById("runBtn");
const hintBtn = document.getElementById("hintBtn");
const startTestBtn = document.getElementById("startTestBtn");
const startEasyTestBtn = document.getElementById("startEasyTestBtn");
const startHardTestBtn = document.getElementById("startHardTestBtn");
const nextTaskBtn = document.getElementById("nextTaskBtn");
const testInfo = document.getElementById("testInfo");

let tasks = [];
let testSession = null;
let editor = null;
let syntaxTimer = null;

// Все задачи, не попавшие в этот список, автоматически считаются легкими.
const HARD_TASK_IDS = new Set([
  5, 6, 9, 10, 11, 12, 21, 22, 23, 30, 31, 34, 36, 43, 44, 46, 47, 48, 49,
  50, 51, 52, 53, 54, 66, 67, 69, 70, 71, 74, 75, 76, 77, 78, 79,
]);

function initEditor() {
  if (!window.ace || !codeEditorEl) {
    resultOutput.textContent = "Ошибка: редактор не загрузился.";
    return;
  }

  editor = window.ace.edit("codeEditor");
  editor.setTheme("ace/theme/chrome");
  editor.session.setMode("ace/mode/python");
  editor.setOptions({
    fontFamily: "IBM Plex Mono",
    fontSize: "14px",
    tabSize: 4,
    useSoftTabs: false,
    showPrintMargin: false,
    enableBasicAutocompletion: true,
    enableLiveAutocompletion: false,
    wrap: false,
  });

  editor.session.on("change", () => {
    scheduleSyntaxCheck();
  });

  window.addEventListener("resize", () => {
    editor.resize();
  });
}

function getCode() {
  return editor ? editor.getValue() : "";
}

function setCode(value) {
  if (!editor) return;
  editor.setValue(value, -1);
  scheduleSyntaxCheck();
}

function setSyntaxOk(text = "Синтаксис: ошибок нет") {
  if (!syntaxStatus) return;
  syntaxStatus.textContent = text;
  syntaxStatus.classList.remove("syntax-error");
  syntaxStatus.classList.add("syntax-ok");
  if (editor) {
    editor.session.setAnnotations([]);
  }
}

function setSyntaxError(msg, line, column) {
  if (!syntaxStatus) return;
  syntaxStatus.textContent = `Синтаксис: ${msg} (строка ${line}, позиция ${column})`;
  syntaxStatus.classList.remove("syntax-ok");
  syntaxStatus.classList.add("syntax-error");
  if (editor) {
    editor.session.setAnnotations([
      {
        row: Math.max(0, (line || 1) - 1),
        column: Math.max(0, (column || 1) - 1),
        text: msg,
        type: "error",
      },
    ]);
  }
}

async function checkSyntaxNow() {
  const code = getCode();
  if (!code.trim()) {
    setSyntaxOk("Синтаксис: ожидаю код");
    return;
  }

  try {
    const res = await fetch("/api/syntax-check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
    });
    const data = await res.json();
    if (data.ok) {
      setSyntaxOk();
      return;
    }
    setSyntaxError(data.error || "SyntaxError", data.line || 1, data.column || 1);
  } catch (_err) {
    setSyntaxError("не удалось проверить код", 1, 1);
  }
}

function scheduleSyntaxCheck() {
  if (syntaxTimer) {
    clearTimeout(syntaxTimer);
  }
  syntaxTimer = setTimeout(() => {
    checkSyntaxNow();
  }, 250);
}

function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function buildHint(task) {
  const t = (task.title || "").toLowerCase();
  if (task.task_kind === "class") {
    return "Начни с структуры хранения состояния: стек, очередь или массивы истории. Затем реализуй каждый метод отдельно и проверь крайние случаи (пустая структура, один элемент).";
  }
  if (t.includes("префикс")) return "Подумай о массиве pi и откате по pi[j - 1], когда символы не совпадают.";
  if (t.includes("z‑функции") || t.includes("z-функции")) return "Держи окно [l, r] и используй уже посчитанные значения для ускорения.";
  if (t.includes("циклическим сдвигом")) return "Проверь длины строк, затем ищи одну строку внутри удвоенной другой.";
  if (t.includes("простым")) return "Проверять делители достаточно до sqrt(n), отдельно обработай n < 2 и чётные числа.";
  if (t.includes("нод") || t.includes("делитель")) return "Используй алгоритм Евклида: пока b != 0, делай a, b = b, a % b.";
  return "Разбей задачу на шаги: корректность на крайних случаях, затем оптимизация под лимит времени.";
}

function getCurrentTask() {
  const id = Number(taskSelect.value);
  return tasks.find((t) => t.id === id) || null;
}

function updateTestUi() {
  if (!testSession) {
    testInfo.textContent = "";
    nextTaskBtn.disabled = true;
    return;
  }
  const modeLabel = testSession.modeLabel || "все";
  testInfo.textContent = `Тест (${modeLabel}) запущен: задача ${testSession.index + 1} из ${testSession.ids.length}`;
  nextTaskBtn.disabled = testSession.index >= testSession.ids.length - 1;
}

function setTaskById(taskId) {
  taskSelect.value = String(taskId);
  const task = tasks.find((t) => t.id === taskId);
  if (task) {
    showTask(task);
  }
}

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
  taskDescription.textContent = task.description || "Описание задачи не найдено.";
  if (task.task_kind === "class") {
    setCode(templateForClass(task.entry_name));
  } else {
    setCode(templateForSignature(task.signature));
  }
}

function getTaskIdsByMode(mode) {
  if (mode === "hard") {
    return tasks.filter((t) => HARD_TASK_IDS.has(t.id)).map((t) => t.id);
  }
  if (mode === "easy") {
    return tasks.filter((t) => !HARD_TASK_IDS.has(t.id)).map((t) => t.id);
  }
  return tasks.map((t) => t.id);
}

function startTest(mode = "all") {
  if (!tasks.length) return;

  const requested = Number(testTaskCountInput.value || 5);
  const pool = getTaskIdsByMode(mode);
  if (!pool.length) {
    resultOutput.textContent = "Для выбранной категории нет задач.";
    return;
  }

  const count = Math.max(1, Math.min(pool.length, requested));
  const ids = shuffle(pool).slice(0, count);
  const modeLabel = mode === "easy" ? "легкие" : mode === "hard" ? "сложные" : "все";

  testSession = { ids, index: 0, mode, modeLabel };
  setTaskById(ids[0]);
  resultOutput.textContent = `Тест начат (${modeLabel}).\nСлучайно выбрано задач: ${count}.\nРешай по очереди, кнопка \"Следующая задача теста\" переведет к следующей.`;
  updateTestUi();
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
    if (testSession) {
      const idx = testSession.ids.indexOf(id);
      if (idx >= 0) {
        testSession.index = idx;
      } else {
        testSession = null;
      }
      updateTestUi();
    }
  }
});

hintBtn.addEventListener("click", () => {
  const task = getCurrentTask();
  if (!task) return;
  resultOutput.textContent = `Подсказка:\n${buildHint(task)}`;
});

startTestBtn.addEventListener("click", () => {
  startTest("all");
});

startEasyTestBtn.addEventListener("click", () => {
  startTest("easy");
});

startHardTestBtn.addEventListener("click", () => {
  startTest("hard");
});

nextTaskBtn.addEventListener("click", () => {
  if (!testSession) return;
  if (testSession.index >= testSession.ids.length - 1) {
    resultOutput.textContent = "Тест завершен: все случайные задачи пройдены.";
    return;
  }
  testSession.index += 1;
  setTaskById(testSession.ids[testSession.index]);
  resultOutput.textContent = `Переход к задаче ${testSession.index + 1} из ${testSession.ids.length}.`;
  updateTestUi();
});

runBtn.addEventListener("click", async () => {
  const id = Number(taskSelect.value);
  const rounds = Number(roundsInput.value || 80);
  const code = getCode();

  resultOutput.textContent = "Запуск проверки...";

  try {
    const res = await fetch("/api/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task_id: id, rounds, code }),
    });
    const contentType = (res.headers.get("content-type") || "").toLowerCase();
    let data;
    if (contentType.includes("application/json")) {
      data = await res.json();
    } else {
      const raw = await res.text();
      const preview = raw.replace(/\s+/g, " ").slice(0, 220);
      resultOutput.textContent = `Ошибка сервера (${res.status}). Ожидался JSON, но пришел другой ответ:\n${preview}`;
      return;
    }

    if (data.ok) {
      resultOutput.textContent = [
        "Статус: OK",
        `Тестов: ${data.rounds}`,
        `Среднее время: ${data.timing.avg_ms} ms`,
        `Макс время: ${data.timing.max_ms} ms`,
        `Мин время: ${data.timing.min_ms} ms`,
        `Лимит: ${data.timing.limit_ms} ms`,
      ].join("\n");

      if (testSession && testSession.ids[testSession.index] === id && testSession.index < testSession.ids.length - 1) {
        resultOutput.textContent += "\n\nЗадача в тест-сессии пройдена. Нажми \"Следующая задача теста\".";
      }
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

initEditor();
loadTasks();
