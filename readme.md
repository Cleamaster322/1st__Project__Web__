Небольшой гайд , который будет уточняться , по мере
вкуривания данной темы . 
1. Вы запуллили эту директорию себе в локальное хранилище.
2. Открыли в ide директорию flask_directory
3. Вам нужно создать виртуальное окружение . Пичарм
обычно делает это сам , но если этого не произошло
   используйте в терминале команду: python -m venv venv
   Эта команда создаст в рабочей директории виртуальное окружение . 
4. Далее вам нужно установить пакеты , список которых
указан в файле requirements.txt . Опять же , пичарм обычно
   делает это сам , но на всякий , консольная команда 
   для этого : pip install -r requirements.txt
5. Если вы используете не пичарм , могут потребоваться
некоторые лишние телодвижения , но там уже если че 
   мне (Егору) черканите и я подскажу мб , ну или сами
   выкупите , впринципе то , что я написал это основное , 
   но допустим vscode нужно отдельно указывать имя исполняемого файла
   , на всякий случай далее будет копипаст ридмихи Загуменова, там
   некоторые такие случаи отражены .
   
6. В папке templates хранятся html шаблоны.
7. В папке статик хранятся css-файлы , картинки ,
шрифты и т.д.




README FROM ZAGUMENOV
1. Clone or download as zip this repository to projects folder on your computer.
2. Open terminal in project folder and run command `python -m venv venv`. This will create virtual environment.
3. Activate virtual environment via `venv\Scripts\activate` command.
4. Install required packages via `pip install -r requirements.txt`.
5. Set environment variables for flask: `set FLASK_APP=app.py` and `set FLASK_ENV=development`.
6. Run flask server via `flask run` command.
   