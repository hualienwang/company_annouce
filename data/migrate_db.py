"""
數據庫遷移腳本，用於修復數據庫結構與模型不匹配的問題
"""
import sqlite3

def migrate_database():
    print("開始遷移數據庫...")
    
    # 連接到數據庫
    conn = sqlite3.connect('D:/develop/Python/company_annouce/data/company.db')
    cursor = conn.cursor()
    
    # 檢查announcement表是否缺少file_key和file_name字段
    cursor.execute("PRAGMA table_info(announcement);")
    announcement_columns = [col[1] for col in cursor.fetchall()]
    
    print(f"當前announcement表字段: {announcement_columns}")
    
    # 添加缺失的字段
    if 'file_key' not in announcement_columns:
        cursor.execute("ALTER TABLE announcement ADD COLUMN file_key VARCHAR NULL;")
        print("✓ 已添加file_key字段到announcement表")
    
    if 'file_name' not in announcement_columns:
        cursor.execute("ALTER TABLE announcement ADD COLUMN file_name VARCHAR NULL;")
        print("✓ 已添加file_name字段到announcement表")
    
    # 檢查response表（確保它有所有需要的字段）
    cursor.execute("PRAGMA table_info(response);")
    response_columns = [col[1] for col in cursor.fetchall()]
    
    print(f"當前response表字段: {response_columns}")
    
    # 提交更改
    conn.commit()
    conn.close()
    
    print("數據庫遷移完成！")

if __name__ == "__main__":
    migrate_database()