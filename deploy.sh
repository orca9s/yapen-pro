#!/usr/bin/env bash
git add -A
echo "전체파일 staged 영역에 추가"
git add -f .secrets/
echo "git add 막아논 파일 강제로 추가"
eb deploy --profile jsm-eb-user --staged
echo "staged 영역에서 배포시작"
git reset HEAD .secrets/ requirements.txt
echo "staged 영역에 강제로 추가한 파일들 다시 해제"
git reset HEAD
echo "staged 영역에 추가한 파일 전부 해제"
rm requirements.txt
echo "requirements 제거"
git status
echo "배포 완료"