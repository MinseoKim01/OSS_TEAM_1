/*
 * 삭제 시 동작 담당.
*/

// 상세 모달의 삭제하기 버튼 클릭 시 삭제 dialog 열기
const deleteDialog = document.getElementById('delete-dialog');

document.getElementById('modal-delete-btn').addEventListener('click', () => {
    // 상세 모달에 기록된 게시글 id와 유형을 삭제 form에 전달
    const modal = document.getElementById('lost-item-modal');
    document.getElementById('delete-item-id').value = modal.dataset.id;
    document.getElementById('delete-item-type').value = modal.dataset.type;

    deleteDialog.showModal();
});

// 비밀번호 비교 결과를 Toast 임시 메시지로 표시
const passwordResult = new URLSearchParams(window.location.search).get('password');

if (passwordResult === 'match' || passwordResult === 'mismatch') {
    const toast = document.getElementById('toast');
    document.getElementById('toast-message').textContent =
        passwordResult === 'match' ? '비밀번호가 같습니다.' : '비밀번호가 일치하지 않습니다.';
    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
