# kma-grid-location (변환유틸역할만 담당 - 서비스 아님)
공공데이터포털 - 기상청 예보 API - 사용에 필요한 격자-위경도 정보 변환 시스템

* 기상청 읍면동, 격자, 위경도 업데이트 방법
1. raw 폴더에 기상청엑셀파일을 업로드 한다. 파일명은 똑같이 한다. (컬럼이 변경되었는지 확인할것)
2. Actions Tab >> 좌측 상단 'Convert Excel to JSON' 탭? 누르고 오른쪽 Run workflow >> Run workflow 를 누르면 수동으로 동작된다.
3. 로그를 확인한다.
4. Processed 폴더에 kma_grid_location.json 파일 생성 확인
5. 안드로이드스튜디오 assets 폴더에 복사 하여 사용.
