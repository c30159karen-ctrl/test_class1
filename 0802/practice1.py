"""
學生成績管理系統
功能：新增/查詢/修改/刪除學生、成績統計分析、排名
"""


class Student:
    """代表一位學生及其各科成績"""

    def __init__(self, student_id: str, name: str):
        self.student_id = student_id
        self.name = name
        self.grades: dict[str, float] = {}  # 科目 -> 成績

    def add_grade(self, subject: str, score: float):
        """新增或更新單科成績"""
        if not (0 <= score <= 100):
            raise ValueError(f"成績必須介於 0 ~ 100，輸入值：{score}")
        self.grades[subject] = score

    def remove_grade(self, subject: str):
        """刪除單科成績"""
        if subject not in self.grades:
            raise KeyError(f"科目「{subject}」不存在")
        del self.grades[subject]

    def average(self) -> float:
        """計算平均分數，無成績時回傳 0"""
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)

    def __str__(self):
        avg = self.average()
        grade_str = "、".join(f"{s}:{g:.1f}" for s, g in self.grades.items())
        return f"[{self.student_id}] {self.name}  平均:{avg:.1f}  ({grade_str})"


class GradeManager:
    """管理所有學生資料的核心類別"""

    def __init__(self):
        self.students: dict[str, Student] = {}  # student_id -> Student

    # ── 學生管理 ────────────────────────────────────────────────

    def add_student(self, student_id: str, name: str) -> Student:
        """新增學生；若 ID 已存在則拋出例外"""
        if student_id in self.students:
            raise ValueError(f"學號 {student_id} 已存在")
        student = Student(student_id, name)
        self.students[student_id] = student
        return student

    def get_student(self, student_id: str) -> Student:
        """查詢學生；找不到時拋出例外"""
        if student_id not in self.students:
            raise KeyError(f"找不到學號 {student_id}")
        return self.students[student_id]

    def delete_student(self, student_id: str):
        """刪除學生"""
        self.get_student(student_id)  # 確認存在
        del self.students[student_id]

    def rename_student(self, student_id: str, new_name: str):
        """修改學生姓名"""
        student = self.get_student(student_id)
        student.name = new_name

    def list_all(self) -> list[Student]:
        """回傳所有學生清單（依學號排序）"""
        return sorted(self.students.values(), key=lambda s: s.student_id)

    # ── 成績管理 ────────────────────────────────────────────────

    def add_grade(self, student_id: str, subject: str, score: float):
        student = self.get_student(student_id)
        student.add_grade(subject, score)

    def remove_grade(self, student_id: str, subject: str):
        student = self.get_student(student_id)
        student.remove_grade(subject)

    # ── 統計分析 ────────────────────────────────────────────────

    def subject_stats(self, subject: str) -> dict:
        """計算特定科目的統計數據"""
        scores = [
            (s.name, s.grades[subject])
            for s in self.students.values()
            if subject in s.grades
        ]
        if not scores:
            return {}
        values = [v for _, v in scores]
        return {
            "subject": subject,
            "count": len(values),
            "average": sum(values) / len(values),
            "highest": max(values),
            "lowest": min(values),
            "scores": sorted(scores, key=lambda x: x[1], reverse=True),
        }

    def ranking(self) -> list[tuple[int, Student]]:
        """依平均分數由高到低排名，回傳 (名次, Student) 串列"""
        sorted_students = sorted(
            self.students.values(),
            key=lambda s: s.average(),
            reverse=True,
        )
        result = []
        rank = 1
        for i, student in enumerate(sorted_students):
            if i > 0 and student.average() < sorted_students[i - 1].average():
                rank = i + 1
            result.append((rank, student))
        return result

    def all_subjects(self) -> list[str]:
        """取得目前所有出現過的科目"""
        subjects = set()
        for s in self.students.values():
            subjects.update(s.grades.keys())
        return sorted(subjects)


# ── 互動選單輔助函式 ─────────────────────────────────────────────

def input_float(prompt: str) -> float:
    """持續要求輸入直到得到合法的浮點數"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  ✗ 請輸入數字")


def print_divider(title: str = ""):
    line = "─" * 40
    if title:
        print(f"\n{'─'*5} {title} {'─'*5}")
    else:
        print(line)


def show_menu():
    print("""
