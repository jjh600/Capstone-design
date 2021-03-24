# 동작감지 기반 객체 인식 및 검색 시스템
YOLOv4를 사용해 객체가 인식될때만 영상을 저장하여 시간, 객체 이름으로 검색 가능한 시스템  
https://object-detection-ljj.herokuapp.com/

# 개발목표
- 다양한 객체를 실시간으로 인식하여 저장 공간을 효율적으로 구성할 수 있는 모듈 개발

# 목적
- 물체인식을 수행하기 위해 고안된 심층 신경망 프로그램으로 다양한 객체를 인식하고, 인식된 물체마다 저장하여 분류하는 기능을 통해 검색 기능을 강화. 찾고자 하는 물체를 빠르게 찾을 수 있도록 하는 목적. 

# 필요성
- 보통 실시간 영상 스트리밍을 통해 특정 사건의 정보를 확인하기에는 구체적인 시간대 및 대략적 추론으로 오랜 시간을 투자해야 할 수도 있는 상대적 비효율적 탐색 방법을 사용해야만 했음.
- 실시간 영상의 스트리밍 기능을 유지하면서, 찾고자 하는 것을 물체 또는 시간으로 자유롭게 검색하여 빠르게 검색할 수 있는 기술이 가능.
- 전체 영상을 모두 저장해서 보관하는 기존 저장 방식과 다르게, 특정 물체가 인식되었을 때만 저장하는 기능을 이용해 저장 공간을 효율적으로 구성할 수 있는 큰 이점이 있음.

# 시스템 구성도
![시스템 구성도](https://user-images.githubusercontent.com/66826815/112254950-be4a5600-8ca4-11eb-902c-6c20a488616e.PNG)

# 개발 환경 및 도구
|작품 관련 기술|내용|
|---|---|
|YOLOv4|효율적인 저장을 하려면 객체 인식을 통한 영상의 분류가 필요했고, 이에 적합한 기술로 실시간 객체 인식이 가능한 YOLO를 선택.|
|MongoDB|분류된 영상을 저장하기 위해 GridFS로 파일 저장이 가능한 MongoDB가 적합.|
|Flask|실시간 스트리밍, 영상 검색 기능 등 사용자를 위한 UI 구성을 위해 Flask 사용.|
|RTSP|웹캠의 영상을 실시간으로 가져오기 위해 RTSP 사용.|
|Python 3.8|머신러닝관련 다양한 라이브러리를 지원하는 언어인 python 사용.|

# 해결방안 및 수행과정
*1. 실시간 객체 인식*
- real-time object detection system인 YOLO를 이용하여 실시간으로 웹 캠을 통해 객체를 인식. 
- Darknet에서 제공하는 훈련된 weights 파일을 이용하여 80 종류의 객체를 인식.

![image](https://user-images.githubusercontent.com/66826815/112257082-ac1de700-8ca7-11eb-9d15-c3e020b9b34b.png)

*2. 인식 영상 추출*
- Python으로 YOLO를 실행해 객체가 최초로 인식될 때 cv2 모듈의 VideoWriter() 함수를 사용해 영상 저장을 시작하고 인식되는 객체가 존재하지 않을 때 영상 저장이 끝나며 최초 인식시간을 파일 이름으로 저장.

*3. 영상 업로드 및 조회*
- 인식 영상 추출이 끝남과 동시에 MongoDB의 playlist 데이터베이스의 list 컬렉션에 최초 인식시간(파일 이름), 인식된 객체의 종류를 업로드하고 GridFS를 사용해 동영상을 업로드. 
- 동영상은 playlist 데이터베이스의 fs.files, fs.chunks 컬렉션에 저장. 
- fs.files에는 id(자동으로 생성), metadata(파일 이름, 크기, 날짜 등)가 저장되며 fs.chunks에는 동영상 데이터가 분산되어 fs.files의 id를 포함해 저장. 
- 파일 이름을 통해 동영상을 조회 가능.

![image](https://user-images.githubusercontent.com/66826815/112256612-6bbe6900-8ca7-11eb-852b-61f53e6e9cda.png)

*4. UI*
- 반응형 웹 디자인으로 PC뿐만 아니라 스마트폰, 태블릿 PC 등 접속하는 디스플레이의 종류에 따라 화면의 크기가 자동으로 변하도록 Flask(web app) 제작.

*5. 실시간 스트리밍*
- 실시간 스트리밍 프로토콜(RTSP)을 이용해 Flask에 실시간 웹 캠 영상을 스트리밍.

*6. 영상 검색*
- Flask에서 MongoDB의 list 컬렉션 조회를 통해 동영상 검색.  
- list 컬렉션에서 인식된 객체 이름을 검색하면 해당하는 문서를 찾아 파일 이름을 통해 동영상을 조회.

*7. 관리자 로그인*
- 관리자 계정을 통해 영상을 관리. 로그인 상태에서만 영상 삭제 가능.

# 스크린샷

- 메인

<div>
  <img height="300" src="https://user-images.githubusercontent.com/66826815/99513576-24a92a00-29ce-11eb-8390-295751931c43.PNG">
  <img height="300" src="https://user-images.githubusercontent.com/66826815/99513581-2672ed80-29ce-11eb-8a3d-107d14d9661d.jpg">
</div>

- 실시간 스트리밍

<div>
  <img height="300" src="https://user-images.githubusercontent.com/66826815/99513596-27a41a80-29ce-11eb-852c-b144b194d128.PNG">
  <img height="300" src="https://user-images.githubusercontent.com/66826815/99513583-2672ed80-29ce-11eb-9885-746bfc3bbe02.jpg">
</div>

- 검색

<div>
  <img height="300" src="https://user-images.githubusercontent.com/66826815/99513600-283cb100-29ce-11eb-8ff5-89cc76e832cc.PNG">
  <img height="300" src="https://user-images.githubusercontent.com/66826815/99513602-296dde00-29ce-11eb-8936-028ee3c71484.PNG">
  <img height="300" src="https://user-images.githubusercontent.com/66826815/99513594-27a41a80-29ce-11eb-85ab-292881577b7e.jpg">
</div>

- 검색결과

<div>
  <img height="300" src="https://user-images.githubusercontent.com/66826815/99513604-296dde00-29ce-11eb-84d1-a8d199ef87cf.PNG">
  <img height="300" src="https://user-images.githubusercontent.com/66826815/99513592-270b8400-29ce-11eb-8851-18c171e1731b.jpg">
</div>

- 로그인

<div>
  <img height="300" src="https://user-images.githubusercontent.com/66826815/99513601-28d54780-29ce-11eb-93ac-a2bb46cde175.PNG">
  <img height="300" src="https://user-images.githubusercontent.com/66826815/99513587-270b8400-29ce-11eb-8a88-6eb982b68d49.jpg">
</div>

# 기대효과
- 시설안전․화재예방 및 도난사고예방 등의 안전 관리와, 출입통제 등의 보안 관리에 사용되는 모든 실시간 CCTV에 활용될 수 있음.
- 기존의 전체 영상 전부를 저장하는 구조에서, 동일 용량대비 물체가 인식되었을 때만 저장하는 방식을 활용한 저장 공간 경량화로 경제적 비용이 절감됨.

# References
https://github.com/theAIGuysCode/yolov4-deepsort
