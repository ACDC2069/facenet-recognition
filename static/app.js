// 全局变量
let video = null;
let canvas = null;
let ctx = null;
let isRecognizing = false;
let recognitionInterval = null;

// 初始化
document.addEventListener('DOMContentLoaded', async () => {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');

    // 设置按钮事件
    document.getElementById('enrollBtn').addEventListener('click', enrollFace);
    document.getElementById('toggleBtn').addEventListener('click', toggleRecognition);

    // 启动摄像头
    await startCamera();
});

// 启动摄像头
async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: { width: 640, height: 480 }
        });
        video.srcObject = stream;
        
        video.addEventListener('loadedmetadata', () => {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            updateStatus('摄像头已就绪');
        });
    } catch (error) {
        console.error('无法访问摄像头:', error);
        updateStatus('错误: 无法访问摄像头');
    }
}

// 更新状态文本
function updateStatus(message) {
    document.getElementById('statusText').textContent = message;
}

// 切换识别状态
function toggleRecognition() {
    const btn = document.getElementById('toggleBtn');
    
    if (isRecognizing) {
        // 停止识别
        clearInterval(recognitionInterval);
        isRecognizing = false;
        btn.textContent = '开始识别';
        updateStatus('识别已停止');
        clearCanvas();
    } else {
        // 开始识别
        isRecognizing = true;
        btn.textContent = '停止识别';
        updateStatus('正在识别...');
        recognitionInterval = setInterval(recognizeFaces, 1000);
    }
}

// 识别人脸
async function recognizeFaces() {
    if (!isRecognizing) return;

    try {
        // 捕获当前帧
        const imageData = captureFrame();
        
        // 发送到后端识别
        const response = await fetch('/recognize_base64', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        });

        const data = await response.json();
        
        // 显示结果
        displayResults(data.results);
        drawBoundingBoxes(data.results);
        
    } catch (error) {
        console.error('识别错误:', error);
        updateStatus('识别错误: ' + error.message);
    }
}

// 录入人脸
async function enrollFace() {
    const nameInput = document.getElementById('nameInput');
    const name = nameInput.value.trim();

    if (!name) {
        alert('请输入姓名');
        return;
    }

    try {
        updateStatus('正在录入...');
        
        // 捕获当前帧
        const imageData = captureFrame();
        
        // 发送到后端录入
        const response = await fetch('/enroll_base64', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                image: imageData
            })
        });

        const data = await response.json();
        
        if (data.success) {
            updateStatus(data.message);
            nameInput.value = '';
            alert('录入成功!');
        } else {
            updateStatus(data.message);
            alert('录入失败: ' + data.message);
        }
        
    } catch (error) {
        console.error('录入错误:', error);
        updateStatus('录入错误: ' + error.message);
        alert('录入失败: ' + error.message);
    }
}

// 捕获视频帧
function captureFrame() {
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = video.videoWidth;
    tempCanvas.height = video.videoHeight;
    const tempCtx = tempCanvas.getContext('2d');
    tempCtx.drawImage(video, 0, 0);
    return tempCanvas.toDataURL('image/jpeg', 0.8);
}

// 显示识别结果
function displayResults(results) {
    const resultsList = document.getElementById('resultsList');
    resultsList.innerHTML = '';

    if (results.length === 0) {
        resultsList.innerHTML = '<p style="color: #718096;">未检测到人脸</p>';
        return;
    }

    results.forEach(result => {
        const div = document.createElement('div');
        div.className = 'result-item' + (result.name === 'Unknown' ? ' unknown' : '');
        
        const namePara = document.createElement('div');
        namePara.className = 'result-name';
        namePara.textContent = result.name;
        
        const confidencePara = document.createElement('div');
        confidencePara.className = 'result-confidence';
        confidencePara.textContent = `置信度: ${(result.confidence * 100).toFixed(1)}%`;
        
        div.appendChild(namePara);
        div.appendChild(confidencePara);
        resultsList.appendChild(div);
    });
}

// 绘制边界框
function drawBoundingBoxes(results) {
    clearCanvas();

    results.forEach(result => {
        const [x, y, w, h] = result.box;
        const color = result.name === 'Unknown' ? '#f56565' : '#48bb78';

        // 绘制矩形框
        ctx.strokeStyle = color;
        ctx.lineWidth = 3;
        ctx.strokeRect(x, y, w, h);

        // 绘制标签背景
        ctx.fillStyle = color;
        const label = `${result.name} (${(result.confidence * 100).toFixed(0)}%)`;
        const textWidth = ctx.measureText(label).width;
        ctx.fillRect(x, y - 25, textWidth + 10, 25);

        // 绘制标签文字
        ctx.fillStyle = 'white';
        ctx.font = '16px Arial';
        ctx.fillText(label, x + 5, y - 7);
    });
}

// 清除画布
function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

