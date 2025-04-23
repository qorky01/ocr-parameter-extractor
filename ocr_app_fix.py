import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd

# 1. Tesseract 경로 설정 (Windows 기준)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 2. OCR 오타 보정 딕셔너리
corrections = {
    "ntroduction Method": "Introduction Method",
    "jon Mode": "Ion Mode"
}

# 3. 파라미터/값 줄 고정 매칭 함수
def extract_fixed_parameters(lines):
    if len(lines) < 22:
        return []

    # 고정된 줄 번호 기준 분리
    params = lines[:11]
    values = lines[11:22]

    extracted_data = []
    for p, v in zip(params, values):
        param = corrections.get(p.strip(), p.strip())
        value = v.strip()
        extracted_data.append((param, value))

    return extracted_data

# Streamlit UI 시작
st.title("🧪 고정 구조 장비 파라미터 OCR 추출기")

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드한 이미지", use_container_width=True)

    # OCR 실행
    text = pytesseract.image_to_string(image, lang='eng')

    # 📌 OCR 텍스트는 expander 안에 넣어서 "펼쳐보기" 형태로
    with st.expander("📄 OCR 텍스트 보기"):
        st.text(text)

    # 줄 정리
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    extracted_data = extract_fixed_parameters(lines)

    if extracted_data:
        df = pd.DataFrame(extracted_data, columns=["Parameter", "Value"])
        st.subheader("📊 추출된 파라미터")
        st.dataframe(df)

        # 다운로드 버튼
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ CSV 다운로드", csv, "ocr_parameters.csv", "text/csv")
    else:
        st.warning("❗ 줄 수가 예상과 다릅니다. 올바른 형식의 이미지를 업로드해주세요.")
