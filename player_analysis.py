import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# 기존의 main 분석 함수 (필요한 분석 코드를 포함)
def main(player_id, player_name, video_path, player_number):
    # 여기서는 샘플 데이터를 생성합니다 (API를 통해 가져온 데이터를 사용할 수도 있음)
    df = pd.DataFrame({
        'passes': [10],
        'goals': [2],
        'tackles': [5]
    })

    # PDF 생성
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, f'{player_name} 분석 보고서', ln=True, align='C')

    # 스탯 기록
    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 10, f'Player ID: {player_id}', ln=True)
    pdf.cell(200, 10, f'Player Number: {player_number}', ln=True)
    pdf.cell(200, 10, f'Passes: {df["passes"][0]}', ln=True)
    pdf.cell(200, 10, f'Goals: {df["goals"][0]}', ln=True)
    pdf.cell(200, 10, f'Tackles: {df["tackles"][0]}', ln=True)

    # 그래프 시각화
    plt.bar(df.columns, df.iloc[0])
    plt.title(f"{player_name}'s Performance")
    plt.savefig('stat_plot.png')

    # PDF에 그래프 삽입
    pdf.image('stat_plot.png', x=10, y=60, w=100)

    # PDF 저장
    pdf_filename = f"{player_name}_stat_report.pdf"
    pdf.output(pdf_filename)

    # 그래프 이미지 삭제 (청소 작업)
    os.remove('stat_plot.png')
