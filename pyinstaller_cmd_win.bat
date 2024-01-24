pyinstaller --onefile --windowed ^
            --name="PDF Merger" ^
            --icon="icons\\logo200.ico" ^
            --paths "venv\\Lib\\site-packages" ^
            --hidden-import PySide6 ^
            --hidden-import PyPDF2 ^
            --add-data="icons\logo200.ico;.\icons' ^
            --add-data="icons\copy24.png;.\icons' ^
            --add-data="icons\delete24.png;.\icons" ^
            "src\main_app.py"
