$(document).ready(function () {
  $('#inventoryTable').DataTable({
    "ordering": True,
    "paging": false,
    "order": [[ 0, "desc" ]]
    });
  $('.dataTables_length').addClass('bs-select');
});