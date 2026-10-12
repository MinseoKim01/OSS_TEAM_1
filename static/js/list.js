/*
 * 조회 시 동작 담당.
 * 메인 페이지에서 분실물 목록을 조회하여 화면에 표시
 */

document.addEventListener('DOMContentLoaded', () => {
    const listContainer = document.getElementById('lost-items-list');
    if (!listContainer) return;

    fetch('/api/items')
        .then(response => response.json())
        .then(items => {
            items.forEach(item => {
                const li = document.createElement('li');
                const extra = [];

                if (item.type === 'found') {
                    if (item.found_location) extra.push(`습득장소: ${item.found_location}`);
                    if (item.storage_location) extra.push(`보관위치: ${item.storage_location}`);
                } else if (item.type === 'report' && item.chat_room_name) {
                    extra.push(`제보 단톡방: ${item.chat_room_name}`);
                }

                if (item.description) {
                    extra.push(`특징: ${item.description}`);
                }

                const extraText = extra.length > 0 ? `, ${extra.join(', ')}` : '';
                li.textContent = `[${item.type_label}] ${item.item_name} - 일시: ${item.date} ${item.time}${extraText}`;
                listContainer.appendChild(li);
            });
        });
});


