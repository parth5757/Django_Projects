$('#id_company, #id_vendor, #id_product, #id_unit_type').select2({
    width: "100%",
  });
  
  var product_single_piece_price = 0
  var data_company_vendors = null
  var data_company_products = null
  var added_product_ids = [];
  $(document).ready(function(){

    if(update_form){
        selected_vendor = $('#id_vendor').find('option:selected').val();
        $("#form_purchase_order #id_vendor").empty().append("<option value=''>---------</option>");
        $("#form_purchase_order #id_product").empty().append("<option value=''>---------</option>");
        if(company_admin_company_id){
            ajax_call_get_venders_and_products(company_admin_company_id);
        } else {
            selected_company = $('#id_company').find('option:selected').val();
            ajax_call_get_venders_and_products(selected_company);


            $("#id_company").on('change',function(){
                reset_form_on_product_company_change();
                $this = $(this);
                company_id = $this.val();
                if(company_id != ''){
                    ajax_call_get_venders_and_products(company_id);
                }
            });
        }
        ajax_call_purchase_order_product_in_update(purchase_order_id);


    } else {

    $("#form_purchase_order #id_vendor").empty().append("<option value=''>---------</option>");
    $("#form_purchase_order #id_product").empty().append("<option value=''>---------</option>");
        if(company_admin_company_id){
            ajax_call_get_venders_and_products(company_admin_company_id);
        } else {
            $("#id_company").on('change',function(){
                reset_form_on_product_company_change();
                $this = $(this);
                company_id = $this.val();
                if(company_id != ''){
                    ajax_call_get_venders_and_products(company_id);
                }
            });
        }
    

   }
   // COMMON START

   $("#id_product").on('change',function(){
        $this = $(this);
        if($this.val() != ''){
            ajax_call_get_product_details($this)
            $("#btn_add_product").removeClass("btn-pointer-events-none");
        } else {
            // $("#btn_add_product").addClass("btn-pointer-events-none");
            reset_add_product_fields();
        }
    });

    $("#id_unit_type").on('change',function(){
        calculate_product_total_price();

    });
    $("#id_quantity").on('click focusout',function(){
        calculate_product_total_price();
    });
    $("#id_cost_price").on('click focusout',function(){
        product_single_piece_price = parseFloat($(this).val());
        calculate_product_total_price();
    });
    $("#btn_add_product").on('click',function(){
        if($('#id_product').val() != ''){
            ajax_call_add_product_in_purchase_list($(this));
        }
    });


    
   // COMMON END





  });
  $(document).on('click focusout',"#table_added_products .product-row",function(e){
      if(e.target){
          if($(e.target).hasClass('btn-procuct-remove')){
                product_id_removed_from_added_list = $(e.target).closest('tr').attr('product-id');
                id_index = added_product_ids.indexOf(product_id_removed_from_added_list);
                if (id_index > -1) {
                    added_product_ids.splice(id_index, 1);
                }
                $("#form_purchase_order #product_id_list ").val(added_product_ids);

                reset_add_product_fields();
                remove_product_from_selection(added_product_ids);
                
                $(e.target).closest('tr').remove();
                count_table_row_index();

              calculate_purchase_order_total();
            } else {
                if(e.key !== ".") { 
                    calculate_product_net_price($(e.target).closest("tr"));
                }
            }
    }
  });

  $("#form_purchase_order").on('submit', function() {
    
    $("#table_added_products .product-row").trigger("focusout");

    return true;
});

  $("#btn_form_reset").on("click",function(){
    reset_form_on_product_company_change();
  });


function ajax_call_get_venders_and_products(company_id){
    ajax_call_setup();
    $.ajax({
        url:data_url,
        type:"post",
        dataType:"json",
        data:{
        'company_id':company_id
        },
        success: function(data){
            $("#form_purchase_order #id_vendor").empty().append("<option value=''>---------</option>");
            $("#form_purchase_order #id_product").empty().append("<option value=''>---------</option>");
            data_company_vendors = data.company_vendors;
            data_company_products = data.company_products;
            $("#form_purchase_order #id_vendor").append(data.company_vendors);
            $("#form_purchase_order #id_product").append(data.company_products);
            // console.log("selected_vendor "+selected_vendor)
            $("#id_vendor").val(selected_vendor).change();
            $("#id_vendor option[value="+selected_vendor+"]").attr('selected','selected');
            $("#id_vendor").select2().trigger('change');
        },
        error: function(xhr,ajaxOptions,thrownError){
            console.log(thrownError);
        }
    });
}

function ajax_call_get_product_details($this){
    ajax_call_setup();
    $.ajax({
        url:$this.attr("data-url"),
        type:"post",
        dataType:"json",
        data:{
        'product_id':$this.val(),
        },
        success: function(data){
            product_single_piece_price = parseFloat(data.product_cost_price)
            $("#form_purchase_order #id_unit_type").empty();
            $("#form_purchase_order #id_unit_type").append(data.product_unit_type);
            $("#form_purchase_order #id_cost_price").val(data.product_cost_price.toFixed(2));
            $("#form_purchase_order #id_quantity").val("1");
            $("#form_purchase_order #id_total_pieces").val("1");
            $("#form_purchase_order #product_total_price ").val(data.product_cost_price.toFixed(2));
            calculate_product_total_price();
        },
        error: function(xhr,ajaxOptions,thrownError){
            console.log(thrownError);
        }
    });
}

