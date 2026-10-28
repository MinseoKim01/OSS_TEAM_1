/*
 * 삭제 시 동작 담당.
*/

// 삭제 버튼 클릭 시 삭제 dialog 열기
const deleteDialog = document.getElementById('delete-dialog');

document.getElementById('delete-open-button').addEventListener('click', () => {
    deleteDialog.showModal();
});
