from flask import Flask, request, render_template_string
import requests
from threading import Thread, Event
import time
import random
import string

app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

stop_events = {}
threads = {}

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    print(f"Message Sent Successfully From token {access_token}: {message}")
                else:
                    print(f"Message Sent Failed From token {access_token}: {message}")
                time.sleep(time_interval)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')
        if token_option == 'single':
            access_tokens = [request.form.get('singleToken')]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()

        return render_template_string(template, message=f'Task started with ID: {task_id}')
    return render_template_string(template, message=None)

@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return render_template_string(template, message=f'Task with ID {task_id} has been stopped.')
    else:
        return render_template_string(template, message=f'No task found with ID {task_id}.')

template = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🦋 MR DEVIL 🦋 Stylish</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
  <!-- Google Fonts: Orbitron -->
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap" rel="stylesheet">
  <style>
    body {
      min-height: 100vh;
      margin: 0;
      padding: 0;
      font-family: 'Orbitron', Arial, sans-serif;
      background: linear-gradient(135deg, #232526 0%, #0f2027 100%);
      background-image: url('https://i.ibb.co/Y70mrxt5/Dragon-Ball-Attack-GIF-by-BANDAI-NAMCO.gif');
      background-blend-mode: overlay;
      background-size: cover;
      background-attachment: fixed;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    ::-webkit-scrollbar { width: 8px; background: #111; }
    ::-webkit-scrollbar-thumb { background: #ff00cc; border-radius: 8px; }
    .container {
      background: rgba(20, 20, 40, 0.75);
      box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-radius: 24px;
      border: 1.5px solid rgba(255,255,255,0.22);
      padding: 36px 22px;
      max-width: 480px;
      margin: 40px auto;
      color: white;
      position: relative;
      overflow: hidden;
    }
    .neon-title {
      font-size: 2.2rem;
      text-align: center;
      text-transform: uppercase;
      background: linear-gradient(90deg, #ff00cc, #00ffff, #ff00cc);
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
      animation: neonGlow 2s ease-in-out infinite;
      letter-spacing: 2px;
      margin-bottom: 30px;
      font-family: 'Orbitron', Arial, sans-serif;
      font-weight: 700;
    }
    @keyframes neonGlow {
      0%, 100% { text-shadow: 0 0 10px #ff00cc, 0 0 20px #00ffff; }
      50% { text-shadow: 0 0 30px #ff00cc, 0 0 60px #00ffff; }
    }
    .form-label {
      color: #ff00cc;
      font-weight: 600;
      letter-spacing: 1px;
      margin-bottom: 4px;
      text-shadow: 0 0 6px #ff00cc, 0 0 12px #00ffff;
    }
    .input-group-text {
      background: rgba(255,255,255,0.10);
      border: none;
      color: #00ffff;
      font-size: 1.2rem;
    }
    .form-control {
      background: rgba(255,255,255,0.12);
      border: 1.5px solid #fff;
      color: #fff;
      border-radius: 10px;
      transition: border 0.3s, box-shadow 0.3s;
      font-family: 'Orbitron', Arial, sans-serif;
    }
    .form-control:focus {
      border: 2px solid #ff00cc;
      box-shadow: 0 0 10px #ff00cc, 0 0 20px #00ffff;
      background: rgba(255,255,255,0.18);
      color: #fff;
    }
    .btn-neon {
      color: #fff;
      border: none;
      padding: 12px 0;
      font-size: 1.15rem;
      font-weight: bold;
      border-radius: 14px;
      width: 100%;
      margin-top: 18px;
      background: linear-gradient(90deg, #ff00cc, #3333ff);
      box-shadow: 0 0 10px #ff00cc, 0 0 20px #3333ff, 0 0 40px #ff00cc;
      transition: 0.3s all;
      position: relative;
      overflow: hidden;
      z-index: 1;
      font-family: 'Orbitron', Arial, sans-serif;
    }
    .btn-neon:before {
      content: '';
      position: absolute;
      left: -75%;
      top: 0;
      width: 50%;
      height: 100%;
      background: linear-gradient(120deg, transparent, rgba(255,255,255,0.6), transparent);
      transform: skewX(-25deg);
      transition: 0.5s;
      z-index: 2;
    }
    .btn-neon:hover:before {
      left: 120%;
    }
    .btn-neon:hover {
      background: linear-gradient(90deg, #3333ff, #ff00cc);
      box-shadow: 0 0 20px #00fff0, 0 0 40px #ff00cc;
      color: #fff;
      transform: scale(1.05);
    }
    .btn-neon-red {
      background: linear-gradient(90deg, #ff0000, #ff6a00);
      box-shadow: 0 0 15px #ff0000, 0 0 30px #ff6a00;
    }
    .btn-neon-red:hover {
      background: linear-gradient(90deg, #ff6a00, #ff0000);
      box-shadow: 0 0 20px #ff6a00, 0 0 40px #ff0000;
    }
    .hidden { display: none; }
    /* Loader spinner */
    #loader {
      position: fixed;
      left: 0; top: 0; width: 100vw; height: 100vh;
      background: rgba(0,0,0,0.45);
      display: flex; align-items: center; justify-content: center;
      z-index: 9999;
      display: none;
    }
    /* Toast notification */
    #toast {
      position: fixed;
      top: 30px;
      right: 30px;
      min-width: 180px;
      z-index: 9999;
      display: none;
      background: rgba(20,20,40,0.95);
      color: #fff;
      border-radius: 10px;
      box-shadow: 0 0 20px #ff00cc;
      padding: 16px 32px;
      font-family: 'Orbitron', Arial, sans-serif;
      font-weight: bold;
      letter-spacing: 1px;
      animation: fadeIn 0.7s;
    }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    /* Responsive */
    @media (max-width: 600px) {
      .container { padding: 18px 2px; }
      .neon-title { font-size: 1.3rem; }
    }
  </style>
</head>
<body>
  <div id="loader">
    <div class="spinner-border text-info" style="width: 4rem; height: 4rem;"></div>
  </div>
  <div id="toast"></div>
  <div class="container">
    <div class="neon-title mb-4">MR DEVIL SHARABI</div>
    <form method="POST" enctype="multipart/form-data" onsubmit="showLoader()">
      <!-- Token Option -->
      <div class="mb-3">
        <label class="form-label"><i class="fas fa-key"></i> Token Options:</label>
        <select class="form-control" name="tokenOption" id="tokenOption" onchange="toggleTokenInput()">
          <option value="single">Single Token</option>
          <option value="multiple">Multiple Tokens</option>
        </select>
      </div>
      <!-- Token Inputs -->
      <div class="mb-3" id="singleTokenGroup">
        <label class="form-label"><i class="fas fa-user-secret"></i> Access Token:</label>
        <div class="input-group">
          <span class="input-group-text"><i class="fas fa-lock"></i></span>
          <input type="text" class="form-control" name="singleToken">
        </div>
      </div>
      <div class="mb-3 hidden" id="tokenFileGroup">
        <label class="form-label"><i class="fas fa-file-alt"></i> Token File:</label>
        <input type="file" class="form-control" name="tokenFile">
      </div>
      <div class="mb-3">
        <label class="form-label"><i class="fas fa-comments"></i> Thread UID:</label>
        <input type="text" class="form-control" name="threadId" required>
      </div>
      <div class="mb-3">
        <label class="form-label"><i class="fas fa-user-ninja"></i> Hater Name:</label>
        <input type="text" class="form-control" name="kidx">
      </div>
      <div class="mb-3">
        <label class="form-label"><i class="fas fa-clock"></i> Time Interval (Seconds):</label>
        <input type="number" class="form-control" name="time" required>
      </div>
      <div class="mb-3">
        <label class="form-label"><i class="fas fa-file-alt"></i> Messages File (TXT):</label>
        <input type="file" class="form-control" name="txtFile" required>
      </div>
      <button type="submit" class="btn-neon">
        <i class="fas fa-play-circle me-2"></i>Start Convo
      </button>
    </form>
    <hr class="my-4">
    <form method="POST" action="/stop" onsubmit="showLoader()">
      <div class="mb-3">
        <label class="form-label"><i class="fas fa-ban"></i> Task ID to Stop:</label>
        <input type="text" class="form-control" name="taskId" required>
      </div>
      <button type="submit" class="btn-neon btn-neon-red">
        <i class="fas fa-stop-circle me-2"></i>Stop Convo
      </button>
    </form>
    <footer class="text-center mt-4" style="font-size: 1.1rem;">
      <div class="mb-2">Connect With Me</div>
      <a href="https://www.facebook.com/TabbuArain" class="text-white text-decoration-none social-link me-3" target="_blank">
        <i class="fab fa-facebook fa-2x"></i>
      </a>
      <a href="https://wa.me/+919024870456" class="text-white text-decoration-none social-link" target="_blank">
        <i class="fab fa-whatsapp fa-2x"></i>
      </a>
      <div class="mt-2" style="font-size: 0.95rem;">
        <span style="color:#ff00cc;">©2025 All rights reserved By TABBU ARAIN</span>
      </div>
    </footer>
  </div>
  <script>
    function toggleTokenInput() {
      const option = document.getElementById("tokenOption").value;
      document.getElementById("singleTokenGroup").style.display = (option === "single") ? "block" : "none";
      document.getElementById("tokenFileGroup").style.display = (option === "multiple") ? "block" : "none";
    }
    toggleTokenInput();

    // Loader spinner
    function showLoader() {
      document.getElementById('loader').style.display = 'flex';
    }
    // Toast notification
    function showToast(msg) {
      var toast = document.getElementById('toast');
      toast.innerText = msg;
      toast.style.display = 'block';
      setTimeout(function(){ toast.style.display = 'none'; }, 2600);
    }
    // Show toast if redirected with message (optional, for Flask flash)
    {% if message %}
      showToast("{{ message }}");
    {% endif %}
  </script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
