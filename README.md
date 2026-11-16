# 터치라인

브라우저에서 실행하는 축구 전술 시뮬레이터입니다. 공격·수비 레슨과 Metrica Sports의 세 경기 샘플을 포함합니다.

## 실행

`outputs/tactics-lab.html`을 브라우저로 열면 됩니다. 웹 서버와 패키지 설치 없이 실행됩니다.

- **공격 배우기**에서 3자 플레이, 반대편 전환, 측면 공략을 볼 수 있습니다.
- **같은 빌드업, 다른 압박**에서 우리 팀의 패스를 고르면 상대가 자동으로 대응합니다. 네 가지 압박 패턴의 자동 시연도 열 수 있습니다.
- **직접 실험하기**에서는 실제 경기 좌표를 기준으로 배치, 커버, 패스 결과를 비교할 수 있습니다.

## 빌드

Python 3.9 이상으로 아래 명령을 실행하면 단일 HTML을 다시 만듭니다.

```sh
python work/build.py
```

레슨 시나리오를 수정한 뒤에는 Node.js와 Python으로 JSON을 먼저 갱신합니다.

```sh
python work/make_tactics_dataset.py
python work/build.py
```

`work/app.html`이 앱 소스이며 `outputs/tactics-dataset.json`은 설명용 레슨 데이터입니다. `outputs/match-format.txt`에 경기 데이터 가져오기 형식이 있습니다.

## 데이터 출처

경기 위치와 이벤트 자료는 [Metrica Sports Sample Data](https://github.com/metrica-sports/sample-data)의 익명 샘플을 변환했습니다. 압박·커버 지표는 좌표에서 추정했습니다. 레슨 시나리오와 시뮬레이션 결과는 교육용 예시입니다.
