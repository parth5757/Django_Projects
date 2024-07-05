function intailize_datatables() {
    $('#table').DataTable({
        columnDefs: [{
                targets: to_center,
                className: "text-center",
            },

            {
                orderable: false,
                targets: order_false,
            },
            {
                targets: invisible_columns,
                visible: role // new variable true or false based on user role.
            }
        ],
        order: [],
        // Ajax for pagination
        processing: true,
        serverSide: true,
        // pageLength: 4,
        ajax: {
            url: url,
            type: 'get',
            data: set_filters(),
        },
        columns: columns,
        rowCallback: function(nRow, aData, iDisplayIndex) {
            var oSettings = this.fnSettings();
            $("td:first", nRow).html(oSettings._iDisplayStart + iDisplayIndex + 1);
            return nRow;
        },
    });
};
intailize_datatables()

filter_id.on("change", function() {
    $("#table").DataTable().destroy();
    intailize_datatables()
});