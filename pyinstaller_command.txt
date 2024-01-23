command for Mac:
pyinstaller --onefile \
            --windowed \
            --name='PDF Merger' \
            --icon='icon.png' \
            --paths ".venv/lib/python3.11/site-packages" \
            --hidden-import PySide6 \
            --hidden-import PyPDF2 \
            --add-data='logo200.ico:.' \ 
            'src\main_app.py'

command for Windows:
pyinstaller --onefile --windowed --name='PDF Merger' --icon='logo200.ico' --paths "venv\Lib\site-packages" --hidden-import PySide6 --hidden-import PyPDF2 --add-data='logo200.ico:.' 'src\main_app.py'