// 密钥，必须与服务器端一致
const SECRET_KEY = "SerialQt@2025#Secure";

// 生成密码的核心函数
async function generatePassword(month, day) {
    const dateNum = month * 100 + day;
    const raw = `${dateNum}${SECRET_KEY}`;
    
    // SHA256 哈希
    const encoder = new TextEncoder();
    const data = encoder.encode(raw);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    
    // 转换为 Base64
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashBase64 = btoa(String.fromCharCode.apply(null, hashArray));
    
    // 提取8位密码（去掉容易混淆的字符）
    const cleanChars = hashBase64.replace(/[^a-zA-Z0-9]/g, '')
                                  .replace(/[O0Il1]/g, '')
                                  .toUpperCase();
    
    return cleanChars.substring(0, 8);
}

// 显示提示消息
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.style.background = type === 'success' ? '#4ade80' : '#ef4444';
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// 复制密码到剪贴板
async function copyPassword() {
    const element = document.getElementById('todayPassword');
    const passwordText = element.querySelector('.password-text').textContent;
    
    if (passwordText === '--------') {
        showToast('请先生成密码！', 'error');
        return;
    }
    
    try {
        await navigator.clipboard.writeText(passwordText);
        showToast('✅ 密码已复制到剪贴板！');
    } catch (err) {
        // 降级方案
        const textarea = document.createElement('textarea');
        textarea.value = passwordText;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showToast('✅ 密码已复制到剪贴板！');
    }
}

// 格式化日期显示
function formatDate(date) {
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
    const weekday = weekdays[date.getDay()];
    
    return `${year}年${month.toString().padStart(2, '0')}月${day.toString().padStart(2, '0')}日 ${weekday}`;
}

// 生成今日密码
async function generateToday() {
    const today = new Date();
    const month = today.getMonth() + 1;
    const day = today.getDate();
    
    // 显示日期
    document.getElementById('todayDate').textContent = formatDate(today);
    
    // 生成密码
    const password = await generatePassword(month, day);
    
    // 显示密码
    const passwordDisplay = document.getElementById('todayPassword');
    passwordDisplay.querySelector('.password-text').textContent = password;
    passwordDisplay.style.display = 'flex';
    
    showToast('✅ 今日密码已生成！');
}


// 页面加载时自动生成今日密码
window.addEventListener('DOMContentLoaded', () => {
    generateToday();
});
