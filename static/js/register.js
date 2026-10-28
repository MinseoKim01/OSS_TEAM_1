/*
 * 등록 화면의 브라우저 동작 담당.
*/
/* 등록 유형별 입력칸 전환 및 입력값 오류 안내 */
const form = document.querySelector('.register-form');
const password = form.elements.namedItem('password');

function updateType() {
    const found = form.elements.type.value === 'found';

    document.getElementById('date-label').textContent =
        found ? '습득 날짜' : '안내 날짜';

    document.getElementById('time-label').textContent =
        found ? '습득 시간' : '안내 시간';

    const groups = [
        ['report-fields', !found],
        ['found-fields', found]
    ];

    for (const [id, active] of groups) {
        const group = document.getElementById(id);
        group.hidden = !active;

        for (const input of group.querySelectorAll('input')) {
            input.disabled = !active;
            input.required = active;
        }
    }
}

function validatePassword() {
    let message = '';

    if (!password.value) {
        message = '삭제 비밀번호를 입력해 주세요.';
    } else if (!/^[0-9]+$/.test(password.value)) {
        message = '삭제 비밀번호는 숫자만 입력해 주세요.';
    } else if (password.value.length !== 4) {
        message = '삭제 비밀번호는 정확히 4자리로 입력해 주세요.';
    }

    password.setCustomValidity(message);
}

for (const radio of form.querySelectorAll('input[name="type"]')) {
    radio.addEventListener('change', updateType);
}

form.addEventListener('submit', (event) => {
    const inputs = form.querySelectorAll('[required]:not(:disabled)');

    for (const input of inputs) {
        if (!input.value.trim()) {
            event.preventDefault();
            input.setCustomValidity('공백만 입력할 수 없습니다.');
            input.reportValidity();
            break;
        }
    }
});

form.addEventListener('input', (event) => {
    if (event.target === password) {
        validatePassword();
    } else {
        event.target.setCustomValidity('');
    }
});

password.addEventListener('invalid', validatePassword);

updateType();
validatePassword();