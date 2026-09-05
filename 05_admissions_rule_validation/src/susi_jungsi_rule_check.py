# -*- coding: utf-8 -*-
"""
대학별 정시 산출식을 규칙 테이블로 옮기고 검증하는 연습
- 목적 : 문서에 흩어진 규칙을 데이터로 옮길 때 무엇을 검증해야 하는지 정리한 개인 연습입니다.
- 자료 : 연세대학교 서울캠퍼스 「2027학년도 대학입학전형 시행계획」(공개본) 정시모집 일반전형
         「대학수학능력시험 반영점수 산출방법」 표를 그대로 옮겼습니다.
- 한계 : 참고한 시행계획 공개본만으로는 최종 환산에 필요한 세부 값까지 확인할 수 없습니다.
         여기서는 공개된 반영 배점 범위에서 단순 환산까지만 계산합니다.
실행 : python susi_jungsi_rule_check.py
"""

import pandas as pd

# ---------------------------------------------------------------
# 1. 규칙 테이블  — 모집요강의 표를 '행'으로 옮긴다
# ---------------------------------------------------------------
# 한 대학·한 전형·한 계열이 하나의 규칙 묶음이다.
# 나중에 대학이 늘어나도 코드를 고치지 않고 행만 늘리면 되도록 만들었다.

RULE_AREA = pd.DataFrame([
    # 학년도, 대학, 전형, 계열,     영역,  배점,  활용지표
    (2027, "연세대학교(서울)", "일반전형", "인문", "국어",  300, "표준점수"),
    (2027, "연세대학교(서울)", "일반전형", "인문", "수학",  200, "표준점수"),
    (2027, "연세대학교(서울)", "일반전형", "인문", "탐구",  200, "표준점수"),
    (2027, "연세대학교(서울)", "일반전형", "인문", "영어",  100, "등급"),
    (2027, "연세대학교(서울)", "일반전형", "자연", "국어",  200, "표준점수"),
    (2027, "연세대학교(서울)", "일반전형", "자연", "수학",  300, "표준점수"),
    (2027, "연세대학교(서울)", "일반전형", "자연", "탐구",  300, "표준점수"),
    (2027, "연세대학교(서울)", "일반전형", "자연", "영어",  100, "등급"),
], columns=["학년도", "대학", "전형", "계열", "영역", "배점", "활용지표"])

# 계열별로 요강에 적힌 '합계'를 따로 적어 둔다.
# 배점을 더한 값과 이 값이 같은지 확인하기 위해서다.
RULE_TOTAL = pd.DataFrame([
    (2027, "연세대학교(서울)", "일반전형", "인문", 800),
    (2027, "연세대학교(서울)", "일반전형", "자연", 900),
], columns=["학년도", "대학", "전형", "계열", "합계"])

# 탐구 반영 과목 수
RULE_TAMGU = {("연세대학교(서울)", "일반전형"): 2}

# 영어 등급별 반영점수 (요강 표 그대로)
RULE_ENGLISH = pd.DataFrame([
    (1, 100.0), (2, 95.0), (3, 87.5), (4, 75.0), (5, 60.0),
    (6, 40.0), (7, 25.0), (8, 12.5), (9, 5.0),
], columns=["등급", "점수"])

# 한국사 등급별 감점 (요강 표 그대로)
RULE_HISTORY = pd.DataFrame([
    (1, 0.0), (2, 0.0), (3, 0.0), (4, 0.0), (5, 0.2),
    (6, 0.4), (7, 0.6), (8, 0.8), (9, 1.0),
], columns=["등급", "감점"])


# ---------------------------------------------------------------
# 2. 검증 — 규칙을 옮긴 다음에 반드시 돌리는 여섯 가지
# ---------------------------------------------------------------
def validate(area, total, english, history, tamgu):
    """규칙 테이블이 요강과 어긋나 있는지 확인한다. 어긋난 항목을 목록으로 돌려준다."""
    issues = []

    # V1. 영역 배점의 합이 요강에 적힌 합계와 같은가
    s = area.groupby(["학년도", "대학", "전형", "계열"])["배점"].sum().reset_index()
    m = s.merge(total, on=["학년도", "대학", "전형", "계열"], how="outer", indicator=True)
    for _, r in m.iterrows():
        if r["_merge"] != "both":
            issues.append(f"V1 합계 행이 없음 : {r['대학']} {r['계열']}")
        elif r["배점"] != r["합계"]:
            issues.append(f"V1 배점 합 불일치 : {r['대학']} {r['계열']} — 배점 합 {r['배점']} vs 요강 합계 {r['합계']}")

    # V2. 한 계열 안에서 활용지표가 두 종류 이상 섞여 있지 않은가
    #     (영어처럼 등급으로 쓰는 영역은 예외로 둔다)
    for key, g in area[area["영역"] != "영어"].groupby(["대학", "전형", "계열"]):
        kinds = set(g["활용지표"])
        if len(kinds) > 1:
            issues.append(f"V2 활용지표 혼용 : {key} — {sorted(kinds)}")

    # V3. 등급 환산표에 1~9등급이 빠짐없이 있고 점수가 뒤집히지 않았는가
    for name, df, col, desc in [("영어", english, "점수", True), ("한국사", history, "감점", False)]:
        missing = sorted(set(range(1, 10)) - set(df["등급"]))
        if missing:
            issues.append(f"V3 {name} 등급 누락 : {missing}")
        v = df.sort_values("등급")[col].tolist()
        ok = all(v[i] >= v[i + 1] for i in range(len(v) - 1)) if desc \
            else all(v[i] <= v[i + 1] for i in range(len(v) - 1))
        if not ok:
            issues.append(f"V3 {name} 값이 등급 순서와 어긋남 : {v}")

    # V4. 탐구 반영 과목 수가 규칙에 적혀 있는가
    for key, g in area.groupby(["대학", "전형"]):
        if "탐구" in set(g["영역"]) and key not in tamgu:
            issues.append(f"V4 탐구 반영 과목 수가 없음 : {key}")

    # V5. 배점이 0 이하이거나 비어 있는 행이 없는가
    bad = area[(area["배점"].isna()) | (area["배점"] <= 0)]
    for _, r in bad.iterrows():
        issues.append(f"V5 배점이 비었거나 0 이하 : {r['대학']} {r['계열']} {r['영역']}")

    # V6. 규칙의 학년도가 하나로 통일되어 있는가
    years = sorted(set(area["학년도"]))
    if len(years) > 1:
        issues.append(f"V6 학년도가 섞여 있음 : {years}")

    return issues


