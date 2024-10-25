/*
@Description: 微信小程序泡泡玛特
抓user_id和openid和 分别在请求头和请求参数里面 用#连接 多账号&或换行 分开 或新建同名变量
https://popvip.paquapp.com/miniapp/v2/wechat/getUserInfo/
[Script]
http-response

[MITM]
hostname = 


*/

const $ = new Env("微信小程序泡泡玛特");
let ckName = `paopaomate`
let userCookie = checkEnv($.isNode() ? process.env[ckName] : "");
const notify = $.isNode() ? require("./sendNotify") : "";



!(async () => {
    console.log(
        `==================================================\n 脚本执行 - 北京时间(UTC+8): ${new Date(
            new Date().getTime() +
            new Date().getTimezoneOffset() * 60 * 1000 +
            8 * 60 * 60 * 1000
).toLocaleString()} \n==================================================`
);
    //console.log(userCookie)
    if (!userCookie?.length) return console.log(`没有找到CK哦`)
    let index = 0;
    let strSplitor = "#";

    for (let user of userCookie) {
        $.log(`\n🚀 user:【${index || ++index}】 start work\n`)
        $.id = user.split(strSplitor)[0]
        $.openid = user.split(strSplitor)[1]
        $.ckStatus = false
        await UserInfo($.id, $.openid)
        if ($.ckStatus) {
            await SignIn($.openid)
        }

    }

    await $.sendMsg($.logs.join("\n"));
})().catch((e) => console.log(e)).finally(() => $.done());
function base64Encode(data) {
    const buffer = Buffer.from(data);
    return buffer.toString('base64');
}
function getSign(t, e, n) {
    function md5(data) {
        const crypto = require('crypto');
        return crypto.createHash('md5').update(data).digest('hex');
    }
    function d(t, e, n) {
        var o = {};
        Object.keys(t).sort().forEach((function (n) {
            o[n] = "POST" === e ? t[n] : t[n].toString()
        }
)),
            o.version = "5.0.34";
        var s = (new Date).getTime().toString()
            , c = JSON.stringify(o) + "PopMartminiApp1117" + s
            , u = md5(c);
        return t.sign = n ? md5(base64Encode(u + "PopMartminiApp0314")) : u,
            t.time = s,
            t.version = "5.0.34",
            t
    }

    return d(t, e, n)
}
async function SignIn() {
    let { sign: sign, time: time, version: version } = getSign({
        openid: $.openid
    }, 'GET', false)
    let { data: result } = await Request({
        method: 'GET',
        url: 'https://popvip.paquapp.com/miniapp/v2/sign_in/everySignDay/?openid=' + $.openid + '&sign=' + sign + '&time=' + time + '&version=' + version,
        headers: {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; MI 8 Lite Build/QKQ1.190910.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.120 Mobile Safari/537.36 XWEB/1220067 MMWEBSDK/20241001 MMWEBID/8150 MicroMessenger/8.0.49.2600(0x28003156) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'identity_code': $.openid,
            'charset': 'utf-8',
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Referer': 'https://servicewechat.com/wx9627eb7f4b1c69d5/638/page-frame.html'
        }
    })
    result?.code == 1 ? $.log(`签到状态：${result.data.sign}`) : ""
}
async function UserInfo() {
    let { sign: sign, time: time, version: version } = getSign({
        user_id: $.id
    }, 'GET', false)
    let { data: result } = await Request({
        method: 'GET',
        url: 'https://popvip.paquapp.com/miniapp/v2/wechat/getUserInfo/?user_id=' + $.id + '&sign=' + sign + '&time=' + time + '&version=' + version,
        headers: {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; MI 8 Lite Build/QKQ1.190910.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.120 Mobile Safari/537.36 XWEB/1220067 MMWEBSDK/20241001 MMWEBID/8150 MicroMessenger/8.0.49.2600(0x28003156) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'identity_code': $.openid,
            'charset': 'utf-8',
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Referer': 'https://servicewechat.com/wx9627eb7f4b1c69d5/638/page-frame.html'
        }
    })
    result?.code == 1 ? ($.log(`${result.data.nickname} 积分【${result.data.points}】`), $.ckStatus = true) : $.ckStatus = false
}

function checkEnv(userCookie) {
    const envSplitor = ["&", "\n"];
    let userList = userCookie.split(envSplitor.find(o => userCookie.includes(o)) || "&").filter(n => n);
    console.log(`共找到${userList.length}个账号`);
    return userList;
}
//Env Api =============================

