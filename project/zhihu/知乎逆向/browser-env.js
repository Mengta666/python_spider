const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const fetch = require('node-fetch');
const toughCookie = require('tough-cookie');
const { CookieJar } = toughCookie;

// 创建一个模拟的浏览器环境
function createBrowserEnv(options = {}) {
    const cookieJar = new CookieJar();

    // 配置选项，允许自定义
    const config = {
        url: options.url || 'http://localhost',
        userAgent: options.userAgent || 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        viewport: options.viewport || { width: 1920, height: 1080 },
        language: options.language || 'zh-CN',
        ...options
    };

    // 初始化 JSDOM，创建一个虚拟的 DOM 环境
    const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>', {
        url: config.url,
        resources: 'usable',
        runScripts: 'dangerously',
        pretendToBeVisual: true,
        cookieJar: cookieJar
    });

    // 获取 window 和 document 对象
    const window = dom.window;
    const document = window.document;

    // 模拟 navigator 对象
    const navigator = {
        userAgent: config.userAgent,
        platform: options.platform || 'Win32',
        language: config.language,
        languages: [config.language, 'en-US'],
        cookieEnabled: true,
        onLine: true,
        javaEnabled: () => false,
        vibrate: () => false,
        credentials: {
            get: () => Promise.resolve(null),
            store: () => Promise.resolve(undefined)
        },
        getBattery: () => Promise.resolve({
            charging: true,
            chargingTime: 0,
            dischargingTime: Infinity,
            level: 1.0
        }),
        geolocation: {
            getCurrentPosition: (success, error) => {
                if (error) error({ code: 1, message: 'Geolocation permission denied' });
            },
            watchPosition: () => 0,
            clearWatch: () => {}
        },
        mediaDevices: {
            getUserMedia: () => Promise.reject(new Error('Not implemented')),
            enumerateDevices: () => Promise.resolve([])
        },
        plugins: [],
        mimeTypes: []
    };

    // 模拟 localStorage
    const localStorage = (function() {
        let store = {};
        return {
            getItem: (key) => store[key] || null,
            setItem: (key, value) => store[key] = value.toString(),
            removeItem: (key) => delete store[key],
            clear: () => store = {},
            key: (index) => Object.keys(store)[index] || null,
            get length() { return Object.keys(store).length; }
        };
    })();

    // 模拟 sessionStorage
    const sessionStorage = (function() {
        let store = {};
        return {
            getItem: (key) => store[key] || null,
            setItem: (key, value) => store[key] = value.toString(),
            removeItem: (key) => delete store[key],
            clear: () => store = {},
            key: (index) => Object.keys(store)[index] || null,
            get length() { return Object.keys(store).length; }
        };
    })();

    // 模拟 history API
    const history = {
        _entries: [{ url: config.url, title: document.title, state: null }],
        _index: 0,
        get length() { return this._entries.length; },
        get state() { return this._entries[this._index].state; },
        back() { if (this._index > 0) this._index--; },
        forward() { if (this._index < this._entries.length - 1) this._index++; },
        go(delta) {
            const newIndex = this._index + delta;
            if (newIndex >= 0 && newIndex < this._entries.length) {
                this._index = newIndex;
            }
        },
        pushState(state, title, url) {
            this._entries = this._entries.slice(0, this._index + 1);
            this._entries.push({ url, title, state });
            this._index = this._entries.length - 1;
        },
        replaceState(state, title, url) {
            this._entries[this._index] = { url, title, state };
        }
    };

    // 创建一个自定义的位置对象，代理到真实的window.location
    const customLocation = {
        get href() { return window.location.href; },
        set href(value) { window.location.href = value; },
        get protocol() { return window.location.protocol; },
        set protocol(value) { window.location.protocol = value; },
        get host() { return window.location.host; },
        set host(value) { window.location.host = value; },
        get hostname() { return window.location.hostname; },
        set hostname(value) { window.location.hostname = value; },
        get port() { return window.location.port; },
        set port(value) { window.location.port = value; },
        get pathname() { return window.location.pathname; },
        set pathname(value) { window.location.pathname = value; },
        get search() { return window.location.search; },
        set search(value) { window.location.search = value; },
        get hash() { return window.location.hash; },
        set hash(value) { window.location.hash = value; },
        get origin() { return window.location.origin; },

        // 方法也代理到真实的window.location
        replace(url) { window.location.replace(url); },
        assign(url) { window.location.assign(url); },
        reload() { window.location.reload(); },
        toString() { return window.location.toString(); }
    };

    // 模拟 XMLHttpRequest
    class CustomXMLHttpRequest {
        constructor() {
            this.readyState = 0;
            this.response = null;
            this.responseText = '';
            this.responseType = '';
            this.responseURL = '';
            this.status = 0;
            this.statusText = '';
            this.timeout = 0;
            this.withCredentials = false;
            this._requestHeaders = {};
            this._method = null;
            this._url = null;
            this._async = true;
            this._data = null;
            this._aborted = false;
            this._listeners = {
                readystatechange: [],
                load: [],
                error: [],
                timeout: [],
                abort: [],
                loadend: []
            };
        }

        open(method, url, async = true, username = null, password = null) {
            this._method = method;
            this._url = url;
            this._async = async;
            this.readyState = 1;
            this._dispatchEvent('readystatechange');
        }

        setRequestHeader(header, value) {
            this._requestHeaders[header] = value;
        }

        addEventListener(type, listener) {
            if (this._listeners[type]) {
                this._listeners[type].push(listener);
            }
        }

        removeEventListener(type, listener) {
            if (this._listeners[type]) {
                const index = this._listeners[type].indexOf(listener);
                if (index !== -1) {
                    this._listeners[type].splice(index, 1);
                }
            }
        }

        _dispatchEvent(type, event = {}) {
            if (this._listeners[type]) {
                const listeners = this._listeners[type].slice();
                for (const listener of listeners) {
                    listener.call(this, { ...event, type, target: this });
                }
            }
            if (type !== 'readystatechange' && this[`on${type}`]) {
                this[`on${type}`]({ ...event, type, target: this });
            }
        }

        send(data = null) {
            this._data = data;

            if (this._aborted) return;

            this.readyState = 2;
            this._dispatchEvent('readystatechange');

            const handleResponse = (response) => {
                if (this._aborted) return;

                setTimeout(() => {
                    this.status = response.status;
                    this.statusText = response.statusText;
                    this.responseURL = response.url;

                    this.readyState = 3;
                    this._dispatchEvent('readystatechange');

                    response.text().then(text => {
                        if (this._aborted) return;

                        this.responseText = text;
                        this.response = text;

                        this.readyState = 4;
                        this._dispatchEvent('readystatechange');
                        this._dispatchEvent('load');
                        this._dispatchEvent('loadend');
                    });
                }, 0);
            };

            const handleError = (error) => {
                if (this._aborted) return;

                this.readyState = 4;
                this._dispatchEvent('readystatechange');
                this._dispatchEvent('error', { error });
                this._dispatchEvent('loadend');
            };

            try {
                const fetchOptions = {
                    method: this._method,
                    headers: this._requestHeaders,
                    body: this._data,
                    credentials: this.withCredentials ? 'include' : 'same-origin',
                    redirect: 'follow'
                };

                const timeoutPromise = new Promise((_, reject) => {
                    if (this.timeout > 0) {
                        setTimeout(() => {
                            if (this.readyState !== 4) {
                                this._aborted = true;
                                reject(new Error('Timeout'));
                                this._dispatchEvent('timeout');
                                this._dispatchEvent('loadend');
                            }
                        }, this.timeout);
                    }
                });

                Promise.race([
                    fetch(this._url, fetchOptions),
                    timeoutPromise
                ])
                .then(handleResponse)
                .catch(handleError);

            } catch (error) {
                handleError(error);
            }
        }

        abort() {
            if (this.readyState === 0 || this.readyState === 4) return;

            this._aborted = true;
            this.readyState = 4;
            this.status = 0;
            this.statusText = '';

            this._dispatchEvent('abort');
            this._dispatchEvent('loadend');
        }

        getAllResponseHeaders() {
            // 简单模拟，实际应用中应该从response中提取
            return '';
        }

        getResponseHeader(name) {
            // 简单模拟，实际应用中应该从response中提取
            return null;
        }
    }

    // 模拟 fetch API
    const customFetch = (url, options = {}) => {
        // 为了简化，直接使用node-fetch
        return fetch(url, {
            ...options,
            headers: {
                ...options.headers,
                'User-Agent': navigator.userAgent
            }
        });
    };

    // 模拟 Screen 对象
    const screen = {
        availWidth: config.viewport.width,
        availHeight: config.viewport.height,
        width: config.viewport.width,
        height: config.viewport.height,
        colorDepth: 24,
        pixelDepth: 24,
        orientation: {
            type: 'landscape-primary',
            angle: 0,
            onchange: null
        }
    };

    // 模拟 Performance API
    const performance = {
        now: () => {
            const [seconds, nanoseconds] = process.hrtime();
            return seconds * 1000 + nanoseconds / 1000000;
        },
        timing: {
            navigationStart: Date.now(),
            domComplete: Date.now()
        },
        mark: () => {},
        measure: () => {},
        getEntriesByType: () => [],
        getEntriesByName: () => []
    };

    // 更完整的事件处理系统
    class EventTarget {
        constructor() {
            this._listeners = new Map();
        }

        addEventListener(type, listener, options = {}) {
            if (typeof listener !== 'function') return;

            if (!this._listeners.has(type)) {
                this._listeners.set(type, new Set());
            }

            const listeners = this._listeners.get(type);
            listeners.add({
                callback: listener,
                once: options.once || false
            });
        }

        removeEventListener(type, listener) {
            if (!this._listeners.has(type)) return;

            const listeners = this._listeners.get(type);
            for (const entry of listeners) {
                if (entry.callback === listener) {
                    listeners.delete(entry);
                    break;
                }
            }

            if (listeners.size === 0) {
                this._listeners.delete(type);
            }
        }

        dispatchEvent(event) {
            if (!event || !event.type) return true;

            const type = event.type;
            if (!this._listeners.has(type)) return true;

            // 设置目标
            if (!event.target) {
                Object.defineProperty(event, 'target', { value: this });
            }

            if (!event.currentTarget) {
                Object.defineProperty(event, 'currentTarget', { value: this });
            }

            // 阻止默认行为和传播标志
            let defaultPrevented = false;
            let propagationStopped = false;

            Object.defineProperties(event, {
                preventDefault: {
                    value: function() { defaultPrevented = true; }
                },
                isDefaultPrevented: {
                    value: function() { return defaultPrevented; }
                },
                stopPropagation: {
                    value: function() { propagationStopped = true; }
                },
                isPropagationStopped: {
                    value: function() { return propagationStopped; }
                }
            });

            // 复制监听器列表，防止在遍历过程中修改
            const listeners = Array.from(this._listeners.get(type));

            for (const entry of listeners) {
                if (propagationStopped) break;

                try {
                    entry.callback.call(this, event);
                } catch (error) {
                    console.error(`Error in event handler for ${type}:`, error);
                }

                if (entry.once) {
                    this.removeEventListener(type, entry.callback);
                }
            }

            return !defaultPrevented;
        }
    }

    // 模拟 WebSocket
    class WebSocket extends EventTarget {
        constructor(url, protocols) {
            super();
            this.url = url;
            this.protocols = protocols;
            this.readyState = 0; // CONNECTING
            this.bufferedAmount = 0;
            this.extensions = '';
            this.protocol = '';

            // WebSocket 状态常量
            this.CONNECTING = 0;
            this.OPEN = 1;
            this.CLOSING = 2;
            this.CLOSED = 3;

            // 模拟连接
            setTimeout(() => {
                this.readyState = 1; // OPEN
                this.dispatchEvent(new window.Event('open'));
            }, 100);
        }

        send(data) {
            if (this.readyState !== 1) {
                throw new Error('WebSocket is not open');
            }

            // 模拟发送数据
            this.bufferedAmount += String(data).length;
            setTimeout(() => {
                this.bufferedAmount = 0;
            }, 50);
        }

        close(code, reason) {
            if (this.readyState === 0 || this.readyState === 1) {
                this.readyState = 2; // CLOSING

                setTimeout(() => {
                    this.readyState = 3; // CLOSED

                    const closeEvent = new window.Event('close');
                    closeEvent.code = code || 1000;
                    closeEvent.reason = reason || '';
                    closeEvent.wasClean = true;

                    this.dispatchEvent(closeEvent);
                }, 50);
            }
        }
    }

    // 模拟 Canvas 功能
    // 不使用 customElements.define，而是直接扩展功能

    // 模拟 CanvasRenderingContext2D
    class CanvasRenderingContext2D {
        constructor(canvas) {
            this.canvas = canvas;
            this.fillStyle = '#000000';
            this.strokeStyle = '#000000';
            this.lineWidth = 1;
            this.font = '10px sans-serif';
            this.textAlign = 'start';
            this.textBaseline = 'alphabetic';
            this.globalAlpha = 1.0;
            this.globalCompositeOperation = 'source-over';
            this.imageSmoothingEnabled = true;
            this._path = [];
        }

        // 实现基本方法
        fillRect() {}
        strokeRect() {}
        clearRect() {}
        beginPath() { this._path = []; }
        closePath() {}
        moveTo(x, y) { this._path.push(['M', x, y]); }
        lineTo(x, y) { this._path.push(['L', x, y]); }
        bezierCurveTo() {}
        quadraticCurveTo() {}
        arc() {}
        arcTo() {}
        rect() {}
        fill() {}
        stroke() {}
        clip() {}
        isPointInPath() { return false; }
        isPointInStroke() { return false; }
        measureText(text) { return { width: text.length * 5 }; }
        fillText() {}
        strokeText() {}
        setLineDash() {}
        getLineDash() { return []; }
        createLinearGradient() { return { addColorStop: () => {} }; }
        createRadialGradient() { return { addColorStop: () => {} }; }
        createPattern() { return null; }
        drawImage() {}
        createImageData() { return { data: new Uint8ClampedArray(), width: 0, height: 0 }; }
        getImageData() { return { data: new Uint8ClampedArray(), width: 0, height: 0 }; }
        putImageData() {}
        save() {}
        restore() {}
        scale() {}
        rotate() {}
        translate() {}
        transform() {}
        setTransform() {}
        resetTransform() {}
    }

    // 扩展原生 Canvas 功能
    const originalCreateElement = document.createElement.bind(document);
    document.createElement = function(tagName, options) {
        const element = originalCreateElement(tagName, options);

        // 如果创建的是canvas元素，添加额外功能
        if (tagName.toLowerCase() === 'canvas') {
            element.width = 300;
            element.height = 150;

            element.getContext = function(contextType) {
                if (contextType === '2d') {
                    return new CanvasRenderingContext2D(this);
                }
                return null;
            };

            element.toDataURL = function() {
                return 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg==';
            };

            element.toBlob = function(callback) {
                const byteString = atob('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg==');
                const ab = new ArrayBuffer(byteString.length);
                const ia = new Uint8Array(ab);
                for (let i = 0; i < byteString.length; i++) {
                    ia[i] = byteString.charCodeAt(i);
                }
                const blob = new Blob([ab], { type: 'image/png' });
                callback(blob);
            };
        }

        return element;
    };

    // 为 window 注入更多浏览器API
    window.localStorage = localStorage;
    window.sessionStorage = sessionStorage;
    window.navigator = navigator;
    window.history = history;
    window.XMLHttpRequest = CustomXMLHttpRequest;
    window.fetch = customFetch;
    window.WebSocket = WebSocket;
    window.screen = screen;
    window.performance = performance;
    window.console = console;
    window.setTimeout = setTimeout;
    window.setInterval = setInterval;
    window.clearTimeout = clearTimeout;
    window.clearInterval = clearInterval;
    window.requestAnimationFrame = callback => setTimeout(() => callback(performance.now()), 16);
    window.cancelAnimationFrame = id => clearTimeout(id);

    // 为 window 和 document 添加 EventTarget 方法
    const windowEventTarget = new EventTarget();
    const documentEventTarget = new EventTarget();

    // 合并EventTarget方法到window和document
    ['addEventListener', 'removeEventListener', 'dispatchEvent'].forEach(method => {
        window[method] = windowEventTarget[method].bind(windowEventTarget);
        document[method] = documentEventTarget[method].bind(documentEventTarget);
    });

    // 模拟更多Web API
    window.Blob = global.Blob || class Blob {
        constructor(parts, options = {}) {
            this.parts = parts;
            this.type = options.type || '';
            this.size = parts.reduce((size, part) => {
                return size + (part instanceof ArrayBuffer ? part.byteLength : String(part).length);
            }, 0);
        }
    };

    window.File = global.File || class File extends window.Blob {
        constructor(parts, name, options = {}) {
            super(parts, options);
            this.name = name;
            this.lastModified = options.lastModified || Date.now();
        }
    };

    window.FileReader = global.FileReader || class FileReader extends EventTarget {
        constructor() {
            super();
            this.readyState = 0; // EMPTY
            this.result = null;
            this.error = null;
        }

        readAsArrayBuffer(blob) {
            this._read(blob, 'arraybuffer');
        }

        readAsText(blob, encoding) {
            this._read(blob, 'text');
        }

        readAsDataURL(blob) {
            this._read(blob, 'dataurl');
        }

        abort() {
            this.readyState = 0; // EMPTY
            this.result = null;
            this.dispatchEvent(new window.Event('abort'));
        }

        _read(blob, type) {
            this.readyState = 1; // LOADING
            this.dispatchEvent(new window.Event('loadstart'));

            setTimeout(() => {
                try {
                    if (type === 'text') {
                        this.result = blob.parts.map(p => String(p)).join('');
                    } else if (type === 'dataurl') {
                        this.result = `data:${blob.type};base64,dGVzdA==`; // "test" in base64
                    } else if (type === 'arraybuffer') {
                        const text = blob.parts.map(p => String(p)).join('');
                        const buffer = new ArrayBuffer(text.length);
                        const view = new Uint8Array(buffer);
                        for (let i = 0; i < text.length; i++) {
                            view[i] = text.charCodeAt(i);
                        }
                        this.result = buffer;
                    }

                    this.readyState = 2; // DONE
                    this.dispatchEvent(new window.Event('load'));
                    this.dispatchEvent(new window.Event('loadend'));
                } catch (e) {
                    this.error = e;
                    this.readyState = 2; // DONE
                    this.dispatchEvent(new window.Event('error'));
                    this.dispatchEvent(new window.Event('loadend'));
                }
            }, 50);
        }
    };

    // 返回模拟的浏览器环境
    return {
        window,
        document,
        navigator,
        localStorage,
        sessionStorage,
        location: customLocation,
        history,
        XMLHttpRequest: CustomXMLHttpRequest,
        fetch: customFetch,
        WebSocket,
        cookieJar
    };
}

// 导出模块
module.exports = {
    createBrowserEnv
};