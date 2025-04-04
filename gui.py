from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QTableWidget, \
    QTableWidgetItem, QLineEdit, QComboBox, QRadioButton, QHBoxLayout, QDialog, QGridLayout, QFrame, QSizePolicy, QSplitter, QSpacerItem
from PyQt6.QtGui import QFont
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QValueAxis, QCategoryAxis
from PyQt6.QtCore import Qt
from widgets import MatrixInputDialog
from utils import create_x, create_c, compute_D_matrix, compute_G_matrix, hungarian_algorithm, greedy_algorithm

class AssignmentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    from PyQt6.QtWidgets import QSizePolicy

    def initUI(self):
        self.setWindowTitle("Assignment Problem Solver")
        main_layout = QVBoxLayout()
        main_layout.setSpacing(2)
        main_layout.setContentsMargins(15, 5, 5, 5)

        # Верхняя часть (управление)
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(2)

        # Элементы управления
        self.language_label = QLabel("Choose Language:")
        self.language_selector = QComboBox()
        self.language_selector.addItems(["English", "Русский"])
        self.language_selector.currentIndexChanged.connect(self.update_language)

        self.theme_label = QLabel("Choose a Theme:")
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["🌰 Brown-Mint", "💙 Blue-Pink", "⚫ Black-White", "💚 Green-Yellow"])
        self.theme_selector.currentIndexChanged.connect(self.update_theme)

        self.n_input_label = QLabel("Matrix size (N, max 15):")
        self.n_input = QLineEdit()
        self.n_input.setMaxLength(2)
        self.n_input.setStyleSheet("background-color: #fff; color: #000; border: 1px solid #ccc;")

        self.gen_mode_label = QLabel("Matrix Generation Mode:")

        # Ограничиваем высоту элементов управления
        for widget in [self.language_selector, self.theme_selector, self.n_input, self.gen_mode_label]:
            #widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            widget.setMaximumHeight(25)

        controls_layout.addWidget(self.language_label)
        controls_layout.addWidget(self.language_selector)
        controls_layout.addWidget(self.theme_label)
        controls_layout.addWidget(self.theme_selector)
        controls_layout.addWidget(self.n_input_label)
        controls_layout.addWidget(self.n_input)

        # Радио-кнопки
        mode_layout = QHBoxLayout()
        mode_layout.setSpacing(2)

        self.auto_generate = QRadioButton("Auto Generate")
        self.manual_input = QRadioButton("Manual Input")
        self.auto_generate.setChecked(True)
        self.auto_generate.toggled.connect(self.toggle_generation_mode)

        mode_layout.addWidget(self.manual_input)
        mode_layout.addWidget(self.auto_generate)

        controls_layout.addLayout(mode_layout)

        self.gen_mode = QComboBox()
        self.gen_mode.setStyleSheet("background-color: #fff; color: #000; border: 1px solid #ccc;")
        self.gen_mode.addItems(["Random", "Rows Increasing", "Rows Decreasing", "Cols Increasing", "Cols Decreasing"])
        self.gen_mode.setMaximumHeight(25)

        controls_layout.addWidget(self.gen_mode_label)
        controls_layout.addWidget(self.gen_mode)

        # Кнопка запуска
        self.calc_button = QPushButton("Generate and Solve")
        self.calc_button.clicked.connect(self.calculate)
        self.calc_button.setMaximumHeight(30)

        controls_layout.addWidget(self.calc_button)

        # Добавляем в основной layout
        main_layout.addLayout(controls_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Нижняя часть (результаты + диаграмма)
        splitter = QSplitter()

        data_layout = QVBoxLayout()
        self.data_text = QTextEdit()
        self.data_text.setReadOnly(True)
        self.data_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        data_layout.addWidget(self.data_text, 1)

        left_widget = QWidget()
        left_widget.setLayout(data_layout)

        result_widget = QWidget()
        result_layout = QVBoxLayout(result_widget)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        result_layout.addWidget(self.result_text, 1)

        self.chart_view = QChartView()
        result_layout.addWidget(self.chart_view, 2)

        splitter.addWidget(left_widget)
        splitter.addWidget(result_widget)

        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 1)

        splitter.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        main_layout.addWidget(splitter, 1)

        self.setLayout(main_layout)

        self.toggle_generation_mode()
        self.update_theme()
        self.update_language()

    def update_language(self):
        lang = self.language_selector.currentText()

        themes = {
            "English": ["🌰 Brown-Mint", "💙 Blue-Pink", "⚫ Black-White", "💚 Green-Yellow"],
            "Русский": ["🌰 Коричнево-Мятная", "💙 Сине-розовая", "⚫ Черно-Белая", "💚 Зелено-Желтая"]
        }

        modes = {
            "English": ["Random", "Rows Increasing", "Rows Decreasing", "Cols Increasing", "Cols Decreasing"],
            "Русский": ["Случайные значения", "Возрастание по строкам", "Убывание по строкам",
                        "Возрастание по столбцам", "Убывание по столбцам"]
        }

        if lang == "Русский":
            self.setWindowTitle("Решение задачи о назначениях")
            self.language_label.setText("Выберете язык:")
            self.theme_label.setText("Выберите тему:")
            self.theme_selector.clear()
            self.theme_selector.addItems(themes["Русский"])
            self.n_input_label.setText("Введите размер матрицы (макс. 15):")
            self.gen_mode_label.setText("Режим генерации матрицы:")
            self.auto_generate.setText("Авто-генерация")
            self.manual_input.setText("Ручной ввод")
            self.calc_button.setText("Сгенерировать и решить")
            self.data_text.setPlaceholderText("Здесь будут матрицы...")
            self.result_text.setPlaceholderText("Здесь будут результаты...")
        else:  # English
            self.setWindowTitle("Assignment Problem Solver")
            self.language_label.setText("Choose Language:")
            self.theme_label.setText("Choose a Theme:")
            self.theme_selector.clear()
            self.theme_selector.addItems(themes["English"])
            self.n_input_label.setText("Input matrix size (max 15):")
            self.gen_mode_label.setText("Matrix Generation Mode:")
            self.auto_generate.setText("Auto Generate")
            self.manual_input.setText("Manual Input")
            self.calc_button.setText("Generate and Solve")
            self.data_text.setPlaceholderText("Matrices will be displayed here...")
            self.result_text.setPlaceholderText("Results will be displayed here...")

        current_index = self.gen_mode.currentIndex()  # Запоминаем текущий выбор
        self.gen_mode.clear()
        self.gen_mode.addItems(modes[lang])
        self.gen_mode.setCurrentIndex(current_index)

    def update_theme(self):
        theme_map = {
            "🌰 Brown-Mint": {
                "background": "#A3C1AD",
                "light_background": "#CDE7D6",
                "text": "#654321",
                "button_background": "#654321",
                "button_text": "white"
            },
            "💙 Blue-Pink": {
                "background": "#A6D8E0",
                "light_background": "#D0F0FF",
                "text": "#800000",
                "button_background": "#1E90FF",
                "button_text": "white"
            },
            "⚫ Black-White": {
                "background": "white",
                "light_background": "#E0E0E0",
                "text": "black",
                "button_background": "gray",
                "button_text": "white"
            },
            "💚 Green-Yellow": {
                "background": "#F0E68C",
                "light_background": "#FFFFAA",
                "text": "#3CB371",
                "button_background": "#FFD700",
                "button_text": "black"
            }
        }

        theme_translation = {
            "🌰 Коричнево-Мятная": "🌰 Brown-Mint",
            "💙 Сине-розовая": "💙 Blue-Pink",
            "⚫ Черно-Белая": "⚫ Black-White",
            "💚 Зелено-Желтая": "💚 Green-Yellow"
        }

        theme = self.theme_selector.currentText()

        if theme in theme_translation:
            theme = theme_translation[theme]

        if theme not in theme_map:
            print(f"Warning: Theme '{theme}' not found. Using default.")
            return

        colors = theme_map[theme]

        self.setStyleSheet(f"background-color: {colors['background']}; color: {colors['text']}; font-size: 16px;")
        self.calc_button.setStyleSheet(
            f"background-color: {colors['button_background']}; color: {colors['button_text']}; padding: 5px; font-size: 16px;"
        )
        self.data_text.setStyleSheet(f"background-color: white; color: {colors['text']};")
        self.result_text.setStyleSheet(f"background-color: white; color: {colors['text']};")

        light_bg = colors["light_background"]
        self.language_selector.setStyleSheet(
            f"background-color: {light_bg}; color: {colors['text']}; border: 1px solid #bbb;")
        self.theme_selector.setStyleSheet(
            f"background-color: {light_bg}; color: {colors['text']}; border: 1px solid #bbb;")

    def toggle_generation_mode(self):
        is_auto = self.auto_generate.isChecked()
        self.gen_mode_label.setVisible(is_auto)
        self.gen_mode.setVisible(is_auto)

    def update_chart(self, hungarian_value, greedy_value):
        chart = QChart()
        series = QBarSeries()

        lang = self.language_selector.currentText()
        if lang == "Русский":
            hungarian_text = "Венгерский"
            greedy_text = "Жадный"
            comparison_text = "Сравнение алгоритмов"
        else:
            hungarian_text = "Hungarian"
            greedy_text = "Greedy"
            comparison_text = "Comparison algirithms"

        hungarian_set = QBarSet(hungarian_text)
        hungarian_set.append(hungarian_value)
        greedy_set = QBarSet(greedy_text)
        greedy_set.append(greedy_value)

        series.append(hungarian_set)
        series.append(greedy_set)
        chart.addSeries(series)
        chart.setTitle(comparison_text)
        chart.createDefaultAxes()

        self.chart_view.setChart(chart)

    def format_matrix(self, title, matrix):
        formatted = f"<b><font size='3'>{title}</font></b><br><table border='1' cellpadding='8'>"
        for row in matrix:
            formatted += "<tr>" + "".join(f"<td align='center'>{val}</td>" for val in row) + "</tr>"
        formatted += "</table><br>"
        return formatted

    def format_matrix_2f(self, title, matrix):
        formatted = f"<b><font size='3'>{title}</font></b><br><table border='1' cellpadding='8'>"
        for row in matrix:
            formatted += "<tr>" + "".join(f"<td align='center'>{val:.2f}</td>" for val in row) + "</tr>"
        formatted += "</table><br>"
        return formatted

    def calculate(self):
        try:
            n = int(self.n_input.text())
            if n < 1 or n > 15:
                self.result_text.setText("Error: N must be between 1 and 15.")
                return

            if self.manual_input.isChecked():
                dialog = MatrixInputDialog(n)
                if dialog.exec():
                    C, chi = dialog.get_values()
                    if C is None:
                        return

            else:
                mode = self.gen_mode.currentText()
                C = create_c(n, mode)
                chi = create_x(n, 0, 1)

            D = compute_D_matrix(C, chi)
            G = compute_G_matrix(C, chi)
            hungarian_perm, hungarian_value = hungarian_algorithm(D)
            greedy_perm, greedy_value = greedy_algorithm(D)

            self.update_chart(hungarian_value, greedy_value)

            lang = self.language_selector.currentText()
            if lang == "Русский":
                matrix_title = "Матрица "
                vector_title = "Вектор "
                results_title = "Результаты:"
                hungarian_text = "Венгерский алгоритм:"
                greedy_text = "Жадный алгоритм:"
                comparison_text = "Венгерский лучше Жадного на"
                value_text = "Значение:"
                error_text = "Ошибка: введите значения."
            else:
                matrix_title = "Matrix "
                vector_title = "Vector "
                results_title = "Results:"
                hungarian_text = "Hungarian assignment:"
                greedy_text = "Greedy assignment:"
                comparison_text = "Hungarian is better than Greedy by"
                value_text = "Value:"
                error_text = "Error: Please enter valid numbers."

            data_html = "<table style='border-collapse: collapse;'>"
            data_html += f"<tr><td>{self.format_matrix(matrix_title + 'C', C)}</td>"
            data_html += f"<td style='padding-left: 10px;'>{self.format_matrix_2f(matrix_title + 'D', D)}</td></tr>"
            data_html += f"<tr><td>{self.format_matrix_2f(vector_title + 'X', [chi])}</td>"
            data_html += f"<td style='padding-left: 10px;'>{self.format_matrix_2f(matrix_title + 'G', G)}</td></tr>"
            data_html += "</table>"
            self.data_text.setHtml(data_html)

            result_html = f"<div style='display: flex; flex-direction: column; align-items: flex-start;'>"
            result_html += f"<b><font size='6' color='#8B0000'>{results_title}</font></b><br>"

            result_html += f"<b><font color='#00008B'>{hungarian_text}</font> <font color='#FF0000'>{hungarian_value:.2f}</font></b><br>"
            result_html += f"<b><font color='#008000'>{greedy_text}</font> <font color='#FF0000'>{greedy_value:.2f}</font></b><br>"
            result_html += f"<b><font color='#8B0000'>{comparison_text}</font> <font color='#FF0000'>{(1 - greedy_value / hungarian_value) * 100:.2f}%</font></b><br>"
            self.result_text.setHtml(result_html)

        except ValueError:
            self.result_text.setText(error_text)