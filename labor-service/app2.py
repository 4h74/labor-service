import streamlit as st

# 1. 페이지 설정 및 브라우저 자동 번역 충돌 차단
st.set_page_config(page_title="노동권익 정밀 문진 서비스", layout="centered")
st.markdown("<html lang='ko' class='notranslate' translate='no'>", unsafe_allow_html=True)

# 스타일 커스텀 가독성 업그레이드
st.markdown("""
    <style>
    .report-box { background-color: #F9FAFB; padding: 28px; border-radius: 14px; border-left: 6px solid #2563EB; margin-top: 20px; }
    .law-ref { background-color: #EFF6FF; padding: 12px; border-radius: 6px; font-size: 0.88rem; color: #1E40AF; margin-top: 8px; border: 1px solid #BFDBFE; }
    .law-title { font-weight: bold; color: #1E3A8A; display: block; margin-bottom: 4px; }
    .solution-box { background-color: #FFFBEB; padding: 16px; border-radius: 10px; border-left: 6px solid #D97706; margin-top: 15px; font-size: 0.95rem; }
    .solution-title { font-weight: bold; color: #92400E; display: block; margin-bottom: 6px; font-size: 1.05rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #111827;'>📋 단기·일용직 노동자 권리 진단 문진표</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6B7280;'>한 질문씩 완료하며 내려가세요. 다음 단계로 넘어가면 이전 선택지는 완전히 잠기며, 잘못 골랐다면 바로 아래 '취소' 버튼을 누르시면 됩니다.</p>", unsafe_allow_html=True)
st.write("---")

# 세션 상태 초기화
if "step" not in st.session_state:
    st.session_state.step = 1
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "temp_answers" not in st.session_state:
    st.session_state.temp_answers = {}

current_step = st.session_state.step

# 📌 Q1. 근무 형태 분류 (근로기준법 제4조 동등결정 원칙 기반)
if current_step >= 1:
    is_locked_1 = current_step > 1
    st.markdown("### 🏢 Q1. 출근은 어떤 방식으로 하시나요?")
    q1_options = [
        "하루 단위로 완전히 새로 계약하고, 내일 출근할지 여부가 늘 불투명합니다. (순수 일용직)",
        "이름만 일용직/단기직이고, 정해진 스케줄이나 약속에 따라 매달 고정적으로 계속 출근합니다. (사실상 상시 고용)"
    ]
    default_q1 = st.session_state.answers.get("work_type", q1_options[0])
    idx_q1 = q1_options.index(default_q1) if default_q1 in q1_options else 0

    st.session_state.temp_answers["work_type"] = st.radio(
        "이름은 일용직이나 알바여도 실제 출근 형태는 다를 수 있습니다.",
        q1_options, key="radio_q1", disabled=is_locked_1, index=idx_q1
    )
    if current_step == 1:
        st.write("")
        if st.button("다음 질문으로 이동 ➡️", key="btn_next_1", use_container_width=True):
            st.session_state.answers["work_type"] = st.session_state.temp_answers["work_type"]
            st.session_state.step = 2
            st.rerun()

# 📌 Q2. 근로시간 측정 (근로기준법 제18조 단시간근로자 기준 적용)
if current_step >= 2:
    st.write("---")
    is_locked_2 = current_step > 2
    st.markdown("### ⏱️ Q2. 일주일에 평균 몇 시간 정도 일하시나요?")
    q2_options = [
        "일주일에 총 15시간 미만으로 일합니다. (초단시간 근로)",
        "일주일에 총 15시간 이상 일합니다. (주휴수당 청구 기준 충족)"
    ]
    default_q2 = st.session_state.answers.get("hours", q2_options[0])
    idx_q2 = q2_options.index(default_q2) if default_q2 in q2_options else 0

    st.session_state.temp_answers["hours"] = st.radio(
        "주휴수당 및 퇴직금을 가르는 가장 중요한 기준선입니다.",
        q2_options, key="radio_q2", disabled=is_locked_2, index=idx_q2
    )
    if current_step == 2:
        st.write("")
        b1, b2 = st.columns(2)
        with b1:
            if st.button("⬅️ Q2 취소하고 Q1으로 돌아가기", key="btn_prev_2", use_container_width=True):
                if "work_type" in st.session_state.answers: del st.session_state.answers["work_type"]
                st.session_state.step = 1
                st.rerun()
        with b2:
            if st.button("다음 질문으로 이동 ➡️", key="btn_next_2", use_container_width=True):
                st.session_state.answers["hours"] = st.session_state.temp_answers["hours"]
                st.session_state.step = 3
                st.rerun()

# 📌 Q3. 연속 근무 기간 (근로자퇴직급여 보장법 및 해고예고 기준 적용)
if current_step >= 3:
    st.write("---")
    is_locked_3 = current_step > 3
    st.markdown("### 📅 Q3. 이 일터(현장)에서 일하신 지 얼마나 되셨나요?")
    q3_options = [
        "아직 일한 지 3개월이 채 되지 않았습니다. (해고예고 예외 가능 기간)",
        "3개월 이상 일했고, 1년은 되지 않았습니다. (해고예고수당 적용 청구 가능)",
        "중간에 긴 공백 없이 계속 일한 지 총 1년 이상 되었습니다. (법정 퇴직금 청구 권리 보장)"
    ]
    default_q3 = st.session_state.answers.get("period", q3_options[0])
    idx_q3 = q3_options.index(default_q3) if default_q3 in q3_options else 0

    st.session_state.temp_answers["period"] = st.radio(
        "연속 근무 기간에 따라 국가 고용보험 의무 가입과 퇴직금 권리가 발생합니다.",
        q3_options, key="radio_q3", disabled=is_locked_3, index=idx_q3
    )
    if current_step == 3:
        st.write("")
        b1, b2 = st.columns(2)
        with b1:
            if st.button("⬅️ Q3 취소하고 Q2로 돌아가기", key="btn_prev_3", use_container_width=True):
                if "hours" in st.session_state.answers: del st.session_state.answers["hours"]
                st.session_state.step = 2
                st.rerun()
        with b2:
            if st.button("다음 질문으로 이동 ➡️", key="btn_next_3", use_container_width=True):
                st.session_state.answers["period"] = st.session_state.temp_answers["period"]
                st.session_state.step = 4
                st.rerun()

# 📌 Q4. 임금 수령 방식 (💡 선택지 안내 문구 보완)
if current_step >= 4:
    st.write("---")
    is_locked_4 = current_step > 4
    st.markdown("### 💰 Q4. 일당이나 시급은 어떻게 정해졌나요?")
    q4_options = [
        "순수 시급제/일당제입니다. (내가 일한 시간·날짜만큼 정직하게 계산하며, 요건 충족 시 주휴수당은 별도로 더 얹어서 받아야 합니다.)",
        "포괄임금 형태입니다. (일당이나 월급을 고정으로 받으며, 그 돈 안에 주휴수당과 연장수당이 이미 다 들어있다고 안내받았습니다.)"
    ]
    default_q4 = st.session_state.answers.get("wage_type", q4_options[0])
    idx_q4 = q4_options.index(default_q4) if default_q4 in q4_options else 0

    st.session_state.temp_answers["wage_type"] = st.radio(
        "일반적인 편의점·음식점 알바는 대부분 1번에 해당합니다. 계약 꼼수 여부를 분석하는 문항입니다.",
        q4_options, key="radio_q4", disabled=is_locked_4, index=idx_q4
    )
    if current_step == 4:
        st.write("")
        b1, b2 = st.columns(2)
        with b1:
            if st.button("⬅️ Q4 취소하고 Q3로 돌아가기", key="btn_prev_4", use_container_width=True):
                if "period" in st.session_state.answers: del st.session_state.answers["period"]
                st.session_state.step = 3
                st.rerun()
        with b2:
            if st.button("다음 질문으로 이동 ➡️", key="btn_next_4", use_container_width=True):
                st.session_state.answers["wage_type"] = st.session_state.temp_answers["wage_type"]
                st.session_state.step = 5
                st.rerun()

# 📌 Q5. 피해 유형 선택
if current_step >= 5:
    st.write("---")
    is_locked_5 = current_step > 5
    st.markdown("### 🚨 Q5. 현재 현장에서 어떤 부당한 대우나 피해를 겪고 계시나요?")
    
    q5_options = [
        "💰 임금체불 및 주휴수당 미지급",
        "🏥 산업재해 (일하다 다쳤는데 회사가 처리를 막음)",
        "🚪 부당해고 및 갑작스러운 출근 배제 (잘림)",
        "🏗️ 인력사무소/하도급 팀장의 임금 미지급 (중간착취 및 연대책임)",
        "🌐 외국인 노동자 권리 침해 (체류자격 분쟁, 여권 압수, 미등록 신분 불이익 등)"
    ]
    
    default_q5 = st.session_state.answers.get("damage_type", q5_options[0])
    idx_q5 = q5_options.index(default_q5) if default_q5 in q5_options else 0

    st.session_state.temp_answers["damage_type"] = st.selectbox(
        "현재 일터에서 겪고 계신 가장 핵심적인 어려움 양식을 선택해 주세요.",
        q5_options, key="select_q5", disabled=is_locked_5, index=idx_q5
    )
    
    if current_step == 5:
        st.write("")
        b1, b2 = st.columns(2)
        with b1:
            if st.button("⬅️ Q5 취소하고 Q4로 돌아가기", key="btn_prev_5", use_container_width=True):
                if "wage_type" in st.session_state.answers: del st.session_state.answers["wage_type"]
                st.session_state.step = 4
                st.rerun()
        with b2:
            if st.button("📊 나의 권리 진단 결과 보기", type="primary", key="btn_finish", use_container_width=True):
                st.session_state.answers["damage_type"] = st.session_state.temp_answers["damage_type"]
                st.session_state.step = 6
                st.rerun()

# ---------------------------------------------------------
# [결과 출력 파트]
# ---------------------------------------------------------
if current_step == 6:
    st.write("---")
    ans = st.session_state.answers
    
    is_regular = "사실상 상시 고용" in ans.get("work_type", "")
    is_over_15 = "15시간 이상" in ans.get("hours", "")
    is_under_3m = "3개월이 채 되지 않았습니다" in ans.get("period", "")
    is_over_3m = "3개월 이상" in ans.get("period", "") or "1년 이상" in ans.get("period", "")
    is_over_1y = "1년 이상" in ans.get("period", "")
    is_pogwal = "포괄임금" in ans.get("wage_type", "")
    damage = ans.get("damage_type", "")

    st.markdown("<div class='report-box'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='margin-top:0; color: #1E40AF;'>🔍 맞춤형 노동권익 진단서: {damage}</h3>", unsafe_allow_html=True)
    
    if is_regular:
        st.warning("⚠️ **실질 법적 신분:** [상시 고용된 단기/기간제 근로자]")
        st.write("형식상의 명칭(일용직, 단기 알바)과 상관없이 고정적인 약속과 스케줄에 따라 출근했다면 근로기준법상 일반 근로자 지위와 강력한 권리가 보장됩니다.")
    else:
        st.success("✅ **실질 법적 신분:** [순수 일용 근로자]")
        st.write("하루 단위로 계약 관계가 자유롭게 성립하고 완전히 종료되는 정통 일용직 신분입니다.")

    st.markdown("<h4>🎯 선택하신 분쟁 상황 대처 지침 및 법리</h4>", unsafe_allow_html=True)
    
    if "임금체불" in damage:
        if is_over_15:
            st.write("귀하는 **1주 소정근로시간 15시간 이상** 요건을 명확히 충족합니다. 따라서 기본 일당뿐만 아니라 **주휴수당 미지급분 전체 역시 명백한 임금체불에 해당**하여 고용노동청에 신고할 수 있습니다.")
            st.markdown("""
                <div class='law-ref'>
                    <span class='law-title'>⚖️ 근로기준법 제18조(단시간근로자의 근로조건)</span>
                    4주 동안을 평균하여 1주 동안의 소정근로시간이 15시간 미만인 근로자에게는 휴일(주휴수당)과 연차유급휴가 규정을 적용하지 아니한다.
                </div>
            """, unsafe_allow_html=True)
        else:
            st.write("주 소정근로시간이 15시간 미만이므로 법정 주휴수당은 제외되나, **실제 근무하고 받지 못한 일당 전액은 당연히 임금체불**이므로 전액을 청구할 수 있습니다.")
            st.markdown("""
                <div class='law-ref'>
                    <span class='law-title'>⚖️ 근로기준법 제43조(임금 지급)</span>
                    임금은 통화로 직접 근로자에게 그 '전액'을 지급하여야 한다.
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("""
            <div class='solution-box'>
                <span class='solution-title'>💡 당장 내가 해야 할 일 (임금체불 해결방안)</span>
                1. <b>증거 수집:</b> 출퇴근 기록(캘린더, 문자 기록, 교통카드 내역)과 급여를 받은 계좌 내역을 캡처하세요.<br>
                2. <b>무료 도움처:</b> <b>고용노동부 청소년근로권익센터(국번없이 1644-3119)</b>에 연락하면 만 34세 이하 청년·대학생은 배정된 공인노무사에게 무료로 진정서 작성 도움을 받을 수 있습니다.<br>
                3. <b>신고하기:</b> '고용노동부 민원마당' 사이트에서 <b>[임금체불 진정서]</b>를 접수하십시오.
            </div>
        """, unsafe_allow_html=True)
            
    elif "산업재해" in damage:
        st.write("**산재보험은 사업장의 규모, 근로 기간, 국적 및 체류 자격(미등록 불법체류 포함)을 절대로 차별하지 않고 100% 적용됩니다.** 사업주의 동의를 구걸할 필요가 전혀 없으니, 치료받으신 병원 원무과의 산재 담당자를 통해 근로복지공단에 직접 신청(요양급여 청구)하세요.")
        st.markdown("""
            <div class='law-ref'>
                <span class='law-title'>⚖️ 근로기준법 제78조(요양보상) 및 제6조(균등한 처우)</span>
                근로자가 업무상 부상 또는 질병에 걸리면 사용자는 그 비용으로 필요한 요양을 행하거나 요양비를 부담해야 하며, 국적이나 사회적 신분을 이유로 차별적 처우를 하지 못한다.
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class='solution-box'>
                <span class='solution-title'>💡 당장 내가 해야 할 일 (산재 구제 해결방안)</span>
                1. <b>병원 방문:</b> 의사에게 "일하다가 다쳤다"고 명확히 말하고 최초진단서를 발급받으세요.<br>
                2. <b>사업주 압박 불필요:</b> 회사가 산재 처리를 거부하더라도 근로자가 직접 신청 가능합니다.<br>
                3. <b>무료 도움처:</b> <b>근로복지공단(1588-0075)</b> 고객센터에 문의하여 현장 주소지를 말하고 '요양급여 및 휴업급여 신청서'를 제출하십시오.
            </div>
        """, unsafe_allow_html=True)
        
    elif "부당해고" in damage:
        if is_over_3m:
            st.write("근무 기간이 **3개월 이상**이므로, 회사가 갑작스럽게 나오지 말라고 하거나 출근 배제를 했다면 **최소 30일 전에 예고했어야 합니다.** 그렇지 않았다면 **30일분 이상의 통상임금(해고예고수당)**을 노동청에 즉시 청구해 받아내야 합니다.")
            st.markdown("""
                <div class='law-ref'>
                    <span class='law-title'>⚖️ 근로기준법 제26조(해고의 예고)</span>
                    사용자는 근로자를 해고하려면 적어도 30일 전에 예고를 하여야 하고, 30일 전에 예고를 하지 아니하였을 때에는 30일분 이상의 통상임금을 지급하여야 한다.
                </div>
            """, unsafe_allow_html=True)
        else:
            st.write("연속 근무 기간이 3개월 미만이라 30일 치의 해고예고수당 청구는 법적으로 어렵습니다. 다만, 계약한 당일 중간에 부당하게 쫓겨났거나 약속된 일당이 있다면 근로조건 위반에 따른 손해배상을 따질 수 있습니다.")

        st.markdown("""
            <div class='solution-box'>
                <span class='solution-title'>💡 당장 내가 해야 할 일 (부당해고 대처방안)</span>
                1. <b>"자진 퇴사" 유도 거부:</b> 사직서에 절대 서명하지 말고, 카카오톡이나 문자로 "나는 계속 일하고 싶다"는 의사를 남기세요.<br>
                2. <b>해고 통보 증거 확보:</b> 사장이 "내일부터 나오지 마라"고 말한 녹취록이나 문자메시지를 반드시 저장해두세요.<br>
                3. <b>무료 도움처:</b> 상시 근로자 5인 이상 사업장이라면 해고일로부터 3개월 이내에 <b>지방노동위원회</b>에 구제신청을 하거나, 3개월 이상 근무 시 고용노동청에 '해고예고수당' 지급 진정을 제기할 수 있습니다.
            </div>
        """, unsafe_allow_html=True)

    elif "팀장의 임금 미지급" in damage:
        st.write("중간 하도급 팀장이 일당을 가로채거나 떼먹고 도망치더라도, **근로기준법에 따라 상위 하청 시공사 또는 원청 종합건설 대기업이 연대하여 임금을 지급할 법적 책임**을 집니다. 원청 현장 사무실에 '직불 청구' 의사를 밝히거나, 노동청 신고 시 원청과 팀장을 함께 연대책임으로 진정하십시오.")
        st.markdown("""
            <div class='law-ref'>
                <span class='law-title'>⚖️ 근로기준법 제44조의2(건설업 공사도급에 있어서의 임금지급 연대책임)</span>
                건설업에서 도급받은 하수급인이 근로자에게 임금을 지급하지 못하면, 그 직상 수급인은 하수급인과 연대하여 임금을 지급할 책임을 진다.
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class='solution-box'>
                <span class='solution-title'>💡 당장 내가 해야 할 일 (건설현장 임금 미지급 해결방안)</span>
                1. <b>원청(종합건설사) 압박:</b> 건설현장 내의 원청 안전실이나 공사팀 사무실로 찾아가 "하도급 팀장이 임금을 체불했으니 근로기준법 제44조의2에 따라 원청에서 직접 지급해달라"고 요구하십시오.<br>
                2. <b>현장 증거 확보:</b> 내가 이 현장에서 일했다는 증거(현장 게이트 출입 내역, 안전교육 이수증, 작업 사진)를 모으세요.<br>
                3. <b>무료 도움처:</b> 고용노동청에 신고할 때 피진정인에 <b>'팀장'과 '원청 시공사 대표'를 공동으로 기재</b>하여 제출하십시오.
            </div>
        """, unsafe_allow_html=True)

    elif "외국인" in damage:
        st.error("🚨 **외국인 노동자 특별 보호 소견:**")
        st.write("대한민국 근로기준법은 미등록 체류(불법체류) 여부와 상관없이 똑같이 적용됩니다. 떼인 임금, 주휴수당, 퇴직금, 산재 보상은 법적으로 완벽하게 청구 가능합니다.")
        st.markdown("""
            <div class='law-ref'>
                <span class='law-title'>⚖️ 근로기준법 제6조(균등한 처우) 및 제36조(금품 청산)</span>
                사용자는 국적을 이유로 근로조건에 대한 차별적 처우를 하지 못하며, 퇴직 시 14일 이내에 금품을 청산하여야 한다.
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class='solution-box'>
                <span class='solution-title'>💡 당장 내가 해야 할 일 (외국인 노동자 안전 구제방안)</span>
                1. <b>강제추방 걱정 금지:</b> 법무부 지침상 고용노동청에 임금체불을 신고하더라도 노동청 공무원은 출입국사무소에 고발할 의무가 면제됩니다(통보의무 면제제도). 안심하고 신고하세요.<br>
                2. <b>외국어 상담 센터 이용:</b> 한국어 소통이 어렵다면 전국의 <b>외국인노동자지원센터(1577-0071)</b>에 방문하시면 모국어 통역과 함께 무료 법률 지원을 제공합니다.<br>
                3. <b>여권 압수 대처:</b> 사업주가 여권이나 통장을 강제로 보관하는 것은 불법이므로 즉시 반환을 요구하십시오.
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.write("")
    
    if st.button("🔄 문진표 처음부터 다시 작성하기", use_container_width=True):
        st.session_state.step = 1
        st.session_state.answers = {}
        st.session_state.temp_answers = {}
        st.rerun()