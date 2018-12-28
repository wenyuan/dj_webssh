/**
 * Created by winyuan on 2018/10/15.
 */

function WebSSHClient() {
    this.heartBeatInterval = 30000;
    this.heartBeatTimer = null;
    this.serverTimer = null;
}

WebSSHClient.prototype._generateURL = function (options) {
    let protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    let url = protocol + '://' + window.location.host + '/host/' + encodeURIComponent(options.des_id) + '/';
    return url
};


WebSSHClient.prototype.connect = function (options) {
    // ws://192.168.1.108:8000/host/3/
    let desUrl = this._generateURL(options);
    let self = this;

    if (window.WebSocket) {
        this._connection = new WebSocket(desUrl);
    }
    else if (window.MozWebSocket) {
        this._connection = new MozWebSocket(desUrl);
    }
    else {
        options.onError('当前浏览器不支持WebSocket！');
        return;
    }

    this._connection.onopen = function () {
        options.onConnect();
        self.stopHeartBeatCheck().startHeartBeatCheck()
    };

    this._connection.onmessage = function (evt) {
        let data = JSON.parse(evt.data.toString());
        if (data.error !== undefined) {
            options.onError(data.error);
        } else if (data.data === 'heart beat check...') {
        } else {
            options.onData(data.data);
        }
        self.stopHeartBeatCheck().startHeartBeatCheck()
    };

    this._connection.onclose = function (evt) {
        self.stopHeartBeatCheck();
        options.onClose();
    };
};

WebSSHClient.prototype.send = function (data) {
    this._connection.send(JSON.stringify({'data': data}));
};

WebSSHClient.prototype.close = function () {
    this._connection.close()
};

WebSSHClient.prototype.startHeartBeatCheck = function () {
    let self = this;
    if (this._connection.readyState === this._connection.OPEN) {
        this.heartBeatTimer = window.setInterval(function () {
            self._connection.send(JSON.stringify({'data': 'heart beat check...'}))
            self.serverTimer = window.setInterval(function () {
                self._connection.close()
            }, self.heartBeatInterval)
        }, this.heartBeatInterval)
    }
};

WebSSHClient.prototype.stopHeartBeatCheck = function () {
    window.clearInterval(this.heartBeatTimer);
    window.clearInterval(this.serverTimer);
    return this
};
