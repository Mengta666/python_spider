const puppeteer = require('puppeteer');
const fs = require('fs');

const scriptContent = fs.readFileSync('81.js', 'utf8');

(async () => {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36');
    await page.goto('https://www.zhihu.com/topic/19550517/top-answers', { waitUntil: 'networkidle2' });

    // 注入 81.js
    await page.evaluate(scriptContent);

    // 执行 R 函数
    const result = await page.evaluate(() => {
        const d = 'U1oTCk7iI1E2nDNofzyCRSbQNPVigmgUUPxVHzyjRDcJqWMSNWppH1abNGN887oAIddkmEEIMd7USU0wfxJYCVw=#UVAUC0ngKVY3mzFieD2FRyzXNfJgiG8VV_5fGD2kRj0OqGQQP21oGFSRM2J78bAHINBmkkYJNtzeTkw3fRhfCFs=#zYJpNQH1tKdZu6MXiXsoW6aiFZ6PslrUB9g93haqwei';
        return R(d);
    });

    console.log('Result:', result, 'Length:', result.length);

    await browser.close();
})();