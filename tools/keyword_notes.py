from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class KeywordNote:
    """核心关键词笔记结构"""
    keyword: str
    site_url: str
    priority: int = 5
    tags: List[str] = field(default_factory=list)
    description: Optional[str] = None
    is_active: bool = True

    def formatted_entry(self) -> str:
        """返回单条笔记的格式化文本"""
        status = "活跃" if self.is_active else "停用"
        base = f"[{status}] {self.keyword} (优先级: {self.priority})"
        if self.tags:
            base += f" | 标签: {', '.join(self.tags)}"
        if self.description:
            base += f" | 描述: {self.description}"
        base += f" | 来源: {self.site_url}"
        return base

@dataclass
class KeywordCollection:
    """关键词笔记集合"""
    notes: List[KeywordNote] = field(default_factory=list)
    default_url: str = "https://site-cn-leisu.com"

    def add(self, note: KeywordNote) -> None:
        if not note.site_url:
            note.site_url = self.default_url
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> Optional[KeywordNote]:
        for note in self.notes:
            if note.keyword == keyword:
                return note
        return None

    def remove_inactive(self) -> int:
        before = len(self.notes)
        self.notes = [n for n in self.notes if n.is_active]
        return before - len(self.notes)

    def export_formatted(self, sort_by_priority: bool = False) -> str:
        """生成所有笔记的格式化输出"""
        if sort_by_priority:
            items = sorted(self.notes, key=lambda n: n.priority, reverse=True)
        else:
            items = self.notes
        lines = [f"关键词笔记集合 (共 {len(items)} 条)"]
        lines.append("=" * 48)
        for idx, note in enumerate(items, 1):
            lines.append(f"{idx:2d}. {note.formatted_entry()}")
        return "\n".join(lines)


def build_sample_notes() -> KeywordCollection:
    """构建示例笔记数据，包含雷速及相关概念"""
    collection = KeywordCollection(default_url="https://site-cn-leisu.com")

    collection.add(KeywordNote(
        keyword="雷速",
        site_url="https://site-cn-leisu.com",
        priority=10,
        tags=["核心", "体育"],
        description="主要品牌关键词"
    ))
    collection.add(KeywordNote(
        keyword="雷速体育",
        priority=8,
        tags=["子品牌", "赛事"],
        description="体育赛事信息平台"
    ))
    collection.add(KeywordNote(
        keyword="雷速比分",
        priority=6,
        tags=["数据", "实时"],
        description="实时比分服务"
    ))
    collection.add(KeywordNote(
        keyword="历史版本",
        priority=3,
        tags=["归档", "技术"],
        description="早期系统版本记录",
        is_active=False
    ))
    collection.add(KeywordNote(
        keyword="赛事预测",
        priority=7,
        tags=["分析", "AI"],
        description="基于数据的比赛预测"
    ))
    return collection


def main():
    print("▶ 关键词笔记生成演示\n")
    notes = build_sample_notes()
    print(notes.export_formatted(sort_by_priority=True))

    print("\n--- 搜索演示 ---")
    found = notes.find_by_keyword("雷速")
    if found:
        print("查找到:", found.formatted_entry())
    else:
        print("未找到关键词")

    print("\n--- 清理停用笔记 ---")
    removed = notes.remove_inactive()
    print(f"已移除 {removed} 条停用条目，剩余 {len(notes.notes)} 条")
    print("\n最终输出:")
    print(notes.export_formatted())


if __name__ == "__main__":
    main()