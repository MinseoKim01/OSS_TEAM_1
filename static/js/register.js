/*
 * 등록 화면의 브라우저 동작 담당.
*/
/* 등록 유형에 따라 날짜·시간 제목과 유형별 입력칸을 전환 */
const form = document.querySelector('.register-form');

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

for (const radio of form.querySelectorAll('input[name="type"]')) {
    radio.addEventListener('change', updateType);
}

updateType();