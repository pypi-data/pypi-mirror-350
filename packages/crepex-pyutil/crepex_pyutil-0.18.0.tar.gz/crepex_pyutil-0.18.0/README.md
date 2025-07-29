# CrepeX python util

## 개발환경
- `poetry` 를 사용해서 개발
- 가상환경은 `poetry shell`
- 패키지 설치는 `poetry install`
- 최조 pre-commit 셋팅 `pre-commit install`

## 배포

### 테스트
- TestPypi 계정준비, API 토큰 준비

```shell
# test pypi repository 등록
poetry config repositories.testpypi https://test.pypi.org/legacy/
# poetry 에 토큰 등록
poetry config http-basic.testpypi __token__ pypi-your-api-token-here

# Build & Publish
poetry build
poetry publish -r testpypi

# Get package
pip install -i https://test.pypi.org/.../your-package-name
```

### 프로덕션
- Pypi 계정준비, API 토큰 준비
```shell
# poetry 에 토큰 등록
poetry config pypi-token.pypi pypi-your-token-here

# Build & Publish
poetry publish --build
```
