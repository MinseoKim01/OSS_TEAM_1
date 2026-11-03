/*
 * 등록 화면의 브라우저 동작 담당.
*/
/* 등록 유형별 입력칸 전환 및 입력값 오류 안내 */
const form = document.querySelector('.register-form');
const password = form.elements.namedItem('password');

function updateType() {
    const found = form.elements.type.value === 'found';

    // 선택 유형에 따라 날짜와 시간 제목 변경
    document.getElementById('date-label').textContent =
        found ? '습득 날짜' : '안내 날짜';

    document.getElementById('time-label').textContent =
        found ? '습득 시간' : '안내 시간';

    // 각 입력 영역의 id와 활성화 여부
    const groups = [
        ['report-fields', !found],
        ['found-fields', found]
    ];

    for (const [id, active] of groups) {
        const group = document.getElementById(id);
        group.hidden = !active;

        for (const input of group.querySelectorAll('input')) {
            // 비활성 입력칸은 제출 및 브라우저 검증 대상에서 제외
            input.disabled = !active;
            // 현재 유형에서 사용하는 입력칸만 필수로 설정
            input.required = active;
        }
    }
}

function validatePassword() {
    // 빈 문자열은 사용자 지정 오류가 없다는 의미
    let message = '';

    if (!password.value) {
        message = '삭제 비밀번호를 입력해 주세요.';
    } else if (!/^[0-9]+$/.test(password.value)) {
        message = '삭제 비밀번호는 숫자만 입력해 주세요.';
    } else if (password.value.length !== 4) {
        message = '삭제 비밀번호는 정확히 4자리로 입력해 주세요.';
    }

    // 문구가 있으면 제출 차단, 빈 문자열이면 기존 오류 해제
    password.setCustomValidity(message);
}

// 등록 유형을 바꿀 때 입력 영역과 제목 갱신
for (const radio of form.querySelectorAll('input[name="type"]')) {
    radio.addEventListener('change', updateType);
}

// 브라우저 기본 검증을 통과한 뒤 공백만 입력한 값 추가 검사
form.addEventListener('submit', (event) => {
    const inputs = form.querySelectorAll('[required]:not(:disabled)');

    for (const input of inputs) {
        if (!input.value.trim()) {
            // 서버로 제출하지 않고 해당 입력칸에 오류 표시
            event.preventDefault();
            input.setCustomValidity('공백만 입력할 수 없습니다.');
            input.reportValidity();
            break;
        }
    }
});

// 입력값을 수정하면 비밀번호 재검사 또는 공백 오류 해제
form.addEventListener('input', (event) => {
    if (event.target === password) {
        validatePassword();
    } else {
        event.target.setCustomValidity('');
    }
});

// 브라우저 검증 실패 시 비밀번호 안내 문구 갱신
password.addEventListener('invalid', validatePassword);

// 처음 열거나 서버 응답 후 다시 표시될 때 초기 상태 설정
updateType();
validatePassword();