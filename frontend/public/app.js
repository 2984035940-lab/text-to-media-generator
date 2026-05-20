const API_BASE = 'http://localhost:5000';
let results = [];

// Video Form Handler
document.getElementById('videoForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const prompt = document.getElementById('videoPrompt').value;
    const duration = parseInt(document.getElementById('videoDuration').value);
    const fps = parseInt(document.getElementById('videoFPS').value);
    const width = parseInt(document.getElementById('videoWidth').value);
    const height = parseInt(document.getElementById('videoHeight').value);
    
    const statusDiv = document.getElementById('videoStatus');
    statusDiv.innerHTML = '<div class="status pending"><span class="loading"></span> 正在生成视频...</div>';
    
    try {
        const response = await fetch('/api/generate-video', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt,
                duration,
                fps,
                width,
                height
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            statusDiv.innerHTML = '<div class="status success">✓ 视频生成请求已提交</div>';
            addResult({
                type: 'video',
                prompt,
                status: 'pending',
                taskId: data.task_id || 'unknown',
                timestamp: new Date().toLocaleString('zh-CN')
            });
            document.getElementById('videoForm').reset();
        } else {
            statusDiv.innerHTML = `<div class="status error">✗ 错误: ${data.error || '生成失败'}</div>`;
        }
    } catch (error) {
        statusDiv.innerHTML = `<div class="status error">✗ 错误: ${error.message}</div>`;
    }
});

// Image Form Handler
document.getElementById('imageForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const prompt = document.getElementById('imagePrompt').value;
    const negativePrompt = document.getElementById('negativePrompt').value;
    const numImages = parseInt(document.getElementById('numImages').value);
    const guidanceScale = parseFloat(document.getElementById('guidance').value);
    const width = parseInt(document.getElementById('imageWidth').value);
    const height = parseInt(document.getElementById('imageHeight').value);
    
    const statusDiv = document.getElementById('imageStatus');
    statusDiv.innerHTML = '<div class="status pending"><span class="loading"></span> 正在生成图像...</div>';
    
    try {
        const response = await fetch('/api/generate-image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt,
                negative_prompt: negativePrompt,
                num_images: numImages,
                guidance_scale: guidanceScale,
                width,
                height
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            statusDiv.innerHTML = '<div class="status success">✓ 图像生成请求已提交</div>';
            addResult({
                type: 'image',
                prompt,
                status: 'pending',
                generationId: data.generation_id || 'unknown',
                timestamp: new Date().toLocaleString('zh-CN')
            });
            document.getElementById('imageForm').reset();
        } else {
            statusDiv.innerHTML = `<div class="status error">✗ 错误: ${data.error || '生成失败'}</div>`;
        }
    } catch (error) {
        statusDiv.innerHTML = `<div class="status error">✗ 错误: ${error.message}</div>`;
    }
});

function addResult(result) {
    results.unshift(result);
    renderResults();
}

function renderResults() {
    const resultsList = document.getElementById('resultsList');
    
    if (results.length === 0) {
        resultsList.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📭</div>
                <p>暂无生成记录</p>
            </div>
        `;
        return;
    }
    
    resultsList.innerHTML = results.map((result, index) => `
        <div class="result-item">
            <strong>${result.type === 'video' ? '🎥 视频' : '🖼️ 图像'}</strong>
            <p style="color: #666; margin: 8px 0;">提示词: ${result.prompt.substring(0, 50)}...</p>
            <p style="color: #999; font-size: 0.9em; margin: 5px 0;">时间: ${result.timestamp}</p>
            <span class="status ${result.status}">
                ${result.status === 'pending' ? '⏳ 处理中' : 
                  result.status === 'success' ? '✓ 完成' : 
                  '✗ 失败'}
            </span>
        </div>
    `).join('');
}

// Initial render
renderResults();
