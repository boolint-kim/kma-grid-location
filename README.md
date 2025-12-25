# kma-grid-location
기상청 예보 격자 위경도 배포 시스템

* 기상청 읍면동, 격자, 위경도 업데이트 방법
1. raw 폴더에 엑셀파일을 업로드 한다. 파일명은 똑같이 한다. (컬럼이 변경되었는지 확인할것)
2. Actions Tab >> 좌측 상단 'Convert Excel to JSON Deploy to...' 탭? 누르고 오른쪽 Run workflow >> Run workflow 를 누르면 수동으로 동작된다.
3. 로그를 확인한다.
4. Cloudflare R2 에 kma-grid-location 에 업데이트 됨을 확인한다. location.json + location_version.txt
5. 
