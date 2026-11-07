clean_allure_reports:
	cmd /c "if exist allure_results rmdir /s /q allure_results"

clean_pycache:
	powershell -NoProfile -Command "Get-ChildItem -Directory -Recurse -Filter __pycache__ | Remove-Item -Force -Recurse"

run_allure:
	cmd /c "allure serve allure_results"