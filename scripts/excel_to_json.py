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
    print(f"Columns: {list(df.columns)[:15]}")  # 처음 15개 컬럼만
    
    # 컬럼 인덱스 매핑
    try:
        emd_code_col = df.columns[1]   # B: 행정구역코드
        city_col = df.columns[2]        # C: 1단계 (시/도)
        district_col = df.columns[3]    # D: 2단계 (시/군/구)
        neighborhood_col = df.columns[4]  # E: 3단계 (읍/면/동)
        gridx_col = df.columns[5]       # F: 격자X
        gridy_col = df.columns[6]       # G: 격자Y
        lon_col = df.columns[13]        # N: 경도
        lat_col = df.columns[14]        # O: 위도
    except IndexError as e:
        print(f"Error: Excel 파일의 컬럼이 부족합니다. 최소 15개 컬럼이 필요합니다.")
        print(f"현재 컬럼 수: {len(df.columns)}")
        sys.exit(1)
    
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
                if idx < 5:
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
            if idx < 5:
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

if __name__ == "__main__":
    print("=" * 60)
    print("Excel to JSON Converter for KMA Grid Location Data")
    print("=" * 60)
    
    # raw 폴더 확인 및 생성
    if not os.path.exists("raw"):
        print("\nError: 'raw' directory not found!")
        print("Creating 'raw' directory...")
        os.makedirs("raw")
        print("Please upload an Excel file to the 'raw' folder and run again.")
        sys.exit(1)
    
    # raw 폴더에서 Excel 파일 찾기
    excel_files = []
    for ext in ['*.xlsx', '*.xls', '*.XLSX', '*.XLS']:
        excel_files.extend(glob.glob(f"raw/{ext}"))
    
    if not excel_files:
        print("\nError: No Excel file found in 'raw/' directory")
        print("Available files in raw/:")
        all_files = os.listdir("raw")
        if all_files:
            for f in all_files:
                print(f"  - {f}")
        else:
            print("  (empty)")
        print("\nPlease upload an Excel file (.xlsx or .xls) to the 'raw/' folder")
        sys.exit(1)
    
    # 파일 목록 출력
    print(f"\nFound {len(excel_files)} Excel file(s):")
    for i, f in enumerate(excel_files, 1):
        file_size = os.path.getsize(f)
        file_mtime = datetime.fromtimestamp(os.path.getmtime(f))
        print(f"  {i}. {f} ({file_size:,} bytes, modified: {file_mtime})")
    
    # 가장 최근 파일 사용
    excel_file = sorted(excel_files, key=os.path.getmtime, reverse=True)[0]
    print(f"\nUsing most recent file: {excel_file}")
    
    # processed 폴더 생성
    output_dir = "processed"
    if not os.path.exists(output_dir):
        print(f"\nCreating '{output_dir}' directory...")
        os.makedirs(output_dir)
    
    output_file = os.path.join(output_dir, "kma_grid_location.json")
    
    # 변환 실행
    print("\n" + "=" * 60)
    try:
        convert_excel_to_json(excel_file, output_file)
        
        print("=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("ERROR!")
        print("=" * 60)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
