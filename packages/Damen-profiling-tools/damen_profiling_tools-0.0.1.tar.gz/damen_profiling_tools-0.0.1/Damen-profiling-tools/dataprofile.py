
import datetime
from typing import Dict


class DataQuality:


    def __init__(self, df):
        self.df = df
        # self.df1 =pd.DataFrame(df)
    def generate_schema(self) -> Dict:
        
        schema = {
            "version": 1,
            "creation_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "row_count": self.get_row_count(),
            "column_count": len(self.df.columns),
            "columns": {},
            "schema_fingerprint": ""
        }
        
        for column in self.df.columns:
            col_data = self.df[column]
            dtype_name = str(col_data.dtype)
            
            null_count = col_data.isna().sum()
            unique_count = col_data.nunique()
            
            schema["columns"][column] = {
                "dtype": dtype_name,
                "nullable": bool(null_count > 0),
                "null_count": int(null_count),
                "unique_count": int(unique_count)
            }
        
        column_fingerprints = []
        for col_name in sorted(schema["columns"].keys()):
            col_info = schema["columns"][col_name]
            column_fingerprints.append(
                f"{col_name}:{col_info['dtype']}:{col_info['nullable']}"
            )
        
        schema["schema_fingerprint"] = "|".join(column_fingerprints)
        # print(df)
        
        return schema

    def print_schema(self) -> None: #UNTUK MEMBUKA DETAIL DI DALAM TABLE YANG DI LEMPAR
        schema = self.generate_schema()
        
        print("\n===== DATAFRAME SCHEMA =====")
        print(f"Created: {schema['creation_date']}")
        print(f"Rows: {schema['row_count']}")
        print(f"Columns: {schema['column_count']}")
        print(f"Schema Fingerprint: {schema['schema_fingerprint'][:50]}...")  
        print("\n=== COLUMNS ===")
        
    
        type_counts = {}
        for col_info in schema["columns"].values():
            dtype = col_info["dtype"]
            if dtype not in type_counts:
                type_counts[dtype] = 0
            type_counts[dtype] += 1
            
        
        print("Type Distribution:")
        for dtype, count in type_counts.items():
            print(f"  - {dtype}: {count} columns")
        
        print("\nDetailed Column Information:")
        for col_name, col_info in schema["columns"].items():
            print(f"  • {col_name}")
            print(f"    Type: {col_info['dtype']}")
            print(f"    Nullable: {'Yes' if col_info['nullable'] else 'No'}")
            print(f"    Null Count: {col_info['null_count']}")
            print(f"    Unique Values: {col_info['unique_count']}")
    def get_row_count(self) -> int: #UNTUK MEMBUKA JUMLAH DATA YANG DILEMPAR
            return len(self.df)
    
    def get_dup_row(self) -> int: #UNTUK MENGAMBIL DUPLICATE DATA
        duplicates = self.df.duplicated()
        a= self.df[duplicates]
        b=len(a)
        return b
    
    def get_null_rows(self) -> int: #UNTUK MENGAMBIL DATA NULL
        missing_values = self.df.isnull().sum()
        c=missing_values.sum()
        return c
    
    # def calculate_percentage(self) -> int: #UNTUK MENGAMBIL CALCULATE DARI DATA
    def calculate_percentage(self) -> int:
        total=self.df.count()
        sum=self.df>0
        sum=sum.replace({True: 1, False: 0}).sum()
        return  round(100-(sum/total) * 100,2) 
        # round(100-(sum/total) * 100,2)

 