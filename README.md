# Sample GitLab Project

This sample project shows how a project in GitLab looks for demonstration purposes. It contains issues, merge requests and Markdown files in many branches,
named and filled with lorem ipsum.

You can look around to get an idea how to structure your project and, when done, you can safely delete this project.

[Learn more about creating GitLab projects.](https://docs.gitlab.com/ee/gitlab-basics/create-project.html)

conda env create -f environment.yml     - установить окрыжение из файла
conda activate playwright_env           - активировать окружение
ctrl+_shift+p Python select interpreter - выбрать окружение для vscode, создаётся файл настроек settings.json
ctrl+_shift+p developer: reload window  - обновить страницу
классы не нужны при playwright
файлы тестирования и функции тестирования должны начинаться на test
название класса при selenium начинается с Test
setTimeout(() => { debugger }, 3000)    - остановит выполнение в devtools console