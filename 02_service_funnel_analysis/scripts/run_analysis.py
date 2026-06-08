"""
run_analysis.py - 실행 래퍼 파일
--------------------------------------
이 파일은 표준 실행 경로(scripts/run_analysis.py)를 지원하기 위한 래퍼입니다.
실제 분석 코드는 python/run_analysis_actual.py에 있습니다.

실행 방법:
  python scripts/run_analysis.py
또는 직접 실행:
  python python/run_analysis_actual.py
"""
from pathlib import Path
import runpy

project_root = Path(__file__).resolve().parents[1]
runpy.run_path(str(project_root / "python" / "run_analysis_actual.py"), run_name="__main__")
