function initialize_datatable() {

    var t = $('#table').DataTable({
        columnDefs: [{
                "targets": 0,
                "className": "text-center",
            },
            {
                orderable: false,
            },
            {
                targets: [2],
                visible: role
            }
        ],
        order: [],

        processing: true,
        serverSide: true,
        ajax: {
            url: data_table_url,
            type: 'get',
            data: set_filters(),
        },
        columns: columns_dtl,
        rowCallback: function(nRow, aData, iDisplayIndex) {
            var oSettings = this.fnSettings();
            $("td:first", nRow).html(oSettings._iDisplayStart + iDisplayIndex + 1);
            return nRow;
        },
    });

}

initialize_datatable();