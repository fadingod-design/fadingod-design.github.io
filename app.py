#!/usr/bin/env python3
"""
WindQuant 金融数据 API 服务
提供 A股、美股实时数据
"""
from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

HEADERS = {
    'Referer': 'https://finance.sina.com.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

@app.route('/api/indices/cn')
def get_cn_indices():
    """获取中国指数"""
    codes = {
        '上证指数': 's_sh000001',
        '深证成指': 's_sz399001',
        '创业板': 's_sz399006',
        '沪深300': 's_sh000300',
        '科创50': 's_sh000688'
    }
    result = []
    for name, code in codes.items():
        try:
            resp = requests.get(f"https://hq.sinajs.cn/list={code}", headers=HEADERS, timeout=10)
            data = resp.text.split('"')[1].split(',')
            result.append({
                'name': name,
                'price': float(data[1]),
                'change': float(data[2]),
                'changePercent': float(data[3])
            })
        except:
            pass
    return jsonify(result)

@app.route('/api/stocks/cn')
def get_cn_stocks():
    """获取A股热门股票"""
    codes = ['sh600036', 'sh601318', 'sh600519', 'sh000858', 'sh600900',
             'sz000858', 'sz002594', 'sz300750', 'sz000001', 'sh688981']
    result = []
    for code in codes:
        try:
            resp = requests.get(f"https://hq.sinajs.cn/list={code}", headers=HEADERS, timeout=10)
            data = resp.text.split('"')[1].split(',')
            result.append({
                'code': code,
                'name': data[0],
                'price': float(data[3]),
                'change': float(data[3]) - float(data[2]),
                'changePercent': ((float(data[3]) - float(data[2])) / float(data[2]) * 100) if float(data[2]) > 0 else 0
            })
        except:
            pass
    return jsonify(result)

@app.route('/api/stocks/us')
def get_us_stocks():
    """获取美股数据"""
    stocks = {
        'AAPL': '苹果',
        'NVDA': '英伟达',
        'MSFT': '微软',
        'TSLA': '特斯拉',
        'GOOGL': '谷歌',
        'AMZN': '亚马逊',
        'META': 'Meta',
        'BRK.B': '伯克希尔'
    }
    result = []
    for ticker, name in stocks.items():
        try:
            resp = requests.get(f"https://hq.sinajs.cn/list=gb_{ticker.lower().replace('.', '')}", headers=HEADERS, timeout=10)
            data = resp.text.split('"')[1].split(',')
            result.append({
                'ticker': ticker,
                'name': name,
                'price': float(data[1]),
                'change': float(data[2]),
                'changePercent': (float(data[2]) / (float(data[1]) - float(data[2])) * 100) if float(data[1]) > float(data[2]) else 0
            })
        except Exception as e:
            pass
    return jsonify(result)

@app.route('/api/ticker')
def get_ticker():
    """获取跑马灯数据"""
    tickers = [
        ('sh000001', '上证指数'), ('sz399001', '深证成指'), ('sz399006', '创业板'),
        ('gb_aapl', 'AAPL'), ('gb_nvda', 'NVDA'), ('gb_msft', 'MSFT'),
        ('gb_tsla', 'TSLA'), ('gb_googl', 'GOOGL'), ('gb_amzn', 'AMZN'),
        ('gb_meta', 'META')
    ]
    result = []
    for code, name in tickers:
        try:
            resp = requests.get(f"https://hq.sinajs.cn/list={code}", headers=HEADERS, timeout=10)
            data = resp.text.split('"')[1].split(',')
            if code.startswith('gb_'):
                price = float(data[1])
                change = float(data[2])
            else:
                price = float(data[1])
                change = float(data[3])
            result.append({'name': name, 'price': price, 'change': change})
        except:
            pass
    return jsonify(result)

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
