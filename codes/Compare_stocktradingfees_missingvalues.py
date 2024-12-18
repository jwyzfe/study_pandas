from pymongo import MongoClient
import pandas as pd

# MongoDB 연결
client = MongoClient('python_jupyternote_mongo-mongodb-1')
db = client['pandas_db']
collection = db['stocktradingfees_merge']

# MongoDB에서 조건에 맞는 데이터 불러오기 (구분 필드가 '변경후'인 데이터)
query = {'구분': '변경후'}
data = collection.find(query)  # 쿼리 조건을 사용하여 데이터를 가져옵니다.

# 데이터를 pandas DataFrame으로 변환
df_list = []
for record in data:
    df_list.append(pd.DataFrame([record]))  # 각 문서를 DataFrame으로 변환하여 리스트에 추가

# 여러 DataFrame 합치기
if df_list:
    merged_df = pd.concat(df_list, ignore_index=True)
    
    # 비숫자형 데이터를 숫자형으로 변환하는 함수
    def convert_to_numeric(value):
        if isinstance(value, str):
            value = value.replace("원", "")  # 원 제거

            if "억원" in value:
                return float(value.replace("억원", "").strip()) * 100000000  # 1억원 = 100,000,000
            elif "만원" in value:
                return float(value.replace("만원", "").strip()) * 10000  # 1만원 = 10,000
            elif "백만원" in value:
                return float(value.replace("백만원", "").strip()) * 1000000  # 1백만원 = 1,000,000
            else:
                return float(value)  # 숫자 값 그대로 반환
        return value

    # 각 열에 대해 처리 (apply 없이 변환 및 결측치 처리)
    for column in merged_df.columns:
        # ObjectId 컬럼 제외: 'ObjectId' 타입 컬럼은 숫자형으로 변환하지 않음
        if merged_df[column].dtype != 'object':  # ObjectId는 'object' 타입으로 취급됩니다
            merged_df[column] = merged_df[column].apply(convert_to_numeric)
        
        # 숫자형 데이터에 대해서만 결측치 처리
        if pd.api.types.is_numeric_dtype(merged_df[column]):
            # 결측치가 모두 NaN인 경우 NaN으로 유지, 그렇지 않으면 평균값으로 채우기
            if merged_df[column].isnull().sum() == len(merged_df[column]):
                merged_df[column] = pd.NA  # 모든 값이 결측치일 경우 NaN 처리
            else:
                mean_value = merged_df[column].mean()
                merged_df[column] = merged_df[column].fillna(mean_value)

# '스마트폰.1' 컬럼에 대한 평균 계산
smartphone_avg = merged_df['스마트폰.1'].mean()

# 스마트폰 수수료 평균 이상인 증권사들만 필터링
df_filtered = merged_df[merged_df['스마트폰.1'] >= smartphone_avg]

# 증권사명만 선택
df_filtered_names = df_filtered[['회사명']]

# 필터링된 데이터만 CSV 파일로 저장
output_path = '/apps/study_pandas/datasets/filtered_smartphone_fees3.csv'
df_filtered_names.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"스마트폰 수수료 평균 이상인 증권사들이 {output_path}에 저장되었습니다.")
