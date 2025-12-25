# scripts/excel_to_json.py
import pandas as pd
import json
from datetime import datetime
import sys
import os
import glob

def convert_excel_to_json(excel_path, output_path):
    """
    Excel을 JSON으로 변환
    """
    print(f"Reading Excel: {excel_path}")
    
    # Excel 읽기
    df = pd.read_excel(excel_path)
    
    print(f"Total rows: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    
    # 컬럼 인덱스 매핑
    emd_code_col = df.columns[1]   # B: 행정구역코드
    city_col = df.columns[2]        # C: 1단계 (시/도)
    district_col = df.columns[3]    # D: 2단계 (시/군/구)
    neighborhood_col = df.columns[4]  # E: 3단계 (읍/면/동)
    gridx_col = df.columns[5]       # F: 격자X
    gridy_col = df.columns[6]       # G: 격자Y
    lon_col = df.columns[13]        # N: 경도
    lat_col = df.columns[14]        # O: 위도
    
    print(f"\n컬럼 매핑:")
    print(f"  B(1) [{emd_code_col}] → emdCode")
    print(f"  C(2) [{city_col}] → city")
    print(f"  D(3) [{district_col}] → district")
    print(f"  E(4) [{neighborhood_col}] → neighborhood")
    print(f"  F(5) [{gridx_col}] → gridX")
    print(f"  G(6) [{gridy_col}] → gridY")
    print(f"  N(13) [{lon_col}] → longitude")
    print(f"  O(14) [{lat_col}] → latitude")
    
    locations = []
    skipped = 0
    
    for idx, row in df.iterrows():
        try:
            # B: 행정구역코드
            emd_code = str(row[emd_code_col]).strip()
            
            # C: 1단계 (시/도)
            city = str(row[city_col]).strip()
            
            # D: 2단계 (시/군/구)
            district = str(row[district_col]).strip()
            
            # E: 3단계 (읍/면/동)
            neighborhood = str(row[neighborhood_col]).strip()
            
            # 유효성 검사
            if not city or city == 'nan' or \
               not district or district == 'nan' or \
               not neighborhood or neighborhood == 'nan':
                skipped += 1
                if idx < 10:
                    print(f"  Row {idx+1} skipped: city='{city}', district='{district}', neighborhood='{neighborhood}'")
                continue
            
            gridX = int(row[gridx_col])
            gridY = int(row[gridy_col])
            longitude = float(row[lon_col])
            latitude = float(row[lat_col])
            
            location = {
                "emdCode": emd_code,
                "city": city,
                "district": district,
                "neighborhood": neighborhood,
                "gridX": gridX,
                "gridY": gridY,
                "longitude": round(longitude, 7),
                "latitude": round(latitude, 7)
            }
            
            locations.append(location)
            
            # 처음 3개 데이터 출력
            if idx < 3:
                print(f"  Row {idx+1}: {emd_code} | {city} {district} {neighborhood} | Grid({gridX},{gridY}) | ({longitude:.6f}, {latitude:.6f})")
            
        except Exception as e:
            skipped += 1
            if idx < 10:
                print(f"  Row {idx+1} error: {e}")
    
    # 버전 생성
    version = datetime.now().strftime("%Y%m%d")
    
    # JSON 생성
    output_data = {
        "version": version,
        "updated_at": datetime.now().isoformat(),
        "count": len(locations),
        "locations": locations
    }
    
    # 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Conversion completed!")
    print(f"✓ Version: {version}")
    print(f"✓ Valid records: {len(locations)}")
    print(f"✓ Skipped: {skipped}")
    print(f"✓ Output: {output_path}")
    
    # JSON 파일 크기 확인
    file_size = os.path.getsize(output_path)
    print(f"✓ File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    
    return version

if __name__ == "__main__":
    # raw 폴더에서 Excel 파일 자동 찾기
    excel_files = glob.glob("raw/*.xlsx") + glob.glob("raw/*.xls")
    
    if not excel_files:
        print("Error: No Excel file found in raw/ directory")
        print("Please upload an Excel file (.xlsx or .xls) to the raw/ folder")
        sys.exit(1)
    
    # 가장 최근 파일 사용
    excel_file = sorted(excel_files, key=os.path.getmtime, reverse=True)[0]
    print(f"Found Excel file: {excel_file}")
    
    output_file = "processed/location.json"
    
    # processed 디렉토리가 없으면 생성
    os.makedirs("processed", exist_ok=True)
    
    version = convert_excel_to_json(excel_file, output_file)
    
    # 버전 파일 생성
    with open("processed/location_version.txt", "w") as f:
        f.write(version)
    
    print(f"\n✓ Version file created: processed/location_version.txt")
```

## 질문에 대한 답변

### 1. 엑셀파일을 다음에 업로드 할때는 기존 파일은 지워야 하나?

**답변: 아니요, 지울 필요 없습니다!**

위의 수정된 스크립트는:
- `raw/` 폴더에서 `.xlsx` 또는 `.xls` 파일을 **자동으로 찾습니다**
- 여러 파일이 있으면 **가장 최근 파일**을 사용합니다
- 파일명이 무엇이든 상관없습니다

**운영 방법:**
```
# 방법 A: 덮어쓰기 (권장)
- 같은 파일명으로 업로드 → 자동으로 교체됨

# 방법 B: 새 파일 추가
- 다른 파일명으로 업로드 → 가장 최근 파일 자동 선택
- 나중에 오래된 파일은 삭제 가능 (선택사항)