╔══════════════════════════════════╗
║      學生成績管理系統              ║
╠══════════════════════════════════╣
║  1. 新增學生                      ║
║  2. 刪除學生                      ║
║  3. 修改學生姓名                   ║
║  4. 查詢學生                      ║
║  5. 列出所有學生                   ║
╠══════════════════════════════════╣
║  6. 新增/更新成績                  ║
║  7. 刪除成績                      ║
╠══════════════════════════════════╣
║  8. 科目統計分析                   ║
║  9. 全班排名                      ║
╠══════════════════════════════════╣
║  0. 離開                          ║
╚══════════════════════════════════╝""")


def handle_add_student(mgr: GradeManager):
    sid = input("  學號：").strip()
    name = input("  姓名：").strip()
    try:
        mgr.add_student(sid, name)
        print(f"  ✓ 已新增學生 {name}（{sid}）")
    except ValueError as e:
        print(f"  ✗ {e}")


def handle_delete_student(mgr: GradeManager):
    sid = input("  學號：").strip()
    try:
        student = mgr.get_student(sid)
        confirm = input(f"  確認刪除 {student.name}？(y/n)：").strip().lower()
        if confirm == "y":
            mgr.delete_student(sid)
            print("  ✓ 已刪除")
        else:
            print("  已取消")
    except KeyError as e:
        print(f"  ✗ {e}")


def handle_rename_student(mgr: GradeManager):
    sid = input("  學號：").strip()
    new_name = input("  新姓名：").strip()
    try:
        mgr.rename_student(sid, new_name)
        print(f"  ✓ 已更新為 {new_name}")
    except KeyError as e:
        print(f"  ✗ {e}")


def handle_query_student(mgr: GradeManager):
    sid = input("  學號：").strip()
    try:
        student = mgr.get_student(sid)
        print_divider("學生資料")
        print(f"  學號：{student.student_id}")
        print(f"  姓名：{student.name}")
        if student.grades:
            print("  成績：")
            for subject, score in student.grades.items():
                print(f"    {subject}：{score:.1f}")
            print(f"  平均：{student.average():.1f}")
        else:
            print("  （尚無成績）")
    except KeyError as e:
        print(f"  ✗ {e}")


def handle_list_all(mgr: GradeManager):
    students = mgr.list_all()
    if not students:
        print("  （目前無任何學生）")
        return
    print_divider("所有學生")
    for s in students:
        print(f"  {s}")


def handle_add_grade(mgr: GradeManager):
    sid = input("  學號：").strip()
    subject = input("  科目：").strip()
    score = input_float("  成績（0~100）：")
    try:
        mgr.add_grade(sid, subject, score)
        print(f"  ✓ 已記錄 {subject}：{score:.1f}")
    except (KeyError, ValueError) as e:
        print(f"  ✗ {e}")


def handle_remove_grade(mgr: GradeManager):
    sid = input("  學號：").strip()
    subject = input("  科目：").strip()
    try:
        mgr.remove_grade(sid, subject)
        print(f"  ✓ 已刪除 {subject} 成績")
    except (KeyError) as e:
        print(f"  ✗ {e}")


def handle_subject_stats(mgr: GradeManager):
    subjects = mgr.all_subjects()
    if not subjects:
        print("  （目前無任何成績資料）")
        return
    print(f"  現有科目：{', '.join(subjects)}")
    subject = input("  查詢科目：").strip()
    stats = mgr.subject_stats(subject)
    if not stats:
        print(f"  ✗ 科目「{subject}」無資料")
        return
    print_divider(f"{subject} 統計")
    print(f"  人數：{stats['count']}")
    print(f"  平均：{stats['average']:.1f}")
    print(f"  最高：{stats['highest']:.1f}")
    print(f"  最低：{stats['lowest']:.1f}")
    print("  排名：")
    for i, (name, score) in enumerate(stats["scores"], 1):
        print(f"    {i}. {name}  {score:.1f}")


def handle_ranking(mgr: GradeManager):
    ranking = mgr.ranking()
    if not ranking:
        print("  （目前無任何學生）")
        return
    print_divider("全班排名")
    for rank, student in ranking:
        print(f"  第 {rank} 名  {student.name}（{student.student_id}）  平均：{student.average():.1f}")


# ── 主程式 ───────────────────────────────────────────────────────

def main():
    mgr = GradeManager()

    # 預載範例資料，方便直接測試
    sample_data = [
        ("S001", "王小明", {"數學": 92, "英文": 85, "自然": 78}),
        ("S002", "李小華", {"數學": 76, "英文": 91, "自然": 88}),
        ("S003", "陳美玲", {"數學": 65, "英文": 70, "自然": 72}),
    ]
    for sid, name, grades in sample_data:
        s = mgr.add_student(sid, name)
        for subject, score in grades.items():
            s.add_grade(subject, score)

    print("（已預載 3 筆範例學生資料）")

    handlers = {
        "1": handle_add_student,
        "2": handle_delete_student,
        "3": handle_rename_student,
        "4": handle_query_student,
        "5": handle_list_all,
        "6": handle_add_grade,
        "7": handle_remove_grade,
        "8": handle_subject_stats,
        "9": handle_ranking,
    }

    while True:
        show_menu()
        choice = input("請選擇功能：").strip()
        if choice == "0":
            print("再見！")
            break
        elif choice in handlers:
            handlers[choice](mgr)
        else:
            print("  ✗ 無效選項，請重新輸入")


if __name__ == "__main__":
    main()
