#!/bin/zsh
cd -- "${0:A:h}"
if [[ -x .venv/bin/python ]] && .venv/bin/python -c 'import sc2reader' 2>/dev/null; then
  exec .venv/bin/python launch.py
elif [[ -x .venv312/bin/python ]]; then
  exec .venv312/bin/python launch.py
else
  echo '請先依 README 安裝 Python 與 requirements.txt。'
  read '?按 Enter 關閉'
fi
