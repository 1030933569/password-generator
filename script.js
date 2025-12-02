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
async function copyPassword(type) {
    const element = document.getElementById(type === 'today' ? 'todayPassword' : 'customPassword');
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

// 生成自定义日期密码
async function generateCustom() {
    const monthInput = document.getElementById('monthInput');
    const dayInput = document.getElementById('dayInput');
    
    const month = parseInt(monthInput.value);
    const day = parseInt(dayInput.value);
    
    // 验证输入
    if (!month || !day) {
        showToast('❌ 请输入月份和日期！', 'error');
        return;
    }
    
    if (month < 1 || month > 12) {
        showToast('❌ 月份必须在 1-12 之间！', 'error');
        return;
    }
    
    if (day < 1 || day > 31) {
        showToast('❌ 日期必须在 1-31 之间！', 'error');
        return;
    }
    
    // 生成密码
    const password = await generatePassword(month, day);
    
    // 显示密码
    const passwordDisplay = document.getElementById('customPassword');
    passwordDisplay.querySelector('.password-text').textContent = password;
    passwordDisplay.style.display = 'flex';
    
    showToast(`✅ ${month}月${day}日的密码已生成！`);
}

// 生成本周密码
async function generateWeek() {
    const today = new Date();
    const weekPasswords = [];
    
    // 生成7天的密码
    for (let i = 0; i < 7; i++) {
        const date = new Date(today);
        date.setDate(today.getDate() + i);
        
        const month = date.getMonth() + 1;
        const day = date.getDate();
        const password = await generatePassword(month, day);
        
        weekPasswords.push({
            date: formatDate(date),
            display: `${month.toString().padStart(2, '0')}月${day.toString().padStart(2, '0')}日`,
            password: password
        });
    }
    
    // 生成表格
    let tableHTML = `
        <table class="week-table">
            <thead>
                <tr>
                    <th>日期</th>
                    <th>星期</th>
                    <th>密码</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    weekPasswords.forEach(item => {
        const parts = item.date.split(' ');
        tableHTML += `
            <tr>
                <td>${item.display}</td>
                <td>${parts[1] || ''}</td>
                <td class="password-cell">${item.password}</td>
            </tr>
        `;
    });
    
    tableHTML += `
            </tbody>
        </table>
    `;
    
    document.getElementById('weekPasswords').innerHTML = tableHTML;
    showToast('✅ 本周密码已生成！');
}

// 页面加载时自动生成今日密码
window.addEventListener('DOMContentLoaded', () => {
    generateToday();
});

// 添加回车键支持
document.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const monthInput = document.getElementById('monthInput');
        const dayInput = document.getElementById('dayInput');
        
        if (document.activeElement === monthInput || document.activeElement === dayInput) {
            generateCustom();
        }
    }
});