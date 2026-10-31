
/**
 * 분실물 목록 조회 및 카드 UI 렌더링
 */

/**
 * 전체 및 유형별(type: report / found) 등록 건수 카운트 집계 함수 (API 호출)
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
 * 분실물 목록 데이터에서 유형별(report / found) 및 전체 등록 건수 카운트 집계 함수
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
 * 통계 카드 카운터 UI에 집계 데이터 동적 출력 및 숫자 포맷팅
 * @param {{total: number, report: number, found: number}} stats
 */
function updateStatsUI(stats) {
    const totalEl = document.getElementById('stat-total');
    const reportEl = document.getElementById('stat-report');
    const foundEl = document.getElementById('stat-found');

    if (totalEl) {
        totalEl.textContent = Number(stats.total || 0).toLocaleString();
    }

    if (reportEl) {
        reportEl.textContent = Number(stats.report || 0).toLocaleString();
    }

    if (foundEl) {
        foundEl.textContent = Number(stats.found || 0).toLocaleString();
    }
}

/**
 * DB 변경 이벤트 감지 및 실시간 통계 수치 반영 리스너
 * 주기적 변경 감지(Polling) 및 탭 포커스 복귀(visibilitychange)를 통해
 * 새 글 등록/삭제 시 통계 숫자가 반영되도록 함
 *
 * @param {Function} onCountChanged - 건수 변경 시 추가 동작(목록 갱신 등)
 * @param {number} intervalMs - 감지 주기 (기본 3초)
 */
function initRealtimeStatsListener(onCountChanged, intervalMs = 3000) {
    let lastStats = null;

    function checkStatsUpdate() {
        fetchItemStats()
            .then(stats => {
                updateStatsUI(stats);

                // 이전 집계 건수와 달라진 경우 새 글 등록 또는 삭제 감지
                if (
                    lastStats !== null &&
                    (
                        lastStats.total !== stats.total ||
                        lastStats.report !== stats.report ||
                        lastStats.found !== stats.found
                    )
                ) {
                    if (typeof onCountChanged === 'function') {
                        onCountChanged();
                    }
                }

                lastStats = stats;
            })
            .catch(() => {
                // 통계 조회 실패 시 별도 처리 없이 다음 주기에 다시 확인
            });
    }

    // 주기적 DB 변경 감지
    setInterval(checkStatsUpdate, intervalMs);

    // 다른 탭에서 등록/삭제 후 복귀 시 즉시 감지
    document.addEventListener('visibilitychange', () => {
        if (!document.hidden) {
            checkStatsUpdate();
        }
    });

    // 브라우저 탭 간 실시간 변경 이벤트 감지
    window.addEventListener('storage', (e) => {
        if (e.key === 'moajup_db_changed') {
            checkStatsUpdate();
        }
    });
}


