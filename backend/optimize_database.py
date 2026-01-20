"""
数据库优化脚本
添加复合索引、全文搜索索引等，提升查询性能
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import engine


def add_indexes():
    """添加数据库索引以优化查询性能"""

    with engine.connect() as conn:
        # 1. 公告表优化索引

        # 复合索引：类型 + 创建时间（用于按类型筛选并按时间排序）
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_announcement_type_created_at
            ON announcement(type, created_at DESC);
        """)

        # 全文搜索索引：标题 + 内容（用于全文搜索）
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_announcement_search
            ON announcement USING gin(to_tsvector('chinese', title || ' ' || content));
        """)

        # 2. 回复表优化索引

        # 复合索引：公告ID + 创建时间（用于获取某公告的最新回复）
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_response_announcement_created_at
            ON response(announcement_id, created_at DESC);
        """)

        # 复合索引：同事姓名 + 创建时间（用于查看某同事的回复历史）
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_response_colleague_created_at
            ON response(colleague_name, created_at DESC);
        """)

        # 复合索引：公告ID + 同事姓名（用于判断某同事是否已回复某公告）
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_response_announcement_colleague
            ON response(announcement_id, colleague_name);
        """)

        # 全文搜索索引：同事姓名 + 内容（用于搜索回复）
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_response_search
            ON response USING gin(to_tsvector('chinese', colleague_name || ' ' || content));
        """)

        # 索引：文件键（用于文件管理）
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_response_file_key
            ON response(file_key) WHERE file_key IS NOT NULL;
        """)

        conn.commit()

    print("✅ 数据库索引优化完成！")
    print("\n已创建的索引：")
    print("📊 公告表：")
    print("  - idx_announcement_type_created_at (类型 + 创建时间)")
    print("  - idx_announcement_search (全文搜索)")
    print("\n📊 回复表：")
    print("  - idx_response_announcement_created_at (公告ID + 创建时间)")
    print("  - idx_response_colleague_created_at (同事姓名 + 创建时间)")
    print("  - idx_response_announcement_colleague (公告ID + 同事姓名)")
    print("  - idx_response_search (全文搜索)")
    print("  - idx_response_file_key (文件键)")


def create_search_function():
    """创建全文搜索辅助函数"""

    with engine.connect() as conn:
        # 创建简化全文搜索的函数
        conn.execute("""
            CREATE OR REPLACE FUNCTION search_announcements(query TEXT)
            RETURNS TABLE (
                id INTEGER,
                title VARCHAR,
                content TEXT,
                type VARCHAR,
                created_at TIMESTAMP,
                rank REAL
            )
            AS $$
            BEGIN
                RETURN QUERY
                SELECT
                    a.id, a.title, a.content, a.type, a.created_at,
                    ts_rank(to_tsvector('chinese', a.title || ' ' || a.content), query) AS rank
                FROM announcement a
                WHERE to_tsvector('chinese', a.title || ' ' || a.content) @@ query
                ORDER BY rank DESC;
            END;
            $$ LANGUAGE plpgsql;
        """)

        # 创建简化回复搜索的函数
        conn.execute("""
            CREATE OR REPLACE FUNCTION search_responses(query TEXT)
            RETURNS TABLE (
                id INTEGER,
                announcement_id INTEGER,
                colleague_name VARCHAR,
                content TEXT,
                created_at TIMESTAMP,
                rank REAL
            )
            AS $$
            BEGIN
                RETURN QUERY
                SELECT
                    r.id, r.announcement_id, r.colleague_name, r.content, r.created_at,
                    ts_rank(to_tsvector('chinese', r.colleague_name || ' ' || r.content), query) AS rank
                FROM response r
                WHERE to_tsvector('chinese', r.colleague_name || ' ' || r.content) @@ query
                ORDER BY rank DESC;
            END;
            $$ LANGUAGE plpgsql;
        """)

        conn.commit()

    print("✅ 全文搜索函数创建完成！")
    print("\n可用的搜索函数：")
    print("  - search_announcements(query TEXT)")
    print("  - search_responses(query TEXT)")


def analyze_tables():
    """分析表统计信息，优化查询计划"""

    with engine.connect() as conn:
        conn.execute("ANALYZE announcement;")
        conn.execute("ANALYZE response;")
        conn.commit()

    print("✅ 表统计信息分析完成！")


if __name__ == "__main__":
    print("=" * 60)
    print("数据库优化脚本")
    print("=" * 60)
    print()

    try:
        add_indexes()
        print()
        create_search_function()
        print()
        analyze_tables()

        print()
        print("=" * 60)
        print("🎉 数据库优化全部完成！")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 优化失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
