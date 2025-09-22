# 📈 주식 모니터링 시스템 (Stock Monitor Alert)

미국과 한국 주식을 모니터링하고, 관심 주식의 3% 이상 등락 시 콘솔에 알림을 보내는 웹 애플리케이션입니다.

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 주요 기능

- 🇺🇸 **미국 주식 조회**: Alpha Vantage API를 통한 실시간 주식 데이터
- 🇰🇷 **한국 주식 조회**: 샘플 데이터 (실제 구현시 한국투자증권 API 등 사용)
- ⭐ **관심 주식 관리**: 관심 주식 추가/제거 기능
- 🚨 **알림 시스템**: 3% 이상 등락 시 콘솔 알림
- 📱 **반응형 웹 UI**: Bootstrap을 사용한 모던한 디자인

## 🚀 설치 및 실행

### 1. 레포지토리 클론
```bash
git clone https://github.com/your-username/25-2-cursor-newbie-stock.git
cd 25-2-cursor-newbie-stock
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 애플리케이션 실행
```bash
python app.py
```

### 4. 웹 브라우저에서 접속
```
http://localhost:5000
```

> **참고**: Windows에서 Python이 PATH에 등록되지 않은 경우, 전체 경로를 사용하세요:
> ```bash
C:\Users\[사용자명]\AppData\Local\Programs\Python\Python313\python.exe app.py
```

## 사용 방법

1. **주식 검색**: 상단 검색창에서 주식 코드나 이름으로 검색
2. **관심 주식 추가**: 검색 결과나 주식 카드에서 "관심추가" 버튼 클릭
3. **알림 확인**: 관심 주식이 3% 이상 등락하면 콘솔에 색상으로 표시된 알림 확인
4. **관심 주식 관리**: 좌측 패널에서 관심 주식 목록 확인 및 제거

## 알림 시스템

- 30초마다 관심 주식의 가격 변동을 확인
- 3% 이상 등락 시 콘솔에 다음과 같은 알림 표시:
  - 🚨 상승: 초록색으로 표시
  - 🚨 하락: 빨간색으로 표시

## API 정보

### 미국 주식
- Alpha Vantage API 사용 (무료 버전)
- 실제 사용시에는 API 키를 환경변수로 설정 필요

### 한국 주식
- 현재는 샘플 데이터 사용
- 실제 구현시에는 한국투자증권 API 또는 다른 한국 주식 API 연동 필요

## 기술 스택

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **API**: Alpha Vantage (미국), 샘플 데이터 (한국)
- **알림**: 콘솔 출력 (색상 지원)

## ⚠️ 주의사항

- 무료 API 사용으로 인한 요청 제한이 있을 수 있습니다
- 한국 주식은 실제 API 연동이 필요합니다
- 알림은 콘솔창에서만 확인 가능합니다

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주세요.