document.addEventListener('DOMContentLoaded', () => {
    const listContainer = document.getElementById('lost-items-list');

    // 데이터 조회 로딩 화면
    const loadingState = document.getElementById('loading-state');

    // 빈 목록 안내 화면
    const emptyState = document.getElementById('empty-state');

    const countBadge = document.getElementById('items-count');
    const sortRecent = document.getElementById('sort-recent');
    const sortOldest = document.getElementById('sort-oldest');
    const modal = document.getElementById('lost-item-modal');

    if (!listContainer) return;

    // 모달 X 버튼 및 삭제하기 버튼
    const modalCloseIcon = document.getElementById('modal-close-icon');
    const modalDeleteBtn = document.getElementById('modal-delete-btn');

    // X 버튼 클릭 시 상세보기 팝업 닫기
    if (modalCloseIcon && modal) {
        modalCloseIcon.addEventListener('click', () => {
            modal.classList.remove('active');
            modal.style.display = 'none';
            modal.setAttribute('aria-hidden', 'true');
        });
    }

    let currentItems = [];
    let selectedItem = null;

    // 모달 내부 상세 정보 필드 엘리먼트
    const modalBadge = document.getElementById('modal-item-badge');
    const modalName = document.getElementById('modal-item-name');
    const modalDatetimeLabel = document.getElementById('modal-datetime-label');
    const modalDatetimeValue = document.getElementById('modal-datetime-value');
    const modalChatroomValue = document.getElementById('modal-chatroom-value');
    const modalLocationValue = document.getElementById('modal-location-value');
    const modalStorageValue = document.getElementById('modal-storage-value');
    const modalDescValue = document.getElementById('modal-description-value');

    // 게시글 유형별 상세 정보 행 요소
    const modalChatroomRow = document.getElementById('modal-row-chatroom');
    const modalLocationRow = document.getElementById('modal-row-location');
    const modalStorageRow = document.getElementById('modal-row-storage');

    /**
     * 게시글 상세 정보 모달 열기 및 상태 데이터 바인딩 함수
     * @param {Object} item - 선택된 분실물 게시글 객체
     */
    function openItemDetailModal(item) {
        if (!item || !modal) return;

        selectedItem = item;

        const isReport = item.type === 'report';

        // 게시글 유형에 따라 상세 정보 항목 표시 여부 구분
        if (isReport) {
            // 제보형: 단톡방, 보관 위치 표시
            if (modalChatroomRow) modalChatroomRow.style.display = 'flex';
            if (modalLocationRow) modalLocationRow.style.display = 'none';
            if (modalStorageRow) modalStorageRow.style.display = 'flex';
        } else {
            // 습득형: 습득 장소, 보관 위치 표시
            if (modalChatroomRow) modalChatroomRow.style.display = 'none';
            if (modalLocationRow) modalLocationRow.style.display = 'flex';
            if (modalStorageRow) modalStorageRow.style.display = 'flex';
        }

        // 1. 유형 배지 바인딩
        if (modalBadge) {
            modalBadge.textContent = isReport ? '제보형' : '습득형';
            modalBadge.className = `badge ${isReport ? 'badge-report' : 'badge-found'}`;
        }

        // 2. 제목(물건 이름) 바인딩
        if (modalName) {
            modalName.textContent = item.item_name || '';
        }

        // 3. 일시 바인딩
        if (modalDatetimeLabel) {
            modalDatetimeLabel.textContent = isReport ? '안내 일시' : '습득 일시';
        }

        if (modalDatetimeValue) {
            modalDatetimeValue.textContent = `${item.date || ''} ${item.time || ''}`.trim();
        }

        // 4. 장소 및 단톡방 바인딩
        if (modalChatroomValue) {
            modalChatroomValue.textContent = item.chat_room_name || '-';
        }

        if (modalLocationValue) {
            modalLocationValue.textContent = item.found_location || '-';
        }

        if (modalStorageValue) {
            modalStorageValue.textContent = item.storage_location || '-';
        }

        // 5. 특징 및 상세 설명 바인딩
        if (modalDescValue) {
            modalDescValue.textContent = item.description || '등록된 상세 설명이 없습니다.';
        }

        // 선택된 게시글 메타 정보 속성 기록
        modal.dataset.id = item.id;
        modal.dataset.type = item.type;

        // 모달 표시
        modal.classList.add('active');
        modal.style.display = 'flex';
        modal.setAttribute('aria-hidden', 'false');
    }

    // 데이터 조회 상태에 따라 로딩 화면 표시 및 숨김
    function setLoading(isLoading) {
        if (loadingState) {
            loadingState.hidden = !isLoading;
        }

        if (isLoading) {
            listContainer.hidden = true;

            if (emptyState) {
                emptyState.hidden = true;
            }
        }
    }

    // 카드 렌더링 함수
    function renderCards(items) {
        listContainer.innerHTML = '';

        // 등록된 게시글이 없는 경우 빈 목록 화면 표시
        if (!items || items.length === 0) {
            listContainer.hidden = true;

            if (emptyState) {
                emptyState.hidden = false;
            }

            return;
        }

        // 게시글이 존재하는 경우 카드 목록 표시
        listContainer.hidden = false;

        if (emptyState) {
            emptyState.hidden = true;
        }

        items.forEach(item => {
            const card = document.createElement('div');
            card.className = 'lost-card';
            card.setAttribute('role', 'button');
            card.setAttribute('tabindex', '0');

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

            // 카드 클릭 시 선택된 게시글 상세 정보 모달 오픈
            card.addEventListener('click', () => {
                openItemDetailModal(item);
            });

            // 키보드 엔터/스페이스바로도 상세 정보 모달 오픈
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    openItemDetailModal(item);
                }
            });

            listContainer.appendChild(card);
        });
    }

    // 정렬 함수 (최근순 / 과거순)
    function sortBy(order) {
        if (order === 'recent') {
            if (sortRecent) sortRecent.classList.add('active');
            if (sortOldest) sortOldest.classList.remove('active');

            currentItems.sort((a, b) =>
                (b.date + b.time).localeCompare(a.date + a.time)
            );
        } else {
            if (sortOldest) sortOldest.classList.add('active');
            if (sortRecent) sortRecent.classList.remove('active');

            currentItems.sort((a, b) =>
                (a.date + a.time).localeCompare(b.date + b.time)
            );
        }

        renderCards(currentItems);
    }

    // 정렬 버튼 이벤트
    if (sortRecent) {
        sortRecent.addEventListener('click', () => sortBy('recent'));
    }

    if (sortOldest) {
        sortOldest.addEventListener('click', () => sortBy('oldest'));
    }

    // 목록 데이터 로딩 함수
    // 목록 데이터 로딩 함수
    function loadItems() {
        // 데이터 조회 시작
        setLoading(true);

        fetch('/api/items')
            .then(response => {
                if (!response.ok) {
                    throw new Error('분실물 목록을 불러오지 못했습니다.');
                }

                return response.json();
            })
            .then(items => {
                // 조회 데이터 저장
                currentItems = Array.isArray(items) ? items : [];

                // 등록 건수 업데이트
                if (countBadge) {
                    countBadge.textContent = currentItems.length;
                }

                // 통계 카드 업데이트
                updateStatsUI(countItemsByType(currentItems));

                // 조회 결과에 따라 카드 또는 빈 목록 화면 표시
                renderCards(currentItems);
            })
            .catch(err => {
                console.error('분실물 목록 조회 오류:', err);
            })
            .finally(() => {
                // 조회 성공 또는 실패와 관계없이 로딩 화면 종료
                setLoading(false);
            });
    }

    // 초기 목록 로드
    loadItems();

    // 초기 상단 통계 수치 로드
    fetchItemStats()
        .then(stats => {
            updateStatsUI(stats);
        })
        .catch(err => {
            console.error('통계 데이터 연동 오류:', err);
        });

    // DB 변경 이벤트 감지 리스너 시작
    initRealtimeStatsListener(() => {
        loadItems();
    }, 3000);
});
