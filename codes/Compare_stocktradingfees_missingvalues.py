from pymongo import MongoClient
import pandas as pd


client = MongoClient('python_jupyternote_mongo-mongodb-1')
db = client['pandas_db']
collection = db['stocktradingfees_merge']


query = {'구분': '변경후'}
data = collection.find(query)


df_list = [pd.DataFrame([record]) for record in data]


merged_df = pd.concat(df_list, ignore_index=True)

# 비숫자형 데이터를 숫자형으로 변환하는 함수
def convert_to_numeric(value):
    if isinstance(value, str):
        value = value.replace("원", "")  # 원 제거

        if "억원" in value:
            return float(value.replace("억원", "").strip()) * 100000000
        elif "만원" in value:
            return float(value.replace("만원", "").strip()) * 10000
        elif "백만원" in value:
            return float(value.replace("백만원", "").strip()) * 1000000
        else:
            try:
                return float(value)  # 숫자로 변환
            except ValueError:
                return value  # 숫자로 변환할 수 없는 값은 그대로 반환
    return value

for column in merged_df.columns:
    if merged_df[column].dtype == 'object':  
        merged_df[column] = merged_df[column].apply(convert_to_numeric)

# 결측치 처리 (각 열의 평균값으로 채우기)
for column in merged_df.columns:
    if pd.api.types.is_numeric_dtype(merged_df[column]):
        merged_df[column] = merged_df[column].fillna(merged_df[column].mean())

# '스마트폰.1' 컬럼에 대한 평균 계산
smartphone_avg = merged_df['스마트폰.1'].mean()

# 스마트폰 수수료 평균 이상인 증권사들만 필터링
df_filtered = merged_df[merged_df['스마트폰.1'] >= smartphone_avg]

# 증권사명만 선택
df_filtered_names = df_filtered[['회사명']]

# 필터링된 데이터만 CSV 파일로 저장
output_path = '/apps/study_pandas/datasets/filtered_smartphone_fees6.csv'
df_filtered_names.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"스마트폰 수수료 평균 이상인 증권사들이 {output_path}에 저장되었습니다.")
