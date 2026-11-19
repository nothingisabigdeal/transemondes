#!/bin/zsh
# Usage : _source/tools/publish.sh "message de commit"
# Reconstruit le site, lance tous les tests, et ne publie QUE si tout est OK et que le compte GitHub actif est le bon.
set -e
cd "${0:A:h}/../.."
python3 _source/tools/build.py "$PWD" >/dev/null
python3 _source/tools/variants.py >/dev/null
if ! python3 _source/tests/run_tests.py > /tmp/transemondes-tests.log 2>&1; then
  grep -E "^KO|réussis|PROBLÈME" /tmp/transemondes-tests.log; echo "❌ Tests en échec : rien n'a été publié."; exit 1
fi
grep -E "réussis|TOUT EST OK" /tmp/transemondes-tests.log
[ "$(gh api user --jq .login)" = "nothingisabigdeal" ] || { echo "❌ Mauvais compte GitHub actif : rien n'a été publié."; exit 1; }
ID=$(gh api user --jq .id)
git add -A
git -c user.name="nothingisabigdeal" -c user.email="${ID}+nothingisabigdeal@users.noreply.github.com" commit -q -m "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git push -q && echo "✅ Publié"