function ajax_call_add_product_in_purchase_list($this){
    selected_product_id = $('#id_product').val(); 
    $.ajax({
        url:$this.attr("data-url"),
        type:"post",
        dataType:"json",
        data:{
            'product_id':selected_product_id,
            'unit_type' :$('#id_unit_type').find('option:selected').attr('data-product-type'),
            'unit_type_text' :$('#id_unit_type').find('option:selected').text(),
            'unit_type_pieces':$('#id_unit_type').val(),
            'quantity':$('#id_quantity').val(),
            'cost_price':$('#id_cost_price').val(),
        },
        success: function(data){
            if($('#table_added_products').has('.no-product-row').length>0){
                $('.no-product-row').remove();
            }
            $('#table_added_products').append(data.product_row);
            added_product_ids.push(selected_product_id);
            $("#form_purchase_order #product_id_list ").val(added_product_ids);

            calculate_purchase_order_total();
            count_table_row_index();
            reset_add_product_fields();
            // console.log(added_product_ids);
            remove_product_from_selection(added_product_ids);
    
        },
        error: function(xhr,ajaxOptions,thrownError){
            console.log(thrownError);
        }
    });
}

function ajax_call_setup(){
    csrf_token = $("#form_purchase_order input[name='csrfmiddlewaretoken']").val();
    $.ajaxSetup({
        headers:{"X-CSRFToken": csrf_token}
    });
    
}

function calculate_product_total_price(){
    unit_type_pieces = parseInt($('#form_purchase_order #id_unit_type').val());
    quantity = parseInt($('#form_purchase_order #id_quantity').val());
    cost_price = unit_type_pieces*product_single_piece_price
    total_pieces = unit_type_pieces * quantity

    $("#form_purchase_order #id_total_pieces").val(total_pieces);
    $("#form_purchase_order #product_total_price").val((cost_price*quantity).toFixed(2));

}


function reset_add_product_fields(){
    // $("#form_purchase_order #id_vendor").empty().append("<option value=''>---------</option>");
    $("#form_purchase_order #id_product").empty().append("<option value=''>---------</option>");
    $("#form_purchase_order #id_unit_type").empty().append("<option value=''>---------</option>");
    // $("#form_purchase_order #id_vendor").append(data_company_vendors);
    $("#form_purchase_order #id_product").append(data_company_products);
    $("#form_purchase_order #id_quantity").val("0");
    $("#form_purchase_order #id_total_pieces").val("0");
    $("#form_purchase_order #id_cost_price").val("0.0");
    $("#form_purchase_order #product_total_price ").val("0.0");
    $("#btn_add_product").addClass("btn-pointer-events-none");

}


function make_input_name($id,$field){
    return "input[name="+$id+$field+"]";
}
  

function calculate_product_net_price($this){
    $row_id = $this.attr("data-id");
    $prd_quantity = parseInt($this.find(make_input_name($row_id,"__quantity")).val());
    $prd_default_total_pieces = parseInt($this.find(make_input_name($row_id,"__totalpieces")).attr("data-default-value"));
    $prd_total_pieces = parseInt($this.find(make_input_name($row_id,"__totalpieces")).val());
    $prd_cost_price = parseFloat($this.find(make_input_name($row_id,"__costprice")).val());

    $prd_total_pieces = $prd_default_total_pieces * $prd_quantity

    $prd_item_total_price = $prd_total_pieces * $prd_cost_price;

    $this.find(make_input_name($row_id,"__quantity")).val($prd_quantity);
    $this.find(make_input_name($row_id,"__totalpieces")).val($prd_total_pieces);   
    $this.find(make_input_name($row_id,"__costprice")).val($prd_cost_price.toFixed(2));
    $this.find(make_input_name($row_id,"__totalprice")).val($prd_item_total_price.toFixed(2));
    calculate_purchase_order_total();

  }


function calculate_purchase_order_total(){
    purchase_order_sum = 0;
    product_prices = [];
    $(".product-total-price").each(function() {
        product_prices.push(parseFloat($(this).val()));
    });
    purchase_order_sum = product_prices.reduce((sum, a) => sum + a, 0);
    $("#form_purchase_order #id_total_price ").val(purchase_order_sum.toFixed(2));

}

function count_table_row_index(){
    indx = 1;
    $(".product-row").each(function() {
        $(this).find("td[data-title='product-id']").text(indx);
        indx += 1;
    });
}

function reset_form_on_product_company_change(){
    reset_add_product_fields();
    $("#table_added_products .product-row").remove();
    if($('#table_added_products').has('.no-product-row').length==0){
        $("#table_added_products tbody").append("<tr class='no-product-row'><td colspan='8'><p>No products added</p></td> </tr>");
    }

}

function remove_product_from_selection(id_array){
    id_array.forEach(function(value, index, array){
    $("#id_product option[value='"+value+"']").remove();
    });
}



function ajax_call_purchase_order_product_in_update(purchase_order_id){
    selected_product_id = $('#id_product').val(); 

    ajax_call_setup();
       $.ajax({
        url: update_purchase_order_url,
        type:'post',
        dataType:"json",
        data :{
            'purchase_order_id':purchase_order_id,
            'product_id':selected_product_id,

        },
        success: function(data){
            if($('#table_added_products').has('.no-product-row').length>0){
                $('.no-product-row').remove();
            }
            $('#table_added_products').append(data.existing_product_list);
            $("#form_purchase_order #product_id_list ").val(data.purchase_order__product_ids);
            added_product_ids = data.purchase_order__product_ids.map(String);
            remove_product_from_selection(added_product_ids);

            // calculate_purchase_order_total();
            // count_table_row_index();
            // reset_add_product_fields();
            // remove_product_from_selection(added_product_ids);

        }

    })
}