# ---------------------------------------------------------------
# 3. 환산 — 같은 성적을 규칙에 넣어 본다
# ---------------------------------------------------------------
def convert(score, univ, jeonhyeong, gyeyeol):
    """
    score : dict — 국어/수학/탐구는 표준점수, 영어/한국사는 등급
    반환  : (환산점수, 계산 내역) / 값이 비어 있으면 (None, 사유)
    """
    rules = RULE_AREA[(RULE_AREA["대학"] == univ) &
                      (RULE_AREA["전형"] == jeonhyeong) &
                      (RULE_AREA["계열"] == gyeyeol)]
    if rules.empty:
        return None, "해당 규칙 없음"

    STD_MAX = 200.0          # 표준점수를 배점으로 옮길 때 기준으로 둔 상한
    detail, total = [], 0.0

    for _, r in rules.iterrows():
        area, jeom = r["영역"], r["배점"]
        v = score.get(area)

        # 미응시·결측을 0점으로 계산하지 않는다. 산출 자체를 멈춘다.
        if v is None:
            return None, f"산출 불가 — {area} 성적이 없음"

        if area == "영어":
            hit = RULE_ENGLISH[RULE_ENGLISH["등급"] == v]
            if hit.empty:
                return None, f"산출 불가 — 영어 {v}등급이 환산표에 없음"
            got = float(hit["점수"].iloc[0]) * (jeom / 100.0)
        else:
            got = (float(v) / STD_MAX) * jeom

        total += got
        detail.append((area, v, jeom, round(got, 2)))

    # 한국사는 총점에서 감점한다
    hg = score.get("한국사")
    if hg is None:
        return None, "산출 불가 — 한국사 성적이 없음"
    hit = RULE_HISTORY[RULE_HISTORY["등급"] == hg]
    if hit.empty:
        return None, f"산출 불가 — 한국사 {hg}등급이 감점표에 없음"
    penalty = float(hit["감점"].iloc[0])
    total -= penalty
    detail.append(("한국사 감점", hg, "-", -penalty))

    return round(total, 2), detail


# ---------------------------------------------------------------
# 4. 실행
# ---------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 62)
    print("[1] 규칙을 옮긴 그대로 검증")
    print("=" * 62)
    issues = validate(RULE_AREA, RULE_TOTAL, RULE_ENGLISH, RULE_HISTORY, RULE_TAMGU)
    print("이상 없음" if not issues else "\n".join(issues))

    print()
    print("=" * 62)
    print("[2] 일부러 틀린 규칙 세 건을 넣고 검증기가 잡는지 확인")
    print("=" * 62)
    bad_area = RULE_AREA.copy()
    bad_area.loc[bad_area["영역"] == "탐구", "활용지표"] = "백분위"   # 지표 혼용
    bad_area.loc[0, "배점"] = 250                                    # 배점 합 어긋남
    bad_eng = RULE_ENGLISH[RULE_ENGLISH["등급"] != 5]                # 5등급 행 누락
    for x in validate(bad_area, RULE_TOTAL, bad_eng, RULE_HISTORY, RULE_TAMGU):
        print("-", x)

    print()
    print("=" * 62)
    print("[3] 같은 성적을 같은 규칙에 넣어 환산")
    print("=" * 62)
    student = {"국어": 131, "수학": 137, "탐구": 128, "영어": 2, "한국사": 3}
    for gy in ["인문", "자연"]:
        v, d = convert(student, "연세대학교(서울)", "일반전형", gy)
        print(f"\n[{gy}] 환산점수 = {v}")
        for row in d:
            print("   ", row)

    print()
    print("=" * 62)
    print("[4] 성적이 비어 있을 때")
    print("=" * 62)
    for missing in ["탐구", "한국사"]:
        s = dict(student)
        s[missing] = None
        print(f"{missing} 없음 →", convert(s, "연세대학교(서울)", "일반전형", "인문"))
