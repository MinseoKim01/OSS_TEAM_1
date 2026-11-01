/*
 * 분실물 목록 조회 및 카드 UI 렌더링
 */

document.addEventListener('DOMContentLoaded', () => {
    const listContainer = document.getElementById('lost-items-list');
    const countBadge = document.getElementById('items-count');
    const sortRecent = document.getElementById('sort-recent');
    const sortOldest = document.getElementById('sort-oldest');
    if (!listContainer) return;

    let currentItems = [];

    // 카드 렌더링 함수
    function renderCards(items) {
        listContainer.innerHTML = '';
        items.forEach(item => {
            const card = document.createElement('div');
            card.className = 'lost-card';

            const isReport = item.type === 'report';
            const badgeText = isReport ? '제보형' : '습득형';
            const badgeClass = isReport ? 'badge-report' : 'badge-found';
            const datePrefix = isReport ? '안내' : '습득';
            const subLocation = isReport
                ? (item.chat_room_name || '')
                : (item.found_location || item.storage_location || '');

            card.innerHTML = `
                <div class="card-badge-wrap">
                    <span class="badge ${badgeClass}">${badgeText}</span>
                </div>
                <h3 class="card-title">${item.item_name}</h3>
                <p class="card-desc">${item.description || ''}</p>
                
                <div class="card-divider"></div>

                <div class="card-info">
                    <div class="card-date">${datePrefix} · ${item.date} ${item.time}</div>
                    ${subLocation ? `<div class="card-location">${subLocation}</div>` : ''}
                </div>
            `;

            listContainer.appendChild(card);
        });
    }

    // 정렬 함수 (최근순 / 과거순)
    function sortBy(order) {
        if (order === 'recent') {
            sortRecent.classList.add('active');
            sortOldest.classList.remove('active');
            currentItems.sort((a, b) => (b.date + b.time).localeCompare(a.date + a.time));
        } else {
            sortOldest.classList.add('active');
            sortRecent.classList.remove('active');
            currentItems.sort((a, b) => (a.date + a.time).localeCompare(b.date + b.time));
        }
        renderCards(currentItems);
    }

    if (sortRecent) sortRecent.addEventListener('click', () => sortBy('recent'));
    if (sortOldest) sortOldest.addEventListener('click', () => sortBy('oldest'));

    fetch('/api/items')
        .then(response => response.json())
        .then(items => {
            currentItems = items;
            if (countBadge) {
                countBadge.textContent = items.length;
            }
            renderCards(currentItems);
        });
});