function Env(t, s) {
    return new (class {
        constructor(t, s) {
            this.name = t;
            this.logs = [];
            this.logSeparator = "\n";
            this.startTime = new Date().getTime();
            Object.assign(this, s);
            this.log("", `\ud83d\udd14${this.name},\u5f00\u59cb!`);
        }
        isNode() {
            return "undefined" != typeof module && !!module.exports;
        }
        isQuanX() {
            return "undefined" != typeof $task;
        }

        queryStr(options) {
            return Object.entries(options)
                .map(
                    ([key, value]) =>
                        `${key}=${typeof value === "object" ? JSON.stringify(value) : value
                        }`
)
                .join("&");
        }
        getURLParams(url) {
            const params = {};
            const queryString = url.split("?")[1];
            if (queryString) {
                const paramPairs = queryString.split("&");
                paramPairs.forEach((pair) => {
                    const [key, value] = pair.split("=");
                    params[key] = value;
                });
            }
            return params;
        }
        isJSONString(str) {
            try {
                return JSON.parse(str) && typeof JSON.parse(str) === "object";
            } catch (e) {
                return false;
            }
        }
        isJson(obj) {
            var isjson =
                typeof obj == "object" &&
                Object.prototype.toString.call(obj).toLowerCase() ==
                "[object object]" &&
                !obj.length;
            return isjson;
        }
        async sendMsg(message) {
            if (!message) return;
            if (this.isNode()) {
                await notify.sendNotify(this.name, message);
            } else {
                this.msg(this.name, "", message);
            }
        }
        randomNumber(length) {
            const characters = "0123456789";
            return Array.from(
                { length },
                () => characters[Math.floor(Math.random() * characters.length)]
).join("");
        }
        randomString(length) {
            const characters = "abcdefghijklmnopqrstuvwxyz0123456789";
            return Array.from(
                { length },
                () => characters[Math.floor(Math.random() * characters.length)]
).join("");
        }
        uuid() {
            return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(
                /[xy]/g,
                function (c) {
                    var r = (Math.random() * 16) | 0,
                        v = c == "x" ? r : (r & 0x3) | 0x8;
                    return v.toString(16);
                }
);
        }
        time(t) {
            let s = {
                "M+": new Date().getMonth() + 1,
                "d+": new Date().getDate(),
                "H+": new Date().getHours(),
                "m+": new Date().getMinutes(),
                "s+": new Date().getSeconds(),
                "q+": Math.floor((new Date().getMonth() + 3) / 3),
                S: new Date().getMilliseconds(),
            };
            /(y+)/.test(t) &&
                (t = t.replace(
                    RegExp.$1,
                    (new Date().getFullYear() + "").substr(4 - RegExp.$1.length)
));
            for (let e in s) {
                new RegExp("(" + e + ")").test(t) &&
                    (t = t.replace(
                        RegExp.$1,
                        1 == RegExp.$1.length
                            ? s[e]
                            : ("00" + s[e]).substr(("" + s[e]).length)
));
            }
            return t;
        }
        msg(title = t, subtitle = "", body = "", options) {
            const formatOptions = (options) => {
                if (!options) {
                    return options;
                } else if (typeof options === "string") {
                    if (this.isQuanX()) {
                        return { "open-url": options };
                    } else {
                        return undefined;
                    }
                } else if (
                    typeof options === "object" &&
                    (options["open-url"] || options["media-url"])
) {
                    if (this.isQuanX()) {
                        return options;
                    } else {
                        return undefined;
                    }
                } else {
                    return undefined;
                }
            };
            if (!this.isMute) {
                if (this.isQuanX()) {
                    $notify(title, subtitle, body, formatOptions(options));
                }
            }
            let logs = ["", "==============📣系统通知📣=============="];
            logs.push(title);
            subtitle ? logs.push(subtitle) : "";
            body ? logs.push(body) : "";
            console.log(logs.join("\n"));
            this.logs = this.logs.concat(logs);
        }
        log(...t) {
            t.length > 0 && (this.logs = [...this.logs, ...t]),
                console.log(t.join(this.logSeparator));
        }
        logErr(t, s) {
            const e = !this.isQuanX();
            e
                ? this.log("", `\u2757\ufe0f${this.name},\u9519\u8bef!`, t.stack)
                : this.log("", `\u2757\ufe0f${this.name},\u9519\u8bef!`, t);
        }
        wait(t) {
            return new Promise((s) => setTimeout(s, t));
        }
        done(t = {}) {
            const s = new Date().getTime(),
                e = (s - this.startTime) / 1e3;
            this.log(
                "",
                `\ud83d\udd14${this.name},\u7ed3\u675f!\ud83d\udd5b ${e}\u79d2`
);
            this.log();
            if (this.isNode()) {
                process.exit(1);
            }
            if (this.isQuanX()) {
                $done(t);
            }
        }
    })(t, s);
}

async function Request(options) {
    if ($.isNode()) {
        const axios = require("axios");
        Request = async (options) => {
            try {
                return await axios.request(options);
            } catch (error) {
                throw error && error.error ? error.error : "请求失败";
            }
        };
    }
    if ($.isQuanX()) {
        Request = async (options) => {
            try {
                return await $task.fetch(options);
            } catch (error) {
                throw error && error.error ? error.error : "请求失败";
            }
        };
    }
    return await Request(options)
}

