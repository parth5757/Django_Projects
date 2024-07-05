function loadWareHouse() {
    var id_company = document.getElementById('id_company');
    console.log(id_company)
    var id_warehouse = document.getElementById('id_warehouse');
    var id_product= document.getElementById('id_product');
    var ajax = new XMLHttpRequest();
    id_warehouse.innerHTML = '';
    id_product.innerHTML = '';
    ajax.onreadystatechange = function () {
        if (ajax.readyState === 4) {
            var list = JSON.parse(ajax.responseText);
            list.warehouse_list.forEach(element => {
                var option = document.createElement("option");
                option.value = element.id;
                option.text = element.name;
                id_warehouse.options.add(option);
            });
            list.products_list.forEach(element => {
                var option = document.createElement("option");
                option.value = element.id;
                option.text = element.name;
                id_product.options.add(option);
            });
            loadstockproductform()
        }
    };
    ajax.open('get', 'load_warehouse?id_company=' + id_company.value, true);
    ajax.send();   

}

function loadstockproductform(){
    product=$('#id_product').val();
    warehouse=$('#id_warehouse').val();
    var url = 'get_form/';
    $.ajax({
        url: url,
        type: 'get',
        data : {
            'product':product,
            'warehouse':warehouse,
        },
        success: function (data){
            $("#table-body").html(data);
            

        }
        
    });
    
}

