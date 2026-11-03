/*
 * 삭제 시 동작 담당.
*/

// 상세 모달의 삭제하기 버튼 클릭 시 삭제 dialog 열기
const deleteDialog = document.getElementById('delete-dialog');

document.getElementById('modal-delete-btn').addEventListener('click', () => {
    deleteDialog.showModal();
});
