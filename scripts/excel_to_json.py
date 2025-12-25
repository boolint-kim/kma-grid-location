# scripts/excel_to_json.py
import pandas as pd
import json
from datetime import datetime
import sys

def convert_excel_to_json(excel_path, output_path):
    """
    Excel을 JSON으로 변환
    컬럼 순서 변경시 여기만 수정하면 됨!
    """
    print(f"Reading Excel: {excel_path}")
    
    # Excel 읽기
    df = pd.read_excel(excel_path)
    
    print(f"Total rows: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    
    # 컬럼명 확인 (유연하게 처리)
    # 방법 1: 인덱스 기반 (현재)
    city_col = df.columns[2]      # C: 1단계
    district_col = df.columns[3]  # D: 2단계
    neighborhood_col = df.columns[4]  # E: 3단계
    gridx_col = df.columns[5]     # F: 격자X
    gridy_col = df.columns[6]     # G: 격자Y
    lon_col = df.columns[13]      # N: 경도
    lat_col = df.columns[14]      # O: 위도
    
    # 방법 2: 컬럼명 기반 (더 안전)
    # city_col = '1단계' if '1단계' in df.columns else df.columns[2]
    
    locations = []
    skipped = 0
    
    for idx, row in df.iterrows():
        try:
            city = str(row[city_col]).strip()
            district = str(row[district_col]).strip()
            neighborhood = str(row[neighborhood_col]).strip()
            
            # 유효성 검사
            if not city or city == 'nan' or not district or district == 'nan' or \
               not neighborhood or neighborhood == 'nan':
                skipped += 1
                continue
            
            gridX = int(row[gridx_col])
            gridY = int(row[gridy_col])
            longitude = float(row[lon_col])
            latitude = float(row[lat_col])
            
            location = {
                "city": city,
                "district": district,
                "neighborhood": neighborhood,
                "gridX": gridX,
                "gridY": gridY,
                "longitude": round(longitude, 7),
                "latitude": round(latitude, 7)
            }
            
            locations.append(location)
            
        except Exception as e:
            skipped += 1
            if idx < 10:
                print(f"Row {idx} skipped: {e}")
    
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
    
    return version

if __name__ == "__main__":
    excel_file = "raw/기상청_격자_위경도.xlsx"
    output_file = "processed/location.json"
    
    version = convert_excel_to_json(excel_file, output_file)
    
    # 버전 파일 생성
    with open("processed/location_version.txt", "w") as f:
        f.write(version)
