// Backend API Configuration
const backendUrl = 'https://unhastily-unpadlocked-marlen.ngrok-free.dev';

// Override callOpenClawAI to use backend
const originalCallOpenClawAI = window.callOpenClawAI;

window.callOpenClawAI = async function(userMessage) {
    const lowerMsg = userMessage.toLowerCase();
    
    // Theme switching (local)
    if (lowerMsg.includes('日系') || lowerMsg.includes('anime')) {
        currentTheme = 'anime';
        document.querySelectorAll('.theme-card').forEach(c => c.classList.remove('active'));
        document.querySelector('.theme-card[data-theme="anime"]')?.classList.add('active');
        return `🎨 已切换到主题: ${themeStyles.anime.name}\n\n你可以说"生成分镜"来创建9格画面`;
    }
    if (lowerMsg.includes('赛博') || lowerMsg.includes('cyberpunk')) {
        currentTheme = 'cyberpunk';
        document.querySelectorAll('.theme-card').forEach(c => c.classList.remove('active'));
        document.querySelector('.theme-card[data-theme="cyberpunk"]')?.classList.add('active');
        return `🤖 已切换到主题: ${themeStyles.cyberpunk.name}`;
    }
    if (lowerMsg.includes('古风') || lowerMsg.includes('traditional')) {
        currentTheme = 'traditional';
        document.querySelectorAll('.theme-card').forEach(c => c.classList.remove('active'));
        document.querySelector('.theme-card[data-theme="traditional"]')?.classList.add('active');
        return `🏯 已切换到主题: ${themeStyles.traditional.name}`;
    }
    if (lowerMsg.includes('仙侠') || lowerMsg.includes('xianxia')) {
        currentTheme = 'xianxia';
        document.querySelectorAll('.theme-card').forEach(c => c.classList.remove('active'));
        document.querySelector('.theme-card[data-theme="xianxia"]')?.classList.add('active');
        return `⚔️ 已切换到主题: ${themeStyles.xianxia.name}`;
    }
    if (lowerMsg.includes('写实') || lowerMsg.includes('realistic')) {
        currentTheme = 'realistic';
        document.querySelectorAll('.theme-card').forEach(c => c.classList.remove('active'));
        document.querySelector('.theme-card[data-theme="realistic"]')?.classList.add('active');
        return `📸 已切换到主题: ${themeStyles.realistic.name}`;
    }
    
    // Generate storyboard (local)
    if (lowerMsg.includes('生成') || lowerMsg.includes('创建') || lowerMsg.includes('制作')) {
        generateAllFrames();
        return `🎬 开始生成9格分镜，主题: ${themeStyles[currentTheme].name}`;
    }
    
    // Export (local)
    if (lowerMsg.includes('导出') || lowerMsg.includes('下载')) {
        exportAllFrames();
        return `📦 开始导出9张分镜图`;
    }
    
    // Clear (local)
    if (lowerMsg.includes('清空') || lowerMsg.includes('重置')) {
        clearStoryboard();
        return `🗑️ 已清空所有分镜`;
    }
    
    // Call backend API for other messages
    try {
        const response = await fetch(`${backendUrl}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                agent: 'ceo',
                message: userMessage
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            return data.response || '收到你的消息！';
        } else {
            throw new Error('Backend error');
        }
    } catch (error) {
        console.error('Backend call failed:', error);
        return `我是 OpenClaw 分镜助手\n\n🎨 切换主题: "日系动漫" "赛博朋克" "古风传统"\n🎬 生成分镜: "生成分镜"\n📦 其他功能: "导出图片" "清空分镜"`;
    }
};

console.log('Backend API connected: ' + backendUrl);