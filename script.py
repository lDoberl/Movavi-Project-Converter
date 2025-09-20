from flask import Flask, request, send_file, render_template_string, send_from_directory
import zipfile
import json
import io
import webbrowser
import os
import signal
from threading import Timer

app = Flask(__name__)

# Поддерживаемые версии и соответствие config.json
VERSIONS = [
    "25.9.0",  # 79
    "25.3.0",  # 76
    "23.3.0"   # 63
]

VERSION_MAP = {
    "23.3.0": 63,
    "25.3.0": 76,
    "25.9.0": 79
}


@app.route('/favicon.png')
def favicon_png():
    return send_from_directory(os.path.dirname(__file__), 'favicon.png', mimetype='image/png')


@app.route("/close", methods=["POST"])
def close_app():
    os.kill(os.getpid(), signal.SIGINT)
    return "Server shutting down..."


HTML = """
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Movavi Project Converter</title>
<link rel="icon" type="image/png" sizes="32x32" href="/favicon.png">
<script src="https://cdn.tailwindcss.com"></script>
<style>
/* Модальное окно */
.modal { display:none; position:fixed; inset:0; background:rgba(0,0,0,0.8); justify-content:center; align-items:center; }
.modal-content { background:#1f2937; padding:20px; border-radius:10px; max-width:500px; text-align:center; color:#f3f4f6; }

/* Эффект пульсации кнопки Exit */
.pulse-button { animation: pulse 2s infinite; }
@keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }

/* Дроп-зона */
#dropZone {
    transition: all 0.2s ease;
    cursor: pointer;
}
#dropZone.dragover {
    transform: scale(1.05);
    border-color: #22c55e;
    color: #22c55e;
}
#dropZone.fullscreen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 24px;
    border: 5px dashed #22c55e;
    background: rgba(34,197,94,0.1);
    color: #22c55e;
    z-index: 9999;
    transform: none !important;
}
</style>
</head>
<body class="bg-gray-900 flex items-center justify-center min-h-screen text-gray-100">

<div class="bg-gray-800 p-8 rounded-2xl shadow-lg w-full max-w-md border border-green-600">

  <h1 class="text-2xl font-bold mb-6 text-center text-green-400">Movavi Project Converter</h1>

  <form id="convert-form" method="post" enctype="multipart/form-data" class="space-y-4">
    <input type="file" id="fileInput" name="file" accept=".mepj" required style="display:none;">

    <div id="dropZone" 
         class="mt-4 p-6 border-2 border-dashed border-gray-500 rounded-lg text-center text-gray-400 hover:border-green-500">
      Drag & Drop .mepj file here
    </div>

    <div>
      <label class="block mb-2 font-medium" id="label-version">Target version:</label>
      <select name="target_version" class="w-full border border-gray-600 rounded-md p-2 bg-gray-700 text-gray-100 hover:border-green-500 focus:ring-2 focus:ring-green-400 focus:outline-none transition-all">
        {% for v in versions %}
          <option value="{{v}}">{{v}}</option>
        {% endfor %}
      </select>
    </div>

    <button type="submit" class="w-full bg-green-500 text-white font-semibold py-2 rounded-lg hover:bg-green-600 hover:scale-105 transition-transform shadow-md">
      Convert
    </button>
  </form>

  <div class="flex justify-center mt-6">
    <button 
        type="button" 
        onclick="closeProgram()" 
        class="w-3/4 bg-red-600 text-white font-bold py-3 rounded-lg shadow-lg pulse-button hover:bg-red-700 transition-transform hover:scale-110"
        title="This will stop the program immediately!">
        ✖ Exit
    </button>
  </div>
</div>

<!-- Модальное окно с инструкцией -->
<div id="instructionModal" class="modal">
  <div class="modal-content">
    <h2 class="text-xl font-bold mb-4 text-green-400" id="modal-title">Instructions</h2>
    <p class="mb-4" id="modal-text">
      Upload your <b>.mepj</b> project file (not older than version 22.5.0).<br>
      Then select one of the three supported versions.<br>
      Finally, press <b>Convert</b>.
    </p>
    <div class="flex justify-between mt-6">
      <button onclick="toggleLanguage()" id="lang-btn" class="px-4 py-2 bg-blue-600 rounded hover:bg-blue-700">
        Русский
      </button>
      <button onclick="closeModal()" class="px-6 py-2 bg-green-600 rounded hover:bg-green-700">OK</button>
    </div>
  </div>
</div>

<!-- Уведомление об успешной конверсии -->
<div id="successToast" class="fixed bottom-4 right-4 bg-green-600 text-white px-6 py-3 rounded shadow-lg hidden">
  ✅ Conversion successful!
</div>

<script>
let currentLang = "en";

function closeProgram() {
    if (confirm("Are you sure you want to stop the program?")) {
        fetch('/close', {method:'POST'});
    }
}

function closeModal() {
    document.getElementById("instructionModal").style.display = "none";
}

function toggleLanguage() {
    if (currentLang === "en") {
        currentLang = "ru";
        document.getElementById("modal-title").innerText = "Инструкция";
        document.getElementById("modal-text").innerHTML = "Загрузите ваш проект <b>.mepj</b> (не старее версии 22.5.0).<br>Затем выберите одну из трёх поддерживаемых версий.<br>Нажмите <b>Конвертировать</b>.";
        document.getElementById("label-version").innerText = "Целевая версия:";
        document.getElementById("lang-btn").innerText = "English";
        document.getElementById("dropZone").innerText = "Перетащите .mepj файл сюда";
    } else {
        currentLang = "en";
        document.getElementById("modal-title").innerText = "Instructions";
        document.getElementById("modal-text").innerHTML = "Upload your <b>.mepj</b> project file (not older than version 22.5.0).<br>Then select one of the three supported versions.<br>Finally, press <b>Convert</b>.";
        document.getElementById("label-version").innerText = "Target version:";
        document.getElementById("lang-btn").innerText = "Русский";
        document.getElementById("dropZone").innerText = "Drag & Drop .mepj file here";
    }
}

window.onload = function() {
    document.getElementById("instructionModal").style.display = "flex";
}

document.getElementById("convert-form").addEventListener("submit", function() {
    setTimeout(() => {
        let toast = document.getElementById("successToast");
        toast.classList.remove("hidden");
        setTimeout(() => toast.classList.add("hidden"), 3000);
    }, 1000);
});

const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");

// Клик по зоне открывает проводник
dropZone.addEventListener("click", () => fileInput.click());

// Drag & Drop для всей страницы
document.addEventListener("dragover", e => e.preventDefault());

document.addEventListener("dragenter", e => {
    e.preventDefault();
    dropZone.classList.add("dragover", "fullscreen");
});

document.addEventListener("dragleave", e => {
    e.preventDefault();
    // Если курсор ушёл за предел окна
    if (e.clientX === 0 && e.clientY === 0) {
        dropZone.classList.remove("dragover", "fullscreen");
    }
});

document.addEventListener("drop", e => {
    e.preventDefault();
    dropZone.classList.remove("dragover", "fullscreen");

    const file = e.dataTransfer.files[0];
    if (file && file.name.endsWith(".mepj")) {
        fileInput.files = e.dataTransfer.files;
        dropZone.innerText = `✔ ${file.name}`;
    } else {
        alert("Only .mepj files are allowed!");
    }
});

// Обновление текста после выбора через проводник
fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
        dropZone.innerText = `✔ ${fileInput.files[0].name}`;
    }
});
</script>

</body>
</html>

"""


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        target_version = request.form.get("target_version")
        config_number = VERSION_MAP.get(target_version)

        if not file or not config_number:
            return "Error: invalid file or version", 400

        mem_file = io.BytesIO(file.read())
        new_mem_file = io.BytesIO()

        try:
            with zipfile.ZipFile(mem_file, 'r') as zip_in:
                with zipfile.ZipFile(new_mem_file, 'w', zipfile.ZIP_DEFLATED) as zip_out:
                    for item in zip_in.infolist():
                        data = zip_in.read(item.filename)
                        if item.filename == "meta.json":
                            meta = json.loads(data.decode('utf-8'))
                            if "versions" in meta and "config.json" in meta["versions"]:
                                meta["versions"]["config.json"] = config_number
                            data = json.dumps(meta, ensure_ascii=False, indent=4).encode('utf-8')
                        zip_out.writestr(item, data)
        except zipfile.BadZipFile:
            return "Error: uploaded file is not a valid .mepj archive", 400

        new_mem_file.seek(0)
        return send_file(
            new_mem_file,
            as_attachment=True,
            download_name=f"converted_{target_version}.mepj",
            mimetype="application/octet-stream"
        )

    return render_template_string(HTML, versions=VERSIONS)


if __name__ == "__main__":
    port = 5000
    url = f"http://127.0.0.1:{port}"
    Timer(1, lambda: webbrowser.open(url)).start()
    app.run(debug=False, port=port)
