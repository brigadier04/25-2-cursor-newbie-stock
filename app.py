from flask import Flask, render_template, request, jsonify
import requests
import json
import threading
import time
from datetime import datetime
import os

app = Flask(__name__)

# 관심 주식 목록 (메모리 저장)
watchlist = []

# 주식 데이터 캐시
stock_cache = {}

# 알림 임계값 (3%)
ALERT_THRESHOLD = 3.0

def get_us_stock_price(symbol):
    """미국 주식 가격 조회 (Alpha Vantage API 사용)"""
    try:
        # 무료 API 키 사용 (실제 사용시에는 환경변수로 설정)
        api_key = "demo"  # 실제 API 키로 교체 필요
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
        
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if 'Global Quote' in data and data['Global Quote']:
            quote = data['Global Quote']
            return {
                'symbol': symbol,
                'price': float(quote['05. price']),
                'change': float(quote['09. change']),
                'change_percent': float(quote['10. change percent'].replace('%', '')),
                'volume': int(quote['06. volume']),
                'market': 'US'
            }
    except Exception as e:
        print(f"미국 주식 {symbol} 조회 오류: {e}")
        return None

def get_kr_stock_price(symbol):
    """한국 주식 가격 조회 (실제로는 한국투자증권 API 등 사용)"""
    try:
        # 한국 주식은 실제 API 연동이 필요하므로 샘플 데이터 사용
        # 실제 구현시에는 한국투자증권 API 또는 다른 한국 주식 API 사용
        sample_data = {
            '005930': {'name': '삼성전자', 'price': 75000, 'change': 3000, 'change_percent': 2.04},
            '000660': {'name': 'SK하이닉스', 'price': 120000, 'change': -2000, 'change_percent': -1.64},
            '035420': {'name': 'NAVER', 'price': 180000, 'change': 3000, 'change_percent': 1.69}
        }
        
        if symbol in sample_data:
            data = sample_data[symbol]
            return {
                'symbol': symbol,
                'name': data['name'],
                'price': data['price'],
                'change': data['change'],
                'change_percent': data['change_percent'],
                'market': 'KR'
            }
    except Exception as e:
        print(f"한국 주식 {symbol} 조회 오류: {e}")
        return None

def check_price_alerts():
    """가격 변동 알림 확인"""
    while True:
        try:
            for stock in watchlist:
                symbol = stock['symbol']
                market = stock['market']
                
                # 주식 데이터 조회
                if market == 'US':
                    data = get_us_stock_price(symbol)
                else:
                    data = get_kr_stock_price(symbol)
                
                if data and abs(data['change_percent']) >= ALERT_THRESHOLD:
                    alert_message = f"🚨 알림! {data.get('name', symbol)} ({symbol}) {data['change_percent']:+.2f}% 변동 (현재가: {data['price']:,}원)"
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {alert_message}")
                    
                    # 콘솔에 색상으로 표시
                    if data['change_percent'] > 0:
                        print(f"\033[92m{alert_message}\033[0m")  # 초록색
                    else:
                        print(f"\033[91m{alert_message}\033[0m")  # 빨간색
                
                # 캐시 업데이트
                stock_cache[symbol] = data
                
        except Exception as e:
            print(f"알림 확인 중 오류: {e}")
        
        # 30초마다 확인
        time.sleep(30)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    """주식 목록 조회"""
    return jsonify(list(stock_cache.values()))

@app.route('/api/watchlist', methods=['GET'])
def get_watchlist():
    """관심 주식 목록 조회"""
    return jsonify(watchlist)

@app.route('/api/watchlist', methods=['POST'])
def add_to_watchlist():
    """관심 주식 추가"""
    data = request.json
    symbol = data.get('symbol')
    market = data.get('market')
    name = data.get('name', symbol)
    
    # 중복 확인
    if not any(stock['symbol'] == symbol and stock['market'] == market for stock in watchlist):
        watchlist.append({
            'symbol': symbol,
            'market': market,
            'name': name,
            'added_at': datetime.now().isoformat()
        })
        
        # 즉시 가격 조회
        if market == 'US':
            stock_data = get_us_stock_price(symbol)
        else:
            stock_data = get_kr_stock_price(symbol)
        
        if stock_data:
            stock_cache[symbol] = stock_data
        
        return jsonify({'success': True, 'message': f'{name} ({symbol})이 관심 목록에 추가되었습니다.'})
    
    return jsonify({'success': False, 'message': '이미 관심 목록에 있는 주식입니다.'})

@app.route('/api/watchlist/<symbol>', methods=['DELETE'])
def remove_from_watchlist(symbol):
    """관심 주식 제거"""
    global watchlist
    watchlist = [stock for stock in watchlist if stock['symbol'] != symbol]
    return jsonify({'success': True, 'message': '관심 목록에서 제거되었습니다.'})

@app.route('/api/search', methods=['GET'])
def search_stocks():
    """주식 검색"""
    query = request.args.get('q', '').upper()
    results = []
    
    # 샘플 검색 결과 (실제로는 API에서 검색)
    sample_stocks = [
        {'symbol': 'AAPL', 'name': 'Apple Inc.', 'market': 'US'},
        {'symbol': 'MSFT', 'name': 'Microsoft Corporation', 'market': 'US'},
        {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'market': 'US'},
        {'symbol': '005930', 'name': '삼성전자', 'market': 'KR'},
        {'symbol': '000660', 'name': 'SK하이닉스', 'market': 'KR'},
        {'symbol': '035420', 'name': 'NAVER', 'market': 'KR'},
    ]
    
    for stock in sample_stocks:
        if query in stock['symbol'] or query in stock['name']:
            results.append(stock)
    
    return jsonify(results)

if __name__ == '__main__':
    # 백그라운드에서 알림 확인 스레드 시작
    alert_thread = threading.Thread(target=check_price_alerts, daemon=True)
    alert_thread.start()
    
    print("주식 모니터링 시스템이 시작되었습니다.")
    print("3% 이상 등락 시 콘솔에 알림이 표시됩니다.")
    print("웹 브라우저에서 http://localhost:5000  으로 접속하세요.")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
