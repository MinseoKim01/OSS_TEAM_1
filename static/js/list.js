/*
 * 분실물 목록 조회 및 카드 UI 렌더링
 */

/**
 * 전체 및 유형별(type: report / found) 등록 건수 카운트(count) 집계 함수 (API 호출)
 * @returns {Promise<{total: number, report: number, found: number}>}
 */
async function fetchItemStats() {
    const response = await fetch('/api/stats');
    if (!response.ok) {
        throw new Error('통계 집계 데이터를 불러오지 못했습니다.');
    }
    return await response.json();
}

/**
 * 분실물 목록 데이터에서 유형별(report / found) 및 전체 등록 건수 카운트 집계 함수 (클라이언트 집계)
 * @param {Array} items
 * @returns {{total: number, report: number, found: number}}
 */
function countItemsByType(items) {
    return items.reduce((acc, item) => {
        acc.total += 1;
        if (item.type === 'report') {
            acc.report += 1;
        } else if (item.type === 'found') {
            acc.found += 1;
        }
        return acc;
    }, { total: 0, report: 0, found: 0 });
}

/**
 * 통계 카드 카운터 UI에 집계 데이터(N건) 동적 출력 및 숫자 포맷팅
 * @param {{total: number, report: number, found: number}} stats
 */
function updateStatsUI(stats) {
    const totalEl = document.getElementById('stat-total');
    const reportEl = document.getElementById('stat-report');
    const foundEl = document.getElementById('stat-found');

    if (totalEl) totalEl.textContent = Number(stats.total || 0).toLocaleString();
    if (reportEl) reportEl.textContent = Number(stats.report || 0).toLocaleString();
    if (foundEl) foundEl.textContent = Number(stats.found || 0).toLocaleString();
}

document.addEventListener('DOMContentLoaded', () => {
    const listContainer = document.getElementById('lost-items-list');
    const countBadge = document.getElementById('items-count');
    const sortRecent = document.getElementById('sort-recent');
    const sortOldest = document.getElementById('sort-oldest');
    if (!listContainer) return;

    let currentItems = [];

    // 상단 통계 요약 카드 초기 데이터 연동
    fetchItemStats()
        .then(stats => updateStatsUI(stats))
        .catch(err => console.error('통계 데이터 연동 오류:', err));

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
            // 목록 데이터 기반으로도 통계 카드 수치 동기화
            updateStatsUI(countItemsByType(items));
            renderCards(currentItems);
        });
});
